"""GitHub Trending 爬虫模块"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import httpx
from bs4 import BeautifulSoup

from .config import GITHUB_TRENDING_URL, DATA_DIR, CACHE_FILE


class TrendingRepo:
    """单个 Trending 仓库的数据"""
    def __init__(
        self,
        rank: int,
        name: str,
        url: str,
        description: str,
        language: str,
        stars: int,
        forks: int,
        today_stars: int,
        built_by: list[dict] = None,
    ):
        self.rank = rank
        self.name = name
        self.url = url
        self.description = description or ""
        self.language = language or ""
        self.stars = stars
        self.forks = forks
        self.today_stars = today_stars
        self.built_by = built_by or []

    def to_dict(self) -> dict:
        return {
            "rank": self.rank,
            "name": self.name,
            "url": self.url,
            "description": self.description,
            "language": self.language,
            "stars": self.stars,
            "forks": self.forks,
            "today_stars": self.today_stars,
            "built_by": self.built_by,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "TrendingRepo":
        return cls(**d)


def parse_stars(text: str) -> int:
    """解析 Star 数，如 '12.3k' -> 12300"""
    text = text.strip().replace(",", "")
    if "k" in text.lower():
        return int(float(text.lower().replace("k", "")) * 1000)
    if "m" in text.lower():
        return int(float(text.lower().replace("m", "")) * 1000000)
    try:
        return int(text)
    except ValueError:
        return 0


def fetch_trending(language: str = "", since: str = "daily") -> list[TrendingRepo]:
    """
    爬取 GitHub Trending 页面
    language: 编程语言筛选，空字符串表示全部
    since: daily/weekly/monthly
    """
    url = GITHUB_TRENDING_URL
    if language:
        url += f"/{language}"
    params = {"since": since}

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml",
    }

    resp = httpx.get(url, params=params, headers=headers, follow_redirects=True, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "lxml")
    articles = soup.select("article.Box-row")

    repos = []
    for i, article in enumerate(articles, 1):
        try:
            # 仓库名
            h2 = article.select_one("h2 a")
            if not h2:
                continue
            full_name = h2.get("href", "").strip("/")
            repo_url = f"https://github.com/{full_name}"

            # 描述
            desc_elem = article.select_one("p")
            description = desc_elem.text.strip() if desc_elem else ""

            # 编程语言
            lang_elem = article.select_one("[itemprop='programmingLanguage']")
            language_name = lang_elem.text.strip() if lang_elem else ""

            # 星数
            star_elem = article.select_one("a.Link--muted[href$='/stargazers']")
            stars = parse_stars(star_elem.text.strip()) if star_elem else 0

            # Fork 数
            fork_elem = article.select_one("a.Link--muted[href$='/forks']")
            forks = parse_stars(fork_elem.text.strip()) if fork_elem else 0

            # 今日新增 Star
            today_elem = article.select_one("span.d-inline-block.float-sm-right")
            today_stars = 0
            if today_elem:
                today_text = today_elem.text.strip()
                if "," in today_text:
                    today_stars = int(today_text.split(",")[0].strip("* ,"))
                else:
                    today_stars = parse_stars(today_text.split()[0].strip("* ,"))

            # 贡献者头像
            built_by = []
            avatars = article.select("a>img.avatar")
            for avatar in avatars:
                src = avatar.get("src", "")
                alt = avatar.get("alt", "")
                if src:
                    built_by.append({
                        "username": alt.replace("@", ""),
                        "avatar": src,
                    })

            repos.append(TrendingRepo(
                rank=i,
                name=full_name,
                url=repo_url,
                description=description,
                language=language_name,
                stars=stars,
                forks=forks,
                today_stars=today_stars,
                built_by=built_by,
            ))
        except Exception as e:
            print(f"  [警告] 解析第 {i} 个仓库失败: {e}")
            continue

    return repos


def fetch_all_trending(since: str = "daily") -> dict[str, list[TrendingRepo]]:
    """
    爬取所有语言的 Trending
    返回 { language_name: [repos] }
    """
    from .config import LANGUAGES

    result = {}
    for lang in LANGUAGES:
        lang_label = lang if lang else "全部"
        print(f"  正在爬取 {lang_label} ({since})...")
        try:
            repos = fetch_trending(language=lang, since=since)
            result[lang_label] = repos
            print(f"    [OK] 获取到 {len(repos)} 个仓库")
        except Exception as e:
            print(f"    [FAIL] 失败: {e}")
            result[lang_label] = []
        time.sleep(1)  # 礼貌延迟

    return result


def save_cache(data: dict):
    """保存数据到缓存文件"""
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
    cache = {
        "updated_at": datetime.now().isoformat(),
        "data": {},
    }
    for lang, repos in data.items():
        cache["data"][lang] = [r.to_dict() for r in repos]
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
    print(f"  缓存已保存: {CACHE_FILE}")


def load_cache() -> dict | None:
    """从缓存文件加载数据"""
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
        data = {}
        for lang, repos in cache.get("data", {}).items():
            data[lang] = [TrendingRepo.from_dict(r) for r in repos]
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return None
