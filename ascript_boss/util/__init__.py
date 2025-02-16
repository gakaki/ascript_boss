import types
from ascript.android.node import Node
from ascript.android.node import Selector
from ascript.android.system import R
from ascript.android import action
from ascript.android import screen
from airscript.intent import Intent

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
        subNode = node.find(Selector(1).id(selector).visible(True))
    if not subNode:
        print(f"没有找到任何控件:{selector}")
    else:
        children = getattr(subNode, 'child', lambda: [])() or []
        # 打印时显示 innerText 列表
        print(f"{subNode.id} --{subNode.getInnerText()} -- 子节点数量:{len(children)}  -- {subNode.rect}")
    return subNode

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
