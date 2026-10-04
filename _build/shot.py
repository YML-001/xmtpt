"""页面截图抽查：python3 _build/shot.py pc/school/dashboard.html [更多页面...]

截图输出到 /tmp/xmt-shots/，PC 页面视口 1440×900，APP 页面 1100×900。
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = Path("/tmp/xmt-shots")


def main():
    OUT.mkdir(exist_ok=True)
    full = "--full" in sys.argv
    pages = [p for p in sys.argv[1:] if not p.startswith("--")]
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for rel in pages:
            w = 1100 if rel.startswith("app/") else 1440
            page = browser.new_page(viewport={"width": w, "height": 900}, locale="zh-CN")
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto((ROOT / rel).as_uri())
            page.wait_for_timeout(600)
            out = OUT / (rel.replace("/", "__").replace(".html", ".png"))
            page.screenshot(path=str(out), full_page=full)
            print(out, "JS错误：" + "; ".join(errors) if errors else "")
            page.close()
        browser.close()


if __name__ == "__main__":
    main()
