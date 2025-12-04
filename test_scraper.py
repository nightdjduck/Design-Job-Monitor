"""测试爬虫功能"""
from scraper import JobScraper
import config

def test_scraper():
    """测试爬虫"""
    scraper = JobScraper()
    
    print("测试爬虫功能...\n")
    
    for company_name, company_info in config.COMPANIES.items():
        print(f"测试 {company_name}...")
        try:
            jobs = scraper.scrape_company(
                company_name,
                company_info['url'],
                company_info['keywords']
            )
            print(f"  找到 {len(jobs)} 个设计相关岗位")
            for job in jobs[:3]:  # 只显示前3个
                print(f"    - {job['title']}")
            print()
        except Exception as e:
            print(f"  错误: {e}\n")

if __name__ == "__main__":
    test_scraper()

