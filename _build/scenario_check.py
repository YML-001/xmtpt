"""剧本链路校验：python3 _build/scenario_check.py

逐条检查 8 条演示剧本：每一步页面必须存在，且页面内存在指向下一步页面的
href / data-href / data-submit / data-back 链接，保证演示时可以一路点通。
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifest import SCENARIOS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LINK_RE = re.compile(r'(?:href|data-href|data-submit|data-back)="([^"#?]+)')


def targets(page):
    html = (ROOT / page).read_text(encoding="utf-8")
    return {(ROOT / page).parent.joinpath(v).resolve() for v in LINK_RE.findall(html)}


def main():
    problems = 0
    for sc in SCENARIOS:
        steps = [s[2] for s in sc["steps"]]
        broken = []
        for i, page in enumerate(steps):
            if not (ROOT / page).exists():
                broken.append(f"第{i + 1}步页面不存在：{page}")
                continue
            if i + 1 < len(steps):
                nxt = (ROOT / steps[i + 1]).resolve()
                if nxt != (ROOT / page).resolve() and nxt not in targets(page):
                    broken.append(f"第{i + 1}步 {page} 没有链接到第{i + 2}步 {steps[i + 1]}")
        mark = "通过" if not broken else f"问题 {len(broken)} 个"
        print(f"剧本{sc['no']}《{sc['title']}》{len(steps)} 步：{mark}")
        for b in broken:
            print("   - " + b)
        problems += len(broken)
    print(f"\n剧本链路问题合计 {problems} 个")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
