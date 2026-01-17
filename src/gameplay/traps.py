"""
机关逻辑 - 包含Key、Door等机关类
"""

from .collision import CollisionObject, CollisionDetector
from src.interfaces.i_interactable import IInteractable
import numpy as np

class Trap(IInteractable):
    """机关基类"""
    def __init__(self, position, bounds):
        self.collider = CollisionObject(position, bounds)
        self.active = True
        self.triggered = False
    
    def check_collision(self, player_position, player_radius):
        """检查与玩家的碰撞"""
        if not self.active:
            return False
        
        aabb = self.collider.get_aabb()
        return CollisionDetector.sphere_aabb_collision(player_position, player_radius, aabb)
    
    def on_interact(self):
        """交互时触发"""
        if self.active and not self.triggered:
            self.triggered = True
            self._trigger_effect()
    
    def update(self, delta_time):
        """更新逻辑"""
        pass
    
    def get_position(self):
        """获取位置"""
        return self.collider.position
    
    def is_active(self):
        """是否活跃"""
        return self.active
    
    def _trigger_effect(self):
        """触发效果（子类实现）"""
        pass

class Key(Trap):
    """钥匙机关"""
    def __init__(self, position, key_id=1):
        bounds = [-0.2, 0, -0.2, 0.2, 0.5, 0.2]  # 小盒子大小
        super().__init__(position, bounds)
        self.key_id = key_id
        self.collected = False
    
    def _trigger_effect(self):
        """收集钥匙"""
        self.collected = True
        self.active = False
        print(f"Key {self.key_id} collected!")
    
    def update(self, delta_time):
        """钥匙旋转动画"""
        if self.active:
            # 简单的旋转动画
            self.collider.position[1] = 0.5 + 0.1 * np.sin(np.pi * 2 * delta_time)

class Door(Trap):
    """门机关"""
    def __init__(self, position, required_key_id=1, size=[2, 3, 0.2]):
        bounds = [-size[0]/2, 0, -size[2]/2, size[0]/2, size[1], size[2]/2]
        super().__init__(position, bounds)
        self.required_key_id = required_key_id
        self.opened = False
        self.open_progress = 0.0  # 开门进度 0.0-1.0
    
    def _trigger_effect(self):
        """尝试开门"""
        # 这里需要检查玩家是否拥有对应的钥匙
        # 简化处理：直接开门
        if not self.opened:
            self.opened = True
            print(f"Door opened with key {self.required_key_id}!")
    
    def update(self, delta_time):
        """开门动画"""
        if self.opened and self.open_progress < 1.0:
            self.open_progress += delta_time * 2.0  # 2秒完成开门
            if self.open_progress > 1.0:
                self.open_progress = 1.0
            
            # 模拟开门动画（向右移动）
            self.collider.position[0] += delta_time * 2.0

class PressurePlate(Trap):
    """压力板机关"""
    def __init__(self, position, size=[1, 0.1, 1]):
        bounds = [-size[0]/2, 0, -size[2]/2, size[0]/2, size[1], size[2]/2]
        super().__init__(position, bounds)
        self.pressed = False
        self.target_traps = []  # 关联的机关列表
    
    def _trigger_effect(self):
        """触发压力板"""
        self.pressed = True
        # 激活所有关联的机关
        for trap in self.target_traps:
            trap.on_interact()
        print("Pressure plate activated!")
    
    def add_target_trap(self, trap):
        """添加关联机关"""
        self.target_traps.append(trap)
    
    def update(self, delta_time):
        """压力板动画"""
        if self.pressed:
            # 按下动画
            self.collider.position[1] = max(-0.1, self.collider.position[1] - delta_time)

class MovingPlatform(Trap):
    """移动平台机关"""
    def __init__(self, position, size=[2, 0.5, 2], path_points=None):
        bounds = [-size[0]/2, 0, -size[2]/2, size[0]/2, size[1], size[2]/2]
        super().__init__(position, bounds)
        
        # 移动路径点
        if path_points is None:
            path_points = [position, [position[0] + 5, position[1], position[2]]]
        self.path_points = [np.array(point, dtype=np.float32) for point in path_points]
        
        self.current_point = 0
        self.next_point = 1
        self.progress = 0.0
        self.speed = 1.0  # 移动速度
    
    def _trigger_effect(self):
        """开始移动"""
        # 压力板触发后开始移动
        pass
    
    def update(self, delta_time):
        """平台移动逻辑"""
        if len(self.path_points) < 2:
            return
        
        # 计算移动方向
        start = self.path_points[self.current_point]
        end = self.path_points[self.next_point]
        direction = end - start
        distance = np.linalg.norm(direction)
        
        if distance > 0:
            direction = direction / distance
            
            # 更新进度
            self.progress += delta_time * self.speed / distance
            
            if self.progress >= 1.0:
                # 到达下一个点
                self.progress = 0.0
                self.current_point = self.next_point
                self.next_point = (self.next_point + 1) % len(self.path_points)
            
            # 更新位置
            self.collider.position = start + direction * distance * self.progress

class TrapManager:
    """机关管理器"""
    def __init__(self):
        self.traps = []
    
    def add_trap(self, trap):
        """添加机关"""
        self.traps.append(trap)
    
    def update(self, delta_time, player_position, player_radius):
        """更新所有机关"""
        for trap in self.traps:
            trap.update(delta_time)
            
            # 检查碰撞并触发交互
            if trap.check_collision(player_position, player_radius):
                trap.on_interact()
    
    def get_traps(self):
        """获取所有机关"""
        return self.traps