"""板凳龙（阿基米德螺线）数学建模项目 —— src 包。

包结构（按工具类别拆分）
------------------------
* ``config.params``             : 参数（全部只读常量）
* ``utils.spiral``              : 曲线工具（螺线几何、位置/速度求解与问题 3 二分）
* ``utils.collision``           : 碰撞工具（OBB、SAT 与首次碰撞搜索）
* ``visualisation.plotting``    : 作图工具（螺线、板凳、碰撞与转弯状态可视化）
* ``_archive._archive``         : 原始 notebook 中的实验性代码（仅存档）

入口见项目根目录的 ``main.py``；安装后顶层包名为 ``project``。
"""

from . import config, utils, visualisation  # noqa: F401
from .utils import collision, spiral
from .visualisation import plotting

__all__ = ["config", "utils", "visualisation", "spiral", "collision", "plotting"]
