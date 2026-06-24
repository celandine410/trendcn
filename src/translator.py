"""翻译模块 — 使用百度翻译 API"""

import hashlib
import json
import random
import time
from typing import Optional

import httpx

from .config import BAIDU_APP_ID, BAIDU_SECRET_KEY


def _generate_sign(app_id: str, query: str, salt: str, secret_key: str) -> str:
    """生成百度翻译 API 签名"""
    sign_str = app_id + query + salt + secret_key
    return hashlib.md5(sign_str.encode()).hexdigest()


def translate_text(text: str, from_lang: str = "en", to_lang: str = "zh") -> str:
    """
    调用百度翻译 API 翻译文本
    如果未配置 API 密钥，返回原文
    """
    if not text or not text.strip():
        return text

    # 如果没有配置 API，直接返回原文
    if not BAIDU_APP_ID or not BAIDU_SECRET_KEY:
        return text

    # 限制翻译长度（百度限制 6000 字节）
    if len(text.encode()) > 5000:
        text = text[:1000]

    salt = str(random.randint(10000, 99999))
    sign = _generate_sign(BAIDU_APP_ID, text, salt, BAIDU_SECRET_KEY)

    url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    params = {
        "q": text,
        "from": from_lang,
        "to": to_lang,
        "appid": BAIDU_APP_ID,
        "salt": salt,
        "sign": sign,
    }

    try:
        resp = httpx.get(url, params=params, timeout=10)
        resp.raise_for_status()
        result = resp.json()

        if "trans_result" in result:
            translated = result["trans_result"][0]["dst"]
            return translated

        if "error_code" in result and result["error_code"] != "0":
            print(f"  翻译 API 错误: {result.get('error_msg', '未知错误')} (code: {result['error_code']})")

    except Exception as e:
        print(f"  翻译请求失败: {e}")

    return text


def batch_translate(repos: list, desc_key: str = "description") -> list:
    """
    批量翻译仓库描述
    返回翻译后的 repo 列表（添加 translated_description 字段）
    """
    if not BAIDU_APP_ID or not BAIDU_SECRET_KEY:
        # 没配置 API，直接返回原文
        for repo in repos:
            if hasattr(repo, 'translated_description'):
                continue
            if hasattr(repo, desc_key):
                repo.translated_description = repo.description
            elif isinstance(repo, dict):
                repo["translated_description"] = repo.get(desc_key, "")
        return repos

    print(f"  开始翻译 {len(repos)} 个描述...")
    for i, repo in enumerate(repos):
        if isinstance(repo, dict):
            text = repo.get(desc_key, "")
            if text:
                time.sleep(0.3)
                translated = translate_text(text)
                repo["translated_description"] = translated
                print(f"    [{i+1}/{len(repos)}] {repo.get('name', '')}: {text[:30]}... → {translated[:30]}...")
            else:
                repo["translated_description"] = ""
        else:
            text = getattr(repo, desc_key, "")
            if text:
                time.sleep(0.3)
                translated = translate_text(text)
                repo.translated_description = translated
                print(f"    [{i+1}/{len(repos)}] {repo.name}: {text[:30]}... → {translated[:30]}...")
            else:
                repo.translated_description = ""

    return repos
