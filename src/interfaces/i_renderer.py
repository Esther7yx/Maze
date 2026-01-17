"""
渲染器接口定义 - 定义B必须实现的渲染接口
"""

from abc import ABC, abstractmethod

class IRenderer(ABC):
    """渲染器接口"""
    
    @abstractmethod
    def initialize(self, width, height):
        """初始化渲染器"""
        pass
    
    @abstractmethod
    def render_frame(self):
        """渲染一帧"""
        pass
    
    @abstractmethod
    def load_model(self, model_data):
        """加载模型数据"""
        pass
    
    @abstractmethod
    def load_texture(self, texture_data):
        """加载纹理数据"""
        pass
    
    @abstractmethod
    def set_camera_position(self, x, y, z):
        """设置相机位置"""
        pass
    
    @abstractmethod
    def set_camera_rotation(self, pitch, yaw, roll):
        """设置相机旋转"""
        pass
    
    @abstractmethod
    def cleanup(self):
        """清理资源"""
        pass