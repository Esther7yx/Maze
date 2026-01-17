"""
碰撞检测 - AABB碰撞检测算法
"""

import numpy as np

class CollisionDetector:
    """碰撞检测器"""
    
    @staticmethod
    def aabb_collision(box1, box2):
        """
        AABB碰撞检测
        box1/box2: [min_x, min_y, min_z, max_x, max_y, max_z]
        """
        return (box1[0] <= box2[3] and box1[3] >= box2[0] and
                box1[1] <= box2[4] and box1[4] >= box2[1] and
                box1[2] <= box2[5] and box1[5] >= box2[2])
    
    @staticmethod
    def sphere_aabb_collision(sphere_center, sphere_radius, aabb):
        """球体与AABB碰撞检测"""
        # 找到AABB上距离球心最近的点
        closest_point = [
            max(aabb[0], min(sphere_center[0], aabb[3])),
            max(aabb[1], min(sphere_center[1], aabb[4])),
            max(aabb[2], min(sphere_center[2], aabb[5]))
        ]
        
        # 计算距离
        distance = np.linalg.norm(np.array(sphere_center) - np.array(closest_point))
        
        return distance <= sphere_radius
    
    @staticmethod
    def ray_aabb_intersection(ray_origin, ray_direction, aabb):
        """射线与AABB相交检测"""
        t_min = 0.0
        t_max = float('inf')
        
        for i in range(3):
            if abs(ray_direction[i]) < 1e-6:
                # 射线平行于轴
                if ray_origin[i] < aabb[i] or ray_origin[i] > aabb[i+3]:
                    return False, 0
            else:
                t1 = (aabb[i] - ray_origin[i]) / ray_direction[i]
                t2 = (aabb[i+3] - ray_origin[i]) / ray_direction[i]
                
                if t1 > t2:
                    t1, t2 = t2, t1
                
                t_min = max(t_min, t1)
                t_max = min(t_max, t2)
                
                if t_min > t_max:
                    return False, 0
        
        return True, t_min
    
    @staticmethod
    def point_in_aabb(point, aabb):
        """点是否在AABB内"""
        return (aabb[0] <= point[0] <= aabb[3] and
                aabb[1] <= point[1] <= aabb[4] and
                aabb[2] <= point[2] <= aabb[5])

class CollisionObject:
    """碰撞物体基类"""
    def __init__(self, position, bounds):
        self.position = np.array(position, dtype=np.float32)
        self.bounds = bounds  # 相对于位置的边界偏移
        
    def get_aabb(self):
        """获取世界坐标系下的AABB"""
        return [
            self.position[0] + self.bounds[0],
            self.position[1] + self.bounds[1],
            self.position[2] + self.bounds[2],
            self.position[0] + self.bounds[3],
            self.position[1] + self.bounds[4],
            self.position[2] + self.bounds[5]
        ]
    
    def check_collision(self, other):
        """检查与另一个物体的碰撞"""
        return CollisionDetector.aabb_collision(self.get_aabb(), other.get_aabb())

class PlayerCollider(CollisionObject):
    """玩家碰撞体"""
    def __init__(self, position, radius=0.5, height=2.0):
        # 圆柱体近似为AABB
        bounds = [-radius, 0, -radius, radius, height, radius]
        super().__init__(position, bounds)
        self.radius = radius
        self.height = height

class WallCollider(CollisionObject):
    """墙壁碰撞体"""
    def __init__(self, position, size):
        # size: [width, height, depth]
        bounds = [-size[0]/2, 0, -size[2]/2, size[0]/2, size[1], size[2]/2]
        super().__init__(position, bounds)