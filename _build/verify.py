"""全站校验：python3 _build/verify.py [目录前缀]

检查项：
1. 清单中的页面是否都已生成；
2. 所有 <a href>、data-href、data-back、data-submit 指向的本地页面是否存在，禁止 href="#" / 空链接 / javascript:；
3. 每个 <button> 是否有可响应的行为属性（data-toast / data-href / data-back / data-submit / data-seg / data-toggle / data-copy / data-remove / onclick 或处于分页器内）。
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifest import all_pages  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ACTION_ATTRS = {"data-toast", "data-href", "data-back", "data-submit", "data-seg", "data-toggle", "data-copy",
                "data-remove", "data-choice", "onclick"}


class Scanner(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.bad_buttons, self.stack = [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "") or ""
        if tag == "div" and "pager" in cls.split():
            self.stack.append("pager")
        for key in ("href", "data-href", "data-back", "data-submit"):
            if key in a and not (tag == "link"):
                self.links.append((key, a[key], self.getpos()[0]))
        if tag == "button":
            in_pager = "pager" in self.stack
            if not in_pager and not (ACTION_ATTRS & set(a)) and "switch" not in cls:
                self.bad_buttons.append((self.getpos()[0], cls))

    def handle_endtag(self, tag):
        if tag == "div" and self.stack:
            # 分页器不嵌套 div，遇到第一个结束 div 即退出
            self.stack.pop()


MANIFEST_OK = "--manifest-ok" in sys.argv
PLANNED = {(ROOT / p).resolve() for p, _, _ in all_pages()} | {(ROOT / "index.html").resolve()}


def check_file(path):
    errors = []
    s = Scanner()
    s.feed(path.read_text(encoding="utf-8"))
    for key, val, line in s.links:
        v = (val or "").strip()
        if v in ("", "#") or v.startswith("javascript:"):
            errors.append(f"{line}行 {key} 为空或 #")
            continue
        if re.match(r"^(https?:|mailto:|tel:|data:)", v):
            continue
        target = (path.parent / v.split("#")[0].split("?")[0]).resolve()
        if not target.exists() and not (MANIFEST_OK and target in PLANNED):
            errors.append(f"{line}行 {key} 指向不存在的页面：{v}")
    for line, cls in s.bad_buttons:
        errors.append(f"{line}行 按钮无响应行为（class={cls}）")
    return errors


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    prefix = args[0] if args else ""
    missing = [p for p, _, _ in all_pages() if p.startswith(prefix) and not (ROOT / p).exists()]
    if not prefix and not (ROOT / "index.html").exists():
        missing.append("index.html")
    files = sorted(f for f in ROOT.rglob("*.html") if "_build" not in f.parts and str(f.relative_to(ROOT)).startswith(prefix))
    total = 0
    for f in files:
        errs = check_file(f)
        if errs:
            total += len(errs)
            print(f"\n[{f.relative_to(ROOT)}]")
            for e in errs:
                print("  - " + e)
    for m in missing:
        print(f"缺少页面：{m}")
    print(f"\n共检查 {len(files)} 个页面，发现问题 {total} 个，缺少页面 {len(missing)} 个")
    sys.exit(1 if total or missing else 0)


if __name__ == "__main__":
    main()
