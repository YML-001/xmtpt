#!/usr/bin/env python3
"""按操作指南需要，用 Playwright 截本地原型。手机只截 .phone，电脑视口 1440 宽。"""
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path("/Users/yaomaolin/Documents/AI/新媒体平台")
OUT = ROOT / "_build" / "manual-shots"


def uri(rel, query=""):
    u = (ROOT / rel).resolve().as_uri()
    return u + query if query else u


def scroll_phone(page, text):
    page.evaluate(
        """(t) => {
          const sc = document.querySelector('.phone .scroll');
          if (!sc) return;
          const nodes = sc.querySelectorAll('*');
          for (const el of nodes) {
            const hit = [...el.childNodes].some(n => n.nodeType === 3 && (n.textContent || '').includes(t));
            if (!hit) continue;
            const top = el.getBoundingClientRect().top - sc.getBoundingClientRect().top + sc.scrollTop - 6;
            sc.scrollTop = Math.max(0, top);
            return;
          }
        }""",
        text,
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        phone = browser.new_context(viewport={"width": 1280, "height": 900}, device_scale_factor=2)
        pc = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
        mp = phone.new_page()
        dp = pc.new_page()

        def shot_phone(name, rel, query="", scroll=None, click=None):
            mp.goto(uri(rel, query), wait_until="domcontentloaded")
            mp.locator(".phone").wait_for()
            mp.wait_for_timeout(250)
            if click:
                mp.locator(click).first.click()
                mp.wait_for_timeout(250)
            if scroll:
                scroll_phone(mp, scroll)
                mp.wait_for_timeout(150)
            path = OUT / name
            mp.locator(".phone").screenshot(path=str(path))
            print("phone", name)

        def shot_pc(name, rel, query="", scroll=None, click=None):
            dp.goto(uri(rel, query), wait_until="domcontentloaded")
            dp.wait_for_timeout(400)
            if scroll:
                dp.locator(scroll).first.scroll_into_view_if_needed()
                dp.wait_for_timeout(200)
            if click:
                dp.get_by_role("button", name=click).click()
                dp.wait_for_timeout(250)
            path = OUT / name
            dp.screenshot(path=str(path), full_page=False)
            print("pc", name)

        dp.goto(uri("index.html"), wait_until="domcontentloaded")
        dp.wait_for_timeout(300)
        dp.locator("#entry").screenshot(path=str(OUT / "01-nav-entry.png"))
        print("pc", "01-nav-entry.png")

        shot_phone("02-m-home.png", "app/student/home.html")
        shot_pc("03-pc-home.png", "pc/student/home.html")
        shot_phone("04-m-apply.png", "app/student/apply.html")
        shot_phone("05-m-accounts.png", "app/student/accounts.html")
        shot_phone("06-m-create-basic.png", "app/student/apply-create-basic.html")
        shot_phone("07-m-create-platform.png", "app/student/apply-create-platform.html")
        shot_phone("08-m-create-confirm.png", "app/student/apply-create-platform.html", scroll="平台信息确认")
        shot_phone("09-m-duplicate.png", "app/student/apply-duplicate.html")
        shot_phone("10-m-create-staff.png", "app/student/apply-create-staff.html", scroll="当前管理教师")
        shot_phone("11-m-create-reviewer.png", "app/student/apply-create-reviewer.html")
        shot_phone("12-m-create-result.png", "app/student/apply-result.html")
        shot_phone("13-m-change-pick.png", "app/student/apply-change.html")
        shot_phone("14-m-change-filled.png", "app/student/apply-change.html", "?acct=rename")
        shot_phone("15-m-change-confirm.png", "app/student/apply-change-confirm.html")
        shot_phone("16-m-handover.png", "app/student/apply-handover.html", "?acct=handover")
        shot_phone("17-m-cancel.png", "app/student/apply-cancel.html", "?acct=photo")
        shot_phone("18-m-claim.png", "app/student/apply-claim.html")
        shot_phone("19-m-claim-note.png", "app/student/apply-claim.html", click="#claim-list .pick-act")
        shot_phone("20-m-my-apply.png", "app/student/my-apply.html")
        shot_phone("21-m-progress.png", "app/student/application-detail.html")
        shot_phone("22-m-returned.png", "app/student/application-returned.html")
        shot_phone("23-m-edit.png", "app/student/application-edit.html")
        shot_phone("24-m-annual.png", "app/student/annual.html")
        shot_phone("25-m-annual-fill.png", "app/student/annual-fill.html")
        shot_phone("26-m-annual-result.png", "app/student/annual-result.html")
        shot_phone("27-m-rectify.png", "app/student/rectify.html")
        shot_phone("28-m-rectify-submit.png", "app/student/rectify-submit.html")
        shot_phone("29-m-rectify-done.png", "app/student/rectify-done.html")
        shot_phone("30-m-archive.png", "app/student/account-detail.html", "?acct=rename")
        shot_pc("31-pc-apply.png", "pc/student/apply.html", scroll=".apply-list-hd")
        shot_pc("32-pc-archive.png", "pc/student/account-detail.html")
        shot_pc("33-t-todo.png", "pc/teacher/todo.html")
        shot_pc("34-t-review.png", "pc/teacher/review-create.html")
        shot_pc("35-t-records.png", "pc/teacher/review-create.html", click="审批记录")
        shot_pc("36-t-return.png", "pc/common/modal-return.html")
        shot_pc("37-t-approve.png", "pc/common/modal-approve.html")

        browser.close()
    print("done", OUT)


if __name__ == "__main__":
    main()
