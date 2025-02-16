import types
from ascript.android.node import Node
from ascript.android.node import Selector
from ascript.android.system import R
from ascript.android import action
from ascript.android import screen
from airscript.intent import Intent

import re
from dataclasses import dataclass
def getInnerTexts(self):
    result = []
    children = self.child() or []  # 确保 children 为可迭代对象
    for child in children:
        if hasattr(child, 'text') and child.text:
            result.append(child.text)
        if hasattr(child, 'childCount'):
            result.extend(child.getInnerTexts())
    # 过滤空值
    return [item for item in result if item]

def getInnerText(self):
    """
    返回当前节点的文本数组，不做字符串拼接，
    并自动过滤重复与空值
    """
    # 如果没有子节点，返回自身 text（去除 None）
    if self.childCount == 0:
        return [self.text] if self.text else []
    result = []
    children = self.child() or []  # 确保 children 总是可迭代
    for child in children:
        if child.text:
            result.append(child.text)
        if hasattr(child, 'getInnerText'):
            result.extend(child.getInnerText())
    # 去除重复与空字符串
    unique = []
    for item in result:
        if item and item not in unique:
            unique.append(item)
    return unique

setattr(Node, 'getInnerText', getInnerText)
setattr(Node, 'getInnerTexts', getInnerTexts)

def find_node(node, id_name):
    id_app   = "com.hpbr.bosszhipin:id"
    selector = f"{id_app}/{id_name}"
    subNode  = None
    if not node:
        subNode = Selector(1).id(selector).visible(True).find()
    else:
        try:
            subNode = node.find(Selector(1).id(selector).visible(True))
        except Exception as e:
            print(f"没有找到任何控件:{selector}")
    if not subNode:
        print(f"没有找到任何控件:{selector}")
    else:
        children = getattr(subNode, 'child', lambda: [])() or []
        # 打印时显示 innerText 列表
        print(f"{subNode.id} --{subNode.getInnerText()} -- 子节点数量:{len(children)}  -- {subNode.rect}")
    return subNode
setattr(Node, 'find_node', find_node)

def find_sub_node_text(self, id_name):
    node = find_node(self, id_name)
    if node:
        return node.getInnerText()
    else:
        return []
setattr(Node, 'find_sub_node_text', find_sub_node_text)

def find_all_sub_node_id_with_text(self):
    """
    遍历当前节点的所有子节点（递归），返回一个字典，
    key 为节点 id，value 为该节点去重后的文本数组
    """
    result = {}
    children = getattr(self, 'child', lambda: [])() or []
    for sub_node in children:
        node_id = getattr(sub_node, 'id', None)
        # 获取去重后的文本数组
        node_text = sub_node.getInnerText() if hasattr(sub_node, 'getInnerText') else []
        if node_id and node_text:
            result[node_id] = node_text
            print(f"Node ID: {node_id}, Text: {node_text}")
        if hasattr(sub_node, 'find_all_sub_node_id_with_text'):
            sub_result = sub_node.find_all_sub_node_id_with_text() or {}
            result.update(sub_result)
    # 过滤掉值为空的条目
    filtered_result = {k: v for k, v in result.items() if v}
    return filtered_result

setattr(Node, 'find_all_sub_node_id_with_text', find_all_sub_node_id_with_text)

def yolov11_recognize(text):
    """
    模拟YOLOv11识别方法。
    实际应用中此处应调用YOLOv11模型对图像内容进行识别。
    示例：如果输入 "前端架构/开发 &@ "，则可能返回 ["急聘", "外地", "外聘"]
    """
    # 这里只是示例逻辑，实际情况需调用真实模型接口
    return ["急聘", "外地", "外聘"]

def process_special_yolo_texts(text_list):
    """
    遍历输入的文本数组，对于包含 "&@" 的项，
    调用 YOLOv11 识别返回候选结果，替换原文本。
    如果识别失败，则保留原文本。
    最后返回处理后的去重文本数组。
    """
    result = []
    for item in text_list:
        if "&@" in item:
            recognized = yolov11_recognize(item)
            if recognized:
                result.extend(recognized)
            else:
                result.append(item)
        else:
            result.append(item)
    # 去重处理
    unique = []
    for text in result:
        if text and text not in unique:
            unique.append(text)
    return unique


@dataclass
class Salary:
    price_start: float     # 月薪下限，单位：元
    price_end: float       # 月薪上限，单位：元
    months: int            # 发放薪水的月数
    annual_min: float      # 年薪最低总额（price_start * months）
    annual_max: float      # 年薪最高总额（price_end * months）
    annual_max_wan: float  # 年薪最高总额，以万元表示（annual_max/10000）

def parse_salary(salary_str: str) -> Salary:
    """
    解析薪资字符串，支持以下格式：
    - "25-40K·13薪"
    - "12000-17000元/月"
    """
    if isinstance(salary_str, list):
        salary_str = "".join(salary_str)

    # 分割薪资范围和发薪月数部分
    parts = salary_str.split("·")
    range_part = parts[0]
    month_part = parts[1] if len(parts) > 1 else "12薪"
    
    # 尝试匹配两种格式：K结尾 或 元/月结尾
    k_pattern = r"(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)[Kk]"
    yuan_pattern = r"(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)元/月"
    
    m_k = re.search(k_pattern, range_part)
    m_yuan = re.search(yuan_pattern, range_part)
    
    if m_k:
        # K单位，需要乘以1000
        price_start = float(m_k.group(1)) * 1000
        price_end = float(m_k.group(2)) * 1000
    elif m_yuan:
        # 元单位，直接使用数值
        price_start = float(m_yuan.group(1))
        price_end = float(m_yuan.group(2))
    else:
        # 尝试直接匹配数字
        number_pattern = r"(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)"
        m_number = re.search(number_pattern, range_part)
        if m_number:
            price_start = float(m_number.group(1))
            price_end = float(m_number.group(2))
        else:
            raise ValueError(f"无法解析薪资范围: {range_part}")
    
    # 解析发薪月数
    m2 = re.search(r"(\d+)", month_part)
    months = int(m2.group(1)) if m2 else 12
    
    annual_min = price_start * months
    annual_max = price_end * months
    annual_max_wan = annual_max / 10000
    
    return Salary(
        price_start=price_start,
        price_end=price_end,
        months=months,
        annual_min=annual_min,
        annual_max=annual_max,
        annual_max_wan=annual_max_wan
    )