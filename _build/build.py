"""生成全部原型页面：python3 _build/build.py"""
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

MODULES = ["pages_index", "pages_pc_common", "pages_school", "pages_college", "pages_teacher", "pages_pc_student", "pages_wf",
           "pages_app_student", "pages_app_staff", "pages_app_school"]


def main():
    import base
    only = sys.argv[1:]
    for name in MODULES:
        if only and name not in only:
            continue
        if not (Path(__file__).parent / f"{name}.py").exists():
            print(f"跳过（尚未编写）：{name}")
            continue
        importlib.import_module(name).build()
    print(f"已生成 {len(base.WRITTEN)} 个页面")


if __name__ == "__main__":
    main()
