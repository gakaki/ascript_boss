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
        if hasattr(child, 'child'):
            result.extend(child.getInnerTexts())
    return [item for item in result if item is not None and item != '']

def getInnerText(self):
    result = ""
    children = self.child() or []  # 确保 children 为可迭代对象
    for child in children:
        if hasattr(child, 'text') and child.text:
            result += child.text
        if hasattr(child, 'child'):
            result += child.getInnerText()
    return result

setattr(Node, 'getInnerText', getInnerText)
setattr(Node, 'getInnerTexts', getInnerTexts)