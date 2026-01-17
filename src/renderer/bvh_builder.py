"""
BVH构建器 - BVH树构建逻辑
"""

import numpy as np

class BVHNode:
    """BVH树节点"""
    def __init__(self, bounds=None, left=None, right=None, triangles=None):
        self.bounds = bounds  # [min_x, min_y, min_z, max_x, max_y, max_z]
        self.left = left
        self.right = right
        self.triangles = triangles  # 叶子节点存储的三角形索引

class BVHBuilder:
    def __init__(self):
        self.root = None
    
    def build_bvh(self, model_data):
        """为模型构建BVH树"""
        vertices = model_data['vertices']
        faces = model_data['faces']
        
        # 将面转换为三角形
        triangles = []
        for face in faces:
            if len(face) >= 3:
                # 只处理三角形面
                triangle = [vertices[face[0]], vertices[face[1]], vertices[face[2]]]
                triangles.append(triangle)
        
        if triangles:
            self.root = self._build_node(triangles, 0)
    
    def _build_node(self, triangles, depth):
        """递归构建BVH节点"""
        if len(triangles) <= 4 or depth >= 20:  # 叶子节点条件
            return BVHNode(
                bounds=self._calculate_bounds(triangles),
                triangles=triangles
            )
        
        # 计算所有三角形的中心点
        centers = []
        for triangle in triangles:
            center = np.mean(triangle, axis=0)
            centers.append(center)
        
        # 选择分割轴（选择方差最大的轴）
        centers_array = np.array(centers)
        variances = np.var(centers_array, axis=0)
        split_axis = np.argmax(variances)
        
        # 按中心点坐标排序
        sorted_triangles = sorted(zip(centers, triangles), key=lambda x: x[0][split_axis])
        triangles_sorted = [tri for _, tri in sorted_triangles]
        
        # 分割为左右两部分
        mid = len(triangles_sorted) // 2
        left_triangles = triangles_sorted[:mid]
        right_triangles = triangles_sorted[mid:]
        
        # 递归构建左右子树
        left_node = self._build_node(left_triangles, depth + 1)
        right_node = self._build_node(right_triangles, depth + 1)
        
        # 合并边界框
        left_bounds = left_node.bounds
        right_bounds = right_node.bounds
        bounds = [
            min(left_bounds[0], right_bounds[0]),
            min(left_bounds[1], right_bounds[1]),
            min(left_bounds[2], right_bounds[2]),
            max(left_bounds[3], right_bounds[3]),
            max(left_bounds[4], right_bounds[4]),
            max(left_bounds[5], right_bounds[5])
        ]
        
        return BVHNode(bounds=bounds, left=left_node, right=right_node)
    
    def _calculate_bounds(self, triangles):
        """计算三角形集合的边界框"""
        if not triangles:
            return [0, 0, 0, 0, 0, 0]
        
        min_coords = [float('inf'), float('inf'), float('inf')]
        max_coords = [float('-inf'), float('-inf'), float('-inf')]
        
        for triangle in triangles:
            for vertex in triangle:
                for i in range(3):
                    min_coords[i] = min(min_coords[i], vertex[i])
                    max_coords[i] = max(max_coords[i], vertex[i])
        
        return min_coords + max_coords
    
    def ray_intersect(self, ray_origin, ray_direction):
        """射线与BVH树求交"""
        if self.root is None:
            return None
        
        return self._ray_intersect_node(self.root, ray_origin, ray_direction)
    
    def _ray_intersect_node(self, node, ray_origin, ray_direction):
        """射线与节点求交"""
        # 首先检查射线是否与边界框相交
        if not self._ray_aabb_intersect(ray_origin, ray_direction, node.bounds):
            return None
        
        # 如果是叶子节点，检查与三角形的相交
        if node.triangles is not None:
            return self._ray_triangles_intersect(ray_origin, ray_direction, node.triangles)
        
        # 否则递归检查左右子树
        left_result = self._ray_intersect_node(node.left, ray_origin, ray_direction)
        right_result = self._ray_intersect_node(node.right, ray_origin, ray_direction)
        
        # 返回最近的交点
        if left_result is None:
            return right_result
        if right_result is None:
            return left_result
        
        return left_result if left_result[0] < right_result[0] else right_result
    
    def _ray_aabb_intersect(self, ray_origin, ray_direction, bounds):
        """射线与AABB边界框求交"""
        t_min = 0.0
        t_max = float('inf')
        
        for i in range(3):
            if abs(ray_direction[i]) < 1e-6:
                # 射线平行于轴
                if ray_origin[i] < bounds[i] or ray_origin[i] > bounds[i+3]:
                    return False
            else:
                t1 = (bounds[i] - ray_origin[i]) / ray_direction[i]
                t2 = (bounds[i+3] - ray_origin[i]) / ray_direction[i]
                
                if t1 > t2:
                    t1, t2 = t2, t1
                
                t_min = max(t_min, t1)
                t_max = min(t_max, t2)
                
                if t_min > t_max:
                    return False
        
        return True
    
    def _ray_triangles_intersect(self, ray_origin, ray_direction, triangles):
        """射线与三角形集合求交"""
        closest_hit = None
        
        for triangle in triangles:
            hit = self._ray_triangle_intersect(ray_origin, ray_direction, triangle)
            if hit is not None:
                if closest_hit is None or hit[0] < closest_hit[0]:
                    closest_hit = hit
        
        return closest_hit
    
    def _ray_triangle_intersect(self, ray_origin, ray_direction, triangle):
        """射线与单个三角形求交（Möller–Trumbore算法）"""
        v0, v1, v2 = triangle
        
        edge1 = np.array(v1) - np.array(v0)
        edge2 = np.array(v2) - np.array(v0)
        
        h = np.cross(ray_direction, edge2)
        a = np.dot(edge1, h)
        
        if abs(a) < 1e-6:
            return None  # 射线平行于三角形
        
        f = 1.0 / a
        s = np.array(ray_origin) - np.array(v0)
        u = f * np.dot(s, h)
        
        if u < 0.0 or u > 1.0:
            return None
        
        q = np.cross(s, edge1)
        v = f * np.dot(ray_direction, q)
        
        if v < 0.0 or u + v > 1.0:
            return None
        
        t = f * np.dot(edge2, q)
        
        if t > 1e-6:
            # 计算交点法线
            normal = np.cross(edge1, edge2)
            normal = normal / np.linalg.norm(normal)
            
            return (t, ray_origin + t * ray_direction, normal)
        
        return None