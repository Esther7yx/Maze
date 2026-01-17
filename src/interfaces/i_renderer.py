# src/interfaces/i_renderer.py
from abc import ABC, abstractmethod
import numpy as np

class IRenderer(ABC):
    """
    [成员 B 需实现此接口]
    定义光线追踪渲染器的标准行为。
    """
    
    @abstractmethod
    def initialize(self, width: int, height: int):
        """初始化渲染环境"""
        pass

    @abstractmethod
    def load_model(self, model_data: dict):
        """加载模型数据"""
        pass

    @abstractmethod
    def render_frame(self):
        """执行单帧渲染"""
        pass

    @abstractmethod
    def update_light_param(self, light_id: int, param_type: str, value: float):
        """
        [关键接口] 响应机关触发带来的光照变化。
        """
        pass

    @abstractmethod
    def set_quality_level(self, level: int):
        """
        [性能优化接口] 0=低, 1=中, 2=高
        """
        pass