"""Telegram 通知模块"""
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from typing import List, Dict
import config


class TelegramNotifier:
    """Telegram 通知类"""
    
    def __init__(self):
        self.bot_token = config.TELEGRAM_BOT_TOKEN
        self.chat_id = config.TELEGRAM_CHAT_ID
        self.bot = None
        
        if self.bot_token:
            self.bot = Bot(token=self.bot_token)
    
    async def send_notification(self, jobs: List[Dict]):
        """发送岗位通知"""
        if not self.bot or not self.chat_id:
            print("警告: Telegram 配置未设置，无法发送通知")
            return False
        
        if not jobs:
            return True
        
        try:
            for job in jobs:
                message = self._format_message(job)
                await self.bot.send_message(
                    chat_id=self.chat_id,
                    text=message,
                    parse_mode='HTML',
                    disable_web_page_preview=False
                )
                # 避免发送过快
                await asyncio.sleep(1)
            
            return True
        except TelegramError as e:
            print(f"发送 Telegram 通知失败: {e}")
            return False
    
    def _format_message(self, job: Dict) -> str:
        """格式化消息"""
        company = job.get('company', '未知公司')
        title = job.get('title', '未知职位')
        link = job.get('link', '#')
        
        message = f"""
🎨 <b>新设计岗位发布！</b>

🏢 <b>公司:</b> {company}
💼 <b>职位:</b> {title}
🔗 <b>链接:</b> <a href="{link}">查看详情</a>
"""
        return message.strip()
    
    def send_notification_sync(self, jobs: List[Dict]):
        """同步发送通知（用于非异步环境）"""
        if not self.bot_token or not self.chat_id:
            print("警告: Telegram 配置未设置，无法发送通知")
            return False
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.send_notification(jobs))

