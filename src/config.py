"""TrendCN 配置模块"""

# GitHub Trending URL
GITHUB_TRENDING_URL = "https://github.com/trending"

# 支持的语言
LANGUAGES = [
    "",  # 全部
    "python",
    "javascript",
    "typescript",
    "go",
    "rust",
    "java",
    "c",
    "cpp",
    "csharp",
    "ruby",
    "swift",
    "kotlin",
    "php",
    "shell",
    "html",
    "css",
]

# 时间范围
TIME_RANGES = ["daily", "weekly", "monthly"]

# 数据缓存路径
DATA_DIR = "data"
CACHE_FILE = "data/trending_cache.json"

# 输出目录
OUTPUT_DIR = "docs"

# 站点配置
SITE_TITLE = "GitHub 每日热榜"
SITE_DESCRIPTION = "GitHub Trending 中文版 — 每天自动抓取并翻译为中文"
SITE_URL = "https://celandine410.github.io/trendcn"

# 百度翻译 API (可选，不配则用英文)
BAIDU_APP_ID = ""
BAIDU_SECRET_KEY = ""
