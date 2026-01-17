# MazeGame 核心接口文档

## 项目概述

MazeGame是一个基于Python和OpenGL的3D迷宫游戏项目，采用模块化设计，支持光线追踪渲染和复杂的机关交互系统。

## 程序化建模方案

### 设计理念
采用**OpenGL程序化建模**方案，实现最省力、100%满足作业要求、不给B/C/D添麻烦的设计目标。

### 世界坐标系约定
- **右手坐标系**，Y轴向上
- **单位尺度**：1.0 = 1米
- **地面高度**：y = 0
- **墙高**：3.0米
- **通道宽**：2.5米
- **墙厚**：0.3米

### 基础几何体
仅使用3种基础几何体：
- **长方体**：墙、铁门、压力板
- **大平面**：地面
- **小立方体**：火把基座

### 迷宫结构（俯视）
```
Z
↑
│        ┌───── 假路（死路）
│        │
│  Start ├──────────┐
│        │          │
│        │      PressurePlate
│        │          │
│        └── Torch ──┴── Gate ── Core ── End
│
└──────────────────────────→ X
```

特点：只有一条能通关的主路，假路作为视觉干扰元素。

## 核心接口定义

### 1. 渲染器接口 (IRenderer)

**文件位置**: `src/interfaces/i_renderer.py`

#### 接口方法

- `initialize(width, height)` - 初始化渲染器
- `render_frame()` - 渲染一帧
- `load_model(model_data)` - 加载模型数据
- `load_texture(texture_data)` - 加载纹理数据
- `set_camera_position(x, y, z)` - 设置相机位置
- `set_camera_rotation(pitch, yaw, roll)` - 设置相机旋转
- `cleanup()` - 清理资源

#### 实现要求

- 必须支持OpenGL渲染环境
- 需要实现光线追踪基础功能
- 支持BVH树加速结构
- 提供实时性能监控

### 2. 可交互接口 (IInteractable)

**文件位置**: `src/interfaces/i_interactable.py`

#### 接口方法

- `check_collision(player_position, player_radius)` - 检查碰撞
- `on_interact()` - 交互时触发
- `update(delta_time)` - 更新逻辑
- `get_position()` - 获取位置
- `is_active()` - 是否活跃

#### 实现要求

- 所有机关必须实现此接口
- 支持AABB碰撞检测
- 提供状态管理和动画支持

## 核心模块架构

### 1. 核心管理模块 (core/)

#### GameManager (单例模式)
- 管理游戏全局状态
- 控制游戏流程（开始、暂停、结束）
- 维护玩家数据和关卡信息

#### ResourceLoader
- 统一资源加载接口
- 支持OBJ模型和图片纹理
- 提供资源缓存机制
- **程序化建模功能**：
  - `create_box()` - 创建立方体
  - `create_floor()` - 创建地面
  - `create_wall()` - 创建墙壁
  - 区域生成函数：`build_start_area()`, `build_main_corridor()`等
  - `generate_complete_maze()` - 生成完整迷宫
  - `export_models_to_obj()` - 导出OBJ文件

#### PerfMonitor
- 实时FPS计算和显示
- 性能统计和监控
- 帧时间分析

### 2. 图形渲染模块 (renderer/)

#### RayTracer
- PyOpenGL环境设置
- 渲染循环管理
- 相机控制系统

#### BVHBuilder
- BVH树构建算法
- 射线求交优化
- 空间分割策略

### 3. 游戏逻辑模块 (gameplay/)

#### CollisionDetector
- AABB碰撞检测
- 球体与AABB碰撞
- 射线相交检测

#### Trap系统
- Key: 钥匙收集机关
- Door: 门开启机关
- PressurePlate: 压力板机关
- MovingPlatform: 移动平台机关

## 数据格式规范

### OBJ模型格式
```python
model_data = {
    'vertices': np.array([[x1, y1, z1], [x2, y2, z2], ...]),
    'faces': np.array([[v1, v2, v3], [v4, v5, v6], ...])
}
```

### 纹理数据格式
```python
texture_data = np.array([...])  # PIL Image转换为numpy数组
```

### 碰撞边界格式
```python
# AABB边界框
bounds = [min_x, min_y, min_z, max_x, max_y, max_z]
```

## 开发规范

### 代码规范
- 使用Python类型注解
- 遵循PEP 8代码风格
- 模块间通过接口通信
- 错误处理使用异常机制

### 测试要求
- 每个模块必须有单元测试
- 测试覆盖率不低于80%
- 集成测试验证模块协作

## 扩展接口

### 自定义机关接口
开发者可以通过继承`IInteractable`接口创建新的机关类型：

```python
class CustomTrap(IInteractable):
    def __init__(self, position, custom_params):
        super().__init__(position, bounds)
        # 自定义初始化
    
    def on_interact(self):
        # 自定义交互逻辑
        pass
```

### 自定义渲染器接口
开发者可以通过继承`IRenderer`接口创建新的渲染后端：

```python
class CustomRenderer(IRenderer):
    def initialize(self, width, height):
        # 自定义初始化逻辑
        pass
    
    def render_frame(self):
        # 自定义渲染逻辑
        pass
```

## 版本历史

- v1.0.0: 初始版本，基础框架搭建
- 支持模块化架构设计
- 实现核心接口定义
- 提供基础测试框架

## 联系方式

- 项目负责人: 成员D
- 开发团队: MazeGame开发组
- 最后更新: 2026年1月17日