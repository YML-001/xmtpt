"""脚本错误巡检：python3 _build/jscheck.py [目录前缀]

用无头浏览器逐页打开，收集运行时 JS 报错（不等待外部图片加载）。
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent


def main():
    prefix = sys.argv[1] if len(sys.argv) > 1 else ""
    files = sorted(f for f in ROOT.rglob("*.html")
                   if "_build" not in f.parts and str(f.relative_to(ROOT)).startswith(prefix))
    bad = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.route("**/*", lambda r: r.abort() if r.request.url.startswith("http") else r.continue_())
        for f in files:
            errs = []

            def on_error(e, box=errs):
                box.append(str(e))

            page.on("pageerror", on_error)
            page.goto(f.resolve().as_uri(), wait_until="domcontentloaded")
            page.wait_for_timeout(60)
            page.remove_listener("pageerror", on_error)
            if errs:
                bad += 1
                print(f"[{f.relative_to(ROOT)}] " + " | ".join(errs))
        browser.close()
    print(f"共打开 {len(files)} 个页面，存在脚本错误 {bad} 个")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
