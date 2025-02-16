

import random
b = random.randint(1,100)
import time
# time.sleep(2)

print("Hello AS!",b)
# 同级目录的导入
from ..ascript_boss import a
# 导入子目录文件
from .app import b

# from .app.user import c
# #导入子目录文件
# from .app import b
# from .app.user import d

# from airscript.system import R
# s = R(__file__).name + '.app.b'
# print(R(__file__),__file__,s)
# __import__(s)


from airscript.action import click,slide

# Intent.run("BOSS直聘")

# 案例1:使用应用名称启动APP,推荐萌新使用
# 根据应用名称启动. PS:启动略慢于包名启动


# 雷神模拟器
# Intent.run("BOSS直聘")
# time.sleep(1)
# print("开始点击")
# # click(540,947,2000) # 按压2秒
# print("点击结束")
# 注意要等待画面出现
# slide(540,1277,540,947,300)

# Intent.run("抖音")
#
# while True:
#     slide(660,1600,660,330)
#     ts = random.randint(1,10)
#     print("随机时间",ts)
#     time.sleep(ts)

action.input(" i am gakaki")
