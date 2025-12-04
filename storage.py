"""数据存储模块 - 记录已检测到的岗位"""
import json
import os
from typing import Set, Dict, List, Tuple

STORAGE_FILE = "jobs_data.json"


def load_jobs() -> Tuple[Dict[str, Set[str]], bool]:
    """
    加载已记录的岗位数据
    Returns:
        (data, file_exists): 数据字典和文件是否存在的布尔值
    """
    if not os.path.exists(STORAGE_FILE):
        return {}, False
    
    try:
        with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # 将列表转换为集合
            return {company: set(jobs) for company, jobs in data.items()}, True
    except Exception as e:
        print(f"加载数据失败: {e}")
        return {}, False


def save_jobs(jobs_data: Dict[str, Set[str]]):
    """保存岗位数据"""
    try:
        # 将集合转换为列表以便 JSON 序列化
        data = {company: list(jobs) for company, jobs in jobs_data.items()}
        with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存数据失败: {e}")


def add_job(company: str, job_id: str, jobs_data: Dict[str, Set[str]]):
    """添加新岗位到记录"""
    if company not in jobs_data:
        jobs_data[company] = set()
    jobs_data[company].add(job_id)


def is_new_job(company: str, job_id: str, jobs_data: Dict[str, Set[str]]) -> bool:
    """检查岗位是否为新岗位"""
    if company not in jobs_data:
        return True
    return job_id not in jobs_data[company]
