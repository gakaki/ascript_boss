from .util import *
from dataclasses import dataclass

id_app          = "com.hpbr.bosszhipin:id"
id_ui_container = "cl_card_container"
id_ui_card      = "view_job_card"
def find_node(node,id_name):
    selector = f"{id_app}/{id_name}"
    subNode = None
    if not node:
        subNode = Selector(1|2).id(selector).visible(True).find()
    else:
        subNode = node.find( Selector(1|2).id(selector).visible(True))
    
    if not subNode:
        print(f"没有找到任何控件:{selector}")
    else:
        print(f"{subNode.id} --{subNode.getInnerTexts()} -- 子节点数量:{len(subNode.child())}  -- {subNode.rect}")
    return subNode


def find_sub_node_text(self,id_name):
    node = find_node(self,id_name)
    if node:
        return node.getInnerText()
    else:
        return ""
setattr(Node, 'find_sub_node_text', find_sub_node_text)

def find_all_sub_node_id_with_text(self):
    result = {}
    # 确保 self.child() 返回一个可迭代对象
    children = self.child() or []
    for sub_node in children:
        node_id = getattr(sub_node, 'id', None)
        node_text = sub_node.getInnerText() if hasattr(sub_node, 'getInnerText') else ""
        # 仅当节点id存在且文本不为空时加入结果
        # if node_id is not None and node_text:
        result[node_id] = node_text
        print(f"Node ID: {node_id}, Text: {node_text}")
        # 递归调用获取子节点的子节点
        if hasattr(sub_node, 'find_all_sub_node_id_with_text'):
            sub_result = sub_node.find_all_sub_node_id_with_text() or {}
            result.update(sub_result)
    # 过滤最终结果中没有文本的节点
    filtered_result = {k: v for k, v in result.items() if v}
    return filtered_result

setattr(Node, 'find_all_sub_node_id_with_text', find_all_sub_node_id_with_text)




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

node = find_node(None,id_ui_card)
if node:
    # print(node.find_all_sub_node_id_with_text())

    job = Job()
    job.title           = node.find_sub_node_text("cl_position")
    #todo:需要使用yolo查询 猎头这几个关键词
    job.company_name    = node.find_sub_node_text("ll_company")
    job.company_state   = node.find_sub_node_text("tv_stage")
    job.human_count     = node.find_sub_node_text("tv_scale")
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