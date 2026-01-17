#!/usr/bin/env python3
"""
程序化建模功能测试脚本
验证ResourceLoader的程序化建模功能是否正常工作
"""

import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.resource_loader import ResourceLoader

def test_basic_functions():
    """测试基础建模函数"""
    print("=== 测试基础建模函数 ===")
    
    loader = ResourceLoader()
    
    # 测试创建立方体
    print("1. 测试创建立方体...")
    box = loader.create_box([0, 0, 0], [1, 1, 1])
    assert 'vertices' in box and 'faces' in box
    assert len(box['vertices']) == 8  # 立方体有8个顶点
    assert len(box['faces']) == 12    # 立方体有12个三角形面
    print("✓ 创建立方体成功")
    
    # 测试创建地面
    print("2. 测试创建地面...")
    floor = loader.create_floor(0, 0, 10, 10)
    assert 'vertices' in floor and 'faces' in floor
    print("✓ 创建地面成功")
    
    # 测试创建墙壁
    print("3. 测试创建墙壁...")
    wall_x = loader.create_wall(0, 0, 5, 'x')  # X方向墙
    wall_z = loader.create_wall(0, 0, 5, 'z')  # Z方向墙
    assert 'vertices' in wall_x and 'faces' in wall_x
    assert 'vertices' in wall_z and 'faces' in wall_z
    print("✓ 创建墙壁成功")
    
    print("所有基础函数测试通过！\n")

def test_zone_generation():
    """测试区域生成函数"""
    print("=== 测试区域生成函数 ===")
    
    loader = ResourceLoader()
    
    # 测试起点区域
    print("1. 测试起点区域生成...")
    start_area = loader.build_start_area()
    assert len(start_area) >= 4  # 地面 + 3面墙
    print(f"✓ 起点区域生成成功，包含 {len(start_area)} 个模型")
    
    # 测试主通道
    print("2. 测试主通道生成...")
    corridor = loader.build_main_corridor()
    assert len(corridor) >= 3  # 地面 + 左右墙
    print(f"✓ 主通道生成成功，包含 {len(corridor)} 个模型")
    
    # 测试火把区域
    print("3. 测试火把区域生成...")
    torch_zone = loader.build_torch_zone()
    assert 'torch_holder' in torch_zone
    print("✓ 火把区域生成成功")
    
    # 测试死路
    print("4. 测试死路生成...")
    dead_end = loader.build_dead_end()
    assert len(dead_end) >= 4  # 地面 + 左右墙 + 末端墙
    print(f"✓ 死路生成成功，包含 {len(dead_end)} 个模型")
    
    # 测试压力板区
    print("5. 测试压力板区生成...")
    plate_zone = loader.build_pressure_plate_zone()
    assert 'pressure_plate' in plate_zone
    print("✓ 压力板区生成成功")
    
    # 测试铁门区
    print("6. 测试铁门区生成...")
    gate_zone = loader.build_gate_zone()
    assert 'door_gate' in gate_zone
    print("✓ 铁门区生成成功")
    
    # 测试核心区
    print("7. 测试核心区生成...")
    core_area = loader.build_core_area()
    assert len(core_area) >= 5  # 地面 + 4面墙 + 可选火把
    print(f"✓ 核心区生成成功，包含 {len(core_area)} 个模型")
    
    # 测试终点区
    print("8. 测试终点区生成...")
    end_area = loader.build_end_area()
    assert len(end_area) >= 5  # 地面 + 4面墙
    print(f"✓ 终点区生成成功，包含 {len(end_area)} 个模型")
    
    print("所有区域生成测试通过！\n")

def test_complete_maze_generation():
    """测试完整迷宫生成"""
    print("=== 测试完整迷宫生成 ===")
    
    loader = ResourceLoader()
    
    # 生成完整迷宫
    print("生成完整迷宫...")
    maze_models = loader.generate_complete_maze()
    
    # 验证模型数量
    assert len(maze_models) > 20  # 应该有足够多的模型
    print(f"✓ 完整迷宫生成成功，包含 {len(maze_models)} 个模型")
    
    # 验证关键模型存在
    key_models = ['start_floor', 'torch_holder', 'pressure_plate', 'door_gate', 'end_floor']
    for model_name in key_models:
        assert model_name in maze_models, f"关键模型 {model_name} 缺失"
    
    print("✓ 所有关键模型都存在")
    
    # 验证模型数据结构
    for model_name, model_data in maze_models.items():
        assert 'vertices' in model_data, f"模型 {model_name} 缺少顶点数据"
        assert 'faces' in model_data, f"模型 {model_name} 缺少面数据"
        assert len(model_data['vertices']) > 0, f"模型 {model_name} 顶点数为0"
        assert len(model_data['faces']) > 0, f"模型 {model_name} 面数为0"
    
    print("✓ 所有模型数据结构正确")
    print("完整迷宫生成测试通过！\n")

def test_model_export():
    """测试模型导出功能"""
    print("=== 测试模型导出功能 ===")
    
    loader = ResourceLoader()
    
    # 创建测试输出目录
    test_output_dir = "test_output"
    os.makedirs(test_output_dir, exist_ok=True)
    
    # 导出模型
    print("导出模型到测试目录...")
    try:
        loader.export_models_to_obj(test_output_dir)
        
        # 检查导出的文件
        exported_files = os.listdir(test_output_dir)
        assert len(exported_files) > 0, "没有文件被导出"
        
        # 检查关键文件
        key_files = ['start_floor.obj', 'torch_holder.obj', 'pressure_plate.obj', 'door_gate.obj']
        for file_name in key_files:
            file_path = os.path.join(test_output_dir, file_name)
            assert os.path.exists(file_path), f"关键文件 {file_name} 未导出"
            
            # 检查文件内容
            with open(file_path, 'r') as f:
                content = f.read()
                assert 'v ' in content, f"文件 {file_name} 缺少顶点数据"
                assert 'f ' in content, f"文件 {file_name} 缺少面数据"
        
        print(f"✓ 模型导出成功，生成 {len(exported_files)} 个OBJ文件")
        
        # 清理测试文件
        for file_name in exported_files:
            os.remove(os.path.join(test_output_dir, file_name))
        os.rmdir(test_output_dir)
        print("✓ 测试文件清理完成")
        
    except Exception as e:
        print(f"✗ 模型导出测试失败: {e}")
        # 确保清理测试目录
        if os.path.exists(test_output_dir):
            for file_name in os.listdir(test_output_dir):
                os.remove(os.path.join(test_output_dir, file_name))
            os.rmdir(test_output_dir)
        raise
    
    print("模型导出测试通过！\n")

def main():
    """主测试函数"""
    print("开始测试程序化建模功能...\n")
    
    try:
        # 运行所有测试
        test_basic_functions()
        test_zone_generation()
        test_complete_maze_generation()
        test_model_export()
        
        print("🎉 所有测试通过！程序化建模功能正常工作")
        print("\n=== 测试总结 ===")
        print("✓ 基础建模函数正常")
        print("✓ 区域生成函数正常") 
        print("✓ 完整迷宫生成正常")
        print("✓ 模型导出功能正常")
        print("\n迷宫结构信息：")
        print("- 起点区: (0, 0, 0)")
        print("- 火把区: (13, 0, 0)") 
        print("- 压力板: (16, 0, -4)")
        print("- 铁门区: (18, 0, -4)")
        print("- 终点区: (30, 0, -4)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)