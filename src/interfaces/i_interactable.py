from abc import ABC, abstractmethod
import numpy as np

class IGameplaySystem(ABC):
    """
    [成员 C 需实现此接口]
    定义交互系统与机关逻辑的标准行为。
    """

    @abstractmethod
    def check_collision(self, player_pos: np.array, velocity: np.array) -> np.array:
        """
        计算玩家移动时的物理碰撞。
        :param player_pos: 当前玩家位置
        :param velocity: 玩家期望的移动向量
        :return: 修正后的安全位置 (Safe Position)
        碰撞检测：基于 AABB 碰撞盒编写代码，避免穿墙
        """
        pass

    @abstractmethod
    def handle_interaction(self, ray_origin: np.array, ray_direction: np.array) -> dict:
        """
        处理鼠标点击交互（射线检测）。
        :param ray_origin: 鼠标射线原点
        :param ray_direction: 鼠标射线方向
        :return: 交互事件结果，例如 {'event': 'ignite_torch', 'target_id': 101} 或 None
        机关触发：基于射线检测实现鼠标交互
        """
        pass

    @abstractmethod
    def get_trap_state(self, trap_id: int) -> str:
        """
        获取特定机关当前的状态，用于测试验证或 UI 显示。
        :return: 'locked', 'unlocked', 'active' 等状态字符串
        独立测试机关逻辑完整性
        """
        pass

    @abstractmethod
    def trigger_feedback(self, event_type: str):
        """
        触发场景化反馈（音效、震动）。
        :param event_type: 事件类型，如 'door_open_sound'
        场景化反馈：添加音效、震动
        """
        pass