"""网页爬虫模块 - 使用 Selenium 抓取各公司的招聘信息"""
import time
import re
from typing import List, Dict
from urllib.parse import urljoin, urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class JobScraper:
    """招聘信息爬虫 (Selenium 版)"""
    
    def __init__(self):
        self.options = Options()
        # 无头模式，不显示浏览器窗口
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        # 伪装 User-Agent
        self.options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # 初始化 driver
        try:
            # Selenium 4.6+ 自动管理驱动，无需手动指定 Service
            self.driver = webdriver.Chrome(options=self.options)
            
            # 设置页面加载超时
            self.driver.set_page_load_timeout(30)
        except Exception as e:
            print(f"Selenium 初始化失败: {e}")
            self.driver = None

    def __del__(self):
        """析构函数，关闭浏览器"""
        if hasattr(self, 'driver') and self.driver:
            try:
                self.driver.quit()
            except:
                pass

    def scrape_company(self, company_name: str, url: str, keywords: List[str]) -> List[Dict]:
        """抓取指定公司的设计岗位"""
        if not self.driver:
            print("Driver 未初始化，无法抓取")
            return []
            
        try:
            print(f"正在抓取 {company_name} ...")
            self.driver.get(url)
            
            # 等待页面加载（针对不同公司可能需要不同的等待策略）
            self._wait_for_content(company_name)
            
            # 获取页面源码
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # 根据公司名称使用不同的抓取策略
            if company_name == "Airbnb":
                return self._scrape_airbnb(soup, keywords)
            elif company_name == "OpenAI":
                return self._scrape_openai(soup, keywords)
            elif company_name == "Binance":
                return self._scrape_binance(soup, keywords)
            elif company_name == "Bitget":
                return self._scrape_bitget(soup, keywords, url)
            elif company_name == "Bybit":
                return self._scrape_bybit(soup, keywords)
            elif company_name == "Ethena.fi":
                return self._scrape_generic(soup, keywords, url)
            else:
                return self._scrape_generic(soup, keywords, url)
                
        except Exception as e:
            print(f"抓取 {company_name} 失败: {e}")
            return []

    def _wait_for_content(self, company_name: str):
        """等待特定内容加载"""
        try:
            # 通用等待
            time.sleep(5)
            
            # 针对特定公司的滚动或等待逻辑
            if company_name in ["Binance", "Bitget", "Bybit"]:
                # 滚动到底部以触发懒加载
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
        except:
            pass

    def _is_design_job(self, text: str, keywords: List[str]) -> bool:
        """检查文本是否包含设计相关关键词"""
        if not text:
            return False
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in keywords)

    def generate_job_id(self, title: str, company: str, link: str = "") -> str:
        """生成岗位唯一ID"""
        import hashlib
        content = f"{company}_{title}_{link}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def _scrape_airbnb(self, soup: BeautifulSoup, keywords: List[str]) -> List[Dict]:
        """抓取 Airbnb"""
        jobs = []
        # Airbnb 职位列表通常在 main 或 section 中
        # 排除 footer 等无关区域
        main_content = soup.find('main') or soup
        
        links = main_content.find_all('a', href=True)
        seen = set()
        
        for link in links:
            text = link.get_text(strip=True)
            if len(text) < 5 or "Reasonable Accommodation" in text:
                continue
                
            if self._is_design_job(text, keywords):
                href = link['href']
                if not href.startswith('http'):
                    href = urljoin("https://careers.airbnb.com/", href)
                
                if text not in seen:
                    seen.add(text)
                    jobs.append({
                        'title': text,
                        'link': href,
                        'company': 'Airbnb'
                    })
        return jobs

    def _scrape_openai(self, soup: BeautifulSoup, keywords: List[str]) -> List[Dict]:
        """抓取 OpenAI"""
        jobs = []
        # OpenAI 职位链接
        links = soup.find_all('a', href=True)
        seen = set()
        
        for link in links:
            text = link.get_text(strip=True)
            # 查找内部包含职位的元素
            if not text:
                # 尝试找 h3/h4/div 等
                title_elem = link.find(['h3', 'h4', 'span'])
                if title_elem:
                    text = title_elem.get_text(strip=True)
            
            if len(text) < 5:
                continue

            if self._is_design_job(text, keywords):
                href = link['href']
                if not href.startswith('http'):
                    href = urljoin("https://openai.com/", href)
                
                if text not in seen:
                    seen.add(text)
                    jobs.append({
                        'title': text,
                        'link': href,
                        'company': 'OpenAI'
                    })
        return jobs

    def _scrape_binance(self, soup: BeautifulSoup, keywords: List[str]) -> List[Dict]:
        """抓取 Binance"""
        jobs = []
        # Binance 职位列表
        job_cards = soup.find_all(['div', 'a'], class_=re.compile(r'job|card|item', re.I))
        seen = set()
        
        for card in job_cards:
            text = card.get_text(strip=True)
            if self._is_design_job(text, keywords):
                # 尝试提取具体标题
                title = text
                # 如果是链接直接用
                if card.name == 'a':
                    href = card.get('href', '')
                else:
                    link_elem = card.find('a', href=True)
                    href = link_elem['href'] if link_elem else ''
                    # 尝试在 card 中找标题元素
                    title_elem = card.find(['h4', 'h5', 'div'], class_=re.compile('title'))
                    if title_elem:
                        title = title_elem.get_text(strip=True)

                if not href.startswith('http'):
                    href = urljoin("https://www.binance.com", href)
                
                if title not in seen:
                    seen.add(title)
                    jobs.append({
                        'title': title[:100],
                        'link': href,
                        'company': 'Binance'
                    })
        return jobs

    def _scrape_bitget(self, soup: BeautifulSoup, keywords: List[str], base_url: str) -> List[Dict]:
        """抓取 Bitget (MokaHR)"""
        jobs = []
        # Bitget 使用 MokaHR，通常是 div 列表
        job_items = soup.find_all('div', class_=re.compile(r'job-item|item', re.I))
        seen = set()
        
        for item in job_items:
            text = item.get_text(strip=True)
            if self._is_design_job(text, keywords):
                # 尝试获取标题
                title_elem = item.find(['div', 'span', 'h3'], class_=re.compile('title|name', re.I))
                title = title_elem.get_text(strip=True) if title_elem else text[:50]
                
                # 获取链接 (可能需要点击，或者直接分析 href)
                # MokaHR 可能会用 JS 跳转，这里直接使用列表页 URL
                link = base_url
                
                if title not in seen:
                    seen.add(title)
                    jobs.append({
                        'title': title,
                        'link': link,
                        'company': 'Bitget'
                    })
        return jobs
        
    def _scrape_bybit(self, soup: BeautifulSoup, keywords: List[str]) -> List[Dict]:
        """抓取 Bybit"""
        return self._scrape_generic(soup, keywords, "https://jobs.bybitglobal.com/")

    def _scrape_generic(self, soup: BeautifulSoup, keywords: List[str], base_url: str) -> List[Dict]:
        """通用抓取"""
        jobs = []
        seen = set()
        
        links = soup.find_all('a', href=True)
        for link in links:
            text = link.get_text(strip=True)
            href = link['href']
            
            if len(text) < 4 or text.lower() in ['home', 'careers', 'jobs', 'about us']:
                continue
                
            if self._is_design_job(text, keywords):
                if not href.startswith('http'):
                    href = urljoin(base_url, href)
                
                if text not in seen:
                    seen.add(text)
                    jobs.append({
                        'title': text[:100],
                        'link': href,
                        'company': urlparse(base_url).netloc
                    })
        return jobs
