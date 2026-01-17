# MazeGame - 3D迷宫游戏项目

## 项目简介

MazeGame是一个基于Python和OpenGL开发的3D迷宫游戏，采用模块化架构设计，支持光线追踪渲染和复杂的机关交互系统。项目采用团队协作开发模式，每个成员负责不同的模块。

## 项目特色

- 🎮 **3D迷宫探索** - 沉浸式3D迷宫环境
- 🌟 **光线追踪渲染** - 基于PyOpenGL的高质量渲染
- 🔑 **机关系统** - 丰富的交互机关（钥匙、门、压力板等）
- 🏗️ **模块化架构** - 清晰的接口定义和模块分离
- 📊 **性能监控** - 实时FPS和性能统计

## 项目结构

```
MazeGame_Project/
├── assets/                  # 资源目录
│   ├── models/              # .obj模型文件
│   ├── textures/            # .png/.jpg纹理文件
│   └── audio/               # .wav/.mp3音效文件
├── docs/                    # 文档目录
│   └── interface_doc.md     # 核心接口文档
├── src/                     # 源代码包
│   ├── core/                # 核心管理模块
│   │   ├── game_manager.py  # 单例模式，管理游戏状态
│   │   ├── resource_loader.py  # 负责加载OBJ和图片
│   │   └── perf_monitor.py  # FPS计算与显示类
│   ├── interfaces/          # 定义抽象基类(ABC)
│   │   ├── i_renderer.py    # 定义渲染接口
│   │   └── i_interactable.py  # 定义交互接口
│   ├── renderer/            # 图形渲染模块
│   │   ├── ray_tracer.py    # PyOpenGL设置与渲染循环
│   │   ├── bvh_builder.py   # BVH树构建逻辑
│   │   └── shaders/         # GLSL着色器文件
│   ├── gameplay/            # 游戏逻辑模块
│   │   ├── collision.py     # AABB碰撞检测算法
│   │   └── traps.py         # 机关逻辑(Key,Door类)
│   └── utils/               # 通用工具
│       └── math_helper.py   # 向量计算辅助(使用NumPy)
├── tests/                   # 测试代码
│   ├── test_model_load.py   # 测试模型加载
│   └── test_logic.py        # 测试机关逻辑
├── main.py                  # 程序入口，启动游戏
├── requirements.txt         # 依赖库列表
└── README.md               # 项目说明文档
```

## 安装指南

### 环境要求

- Python 3.8+
- Windows/Linux/macOS

### 安装步骤

1. 克隆项目到本地
```bash
git clone <项目地址>
cd MazeGame_Project
```

2. 安装依赖库
```bash
pip install -r requirements.txt
```

3. 运行游戏
```bash
python main.py
```

## 团队分工

### 成员A - 资源管理
- 负责assets目录下的所有资源文件
- 提供测试用的模型、纹理和音效
- 确保资源格式符合项目规范

### 成员B - 图形渲染
- 实现`src/renderer/`模块
- 负责光线追踪器和BVH构建器
- 优化渲染性能和视觉效果

### 成员C - 游戏逻辑
- 实现`src/gameplay/`模块
- 负责碰撞检测和机关系统
- 确保游戏逻辑的正确性

### 成员D - 核心架构
- 设计并实现核心接口和架构
- 负责模块间的协调和集成
- 编写文档和测试代码

## 开发指南

### 代码规范

- 遵循PEP 8代码风格
- 使用类型注解
- 模块间通过接口通信
- 每个功能模块必须有对应的测试

### 接口定义

项目采用接口驱动的设计模式，主要接口包括：

- `IRenderer` - 渲染器接口
- `IInteractable` - 可交互接口

详细接口定义请参考[接口文档](docs/interface_doc.md)。

### 测试运行

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试模块
python -m pytest tests/test_model_load.py

# 生成测试覆盖率报告
python -m pytest --cov=src tests/
```

## 技术架构

### 渲染系统
- **PyOpenGL** - 底层图形API
- **光线追踪** - 高质量的全局光照
- **BVH树** - 空间分割加速结构
- **实时性能监控** - FPS和帧时间统计

### 游戏逻辑
- **AABB碰撞检测** - 高效的物理碰撞
- **机关系统** - 模块化的交互设计
- **状态管理** - 单例模式管理游戏状态

### 资源管理
- **统一加载接口** - 支持多种资源格式
- **缓存机制** - 提高资源加载效率
- **错误处理** - 健壮的资源加载流程

## 扩展开发

### 添加新机关

继承`IInteractable`接口创建新的机关类型：

```python
from src.interfaces.i_interactable import IInteractable

class NewTrap(IInteractable):
    def __init__(self, position, custom_params):
        super().__init__(position, bounds)
        # 自定义初始化
    
    def on_interact(self):
        # 自定义交互逻辑
        pass
```

### 自定义渲染器

继承`IRenderer`接口创建新的渲染后端：

```python
from src.interfaces.i_renderer import IRenderer

class CustomRenderer(IRenderer):
    def initialize(self, width, height):
        # 自定义初始化
        pass
    
    def render_frame(self):
        # 自定义渲染逻辑
        pass
```

## 常见问题

### Q: 运行游戏时出现OpenGL错误
A: 确保系统支持OpenGL 3.3+，并安装了正确的显卡驱动。

### Q: 模型加载失败
A: 检查OBJ文件格式是否正确，确保文件路径正确。

### Q: 性能问题
A: 可以调整渲染分辨率或关闭一些特效来提升性能。

## 版本历史

- **v1.0.0** (2026-01-17)
  - 项目基础框架搭建完成
  - 核心接口和模块定义
  - 基础测试框架

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 联系方式

- 项目负责人: 成员D
- 开发团队: MazeGame开发组
- 项目仓库: <项目地址>