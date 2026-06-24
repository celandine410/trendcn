"""付费推送订阅相关功能（预留）"""

# TrendCN 付费推送服务
# 
# 用户可以订阅每日热榜推送：
# - 免费版：每天推送 Top 10（通过 GitHub Issues 公开）
# - Pro 版 ¥5/月：完整榜单推送 + 自定义关键词 + 微信/邮件/Telegram 三选一
#
# 技术方案：
# - 使用爱发电处理支付（https://afdian.com）
# - 付款后通过 GitHub Actions 自动发送
# - 推送渠道：PushPlus(微信) / SMTP(邮件) / Telegram Bot
# 
# 本模块暂为占位，待用户量上来后实现

SUBSCRIPTION_PLANS = {
    "free": {
        "name": "免费版",
        "price": 0,
        "features": [
            "每日 GitHub Trending Top 10",
            "公开 GitHub Issues 推送",
        ],
    },
    "pro": {
        "name": "Pro 版",
        "price": 5,
        "unit": "月",
        "features": [
            "完整榜单推送（所有语言）",
            "自定义关键词过滤",
            "微信/邮件/Telegram 推送",
            "每日定时推送",
        ],
    },
}
