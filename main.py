"""主程序 - 监控各公司的设计岗位招聘"""
import time
import schedule
from scraper import JobScraper
from telegram_notifier import TelegramNotifier
from storage import load_jobs, save_jobs, add_job, is_new_job
import config
import asyncio


def check_jobs():
    """检查所有公司的设计岗位"""
    print(f"\n{'='*50}")
    print(f"开始检查时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")
    
    # 加载已记录的岗位
    jobs_data, file_exists = load_jobs()
    
    # 如果文件不存在，说明是首次运行（或数据丢失）
    is_first_run = not file_exists
    if is_first_run:
        print("⚠️ 检测到首次运行（或数据文件不存在），本次将初始化数据但不发送具体岗位通知。")
    
    # 初始化爬虫和通知器
    try:
        scraper = JobScraper()
        if not scraper.driver:
            print("错误: 爬虫初始化失败，跳过本次检查")
            return
    except Exception as e:
        print(f"错误: 爬虫初始化异常 - {e}")
        return

    notifier = TelegramNotifier()
    
    new_jobs_found = []
    
    # 遍历所有公司
    for company_name, company_info in config.COMPANIES.items():
        url = company_info['url']
        keywords = company_info['keywords']
        
        try:
            # 抓取岗位信息
            jobs = scraper.scrape_company(company_name, url, keywords)
            
            print(f"{company_name}: 找到 {len(jobs)} 个设计相关岗位")
            
            # 检查是否有新岗位
            for job in jobs:
                job_id = scraper.generate_job_id(
                    job['title'], 
                    company_name, 
                    job.get('link', '')
                )
                
                # 判断是否为新岗位
                is_new = is_new_job(company_name, job_id, jobs_data)
                
                if is_new:
                    # 添加到数据记录
                    add_job(company_name, job_id, jobs_data)
                    
                    # 只有在非首次运行时，才加入发送列表
                    if not is_first_run:
                        print(f"  ✨ 新岗位: {job['title']}")
                        new_jobs_found.append(job)
                    else:
                        print(f"  📝 初始化记录: {job['title']}")
                else:
                    # print(f"  ✓ 已存在: {job['title']}")
                    pass
        
        except Exception as e:
            print(f"{company_name}: 检查失败 - {e}")
    
    # 主动关闭 driver
    try:
        scraper.driver.quit()
    except:
        pass

    # 保存更新后的数据
    save_jobs(jobs_data)
    
    # 发送通知
    if new_jobs_found:
        print(f"\n发现 {len(new_jobs_found)} 个新岗位，正在发送通知...")
        notifier.send_notification_sync(new_jobs_found)
        print("通知发送完成！")
    elif is_first_run:
        print("\n首次运行初始化完成，已记录所有现有岗位。")
        # 可选：发送一条初始化完成的消息
        init_message = [{
            'company': 'System',
            'title': '监控系统初始化完成',
            'link': 'https://github.com/nightdjduck/Design-Job-Monitor'
        }]
        notifier.send_notification_sync(init_message)
    else:
        print("\n未发现新岗位。")
    
    print(f"\n{'='*50}\n")


import sys
import argparse

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='设计岗位监控系统')
    parser.add_argument('--loop', action='store_true', help='以循环模式运行（每小时检查一次），否则只运行一次')
    args = parser.parse_args()

    print("=" * 50)
    print("设计岗位监控系统启动 (Selenium版)")
    print("=" * 50)
    
    # 检查配置
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("\n⚠️  警告: Telegram 配置未设置")
        print("请在 .env 文件中设置 TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID")
        print("程序将继续运行，但不会发送通知\n")
    
    # 立即执行一次检查
    check_jobs()
    
    if args.loop:
        # 设置定时任务
        schedule.every(config.CHECK_INTERVAL_MINUTES).minutes.do(check_jobs)
        
        print(f"监控已启动，每 {config.CHECK_INTERVAL_MINUTES} 分钟检查一次")
        print("按 Ctrl+C 停止监控\n")
        
        # 运行定时任务
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次是否有待执行的任务
        except KeyboardInterrupt:
            print("\n\n监控已停止")
    else:
        print("检查完成。如需循环监控，请使用 --loop 参数。")


if __name__ == "__main__":
    main()
