# src/core/game_manager.py

class GameManager:
    def __init__(self, renderer: IRenderer, gameplay: IGameplaySystem):
        self.renderer = renderer
        self.gameplay = gameplay
        self.fps_monitor = PerfMonitor() # 你的 FPS 监控模块

    def game_loop(self):
        while True:
            # 1. 获取输入 (假设得到 mouse_click)
            if mouse_click:
                # [D 调用 C] 检测交互
                event = self.gameplay.handle_interaction(cam_pos, mouse_ray)
                
                # [D 的核心调度逻辑] 
                # 文档 : 机关触发 -> 调用光照参数更新
                if event and event['type'] == 'ignite_torch':
                    # C 告诉 D 火把点着了，D 负责通知 B 必须把灯打开
                    light_id = event['target_id']
                    self.renderer.update_light_param(light_id, 'intensity', 1.0)
                    # D 通知 C 播放音效
                    self.gameplay.trigger_feedback('fire_sound')

            # 2. [D 性能优化] 检查帧率
            # 文档 : 低帧率区域调整参数
            current_fps = self.fps_monitor.get_fps()
            if current_fps < 30:
                self.renderer.set_quality_level(0) # 降级为低画质
            else:
                self.renderer.set_quality_level(2)

            # 3. [D 调用 B] 渲染画面
            self.renderer.render_frame(cam_pos, cam_dir, dt)