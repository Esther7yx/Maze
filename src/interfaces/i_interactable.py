# src/interfaces/i_interactable.py
from abc import ABC, abstractmethod
import numpy as np

class IInteractable(ABC):
    """
    [基础接口] 所有可交互物体（机关）必须继承此类
    用于 src/gameplay/traps.py
    """
    @abstractmethod
    def on_interact(self):
        """当被交互时触发"""
        pass
        
    @abstractmethod
    def update(self, delta_time):
        """每帧更新状态"""
        pass

class IGameplaySystem(ABC):
    """
    [成员 C 需实现此接口]
    定义整个交互系统的对外标准行为
    """
    @abstractmethod
    def handle_interaction(self, ray_origin, ray_direction) -> dict:
        """处理交互检测"""
        pass
        
    @abstractmethod
    def trigger_feedback(self, event_type: str):
        """触发反馈"""
        pass