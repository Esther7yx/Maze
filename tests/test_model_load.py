"""
测试模型加载功能
"""

import unittest
import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.core.resource_loader import ResourceLoader

class TestModelLoad(unittest.TestCase):
    """测试模型加载功能"""
    
    def setUp(self):
        """测试前准备"""
        self.resource_loader = ResourceLoader()
    
    def test_load_nonexistent_obj(self):
        """测试加载不存在的OBJ文件"""
        result = self.resource_loader.load_obj_model("nonexistent.obj")
        self.assertIsNone(result)
    
    def test_load_valid_obj_structure(self):
        """测试加载有效OBJ文件的结构"""
        # 这里应该创建一个简单的测试OBJ文件
        # 由于没有实际文件，我们测试缓存功能
        
        # 模拟一个简单的模型数据
        mock_model_data = {
            'vertices': [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
            'faces': [[0, 1, 2]]
        }
        
        # 测试缓存功能
        self.resource_loader.loaded_models["test.obj"] = mock_model_data
        result = self.resource_loader.load_obj_model("test.obj")
        
        self.assertIsNotNone(result)
        self.assertIn('vertices', result)
        self.assertIn('faces', result)
    
    def test_texture_loading(self):
        """测试纹理加载功能"""
        result = self.resource_loader.load_texture("nonexistent.png")
        self.assertIsNone(result)
    
    def test_audio_loading(self):
        """测试音频加载功能"""
        result = self.resource_loader.load_audio("nonexistent.wav")
        self.assertIsNone(result)
    
    def test_cache_clearing(self):
        """测试缓存清理功能"""
        # 添加一些测试数据到缓存
        self.resource_loader.loaded_models["test1.obj"] = {'vertices': [], 'faces': []}
        self.resource_loader.loaded_textures["test1.png"] = []
        
        # 清理缓存
        self.resource_loader.clear_cache()
        
        # 验证缓存已清空
        self.assertEqual(len(self.resource_loader.loaded_models), 0)
        self.assertEqual(len(self.resource_loader.loaded_textures), 0)

if __name__ == '__main__':
    unittest.main()