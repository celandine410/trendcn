"""HTML 页面生成器"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from .config import (
    OUTPUT_DIR,
    SITE_TITLE,
    SITE_DESCRIPTION,
    SITE_URL,
    LANGUAGES,
)


def _render_stars(n: int) -> str:
    """格式化 Star 数"""
    if n >= 1000:
        return f"{n/1000:.1f}k"
    return str(n)


def _language_color(lang: str) -> str:
    """编程语言对应的颜色"""
    colors = {
        "python": "#3572A5",
        "javascript": "#F7DF1E",
        "typescript": "#3178C6",
        "go": "#00ADD8",
        "rust": "#DEA584",
        "java": "#B07219",
        "c": "#555555",
        "cpp": "#F34B7D",
        "csharp": "#178600",
        "ruby": "#701516",
        "swift": "#F05138",
        "kotlin": "#A97BFF",
        "php": "#4F5D95",
        "shell": "#89E051",
        "html": "#E34F26",
        "css": "#563D7C",
        "vue": "#41B883",
        "react": "#61DAFB",
    }
    return colors.get(lang.lower(), "#6e7681")


def generate_html(data: dict, updated_at: str, since: str = "daily", output_file: str = "index.html"):
    """
    生成静态 HTML 页面
    data: { language_name: [repo_dicts] }
    output_file: 输出的文件名 (如 index.html, weekly.html, monthly.html)
    """
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # 时间标签
    if since == "daily":
        since_label = "今日"
    elif since == "weekly":
        since_label = "本周"
    else:
        since_label = "本月"

    # 更新时间
    try:
        dt = datetime.fromisoformat(updated_at)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        time_str = updated_at

    # 按语言生成页面
    all_repos_flat = []
    lang_sections = ""

    for lang_label in data:
        repos = data[lang_label]
        if not repos:
            continue

        all_repos_flat.extend(repos)

        # 语言标签
        lang_display = lang_label if lang_label != "全部" else "所有语言"
        lang_color = _language_color(lang_label)

        repo_cards = ""
        for r in repos:
            desc = r.get("translated_description") or r.get("description", "")
            lang_badge = ""
            if r.get("language"):
                lc = _language_color(r["language"])
                lang_badge = f'<span class="lang-dot" style="background:{lc}"></span><span class="lang-name">{r["language"]}</span>'

            repo_cards += f"""
            <div class="repo-card">
                <div class="repo-header">
                    <span class="repo-rank">#{r['rank']}</span>
                    <a class="repo-name" href="{r['url']}" target="_blank" rel="noopener">
                        <svg class="octicon" viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.25.25 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"></path></svg>
                        {r['name']}
                    </a>
                </div>
                <p class="repo-desc">{desc}</p>
                <div class="repo-meta">
                    {lang_badge}
                    <span class="meta-item">
                        <svg viewBox="0 0 16 16" width="14" height="14"><path fill="currentColor" d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"></path></svg>
                        {_render_stars(r['stars'])}
                    </span>
                    <span class="meta-item">
                        <svg viewBox="0 0 16 16" width="14" height="14"><path fill="currentColor" d="M5 5.372v.878c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-.878a2.25 2.25 0 1 1 1.5 0v.878a2.25 2.25 0 0 1-2.25 2.25h-1.5v2.128a2.251 2.251 0 1 1-1.5 0V8.5h-1.5A2.25 2.25 0 0 1 3.5 6.25v-.878a2.25 2.25 0 1 1 1.5 0ZM5 3.25a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Zm6.75.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm-3 8.75a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Z"></path></svg>
                        {_render_stars(r['forks'])}
                    </span>
                    <span class="meta-item today-stars">
                        <svg viewBox="0 0 16 16" width="14" height="14"><path fill="currentColor" d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"></path></svg>
                        {_render_stars(r['today_stars'])} {since_label}
                    </span>
                </div>
            </div>"""

        lang_sections += f"""
        <section class="lang-section" id="lang-{lang_label}">
            <h2 class="lang-title" style="border-left: 4px solid {lang_color}; padding-left: 12px;">
                {lang_display}
                <span class="count-badge">{len(repos)}</span>
            </h2>
            <div class="repo-grid">
                {repo_cards}
            </div>
        </section>"""

    # 全部仓库（合并去重）
    seen = set()
    unique_repos = []
    for r in all_repos_flat:
        if r["name"] not in seen:
            seen.add(r["name"])
            unique_repos.append(r)

    all_cards = ""
    for r in unique_repos[:50]:  # 最多显示 50 个
        desc = r.get("translated_description") or r.get("description", "")
        lang_badge = ""
        if r.get("language"):
            lc = _language_color(r["language"])
            lang_badge = f'<span class="lang-dot" style="background:{lc}"></span><span class="lang-name">{r["language"]}</span>'

        all_cards += f"""
        <div class="repo-card">
            <div class="repo-header">
                <span class="repo-rank">#{r['rank']}</span>
                <a class="repo-name" href="{r['url']}" target="_blank" rel="noopener">
                    <svg class="octicon" viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.25.25 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"></path></svg>
                    {r['name']}
                </a>
            </div>
            <p class="repo-desc">{desc}</p>
            <div class="repo-meta">
                {lang_badge}
                <span class="meta-item">{_render_stars(r['stars'])} ⭐</span>
                <span class="meta-item">{_render_stars(r['forks'])} 🍴</span>
                <span class="meta-item today-stars">+{_render_stars(r['today_stars'])} {since_label}</span>
            </div>
        </div>"""

    # 语言导航
    lang_nav = ""
    for lang in LANGUAGES:
        label = lang if lang else "全部"
        display = label if label != "全部" else "所有语言"
        color = _language_color(lang)
        lc = f' style="--lang-color:{color}"'
        active = " active" if (lang == LANGUAGES[0]) else ""
        lang_nav += f'<a href="#lang-{label}" class="lang-tag{active}"{lc}>{display}</a>'

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{SITE_TITLE} — {since_label}</title>
    <meta name="description" content="{SITE_DESCRIPTION}">
    <meta property="og:title" content="{SITE_TITLE}">
    <meta property="og:description" content="{SITE_DESCRIPTION}">
    <meta property="og:url" content="{SITE_URL}">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><text y='14' font-size='14'>⭐</text></svg>">
    <style>
        :root {{
            --bg: #0d1117;
            --surface: #161b22;
            --surface-hover: #1c2333;
            --text: #e6edf3;
            --text-secondary: #8b949e;
            --border: #30363d;
            --accent: #58a6ff;
            --star: #d29922;
            --max-width: 1100px;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans SC', Helvetica, Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }}
        .container {{ max-width: var(--max-width); margin: 0 auto; padding: 0 20px; }}

        /* Header */
        header {{
            border-bottom: 1px solid var(--border);
            padding: 24px 0 20px;
            margin-bottom: 24px;
            background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
        }}
        header h1 {{
            font-size: 28px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        header h1 span {{ background: linear-gradient(135deg, #f0883e, #d29922); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        header .subtitle {{ color: var(--text-secondary); font-size: 14px; margin-top: 6px; }}
        header .meta {{ color: var(--text-secondary); font-size: 13px; margin-top: 8px; display: flex; gap: 16px; flex-wrap: wrap; }}

        /* Time nav */
        .time-nav {{ display: flex; gap: 8px; margin: 16px 0; }}
        .time-btn {{
            padding: 6px 16px; border-radius: 20px; font-size: 13px; font-weight: 500;
            border: 1px solid var(--border); background: transparent; color: var(--text-secondary);
            cursor: pointer; text-decoration: none; transition: all 0.2s;
        }}
        .time-btn:hover {{ border-color: var(--accent); color: var(--accent); }}
        .time-btn.active {{ background: var(--accent); color: #fff; border-color: var(--accent); }}

        /* Language nav */
        .lang-nav {{ display: flex; flex-wrap: wrap; gap: 6px; margin: 16px 0 24px; }}
        .lang-tag {{
            padding: 4px 12px; border-radius: 16px; font-size: 12px;
            border: 1px solid var(--border); background: var(--surface); color: var(--text-secondary);
            cursor: pointer; text-decoration: none; transition: all 0.2s;
        }}
        .lang-tag:hover {{ border-color: var(--lang-color, var(--accent)); color: var(--text); }}

        /* Section */
        .lang-section {{ margin-bottom: 32px; }}
        .lang-title {{
            font-size: 20px; font-weight: 600; margin-bottom: 16px;
            display: flex; align-items: center; gap: 10px;
        }}
        .count-badge {{
            font-size: 12px; font-weight: 500; padding: 2px 8px;
            border-radius: 10px; background: var(--surface); color: var(--text-secondary);
        }}

        /* Repo grid */
        .repo-grid {{ display: grid; gap: 12px; }}

        .repo-card {{
            background: var(--surface); border: 1px solid var(--border);
            border-radius: 8px; padding: 16px; transition: all 0.2s;
        }}
        .repo-card:hover {{ background: var(--surface-hover); border-color: #30363d; }}

        .repo-header {{
            display: flex; align-items: center; gap: 8px;
            margin-bottom: 8px;
        }}
        .repo-rank {{
            font-size: 11px; font-weight: 700; color: var(--text-secondary);
            background: var(--bg); padding: 1px 6px; border-radius: 4px;
            min-width: 24px; text-align: center;
        }}
        .repo-name {{
            font-size: 15px; font-weight: 600; color: var(--accent);
            text-decoration: none; display: flex; align-items: center; gap: 6px;
        }}
        .repo-name:hover {{ text-decoration: underline; }}
        .octicon {{ flex-shrink: 0; }}

        .repo-desc {{
            font-size: 13px; color: var(--text-secondary); margin: 4px 0 10px;
            line-height: 1.5; overflow: hidden; text-overflow: ellipsis;
            display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;
        }}

        .repo-meta {{
            display: flex; align-items: center; gap: 16px; font-size: 12px; color: var(--text-secondary);
            flex-wrap: wrap;
        }}
        .lang-dot {{
            display: inline-block; width: 10px; height: 10px; border-radius: 50%;
            margin-right: 4px;
        }}
        .lang-name {{ margin-right: 4px; }}
        .meta-item {{
            display: inline-flex; align-items: center; gap: 4px;
        }}
        .today-stars {{ color: var(--star); }}

        /* Footer */
        footer {{
            text-align: center; padding: 32px 0; color: var(--text-secondary);
            font-size: 13px; border-top: 1px solid var(--border); margin-top: 32px;
        }}
        footer a {{ color: var(--accent); text-decoration: none; }}
        footer a:hover {{ text-decoration: underline; }}
        .donate {{
            margin: 16px 0; display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;
        }}
        .donate a {{
            display: inline-flex; align-items: center; gap: 6px;
            padding: 8px 20px; border-radius: 8px;
            background: var(--surface); border: 1px solid var(--border);
            color: var(--text); text-decoration: none; font-size: 14px;
        }}
        .donate a:hover {{ border-color: var(--accent); }}

        /* Responsive */
        @media (min-width: 768px) {{
            header h1 {{ font-size: 34px; }}
            .repo-grid {{ grid-template-columns: 1fr 1fr; }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>⭐ <span>GitHub 每日热榜</span></h1>
            <p class="subtitle">{SITE_DESCRIPTION}</p>
            <div class="meta">
                <span>🕐 更新于 {time_str}</span>
                <span>📊 共 {sum(len(v) for v in data.values())} 个仓库</span>
            </div>
            <div class="time-nav">
                <a href="index.html" class="time-btn active">今日热榜</a>
                <a href="weekly.html" class="time-btn">本周热榜</a>
                <a href="monthly.html" class="time-btn">本月热榜</a>
            </div>
            <div class="lang-nav">
                {lang_nav}
            </div>
        </div>
    </header>

    <main class="container">
        <!-- 综合榜 -->
        <section class="lang-section">
            <h2 class="lang-title" style="border-left: 4px solid var(--star); padding-left: 12px;">
                🔥 综合热门
                <span class="count-badge">{len(unique_repos)}</span>
            </h2>
            <div class="repo-grid">
                {all_cards}
            </div>
        </section>

        {lang_sections}
    </main>

    <footer>
        <div class="container">
            <div class="donate">
                <a href="https://afdian.com/a/celandine410" target="_blank" rel="noopener">
                    &#x2764;&#xFE0F; 爱发电赞助
                </a>
                <a href="https://github.com/celandine410/trendcn" target="_blank" rel="noopener">
                    &#x2B50; GitHub 开源
                </a>
                <a href="https://github.com/celandine410/trendcn/issues/new?title=%E8%AE%A2%E9%98%85%E6%8E%A8%E9%80%81&body=%E6%88%91%E6%83%B3%E8%AE%A2%E9%98%85%E6%AF%8F%E6%97%A5%E7%83%AD%E6%A6%9C%E6%8E%A8%E9%80%81%EF%BC%8C%E8%AF%B7%E5%9B%9E%E5%A4%8D%E6%88%91%E3%80%82" target="_blank" rel="noopener">
                    &#x1F4EC; 订阅每日推送
                </a>
            </div>
            <p>
                <a href="https://github.com/celandine410/trendcn">TrendCN</a> —
                每天自动抓取 GitHub Trending 并翻译为中文 ·
                数据来源 <a href="https://github.com/trending">GitHub Trending</a>
            </p>
        </div>
    </footer>
</body>
</html>"""

    with open(os.path.join(OUTPUT_DIR, output_file), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  [OK] 页面已生成: {OUTPUT_DIR}/{output_file} ({len(html)} bytes)")

    return html
