"""TrendCN 主入口"""

import sys
import os
from datetime import datetime

# 确保 src 在路径中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scraper import fetch_all_trending, save_cache, load_cache
from src.translator import batch_translate
from src.generator import generate_html


def run(since: str = "daily", use_cache: bool = False):
    """
    主流程：爬取 → 翻译 → 生成页面
    """
    print("=" * 50)
    print(f"  TrendCN — GitHub 每日热榜中文站")
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  范围: {since}")
    print("=" * 50)

    # Step 1: 获取数据
    print("\n[1/3] 获取 GitHub Trending 数据")
    if use_cache:
        cached = load_cache()
        if cached:
            print("  使用缓存数据")
            data = cached
        else:
            print("  无缓存，重新爬取")
            data = fetch_all_trending(since)
            save_cache(data)
    else:
        data = fetch_all_trending(since)
        save_cache(data)

    # Step 2: 翻译
    print("\n[2/3] 翻译描述为中文")
    for lang in data:
        repos = data[lang]
        if repos:
            print(f"\n  [{lang}] {len(repos)} 个仓库")
            batch_translate(repos)

    # Step 3: 生成页面
    print("\n[3/3] 生成静态页面")
    updated_at = datetime.now().isoformat()
    output_map = {"daily": "index.html", "weekly": "weekly.html", "monthly": "monthly.html"}
    out_file = output_map.get(since, "index.html")
    generate_html(
        data={lang: [r.to_dict() if hasattr(r, 'to_dict') else r for r in repos]
              for lang, repos in data.items()},
        updated_at=updated_at,
        since=since,
        output_file=out_file,
    )

    print(f"\n[DONE] 页面已生成到 docs/{out_file}")

    # 如果是 daily 模式，顺便把另外两个时间范围也生成
    if since == "daily":
        for extra_since, extra_file in [("weekly", "weekly.html"), ("monthly", "monthly.html")]:
            print(f"\n--- 同时生成 {extra_since} 页面 ---")
            try:
                extra_data = fetch_all_trending(extra_since)
                for lang in extra_data:
                    repos = extra_data[lang]
                    if repos:
                        batch_translate(repos)
                generate_html(
                    data={lang: [r.to_dict() if hasattr(r, 'to_dict') else r for r in repos]
                          for lang, repos in extra_data.items()},
                    updated_at=datetime.now().isoformat(),
                    since=extra_since,
                    output_file=extra_file,
                )
                print(f"  [DONE] 页面已生成到 docs/{extra_file}")
            except Exception as e:
                print(f"  [FAIL] 生成 {extra_since} 页面失败: {e}")

    return data


def main():
    """CLI 入口"""
    import argparse
    parser = argparse.ArgumentParser(description="TrendCN — GitHub 每日热榜中文站")
    parser.add_argument("--since", choices=["daily", "weekly", "monthly"], default="daily",
                       help="时间范围 (默认: daily)")
    parser.add_argument("--cache", action="store_true", help="优先使用缓存")
    args = parser.parse_args()

    run(since=args.since, use_cache=args.cache)


if __name__ == "__main__":
    main()
