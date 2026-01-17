"""
游戏管理器 - 单例模式，管理游戏状态
"""

class GameManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.game_state = "menu"  # menu, playing, paused, game_over
            self.current_level = 1
            self.player_position = [0.0, 0.0, 0.0]
            self.score = 0
            self.lives = 3
            self._initialized = True
    
    def start_game(self):
        """开始游戏"""
        self.game_state = "playing"
        self.current_level = 1
        self.player_position = [0.0, 0.0, 0.0]
        self.score = 0
        self.lives = 3
    
    def pause_game(self):
        """暂停游戏"""
        if self.game_state == "playing":
            self.game_state = "paused"
    
    def resume_game(self):
        """恢复游戏"""
        if self.game_state == "paused":
            self.game_state = "playing"
    
    def game_over(self):
        """游戏结束"""
        self.game_state = "game_over"
    
    def next_level(self):
        """进入下一关"""
        self.current_level += 1
        self.player_position = [0.0, 0.0, 0.0]
    
    def update_player_position(self, x, y, z):
        """更新玩家位置"""
        self.player_position = [x, y, z]
    
    def add_score(self, points):
        """增加分数"""
        self.score += points
    
    def lose_life(self):
        """失去一条生命"""
        self.lives -= 1
        if self.lives <= 0:
            self.game_over()