"""
性能监控器 - FPS计算与显示类
"""

import time

class PerfMonitor:
    def __init__(self):
        self.frame_count = 0
        self.fps = 0
        self.last_time = time.time()
        self.frame_times = []
        
    def update(self):
        """更新帧率统计"""
        self.frame_count += 1
        current_time = time.time()
        
        # 计算FPS
        if current_time - self.last_time >= 1.0:
            self.fps = self.frame_count / (current_time - self.last_time)
            self.frame_count = 0
            self.last_time = current_time
            
            # 记录帧时间
            self.frame_times.append(self.fps)
            if len(self.frame_times) > 60:  # 保留最近60秒的数据
                self.frame_times.pop(0)
    
    def get_fps(self):
        """获取当前FPS"""
        return self.fps
    
    def get_average_fps(self, seconds=10):
        """获取平均FPS"""
        if not self.frame_times:
            return 0
        
        recent_frames = self.frame_times[-min(seconds, len(self.frame_times)):]
        return sum(recent_frames) / len(recent_frames)
    
    def get_frame_time(self):
        """获取帧时间（毫秒）"""
        if self.fps > 0:
            return 1000.0 / self.fps
        return 0
    
    def display_stats(self):
        """显示性能统计信息"""
        stats = f"FPS: {self.fps:.1f} | Avg FPS (10s): {self.get_average_fps(10):.1f} | Frame Time: {self.get_frame_time():.1f}ms"
        return stats