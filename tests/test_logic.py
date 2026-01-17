"""
测试机关逻辑功能
"""

import unittest
import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.gameplay.collision import CollisionDetector, PlayerCollider, WallCollider
from src.gameplay.traps import Key, Door, PressurePlate, TrapManager

class TestCollisionLogic(unittest.TestCase):
    """测试碰撞逻辑"""
    
    def test_aabb_collision(self):
        """测试AABB碰撞检测"""
        # 两个相交的盒子
        box1 = [0, 0, 0, 2, 2, 2]
        box2 = [1, 1, 1, 3, 3, 3]
        self.assertTrue(CollisionDetector.aabb_collision(box1, box2))
        
        # 不相交的盒子
        box3 = [0, 0, 0, 1, 1, 1]
        box4 = [2, 2, 2, 3, 3, 3]
        self.assertFalse(CollisionDetector.aabb_collision(box3, box4))
    
    def test_sphere_aabb_collision(self):
        """测试球体与AABB碰撞检测"""
        # 球心在AABB内
        sphere_center = [1, 1, 1]
        sphere_radius = 0.5
        aabb = [0, 0, 0, 2, 2, 2]
        self.assertTrue(CollisionDetector.sphere_aabb_collision(sphere_center, sphere_radius, aabb))
        
        # 球心在AABB外但相交
        sphere_center2 = [3, 1, 1]
        sphere_radius2 = 1.5
        self.assertTrue(CollisionDetector.sphere_aabb_collision(sphere_center2, sphere_radius2, aabb))
        
        # 不相交
        sphere_center3 = [4, 4, 4]
        sphere_radius3 = 0.5
        self.assertFalse(CollisionDetector.sphere_aabb_collision(sphere_center3, sphere_radius3, aabb))
    
    def test_player_wall_collision(self):
        """测试玩家与墙壁碰撞"""
        player = PlayerCollider([1, 0, 1])
        wall = WallCollider([2, 0, 1], [2, 3, 0.2])
        
        # 玩家与墙壁相交
        self.assertTrue(player.check_collision(wall))
        
        # 玩家远离墙壁
        player.position = [5, 0, 5]
        self.assertFalse(player.check_collision(wall))

class TestTrapLogic(unittest.TestCase):
    """测试机关逻辑"""
    
    def setUp(self):
        """测试前准备"""
        self.trap_manager = TrapManager()
    
    def test_key_collection(self):
        """测试钥匙收集"""
        key = Key([0, 0, 0])
        
        # 初始状态
        self.assertTrue(key.active)
        self.assertFalse(key.collected)
        
        # 触发交互
        key.on_interact()
        
        # 验证状态变化
        self.assertFalse(key.active)
        self.assertTrue(key.collected)
    
    def test_door_opening(self):
        """测试门开启"""
        door = Door([0, 0, 0])
        
        # 初始状态
        self.assertTrue(door.active)
        self.assertFalse(door.opened)
        self.assertEqual(door.open_progress, 0.0)
        
        # 触发交互
        door.on_interact()
        
        # 验证状态变化
        self.assertTrue(door.opened)
    
    def test_pressure_plate_activation(self):
        """测试压力板激活"""
        pressure_plate = PressurePlate([0, 0, 0])
        test_trap = Key([1, 0, 0])
        
        # 关联机关
        pressure_plate.add_target_trap(test_trap)
        
        # 初始状态
        self.assertFalse(pressure_plate.pressed)
        self.assertTrue(test_trap.active)
        
        # 触发压力板
        pressure_plate.on_interact()
        
        # 验证状态变化
        self.assertTrue(pressure_plate.pressed)
        self.assertTrue(test_trap.collected)  # 关联机关也被触发
    
    def test_trap_manager(self):
        """测试机关管理器"""
        key = Key([0, 0, 0])
        door = Door([2, 0, 0])
        
        # 添加机关到管理器
        self.trap_manager.add_trap(key)
        self.trap_manager.add_trap(door)
        
        # 验证机关数量
        self.assertEqual(len(self.trap_manager.get_traps()), 2)
        
        # 更新管理器
        player_position = [0, 0, 0]
        player_radius = 0.5
        self.trap_manager.update(0.1, player_position, player_radius)
        
        # 验证钥匙被收集（因为玩家位置与钥匙碰撞）
        self.assertTrue(key.collected)

class TestMathHelper(unittest.TestCase):
    """测试数学辅助函数"""
    
    def test_vector_operations(self):
        """测试向量操作"""
        from src.utils.math_helper import MathHelper, Vector3
        
        # 测试向量归一化
        v1 = [3, 0, 4]
        normalized = MathHelper.normalize_vector(v1)
        self.assertAlmostEqual(np.linalg.norm(normalized), 1.0, places=6)
        
        # 测试距离计算
        point1 = [0, 0, 0]
        point2 = [3, 4, 0]
        distance = MathHelper.distance(point1, point2)
        self.assertAlmostEqual(distance, 5.0, places=6)
        
        # 测试Vector3类
        vec = Vector3(1, 2, 3)
        self.assertEqual(vec.x, 1)
        self.assertEqual(vec.y, 2)
        self.assertEqual(vec.z, 3)
        
        # 测试向量运算
        vec2 = Vector3(2, 3, 4)
        result = vec + vec2
        self.assertEqual(result.x, 3)
        self.assertEqual(result.y, 5)
        self.assertEqual(result.z, 7)

if __name__ == '__main__':
    unittest.main()