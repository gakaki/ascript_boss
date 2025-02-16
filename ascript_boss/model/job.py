from dataclasses import dataclass

@dataclass
class Job:
    name: str = "" # 必须给默认值
    age: int = 0
