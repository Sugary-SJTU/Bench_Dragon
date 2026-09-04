"""问题 4：展示原始 notebook 中定义的参数。"""

if __package__:
    from .config import PITCH, TURNING_RADIUS
else:
    from config import PITCH, TURNING_RADIUS


def run():
    """功能：展示问题 4 的题设参数；输入：无；返回：参数字典。"""
    result = {"PITCH": PITCH, "TURNING_RADIUS": TURNING_RADIUS}
    print("问题 4：原始 notebook 中仅定义了如下参数，未包含求解代码。")
    print(f"  PITCH = {PITCH}")
    print(f"  TURNING_RADIUS = {TURNING_RADIUS}")
    print("（若需继续该问，请在 problems/problem4/ 下补充实现。）")
    return result


if __name__ == "__main__":
    run()
