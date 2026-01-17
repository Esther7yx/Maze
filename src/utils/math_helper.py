"""
数学辅助函数 - 向量计算辅助(使用NumPy)
"""

import numpy as np

class MathHelper:
    """数学辅助类"""
    
    @staticmethod
    def normalize_vector(vector):
        """向量归一化"""
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm
    
    @staticmethod
    def distance(point1, point2):
        """计算两点间距离"""
        return np.linalg.norm(np.array(point1) - np.array(point2))
    
    @staticmethod
    def dot_product(v1, v2):
        """点积计算"""
        return np.dot(v1, v2)
    
    @staticmethod
    def cross_product(v1, v2):
        """叉积计算"""
        return np.cross(v1, v2)
    
    @staticmethod
    def angle_between_vectors(v1, v2):
        """计算两向量夹角（弧度）"""
        v1_norm = MathHelper.normalize_vector(v1)
        v2_norm = MathHelper.normalize_vector(v2)
        dot = MathHelper.dot_product(v1_norm, v2_norm)
        dot = np.clip(dot, -1.0, 1.0)  # 防止浮点误差
        return np.arccos(dot)
    
    @staticmethod
    def rotate_vector(vector, axis, angle):
        """绕轴旋转向量"""
        axis = MathHelper.normalize_vector(axis)
        cos_angle = np.cos(angle)
        sin_angle = np.sin(angle)
        
        # 罗德里格斯旋转公式
        rotated = (vector * cos_angle + 
                  np.cross(axis, vector) * sin_angle + 
                  axis * MathHelper.dot_product(axis, vector) * (1 - cos_angle))
        
        return rotated
    
    @staticmethod
    def look_at_matrix(eye, target, up):
        """生成LookAt矩阵"""
        forward = MathHelper.normalize_vector(np.array(target) - np.array(eye))
        right = MathHelper.normalize_vector(np.cross(forward, MathHelper.normalize_vector(up)))
        up = MathHelper.normalize_vector(np.cross(right, forward))
        
        # 构建视图矩阵
        view_matrix = np.eye(4)
        view_matrix[0, :3] = right
        view_matrix[1, :3] = up
        view_matrix[2, :3] = -forward
        view_matrix[:3, 3] = [-np.dot(right, eye), -np.dot(up, eye), np.dot(forward, eye)]
        
        return view_matrix
    
    @staticmethod
    def perspective_matrix(fov, aspect, near, far):
        """生成透视投影矩阵"""
        f = 1.0 / np.tan(fov * 0.5)
        
        perspective = np.zeros((4, 4))
        perspective[0, 0] = f / aspect
        perspective[1, 1] = f
        perspective[2, 2] = (far + near) / (near - far)
        perspective[2, 3] = (2 * far * near) / (near - far)
        perspective[3, 2] = -1.0
        
        return perspective
    
    @staticmethod
    def lerp(a, b, t):
        """线性插值"""
        return a + (b - a) * t
    
    @staticmethod
    def slerp(q1, q2, t):
        """球面线性插值（四元数）"""
        # 计算点积
        dot = MathHelper.dot_product(q1, q2)
        
        # 如果点积为负，取反以保证最短路径
        if dot < 0.0:
            q2 = -q2
            dot = -dot
        
        # 如果角度很小，使用线性插值
        if dot > 0.9995:
            result = MathHelper.lerp(q1, q2, t)
            return MathHelper.normalize_vector(result)
        
        # 计算角度和插值
        theta_0 = np.arccos(dot)
        theta = theta_0 * t
        
        q3 = q2 - q1 * dot
        q3 = MathHelper.normalize_vector(q3)
        
        return q1 * np.cos(theta) + q3 * np.sin(theta)
    
    @staticmethod
    def clamp(value, min_val, max_val):
        """限制值在范围内"""
        return max(min_val, min(value, max_val))
    
    @staticmethod
    def smooth_step(edge0, edge1, x):
        """平滑步进函数"""
        x = MathHelper.clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
        return x * x * (3 - 2 * x)

class Vector3:
    """三维向量类"""
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
    
    def to_array(self):
        """转换为数组"""
        return np.array([self.x, self.y, self.z])
    
    def from_array(self, arr):
        """从数组设置值"""
        self.x, self.y, self.z = arr
        return self
    
    def magnitude(self):
        """计算模长"""
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self):
        """归一化"""
        mag = self.magnitude()
        if mag > 0:
            self.x /= mag
            self.y /= mag
            self.z /= mag
        return self
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __str__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"