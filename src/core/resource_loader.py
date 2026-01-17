"""
资源加载器 - 负责加载OBJ模型和程序化建模
基于OpenGL程序化建模方案，生成固定路线迷宫
"""

import os
import numpy as np
from PIL import Image

class ResourceLoader:
    def __init__(self, assets_path="../assets"):
        self.assets_path = assets_path
        self.loaded_models = {}
        self.loaded_textures = {}
        
        # 世界坐标系约定
        self.WALL_HEIGHT = 3.0      # 墙高
        self.WALL_THICKNESS = 0.3   # 墙厚
        self.CORRIDOR_WIDTH = 2.5   # 通道宽
        self.GROUND_Y = 0.0         # 地面高度
    
    def load_obj_model(self, filename):
        """加载OBJ模型文件"""
        if filename in self.loaded_models:
            return self.loaded_models[filename]
        
        file_path = os.path.join(self.assets_path, "models", filename)
        
        try:
            vertices = []
            faces = []
            
            with open(file_path, 'r') as file:
                for line in file:
                    if line.startswith('v '):
                        # 顶点坐标
                        vertex = list(map(float, line.strip().split()[1:4]))
                        vertices.append(vertex)
                    elif line.startswith('f '):
                        # 面索引
                        face = [int(idx.split('/')[0]) - 1 for idx in line.strip().split()[1:]]
                        faces.append(face)
            
            model_data = {
                'vertices': np.array(vertices, dtype=np.float32),
                'faces': np.array(faces, dtype=np.uint32)
            }
            
            self.loaded_models[filename] = model_data
            return model_data
            
        except Exception as e:
            print(f"Error loading OBJ model {filename}: {e}")
            return None
    
    def load_texture(self, filename):
        """加载纹理图片"""
        if filename in self.loaded_textures:
            return self.loaded_textures[filename]
        
        file_path = os.path.join(self.assets_path, "textures", filename)
        
        try:
            image = Image.open(file_path)
            image_data = np.array(image)
            
            self.loaded_textures[filename] = image_data
            return image_data
            
        except Exception as e:
            print(f"Error loading texture {filename}: {e}")
            return None
    
    def load_audio(self, filename):
        """加载音频文件"""
        file_path = os.path.join(self.assets_path, "audio", filename)
        
        # 这里只是返回文件路径，实际音频加载由音频系统处理
        if os.path.exists(file_path):
            return file_path
        else:
            print(f"Audio file not found: {filename}")
            return None
    
    def clear_cache(self):
        """清空资源缓存"""
        self.loaded_models.clear()
        self.loaded_textures.clear()

    # ==================== 程序化建模基础函数 ====================
    
    def create_box(self, center, size):
        """
        创建立方体模型
        center: [x, y, z] 中心点坐标
        size: [width, height, depth] 尺寸
        """
        half_w, half_h, half_d = size[0]/2, size[1]/2, size[2]/2
        
        # 定义8个顶点
        vertices = [
            # 前面
            [center[0] - half_w, center[1] - half_h, center[2] + half_d],
            [center[0] + half_w, center[1] - half_h, center[2] + half_d],
            [center[0] + half_w, center[1] + half_h, center[2] + half_d],
            [center[0] - half_w, center[1] + half_h, center[2] + half_d],
            # 后面
            [center[0] - half_w, center[1] - half_h, center[2] - half_d],
            [center[0] + half_w, center[1] - half_h, center[2] - half_d],
            [center[0] + half_w, center[1] + half_h, center[2] - half_d],
            [center[0] - half_w, center[1] + half_h, center[2] - half_d]
        ]
        
        # 定义12个三角形面（立方体6个面，每个面2个三角形）
        faces = [
            # 前面
            [0, 1, 2], [2, 3, 0],
            # 后面
            [4, 7, 6], [6, 5, 4],
            # 左面
            [4, 0, 3], [3, 7, 4],
            # 右面
            [1, 5, 6], [6, 2, 1],
            # 上面
            [3, 2, 6], [6, 7, 3],
            # 下面
            [4, 5, 1], [1, 0, 4]
        ]
        
        return {
            'vertices': np.array(vertices, dtype=np.float32),
            'faces': np.array(faces, dtype=np.uint32)
        }
    
    def create_floor(self, center_x, center_z, width, depth, thickness=0.1):
        """创建地面"""
        return self.create_box(
            [center_x, self.GROUND_Y - thickness/2, center_z],
            [width, thickness, depth]
        )
    
    def create_wall(self, center_x, center_z, length, orientation='x'):
        """
        创建墙壁
        orientation: 'x' 或 'z' 方向
        """
        if orientation == 'x':
            # X方向的墙
            return self.create_box(
                [center_x, self.WALL_HEIGHT/2, center_z],
                [length, self.WALL_HEIGHT, self.WALL_THICKNESS]
            )
        else:
            # Z方向的墙
            return self.create_box(
                [center_x, self.WALL_HEIGHT/2, center_z],
                [self.WALL_THICKNESS, self.WALL_HEIGHT, length]
            )

    # ==================== 区域生成函数 ====================
    
    def build_start_area(self):
        """构建起点区域"""
        models = {}
        
        # 地面 (6x6)
        models['start_floor'] = self.create_floor(0, 0, 6, 6)
        
        # 围墙 (留+X方向出口)
        models['start_wall_north'] = self.create_wall(0, 3, 6, 'z')  # 北墙
        models['start_wall_south'] = self.create_wall(0, -3, 6, 'z')  # 南墙
        models['start_wall_west'] = self.create_wall(-3, 0, 6, 'x')  # 西墙
        # 东墙留空作为出口
        
        return models
    
    def build_main_corridor(self):
        """构建主通道1（教学走廊）"""
        models = {}
        
        # 地面 (从x=3到x=13)
        corridor_length = 10
        corridor_center_x = 3 + corridor_length/2
        models['corridor_floor'] = self.create_floor(corridor_center_x, 0, corridor_length, self.CORRIDOR_WIDTH)
        
        # 左右墙
        wall_z_offset = self.CORRIDOR_WIDTH/2 + self.WALL_THICKNESS/2
        models['corridor_wall_left'] = self.create_wall(corridor_center_x, -wall_z_offset, corridor_length, 'x')
        models['corridor_wall_right'] = self.create_wall(corridor_center_x, wall_z_offset, corridor_length, 'x')
        
        return models
    
    def build_torch_zone(self):
        """构建火把教学区"""
        models = {}
        
        # 火把基座 (小立方体)
        torch_position = [13, 0, 0]
        torch_size = [0.5, 1.2, 0.5]
        models['torch_holder'] = self.create_box(torch_position, torch_size)
        
        return models
    
    def build_dead_end(self):
        """构建假路（死路）"""
        models = {}
        
        # 死路通道 (从x=10, z=0 到 z=6)
        dead_end_length = 6
        dead_end_center_z = dead_end_length/2
        
        # 地面
        models['dead_end_floor'] = self.create_floor(10, dead_end_center_z, self.CORRIDOR_WIDTH, dead_end_length)
        
        # 左右墙
        wall_x_offset = self.CORRIDOR_WIDTH/2 + self.WALL_THICKNESS/2
        models['dead_end_wall_left'] = self.create_wall(10 - wall_x_offset, dead_end_center_z, dead_end_length, 'z')
        models['dead_end_wall_right'] = self.create_wall(10 + wall_x_offset, dead_end_center_z, dead_end_length, 'z')
        
        # 末端封墙
        models['dead_end_wall_end'] = self.create_wall(10, dead_end_length, self.CORRIDOR_WIDTH + self.WALL_THICKNESS*2, 'x')
        
        return models
    
    def build_pressure_plate_zone(self):
        """构建压力板区"""
        models = {}
        
        # 压力板
        plate_position = [16, 0.1, -4]  # 稍微高于地面
        plate_size = [1.5, 0.2, 1.5]
        models['pressure_plate'] = self.create_box(plate_position, plate_size)
        
        # 连接通道的地面
        models['plate_zone_floor'] = self.create_floor(16, -4, 4, 4)
        
        return models
    
    def build_gate_zone(self):
        """构建铁门区"""
        models = {}
        
        # 铁门 (完全挡路)
        gate_position = [18, self.WALL_HEIGHT/2, -4]
        gate_size = [2.5, 3.0, 0.3]
        models['door_gate'] = self.create_box(gate_position, gate_size)
        
        return models
    
    def build_core_area(self):
        """构建核心机关区"""
        models = {}
        
        # 地面 (8x8)
        models['core_floor'] = self.create_floor(22, -4, 8, 8)
        
        # 围墙
        models['core_wall_north'] = self.create_wall(22, 0, 8, 'z')  # 北墙
        models['core_wall_south'] = self.create_wall(22, -8, 8, 'z')  # 南墙
        models['core_wall_west'] = self.create_wall(18, -4, 8, 'x')  # 西墙
        models['core_wall_east'] = self.create_wall(26, -4, 8, 'x')  # 东墙
        
        # 可选：额外火把
        torch_position = [22, 0, -4]
        torch_size = [0.5, 1.2, 0.5]
        models['core_torch'] = self.create_box(torch_position, torch_size)
        
        return models
    
    def build_end_area(self):
        """构建终点区"""
        models = {}
        
        # 地面 (6x6)
        models['end_floor'] = self.create_floor(30, -4, 6, 6)
        
        # 围墙 (无出口)
        models['end_wall_north'] = self.create_wall(30, -1, 6, 'z')  # 北墙
        models['end_wall_south'] = self.create_wall(30, -7, 6, 'z')  # 南墙
        models['end_wall_west'] = self.create_wall(27, -4, 6, 'x')  # 西墙
        models['end_wall_east'] = self.create_wall(33, -4, 6, 'x')  # 东墙
        
        return models
    
    def generate_complete_maze(self):
        """生成完整迷宫模型"""
        maze_models = {}
        
        # 按顺序构建所有区域
        maze_models.update(self.build_start_area())
        maze_models.update(self.build_main_corridor())
        maze_models.update(self.build_torch_zone())
        maze_models.update(self.build_dead_end())
        maze_models.update(self.build_pressure_plate_zone())
        maze_models.update(self.build_gate_zone())
        maze_models.update(self.build_core_area())
        maze_models.update(self.build_end_area())
        
        return maze_models
    
    def export_models_to_obj(self, output_dir="../assets/models"):
        """导出模型为OBJ文件"""
        os.makedirs(output_dir, exist_ok=True)
        
        maze_models = self.generate_complete_maze()
        
        for model_name, model_data in maze_models.items():
            obj_file = os.path.join(output_dir, f"{model_name}.obj")
            
            with open(obj_file, 'w') as f:
                # 写入顶点
                for vertex in model_data['vertices']:
                    f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
                
                # 写入面
                for face in model_data['faces']:
                    # OBJ格式的面索引从1开始
                    face_indices = [str(idx + 1) for idx in face]
                    f.write(f"f {' '.join(face_indices)}\n")
            
            print(f"Exported: {obj_file}")
        
        print("All maze models exported successfully!")