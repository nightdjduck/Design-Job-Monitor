"""配置文件"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram 配置
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# 监控配置
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "60"))

# 公司招聘页面配置
COMPANIES = {
    "Airbnb": {
        "url": "https://careers.airbnb.com/positions/?_offices=china",
        "keywords": ["design", "designer", "ui", "ux", "visual", "graphic", "product design", "设计"]
    },
    "OpenAI": {
        "url": "https://openai.com/careers/search/?c=f6aa76fa-ec6f-4dd8-b3c7-531e313e3e63",
        "keywords": ["design", "designer", "ui", "ux", "visual", "graphic", "product design", "设计"]
    },
    "Binance": {
        "url": "https://www.binance.com/en/careers/department?name=Product%20%26%20Design&team=Design&job=",
        "keywords": ["design", "designer", "ui", "ux", "visual", "graphic", "product design", "设计"]
    },
    "Bitget": {
        "url": "https://hire-r1.mokahr.com/social-recruitment/bitget/100000079#/jobs?zhineng%5B0%5D=100004123",
        "keywords": ["design", "designer", "ui", "ux", "visual", "graphic", "product design", "设计"]
    },
    "Bybit": {
        "url": "https://jobs.bybitglobal.com/social-recruitment/bybit/45685#/jobs?department%5B0%5D=1110472",
        "keywords": ["design", "designer", "ui", "ux", "visual", "graphic", "product design", "设计"]
    },
    "Ethena.fi": {
        "url": "https://x.com/ethena_labs/jobs",
        "keywords": ["design", "designer", "ui", "ux", "visual", "graphic", "product design", "设计"]
    },

}

