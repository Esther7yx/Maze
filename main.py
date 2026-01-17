"""
MazeGame - 3D迷宫游戏主程序入口
"""

import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.game_manager import GameManager
from src.core.resource_loader import ResourceLoader
from src.core.perf_monitor import PerfMonitor
from src.renderer.ray_tracer import RayTracer
from src.gameplay.traps import TrapManager

def main():
    """主函数"""
    print("=== MazeGame 3D迷宫游戏 ===")
    print("正在初始化游戏...")
    
    # 初始化游戏管理器（单例）
    game_manager = GameManager()
    
    # 初始化资源加载器
    resource_loader = ResourceLoader()
    
    # 初始化性能监控器
    perf_monitor = PerfMonitor()
    
    # 初始化光线追踪器
    ray_tracer = RayTracer()
    
    # 初始化机关管理器
    trap_manager = TrapManager()
    
    try:
        # 初始化渲染器
        print("初始化渲染器...")
        ray_tracer.initialize(800, 600)
        
        # 加载测试模型（如果有）
        print("加载资源...")
        # 这里可以加载实际的模型文件
        # model_data = resource_loader.load_obj_model("maze.obj")
        # if model_data:
        #     ray_tracer.load_model(model_data)
        
        # 创建测试机关
        print("初始化游戏逻辑...")
        # 创建测试钥匙
        test_key = Key([1, 0, 1])
        trap_manager.add_trap(test_key)
        
        # 创建测试门
        test_door = Door([3, 0, 1])
        trap_manager.add_trap(test_door)
        
        # 开始游戏
        game_manager.start_game()
        print("游戏开始！")
        
        # 主游戏循环
        running = True
        while running and game_manager.game_state == "playing":
            # 更新性能监控
            perf_monitor.update()
            
            # 渲染帧
            ray_tracer.render_frame()
            
            # 更新机关逻辑
            trap_manager.update(0.016, game_manager.player_position, 0.5)
            
            # 显示性能信息（控制台）
            if perf_monitor.frame_count % 60 == 0:  # 每秒显示一次
                print(perf_monitor.display_stats())
            
            # 简单的退出条件（实际游戏中应该处理用户输入）
            if game_manager.score >= 100:  # 测试用
                game_manager.game_over()
                print("游戏胜利！")
        
    except Exception as e:
        print(f"游戏运行出错: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理资源
        print("清理资源...")
        ray_tracer.cleanup()
        print("游戏结束。")

if __name__ == "__main__":
    main()