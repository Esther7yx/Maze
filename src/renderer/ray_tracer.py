"""
光线追踪器 - PyOpenGL设置与渲染循环
"""

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from .bvh_builder import BVHBuilder

class RayTracer:
    def __init__(self):
        self.screen = None
        self.clock = None
        self.running = False
        self.bvh_builder = BVHBuilder()
        self.models = []
        self.camera_position = [0.0, 0.0, 5.0]
        self.camera_rotation = [0.0, 0.0, 0.0]
    
    def initialize(self, width=800, height=600):
        """初始化OpenGL环境"""
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption("MazeGame - Ray Tracer")
        
        # 设置OpenGL
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        
        # 设置光照
        glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        
        # 设置投影矩阵
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (width / height), 0.1, 50.0)
        
        self.clock = pygame.time.Clock()
        self.running = True
    
    def load_model(self, model_data):
        """加载模型数据"""
        if model_data:
            self.models.append(model_data)
            # 为模型构建BVH树
            self.bvh_builder.build_bvh(model_data)
    
    def load_texture(self, texture_data):
        """加载纹理数据"""
        # 这里简化处理，实际需要创建OpenGL纹理
        pass
    
    def set_camera_position(self, x, y, z):
        """设置相机位置"""
        self.camera_position = [x, y, z]
    
    def set_camera_rotation(self, pitch, yaw, roll):
        """设置相机旋转"""
        self.camera_rotation = [pitch, yaw, roll]
    
    def render_frame(self):
        """渲染一帧"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # 设置模型视图矩阵
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # 设置相机
        gluLookAt(
            self.camera_position[0], self.camera_position[1], self.camera_position[2],  # 相机位置
            0, 0, 0,  # 观察点
            0, 1, 0   # 上向量
        )
        
        # 渲染模型
        for model in self.models:
            self._render_model(model)
        
        pygame.display.flip()
    
    def _render_model(self, model):
        """渲染单个模型"""
        vertices = model['vertices']
        faces = model['faces']
        
        glBegin(GL_TRIANGLES)
        for face in faces:
            for vertex_idx in face:
                if vertex_idx < len(vertices):
                    vertex = vertices[vertex_idx]
                    glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()
    
    def run(self):
        """运行渲染循环"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.render_frame()
            self.clock.tick(60)  # 限制为60FPS
    
    def cleanup(self):
        """清理资源"""
        pygame.quit()