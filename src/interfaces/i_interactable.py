"""
可交互接口定义 - 定义C必须实现的交互接口
"""

from abc import ABC, abstractmethod

class IInteractable(ABC):
    """可交互接口"""
    
    @abstractmethod
    def check_collision(self, player_position, player_radius):
        """检查碰撞"""
        pass
    
    @abstractmethod
    def on_interact(self):
        """交互时触发"""
        pass
    
    @abstractmethod
    def update(self, delta_time):
        """更新逻辑"""
        pass
    
    @abstractmethod
    def get_position(self):
        """获取位置"""
        pass
    
    @abstractmethod
    def is_active(self):
        """是否活跃"""
        pass