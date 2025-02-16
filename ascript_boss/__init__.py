from .util import *
from dataclasses import dataclass

@dataclass
class Job:
    title: str = ""         # 算法工程师
    company_name: str = ""  # 博才企业管理咨询（上海）有限公司
    company_state: str = "" # 已融资 尚未融资
    human_count: str = ""    # 10-50人
    price_start: str = ""
    price_end: str = ""
    tags_str: str = ""
    # tags : list = []
    hr_name: str = ""
    hr_position: str = ""
    activity:str = ""
    city_str: str = ""

# s = Selector(1|2).id("com.hpbr.bosszhipin:id/tv_company_name").visible(True).find().getInnerText()
# print(s)

id_ui_card      = "boss_job_card_view"
node = find_node(None,id_ui_card)
if node:
    # print(node.find_all_sub_node_id_with_text())

    job = Job()
    job.title           = node.find_sub_node_text("cl_position")
    # 急聘
    #todo:需要使用yolo查询 猎头这几个关键词
    job.company_name    = node.find_sub_node_text("tv_company_name")

    processed_texts = process_special_yolo_texts(job.title)
    print(processed_texts)
    
    # job.company_state   = node.find_sub_node_text("tv_stage")
    # job.human_count     = node.find_sub_node_text("tv_scale")
    # job.price_start     = node.find_sub_node_text("tv_salary")
    # job.price_end       = node.find_sub_node_text("tv_salary")
    # job.tags_str        = node.find_sub_node_text("ll_tag")
    # job.hr_name         = node.find_sub_node_text("tv_name")
    # job.hr_position     = node.find_sub_node_text("tv_position")
    # job.activity        = node.find_sub_node_text("tv_position_name")
    # job.city_str        = node.find_sub_node_text("ll_area_and_distance")
    # job.title           = node.find_sub_node_text("tv_position_name")
    # job.company_name    = node.find_sub_node_text("tv_company_name")
    # job.company_state   = node.find_sub_node_text("tv_stage
    # job.human_count   = node.find_sub_node_text("tv_scale")



    # job.human_count     = node.find_sub_node_text("fl_require_info")
    # job.title           = node.find_sub_node_text("tv_position_name")
    # job.title           = node.find_sub_node_text("tv_position_name")
    # job.activity        = node.find_sub_node_text("tv_position_name")
    #job.city_str        = node.find_sub_node_text("ll_area_and_distance")
    print(job)
    # txt_job_position    = node.find_sub_node("cl_position")
    # print(txt_job_position.getInnerText())
    #
    #
    # pos_name = text_pos.find( Selector(1|2).id("com.hpbr.bosszhipin:id/tv_position_name"))
    # print(pos_name.id)
    # print(pos_name.text)
    #
    #
    # p = Person()
    # p.name = 'gakaki'
    # print(p)
else:
    print('没有找到任何控件')