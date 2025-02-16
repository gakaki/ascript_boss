from .util import *
from dataclasses import dataclass, field
from typing import List
import re
import time
from ascript.android import action, screen
from airscript.action import key
from airscript.action import slide
import random

@dataclass
class Job:
    title: str = ""         # 算法工程师
    company_name: str = ""  # 博才企业管理咨询（上海）有限公司
    company_state: str = "" # 已融资 尚未融资
    human_count: str = ""    # 10-50人
    salary: str = ""        # 15k-30k tv_salary_statue
    salary_start: str = "" 
    salary_end: str = ""
    annual_max_wan: str = ""

    tags: List[str] = field(default_factory=list)
    hr_name: str = ""
    activity: str = ""
    city_str: str = ""
    is_english_fluently: bool = False  # 新增属性
    is_shanghai: bool = False          # 新增属性

    def check_english_fluency(self):
        """
        当 tags 中包含 "口语" 时，设置 is_english_fluently 为 True，否则False。
        """
        self.is_english_fluently = any("口语" in tag for tag in self.tags)
    
    def check_shanghai(self):
        """
        判断 city_str 是否表明在上海：
        如果 city_str 同时包含 "上海" 和 "区"，则认为在上海，设置 is_shanghai 为 True。
        """
        if "上海" in self.city_str and "区" in self.city_str:
            self.is_shanghai = True
        else:
            self.is_shanghai = False


def get_random_sleep_time():
    """生成2-5秒之间的随机浮点数，保留1位小数"""
    return round(random.uniform(2.0, 5.0), 1)
def step_single():
    id_ui_card = "boss_job_card_view"
    # 尝试寻找当前卡片
    node = find_node(None, id_ui_card)
    if not node:
        print(f"未找到卡片，退出循环。{id_ui_card}")
        return None
        
    if node:
        job = Job()
        job.title           = node.find_sub_node_text("cl_position")
        processed_texts     = process_special_yolo_texts(job.title)
        print(processed_texts)
        
        job.company_name    = node.find_sub_node_text("tv_company_name")
        job.company_state   = node.find_sub_node_text("tv_stage")

        job.salary          = node.find_sub_node_text("tv_salary_statue")  
        salary              = parse_salary(job.salary)
        print(f"当前职位的最大年薪 {salary.annual_max_wan} 万")

        job.salary_start    = salary.price_start
        job.salary_end      = salary.price_end
        job.annual_max_wan  = f"{salary.annual_max_wan}万"

        job.human_count     = node.find_sub_node_text("tv_scale")

        job.tags            = node.find_sub_node_text("fl_require_info")
        job.check_english_fluency()
        print(job.is_english_fluently)
        job.hr_name         = node.find_sub_node_text("tv_employer")
        job.city_str        = node.find_sub_node_text("ll_area_and_distance")
        
        # 判断是否在上海
        job.check_shanghai()
        print(f"is_shanghai: {job.is_shanghai}")
        
        print(job)

        # # 点击卡片
        # print(f"点击卡片: {node.id}")
        card_container_linear_layout = node.parent(1).parent(1)
        card_container_linear_layout.click() 
        # time.sleep(get_random_sleep_time())   # 随机等待2-5秒之间
        # 等待动画 这里要loading api 读取详情的 容易 跳出被检测出来
        time.sleep(2)   # 随机等待2-5秒之间

        # # node_title = node.find_node("cl_position") # 不可点击 不是所有ui都可以点击的
        # # node_title.click()

        # # 模拟后退操作（使用后退 API）
        print("执行返回操作")

        # 模拟 back 按键
        key.back() # http://doc.airscript.cn/airapi/action.html#%E6%8C%89%E9%94%AE
        # time.sleep(get_random_sleep_time())  # 等待返回完成
        time.sleep(1)  # 等待返回完成

        # # 通过解析 node.rect 获取卡片高度 
        # # http://doc.airscript.cn/airapi/node.html#node-%E5%B1%9E%E6%80%A7
        # # 示例 rect 格式："Rect(55, 405 - 1025, 749)"
        # rect_str = str(node.rect)
        # m = re.search(r"Rect\(\s*\d+,\s*(\d+)\s*-\s*\d+,\s*(\d+)", rect_str)
        # if m:
        #     top = int(m.group(1))
        #     bottom = int(m.group(2))
        #     height = bottom - top
        # else:
        #     height = 300  # 默认高度
        # node.slide(-1)
        # start_x ,  start_y      = node.rect.left , node.rect.top 
        # start_x ,  start_y      = node.rect.left , node.rect.top + node.rect.height() * 2
        # print(start_x,node.rect,node.rect.height())
        # end_x,  end_y           = start_x, node.rect.top
        # print(f"滑动屏幕: 从({start_x}, {start_y})到({end_x}, {end_y})")
        # slide(start_x, start_y, end_x, end_y,300)
        # 使用工具里的 图色助手可以方便的截图 和 模拟滑动的 位置 和 捕捉鼠标位置
        # time.sleep(1)
        # 添加随机偏移量到起点和终点坐标
        start_x = node.rect.left + get_random_offset()
        start_y = node.rect.top + node.rect.height() * 2 
        end_x = start_x 
        end_y = node.rect.top 

        print(f"滑动屏幕: 从({start_x}, {start_y})到({end_x}, {end_y})")
        slide(start_x, start_y, end_x, end_y, 300)
def get_random_offset():
    """生成10-50之间的随机偏移量"""
    return random.randint(10, 50)


def get_random_process_cards_sleep_time():
    """生成1-4秒之间的随机浮点数，保留1位小数"""
    return round(random.uniform(1.0, 10.0), 1)

def process_cards():
    count = 0
    while True:
        step_single()
        count += 1
        

        # 每6次循环后随机休眠1-4秒
        if count % 2 == 0:
            sleep_time = get_random_process_cards_sleep_time()
            print(f"已处理2个卡片，休息{sleep_time}秒...")
            time.sleep(sleep_time)

process_cards()

# 使用图片替换法查询 猎之类的文字