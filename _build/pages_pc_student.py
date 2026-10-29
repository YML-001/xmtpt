"""PC 端 · 学生用户（李明）。业务与移动端学生页一致，使用正式系统 PC 外壳。"""
from base import *  # noqa: F401,F403
from data import (ACCOUNTS, PEOPLE, ANNUAL_TASK as T, FLOWS, CANCEL_REASONS, UPDATE_FREQ, PLATFORM_TYPES,
                  ORG_TYPES, LEVELS, COLLEGES, MECHANISMS, LEVEL_TEXT, LEVEL_NOTE, ORG_HINT, ORG_PROMPTS,
                  PLATFORM_TYPE_HINT, ACCOUNT_NAME_HINT, FORMER_NAME_HINT, PID_HINT, FANS_HINT, INTRO_HINT,
                  QR_HINT, TEAM_LABEL, PUBLISH_TIME_LABEL, RUN_STATUS, STUDENTS)
from pages_app_student import INTRO_SHORT, INTRO_FULL, FILING_NO
from pages_pc_common import FILL_JS, STAFF_JS, people_picker, add_people_btn, mech_row
from pages_wf import name_cell
from student_pick import is_cancelled, liming_rows, page_js, pick_buttons, picked_input
from wf import TODO, custom_spec, flow_spec

NEW, REN, HO, AN, PH = ACCOUNTS["new"], ACCOUNTS["rename"], ACCOUNTS["handover"], ACCOUNTS["annual"], ACCOUNTS["photo"]
RE = ACCOUNTS["rectify"]
LM, WX = PEOPLE["李明"], PEOPLE["王晓琳"]
LS, ZJ, CJ = PEOPLE["李四"], PEOPLE["周建华"], PEOPLE["陈静"]
NEW_NO = FLOWS["new"]["no"]
WIZ = ["归属信息", "平台信息", "运行与负责人", "审核人"]
SHORT_N, FULL_N = len(INTRO_SHORT), len(INTRO_FULL)
FILING_OK = "CSU-XMT-2026-0137"

CSS = """
.content{display:flex;flex-direction:column}
.content>*{flex-shrink:0}
.content>div.pin{flex:1 0 auto;display:flex;flex-direction:column}
.pin .card.grow{flex:none}
.s-hero{display:flex;align-items:center;flex-wrap:wrap;gap:18px;padding:20px 24px;border-radius:8px;color:#fff;position:relative;flex:none;
  background:linear-gradient(115deg,#3A97D4 0%,#2A8DC7 48%,#1E6C9E 100%)}
.s-hero .grow{min-width:0}
.s-hero h1{font-size:22px;font-weight:700;color:#fff;line-height:1.3}
.s-hero .dim{font-size:13px;color:rgba(255,255,255,.88);margin-top:4px}
.s-hero .avatar{box-shadow:0 0 0 3px rgba(255,255,255,.35);flex:none}
.s-pills{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.s-pill{display:inline-flex;align-items:center;gap:6px;height:26px;padding:0 10px;border-radius:13px;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.28);font-size:12px;color:#fff}
a.s-pill:hover{background:rgba(255,255,255,.28)}
.s-dead{margin-left:auto;min-width:240px;padding:12px 16px;border-radius:10px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.25);flex:none}
.s-dead .big{font-size:28px;font-weight:700;line-height:1.1}
.s-dead .progress{background:rgba(255,255,255,.22)}.s-dead .progress>i{background:#fff}
.hall{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}
.hall-card{min-width:0;display:flex;flex-direction:column;gap:6px;min-height:0;padding:12px 12px 10px;background:#fff;border-radius:8px;border:1px solid #E1EEF7;color:inherit;overflow:hidden}
.hall-card:hover{border-color:var(--c-primary-border);box-shadow:var(--shadow-lg)}
.hall-ic{width:44px;height:44px;border-radius:10px;display:grid;place-items:center;background:var(--c-primary-light);color:var(--c-primary);flex:none}
.hall-ic .i{width:22px;height:22px}
.hall-card .hall-ic{width:32px;height:32px;border-radius:8px}
.hall-card .hall-ic .i{width:16px;height:16px}
.hall-ic.orange{background:var(--c-warning-bg);color:var(--c-warning)}.hall-ic.green{background:var(--c-success-bg);color:var(--c-success)}
.hall-ic.red{background:var(--c-danger-bg);color:var(--c-danger)}.hall-ic.purple{background:#F0EDFB;color:#6B5BD2}
.hall-t{font-size:14px;font-weight:700;line-height:1.35}.hall-d{font-size:12px;color:var(--c-text-2);line-height:1.5;margin-top:2px;overflow-wrap:anywhere}
.hall-go{margin-top:auto;display:flex;align-items:flex-end;justify-content:space-between;gap:6px;flex-wrap:wrap;padding-top:8px;border-top:1px dashed var(--c-line);font-size:12px;color:var(--c-primary);font-weight:600;line-height:1.4}
.hall-go>span:first-child{color:var(--c-text-3);font-weight:500;min-width:0}
.flow-pills{display:flex;flex-wrap:wrap;gap:4px}
.flow-pills span{height:20px;padding:0 6px;border-radius:10px;background:var(--c-fill);color:var(--c-text-2);font-size:11px;display:inline-flex;align-items:center}
.g-main{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(300px,.9fr);gap:16px;align-items:stretch}
.g-main>.card{height:100%}
.content>.msg-board{flex:1 0 auto;display:flex;flex-direction:column}
.msg-board>.card{flex:1}
.apply-list-hd{display:flex;align-items:baseline;justify-content:space-between;gap:12px;margin:0 0 10px}
.apply-list-hd b{font-size:16px}
.qgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.qtile{display:flex;align-items:center;gap:10px;padding:12px;border:1px solid var(--c-line);border-radius:8px;background:#FAFCFE;min-height:64px}
.qtile:hover{border-color:var(--c-primary-border);background:#fff}
.qtile b{display:block;font-size:14px;line-height:1.3}
.ngrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.ntile{display:flex;gap:12px;align-items:flex-start;padding:16px;background:#fff;border-radius:8px;border:1px solid #E1EEF7;min-height:104px;color:inherit}
.ntile:hover{border-color:var(--c-primary-border);box-shadow:var(--shadow-lg)}
.ntile b{display:block;font-size:14px}
.id-banner{display:flex;align-items:center;gap:14px;padding:16px 18px;border-radius:8px;background:#FDF6EC;border:1px solid #F3D19E;color:#8A5A12}
.id-banner:hover{border-color:#E6A23C;box-shadow:var(--shadow-lg)}
.id-banner .hall-ic{background:#fff;color:#E6A23C}
.job{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--c-line);color:inherit}
.job:last-child{border-bottom:none;padding-bottom:0}.job:first-child{padding-top:0}
.job:hover .bold{color:var(--c-primary)}
.guide{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.guide>div{padding:14px;border-radius:8px;background:#F5F9FC;border:1px solid #E1EEF7;min-height:108px}
.guide b{display:block;margin:6px 0 4px}
.acct-banner{display:flex;align-items:flex-start;gap:14px;padding:16px 18px;border:1px solid #E1EEF7;border-radius:8px;background:linear-gradient(180deg,#F5FAFE,#fff)}
.acct-banner h2{font-size:18px;line-height:1.4}
.chk{padding:16px;border-radius:8px;border:1px solid var(--c-line);background:#fff;min-height:128px}
.chk.ok{border-color:var(--c-success-bd);background:#F7FCF4}
.chk.warn{border-color:var(--c-warning-bd);background:#FFFBF5}
.idbox{display:grid;grid-template-columns:minmax(0,1fr) 56px minmax(0,1fr);gap:8px;align-items:stretch}
.idbox .box{padding:16px;border-radius:8px;border:1px solid var(--c-line);background:#fff;min-height:120px}
.idbox .mid{display:grid;place-items:center;color:var(--c-primary)}
.intro-box{padding:12px 14px;border-radius:8px;background:#F7F9FB;border:1px solid var(--c-line);font-size:13px;line-height:1.75;color:var(--c-text-2)}
.intro-box.warn{background:var(--c-warning-bg);border-color:var(--c-warning-bd)}
.msg-item{display:flex;align-items:flex-start;gap:12px;padding:14px 18px;border-bottom:1px solid var(--c-line);color:inherit}
.msg-item:last-child{border-bottom:none}.msg-item:hover{background:#F5F9FC}
.msg-ic{width:36px;height:36px;border-radius:10px;display:grid;place-items:center;background:var(--c-primary-light);color:var(--c-primary);flex:none}
.msg-t{font-weight:600}
.unread .msg-t::after{content:"";display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--c-danger);margin-left:6px;vertical-align:middle}
.set{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px 0;border-bottom:1px solid var(--c-line)}
.set:last-child{border-bottom:none;padding-bottom:0}.set:first-child{padding-top:0}
.choices.cols{grid-template-columns:repeat(2,minmax(0,1fr))}
.picker{margin-top:12px;border:1px solid var(--c-line);border-radius:8px;padding:12px;background:#FBFCFD}
.pick-list{display:grid;gap:6px;max-height:240px;overflow:auto;margin-top:8px}
.pick-item{display:flex;align-items:center;justify-content:space-between;gap:8px;width:100%;padding:8px 10px;border:1px solid var(--c-line);border-radius:8px;background:#fff;text-align:left}
.pick-item:hover{border-color:var(--c-primary-border)}
.mech{display:grid;grid-template-columns:minmax(0,1fr) 160px;gap:18px;align-items:flex-start;padding:14px 0;border-bottom:1px dashed var(--c-line)}
.mech:last-child{border-bottom:none;padding-bottom:0}.mech:first-child{padding-top:0}
.mech-t{font-weight:600;font-size:14px;display:flex;align-items:flex-start;gap:8px;line-height:1.5}
.mech-t .no{width:20px;height:20px;border-radius:6px;background:var(--c-primary-light);color:var(--c-primary);display:grid;place-items:center;font-size:12px;flex:none;margin-top:1px}
.mech-h{font-size:12px;color:var(--c-text-2);margin-top:6px;line-height:1.75}
.lv-note{font-size:13px;color:var(--c-text-2);line-height:1.7}
#acct-pick .pick-list{max-height:none}
#acct-tbl td{height:auto}
#acct-tbl .ops{flex-wrap:wrap;white-space:normal;row-gap:6px}
.mine-page{display:flex;flex-direction:column;gap:16px}
.mine-page>.page-hd{margin-bottom:0}
.mine-board{align-items:stretch}
.mine-board>.card{display:flex;flex-direction:column}
.mine-board>.card>.card-bd{flex:1;display:flex;flex-direction:column}
.mine-board .qgrid{flex:1;grid-template-rows:1fr 1fr}
.mine-board .ntile{height:100%;min-height:112px}
.mine-actions{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.flow-box .wf-chart{min-height:240px;padding:48px 20px 28px}
"""

PERSON_JS = """
function fillPerson(btn){
  var n=document.getElementById(btn.getAttribute('data-name-id'));
  var o=document.getElementById(btn.getAttribute('data-no-id'));
  var p=document.getElementById(btn.getAttribute('data-phone-id'));
  if(n)n.value=btn.getAttribute('data-name');
  if(o)o.value=btn.getAttribute('data-no');
  if(p)p.value=btn.getAttribute('data-phone');
  var panel=btn.closest('.picker');
  if(panel)panel.classList.add('hidden');
  toast('已选择继任负责人：'+btn.getAttribute('data-name'));
}
"""

ID_JS = """
function syncOldPid(sel){
  var map={
    "中南计院团委 · 微信公众号":"csu_cs_tw",
    "计算机学院学生会 · 微博":"7722108845",
    "计院街舞社 · 抖音":"csu_cs_dance",
    "计院摄影协会 · 视频号":"sph_csu_cs_photo"
  };
  var v=map[sel.value]||"";
  var box=document.getElementById("old-pid");
  var view=document.getElementById("old-pid-view");
  if(box)box.value=v;
  if(view)view.textContent=v;
}
"""

MARK_JS = "function markRead(){document.querySelectorAll('.unread').forEach(function(n){n.classList.remove('unread');});}"


def page(file, active, title, crumbs, content, js=""):
    pc_page("pc/student/" + file, "student", active, title, crumbs, content, css=CSS, js=js)


def bar(note, buttons):
    return f'<div class="actbar"><div class="grow">{note}</div>{buttons}</div>'


def crumbs(*tail):
    return [("学生首页", "home.html")] + list(tail)


def shell(hd, body, action="", dialogs=""):
    return hd + f'<div class="pin" data-form>{body}{action}{dialogs}</div>'


def dialog(id_, title, desc, ok):
    return (f'<div class="mask hidden" id="{id_}"><div class="modal sm"><div class="modal-hd">{title}'
            f'<button class="x-btn" type="button" data-toggle="#{id_}" aria-label="关闭">{icon("x")}</button></div>'
            f'<div class="modal-bd"><p class="fs13 sub">{desc}</p></div><div class="modal-ft">'
            f'<button class="btn btn-default" type="button" data-toggle="#{id_}">取消</button>{ok}</div></div></div>')


def hall_card(title, desc, ic, tone, href, steps, foot, wide=False):
    pills = "".join(f"<span>{s}</span>" for s in steps)
    tone_cls = (" " + tone) if tone else ""
    return (f'<a class="hall-card" href="{href}"><div class="flex between"><span class="hall-ic{tone_cls}">{icon(ic, 16)}</span>'
            f'{icon("arrow-right")}</div><div><div class="hall-t">{title}</div><div class="hall-d">{desc}</div></div>'
            f'<div class="flow-pills">{pills}</div><div class="hall-go"><span>{foot}</span><span>进入办理</span></div></a>')


def tiles(items):
    cells = "".join(
        f'<a class="ntile" href="{h}"><span class="hall-ic{(" " + tone) if tone else ""}">{icon(ic, 20)}</span>'
        f'<div><b>{t}</b><div class="small muted mt4">{d}</div></div></a>'
        for t, d, h, ic, tone in items)
    return f'<div class="ngrid">{cells}</div>'


def wiz(i):
    return f'<div class="card"><div class="card-bd">{steps(WIZ, i)}</div></div>'


def copy_btn(text):
    return f' <button class="link small" type="button" data-copy="{esc(text)}">复制</button>'


def successor_picker():
    items = []
    for name, no, phone, meta in STUDENTS:
        items.append(
            '<button type="button" class="pick-item" data-cat="' + esc(name + " " + no) + '" onclick="fillPerson(this)" '
            'data-name="' + esc(name) + '" data-no="' + no + '" data-phone="' + esc(phone) + '" '
            'data-name-id="ho-name" data-no-id="ho-no" data-phone-id="ho-phone">'
            '<span><b>' + name + '</b> <span class="muted small">' + no + '</span></span>'
            '<span class="small muted">' + phone + " · " + meta + "</span></button>"
        )
    return ('<div id="pick-ho" class="picker hidden"><div class="small muted">输入学号或姓名检索，选中后写入新负责人。不限人数，交接只指定 1 名继任者。</div>'
            '<label class="top-search" style="width:100%;margin-top:8px">' + icon("search") +
            '<input placeholder="输入学号或姓名" data-search="#pick-ho-list"></label>'
            '<div id="pick-ho-list" class="pick-list">' + "".join(items) + "</div></div>")


def annual_fields(last, owner="李明"):
    head = [("1. 账号是否仍存在", "q1", "是"), ("2. 是否正常运营", "q2", "是"), ("3. 是否能正常访问", "q3", "是")]
    tail = [("6. 指导教师是否变化", "q6", "否"), ("7. 账号名称是否变化", "q7", "否"),
            ("8. 是否需要注销", "q8", "否"), ("9. 是否存在其他异常", "q9", "否")]
    checks = "".join(field(q, radios(name, ["是", "否"], ans, True), True) for q, name, ans in head)
    checks += field("4. " + PUBLISH_TIME_LABEL, inp("", last, True, "date"), True, "日期选择")
    checks += field("5. 当前运营负责人", inp("", owner, True), True)
    checks += "".join(field(q, radios(name, ["是", "否"], ans, True), True) for q, name, ans in tail)
    return checks


def belong_kv(a):
    return kv([("所属学校", "中南大学"), ("所属学院", "计算机学院"), ("所属团学组织", a["org"]),
               ("组织类别", a["org_type"]), ("平台管理层级", a["level"]), ("开通时间", a["opened"])], 2)


def platform_kv(a, former="无"):
    return kv([("平台类型", a["platform"]), ("账号名称", a["name"]), ("曾用名", former),
               ("平台 ID", f'<span class="num">{a["pid"]}</span>{copy_btn(a["pid"])}'),
               ("粉丝数", a["fans"]), ("管理教师", a["teacher"]), ("学生负责人", a["student"])], 2)


# ---------------------------------------------------------------- 首页 / 待办 / 消息 / 个人
def home():
    rows = [[name_cell(k, sub), node, who, at_tm, f'<a class="link" href="{href}">办理</a>']
            for k, sub, node, who, _st, at_tm, href in TODO["student"]]
    quick = [
        ("新建备案", "填写四步申请", "file-add", "", "apply-create-basic.html"),
        ("信息变更", "名称、主页等", "file-edit", "orange", "apply-change.html"),
        ("负责人交接", "指定继任学生", "user-switch", "green", "apply-handover.html"),
        ("账号注销", "停运后申请", "power", "red", "apply-cancel.html"),
        ("账号认领", "绑定历史账号", "hand", "purple", "apply-claim.html"),
        ("我的年审", "确认本年度变化", "calendar", "", "annual.html"),
        ("我的申请", "进度与退回重提", "clipboard", "orange", "apply.html"),
        ("整改任务", "提交证明材料", "wrench", "red", "rectify.html"),
    ]
    q = "".join(
        f'<a class="qtile" href="{h}"><span class="hall-ic{(" " + tone) if tone else ""}">{icon(ic, 18)}</span>'
        f'<div><b>{t}</b><div class="small muted">{d}</div></div></a>'
        for t, d, ic, tone, h in quick)
    accts = table(["账号", "平台 / 层级", "状态", "操作"], [
        [acct(a["name"], a["platform"], a["org"]), f'{a["platform"]} · {a["level"]}', st(s), btn("查看", h, "text", "eye", "sm")]
        for a, s, h in [
            (AN, "正常运行", "account-annual.html"), (REN, "变更申请中", "account-detail.html"),
            (HO, "正常运行", "account-handover.html"), (PH, "不活跃", "account-photo.html"),
            (NEW, "备案申请中", "application-detail.html"),
        ]
    ])
    annual_body = ('<div class="chips">' + "".join(
        f'<span class="chip{" on" if i == 1 else ""}">{t}</span>'
        for i, t in enumerate(["发布 09-15", "学生填报 10-15", "教师审核 10-25", "学院提交 11-05", "学校审核 11-20"])) + "</div>"
                   + f'<div class="mt16">{alert("历史数据已自动继承。中南计院团委、计院街舞社待确认；计院摄影协会须先完成僵尸号核实。", "info")}</div>'
                   + f'<div class="flex gap8 mt12">{btn("去填报", "annual-fill.html", "primary", "edit", "sm")}{btn("年审列表", "annual.html", "default", size="sm")}</div>')
    content = f"""
<div class="s-hero">{avatar("李明", "lg")}
  <div class="grow"><h1>李明，下午好</h1>
    <div class="dim">{LM["org"]} · {LM["job"]} · 学号 {LM["no"]} · {LM["grade"]}</div>
    <div class="s-pills"><span class="s-pill">{icon("database", 14)}负责 5 个账号</span>
      <span class="s-pill">{icon("inbox", 14)}5 项待办</span>
      <a class="s-pill" href="../common/identity-switch.html">{icon("user-switch", 14)}切换身份</a></div>
  </div>
  <div class="s-dead"><div class="small" style="opacity:.85">{T["year"]} 年度年审 · 学生填报截止</div>
    <div class="flex gap8 mt4" style="align-items:baseline"><span class="big">15</span><span>天后 · {T["stu_end"]}</span></div>
    <div class="flex gap8 mt8">{progress(50)}<span class="small num">1 / 4 已提交</span></div></div>
</div>
<div class="grid g4 mt16">{stat("我的账号", 5, "仅本人负责或参与", "database", href="accounts.html")}
{stat("进行中申请", 2, "新建备案、名称变更", "clipboard", "orange", href="apply.html")}
{stat("待办事项", 5, "年审、退回、整改、核实", "inbox", "red", href="todo.html")}
{stat("待处理年审", 3, T["stu_end"] + " 截止", "calendar", "green", href="annual.html")}</div>
<div class="g-main mt16">{card("我的待办", '<div class="wf-list" style="padding:0">' + table(["流程名称", "当前节点", "发起人", "到达时间", "操作"], rows) + "</div>", btn("全部待办", "todo.html", "text", size="sm"))}
{card("快捷办理", f'<div class="qgrid">{q}</div>')}</div>
<div class="g-main mt16">{card("我负责的账号", accts, btn("全部账号", "accounts.html", "text", size="sm"))}
{card(T["name"], annual_body)}</div>
<div class="g-main mt16">{card("账号运行概况", donut([("正常运行", 3), ("不活跃", 1), ("备案申请中", 1)], "5", "我的账号"), btn("查看档案", "accounts.html", "text", size="sm"))}
{card("最近动态", timeline([
    ("back", "新建备案被退回", "09-25 · 王晓琳", "平台介绍不足 100 字，修改后已重新提交"),
    ("now", "名称变更审核中", "09-26 · 计算机学院学生会", "拟改为中南计院学生会"),
    ("done", "年审任务已启动", "09-15 · " + T["name"], "学生填报截止 " + T["stu_end"]),
    ("now", "摄影协会待核实", "停更 212 天", "系统只预警，不会直接注销"),
]))}</div>"""
    page("home.html", "home", "学生首页", [("学生首页", None)], content)


def messages():
    data = [
        ("unread biz", "审核退回", "2026-09-25 09:30", "王晓琳退回「中南计算机青年」：平台介绍不足 100 字。", "application-returned.html"),
        ("unread biz", "流转提醒", "2026-09-27 11:20", "「中南计算机青年」已通过指导教师审核，流转至学院团委。", "application-detail.html"),
        ("unread biz", "整改通知", "2026-09-24 11:30", "「计院青年志愿者」继续整改：制度文件缺少签字盖章。", "rectify-detail.html"),
        ("unread biz", "变更受理", "2026-09-26 14:40", "名称变更「计算机学院学生会」已提交，等待王晓琳审核。", "application-change.html"),
        ("biz", "僵尸号预警", "2026-09-22 02:00", "「计院摄影协会」停更 212 天，请核实。系统不会直接注销。", "zombie-verify.html"),
        ("biz", "年审提醒", "2026-09-15 09:00", T["name"] + "已启动，请于 " + T["stu_end"] + " 前填报。", "annual.html"),
        ("biz", "交接提醒", "2026-09-28 10:20", "「计院街舞社」可办理负责人交接，拟于 10 月 1 日生效。", "apply-handover.html?acct=handover"),
    ]
    rows = []
    for cat, t, tm, text, href in data:
        mark = " unread" if "unread" in cat else ""
        rows.append(f'<a class="msg-item{mark}" href="{href}" data-cat="{cat}"><div class="msg-ic">{icon("bell")}</div>'
                    f'<div class="grow"><div class="msg-t">{t}</div><div class="small sub">{text}</div></div>'
                    f'<span class="small muted">{tm[5:16]}</span></a>')
    read_btn = '<button class="btn btn-default btn-sm" type="button" onclick="markRead()" data-toast="已将全部消息标记为已读">全部已读</button>'
    content = f"""{page_hd("消息", "审核结果、年审、整改与系统通知。点一条进入对应办理页", read_btn)}
<div class="card mb12"><div class="card-bd" style="padding-bottom:12px"><div class="toolbar" style="margin:0">
<label class="top-search" style="width:280px">{icon("search")}<input placeholder="搜索消息" data-search="#msg-list"></label>
{seg([("全部", "all"), ("未读", "unread"), ("业务通知", "biz")], target="#msg-list")}</div></div></div>
<div class="msg-board"><div class="card" style="padding:0"><div id="msg-list">{"".join(rows)}</div></div></div>"""
    page("messages.html", "messages", "消息", crumbs(("消息", None)), content, MARK_JS)



# ---------------------------------------------------------------- 账号档案
def _picker(verb):
    body = ('<div class="small muted mb12">请选择要办理的账号。下列为李明可办理的账号，包含名称、平台和编号。</div>'
            '<div class="pick-list">' + pick_buttons() + "</div>")
    return card("选择账号", body, '<span class="small muted">点选后填写' + verb + "</span>", id_="acct-pick") + picked_input()


def _now_banner():
    return ('<div class="acct-banner mb16"><div class="grow"><div class="small muted">当前办理账号</div>'
            '<h2 id="acct-now-name">—</h2><div class="small sub" id="acct-now-meta"></div></div></div>')


def _acct_step(verb, inner):
    return _picker(verb) + '<div id="acct-form" class="hidden">' + _now_banner() + inner + "</div>"


def _row_ops(r):
    if is_cancelled(r):
        return ops(("查看", r["pc_view"]))
    k = r["key"]
    return ops(
        ("查看", r["pc_view"]),
        ("变更", "apply-change.html?acct=" + k),
        ("交接", "apply-handover.html?acct=" + k),
        ("注销", "apply-cancel.html?acct=" + k),
    )


def accounts():
    show = {
        "annual": ("正常运行", "已备案", "待填报"),
        "rename": ("正常运行", "变更申请中", "待指导教师审核"),
        "handover": ("正常运行", "已备案", "待填报"),
        "photo": ("不活跃", "已备案", "待核实"),
        "new": ("—", "备案申请中", "学院团委审核"),
    }
    body_rows = []
    for r in liming_rows():
        a = ACCOUNTS[r["key"]]
        run, filing, extra = show[r["key"]]
        body_rows.append([
            acct(a["name"], a["platform"], a["org"]),
            f'<span class="num">{a["pid"]}</span>',
            f'{a["level"]}<div class="small muted">{a["org"]}</div>',
            st(run) if run != "—" else "—",
            st(filing),
            extra,
            _row_ops(r),
        ])
    body = table(["账号", "平台 ID", "层级 / 组织", "运行", "备案", "年审或申请", "操作"], body_rows, id_="acct-tbl")
    content = f"""{page_hd("我的账号", "只显示李明本人负责，或正在以本人名义申请的账号", btn("账号认领", "apply-claim.html", "default", "hand") + btn("新建备案", "apply-create-basic.html", "primary", "plus"))}
{filter_bar([
    field("关键词", inp("账号名称 / 平台 ID", attrs='data-search="#acct-tbl"')),
    field("平台类型", sel(PLATFORM_TYPES, ph="全部")),
    field("运行状态", sel(["正常运行", "不活跃", "整改中"], ph="全部")),
])}
{card("账号列表", body + pager(5, 1))}"""
    page("accounts.html", "accounts", "我的账号", crumbs(("我的账号", None)), content)


def _banner(a, tags, meta):
    return (f'<div class="acct-banner">{pf(a["platform"], "lg")}<div class="grow"><div class="flex gap8 wrap"><h2>{a["name"]}</h2>{tags}</div>'
            f'<div class="small sub mt4">{meta}</div></div></div>')


def _archive_blocks(a, run_kv, staff_kv, former="无"):
    return f"""<div class="grid g2 mt16">{card("归属信息", belong_kv(a))}{card("平台信息", platform_kv(a, former))}</div>
{card("平台信息确认", mechanism_blocks(), tag("（10）至（13）", "muted"), cls="mt16")}
<div class="grid g2 mt16">{card("运行信息", run_kv)}{card("责任人与审核信息", staff_kv)}</div>"""


def account_detail():
    a = REN
    content = f"""{page_hd(a["name"], f'{a["platform"]} · {a["pid"]} · {a["org"]}', btn("信息变更", "apply-change.html?acct=rename", "primary", "file-edit") + btn("变更进度", "application-change.html", "default", "clipboard"))}
{ptabs([("基本信息", "account-detail.html"), ("历史记录", "account-history.html")], "基本信息")}
{_banner(a, st("正常运行") + st("变更申请中") + st("待指导教师审核"), "名称拟变更为「" + a["new_name"] + "」，平台 ID 不变")}
{_archive_blocks(a, kv([(PUBLISH_TIME_LABEL, "2026-09-18"), ("更新频率", UPDATE_FREQ[1]), ("运行状态", "正常运行"), ("年度异动", "变更"), ("备注", "学生会换届后统一品牌名称")], 2),
  kv([("当前管理教师", "王晓琳 · " + WX["no"]), ("手机号", WX["phone"]), ("具体负责人", "李明 · " + LM["no"]), ("管理员", "陈可欣（8209230221）、刘子涵（8209240133）", True)], 2),
  former="无（变更通过后记入「" + a["name"] + "」）")}
<div class="mt16">{tiles([
    ("继续修改变更", "对照变更前后再提交", "apply-change.html?acct=rename", "file-edit", "orange"),
    ("查看审核进度", "当前在指导教师", "application-change.html", "clipboard", ""),
    ("年审进度", "本账号年审已提交", "annual-ren.html", "calendar", "green"),
    ("返回账号列表", "5 个负责账号", "accounts.html", "database", "purple"),
])}</div>"""
    page("account-detail.html", "accounts", "账号档案", crumbs(("我的账号", "accounts.html"), (a["name"], None)), content)


def account_history():
    content = f"""{page_hd(REN["name"] + " · 历史记录", "历任负责人、历年年审和名称变更都留在账号档案里")}
{ptabs([("基本信息", "account-detail.html"), ("历史记录", "account-history.html")], "历史记录")}
<div class="grid g2 mt16">
  {card("历任负责人", timeline([("now", "李明（现任）", "2025-06-20 至今 · 2023级软件工程2班", "学生会换届后接任"), ("done", "周子豪", "2023-06-15 至 2025-06-20", "毕业离任，交接给李明")]))}
  {card("历年年审", timeline([("now", "2026 年度", "待指导教师审核", "李明已于 09-22 确认"), ("done", "2025 年度", "年审通过", "无异动"), ("done", "2024 年度", "年审通过", "无异动")]))}
</div>
{card("名称变更", table(["时间", "字段", "变更前", "变更后", "状态"], [
    ["2026-09-26", "账号名称", REN["name"], REN["new_name"], st("待指导教师审核")],
    ["2024-03-02", "主页链接", "weibo.com/old", "weibo.com/" + REN["pid"], st("已通过")],
]), cls="mt16")}
<div class="mt16">{alert("平台 ID 没有变化。若 ID 变化，不能记在这张变更表里，要按新建备案办理并注销原 ID。", "warning")}</div>"""
    page("account-history.html", "accounts", "账号历史", crumbs(("我的账号", "accounts.html"), ("历史记录", None)), content)


def account_annual():
    a = AN
    content = f"""{page_hd(a["name"], f'{a["platform"]} · {a["pid"]} · {a["org"]}', btn("去填报年审", "annual-fill.html", "primary", "edit"))}
{_banner(a, st("正常运行") + st("已备案") + st("待填报"), "2026 年度年审进行中，历史信息已继承")}
{_archive_blocks(a, kv([(PUBLISH_TIME_LABEL, "2026-09-17"), ("更新频率", UPDATE_FREQ[0]), ("运行状态", "正常运行"), ("年度异动", "待确认"), ("异常情况", "无")], 2),
  kv([("当前管理教师", "王晓琳 · " + WX["no"]), ("手机号", WX["phone"]), ("具体负责人", "李明 · " + LM["no"]), ("管理员", "新媒体中心编辑组", True)], 2))}
{card("历史记录", '<div class="grid g2">' + timeline([("now", "李明（现任）", "2024-09-01 至今", "学院团委宣传负责人"), ("done", "2025 年度年审", "通过 · 无异动", ""), ("done", "2024 年度年审", "通过 · 无异动", "")]) + "</div>", cls="mt16")}
<div class="mt16">{tiles([
    ("填写年审", "9 项确认后提交", "annual-fill.html", "calendar", ""),
    ("查看消息", "年审提醒", "messages.html", "bell", "orange"),
    ("我的待办", "含本年审", "todo.html", "inbox", "green"),
    ("返回列表", "全部账号", "accounts.html", "database", "purple"),
])}</div>"""
    page("account-annual.html", "accounts", "账号档案", crumbs(("我的账号", "accounts.html"), (a["name"], None)), content)


def account_handover():
    a = HO
    content = f"""{page_hd(a["name"], f'{a["platform"]} · {a["pid"]} · {a["org"]}', btn("发起交接", "apply-handover.html?acct=handover", "primary", "user-switch") + btn("填写年审", "annual-fill-dance.html", "default", "calendar"))}
{_banner(a, st("正常运行") + st("已备案"), "现任负责人李明，拟于 2026-10-01 交接给李四")}
{_archive_blocks(a, kv([(PUBLISH_TIME_LABEL, "2026-09-12"), ("更新频率", UPDATE_FREQ[1]), ("运行状态", "正常运行"), ("年度异动", "待确认"), ("异常情况", "无")], 2),
  kv([("当前管理教师", "王晓琳 · 街舞社指导教师"), ("手机号", WX["phone"]), ("具体负责人", "李明 · " + LM["no"] + " · 2024-09-10 起"), ("拟接任", "李四 · " + LS["no"], True)], 2))}
{card("责任人历史", timeline([("now", "李明（现任）", "2024-09-10 至今", "卸任前仍为负责人，交接审核通过后写入截止日期"), ("wait", "李四（拟接任）", "拟 2026-10-01 生效", LS["job"] + " · " + LS["grade"])]), cls="mt16")}
<div class="mt16">{tiles([
    ("办理交接", "检索并指定李四", "apply-handover.html?acct=handover", "user-switch", "green"),
    ("填写年审", "街舞社待确认", "annual-fill-dance.html", "calendar", ""),
    ("交接结果", "审核通过后的记录", "application-handover.html", "check-circle", "orange"),
    ("返回列表", "全部账号", "accounts.html", "database", "purple"),
])}</div>"""
    page("account-handover.html", "accounts", "账号档案", crumbs(("我的账号", "accounts.html"), (a["name"], None)), content)


def account_photo():
    a = PH
    content = f"""{page_hd(a["name"], f'{a["platform"]} · {a["pid"]} · {a["org"]}', btn("去核实", "zombie-verify.html", "primary", "ghost") + btn("申请注销", "apply-cancel.html?acct=photo", "danger", "power"))}
{_banner(a, st("不活跃") + st("已备案") + st("疑似僵尸号"), "最近发布 " + a["last_post"] + "，停更 " + str(a["idle_days"]) + " 天。系统只预警，不直接注销")}
{_archive_blocks(a, kv([(PUBLISH_TIME_LABEL, a["last_post"]), ("更新频率", UPDATE_FREQ[3]), ("运行状态", "不活跃"), ("停更天数", str(a["idle_days"]) + " 天"), ("异常情况", "疑似僵尸号，待负责人核实")], 2),
  kv([("当前管理教师", "王晓琳 · " + WX["no"]), ("手机号", WX["phone"]), ("具体负责人", "李明 · " + LM["no"]), ("年审", "须先完成核实", True)], 2))}
<div class="mt16">{alert("年审列表里该账号不会直接进入填报。核实为仍在运营后，再按正常年审确认；若确认停运，转入注销。", "warning")}</div>
<div class="mt16">{tiles([
    ("核实仍在运营", "上传近期发布截图", "zombie-verify.html", "ghost", "purple"),
    ("申请注销", "停运后逐级审核", "apply-cancel.html?acct=photo", "power", "red"),
    ("平台 ID 变化", "不能当普通变更", "apply-id-change.html", "swap", "orange"),
    ("返回待办", "核实任务", "todo.html", "inbox", ""),
])}</div>"""
    page("account-photo.html", "accounts", "账号档案", crumbs(("我的账号", "accounts.html"), (a["name"], None)), content)


def account_youth():
    a = NEW
    content = f"""{page_hd(a["name"] + " · 备案档案", "终审通过后的账号档案", btn("返回通过结果", "application-approved.html", "default") + btn("我的申请", "apply.html", "primary", "clipboard"))}
{_banner(a, st("正常运行") + st("已备案"), "备案编号 " + FILING_OK + " · 申请编号 " + NEW_NO + " · 2026-09-30 建档")}
<div class="mt12">{alert("账号列表中的「备案申请中」是当前仍在学院审核的办理态。本页是同一申请终审通过之后的档案，便于查看通过后的结果。", "info")}</div>
{_archive_blocks(a, kv([(PUBLISH_TIME_LABEL, "2026-09-22"), ("更新频率", UPDATE_FREQ[0]), ("运行状态", "正常运行"), ("本年度年审", "新开通，不参与 2026 年审"), ("粉丝数", "0")], 2),
  kv([("当前管理教师", "王晓琳 · " + WX["no"]), ("具体负责人", "李明 · " + LM["no"]), ("管理员", "陈可欣（8209230221）、刘子涵（8209240133）", True), ("一审老师", "王晓琳")], 2))}
{card("建档记录", timeline([("done", "校团委准予备案", "陈静 · 2026-09-30 10:05", FLOWS["new"]["steps"][5][3]), ("done", "生成备案表", FILING_OK, "纳入 2027 年度年审")]), cls="mt16")}"""
    page("account-youth.html", "accounts", "账号档案", crumbs(("业务申请", "apply.html"), ("备案档案", None)), content)


# ---------------------------------------------------------------- 业务申请
def apply_hub():
    cards = "".join([
        hall_card("新建备案", "新开设账号首次登记。填写归属、平台、负责人和审核老师。", "file-add", "", "apply-create-basic.html", ["指导教师", "学院团委", "校团委"], "四步向导"),
        hall_card("信息变更", "名称、主页、二维码等变化。平台 ID 不变才走这条。", "file-edit", "orange", "apply-change.html", ["指导教师", "学院团委", "重要变更报校团委"], "先对比再提交"),
        hall_card("负责人交接", "学生负责人换届或卸任。原任职起止写入历史。", "user-switch", "green", "apply-handover.html", ["指导教师审核", "通过后生效"], "指定一名继任者"),
        hall_card("账号注销", "停运后申请注销。档案与历史永久保留。", "power", "red", "apply-cancel.html", ["指导教师", "学院团委", "校团委"], "选择原因并说明"),
        hall_card("账号认领", "认领已导入、尚未绑定到本人的历史账号。", "hand", "purple", "apply-claim.html", ["检索账号", "指导教师确认"], "先选定再提交"),
    ])
    content = f"""{page_hd("业务申请", "学生发起申请并提交材料，审核由指导教师、学院团委、校团委完成")}
<div class="hall">{cards}</div>
<a class="id-banner mt16" href="apply-id-change.html"><span class="hall-ic">{icon("swap", 22)}</span>
  <div class="grow"><b>平台 ID 发生变化，不能按普通变更办理</b><div class="small mt4">须按新 ID 新建备案，并同时注销原来的 ID。只改名称、主页或二维码的，仍走信息变更。</div></div>
  <span class="bold" style="color:#B88230">查看办理方式 {icon("arrow-right")}</span></a>
{application_table()}"""
    page("apply.html", "apply", "业务申请", crumbs(("业务申请", None)), content)



def create_basic():
    chips_html = "".join(
        f'<button class="chip" type="button" data-fill="{esc(x)}" data-fill-target="#org-input" data-toast="已填入：{esc(x)}">{x}</button>'
        for x in [NEW["org"]] + ORG_PROMPTS)
    levels = "".join(f'<div class="mt12"><b>{n}</b><div class="lv-note">{LEVEL_TEXT[n]}</div></div>' for n in LEVELS if LEVEL_TEXT[n])
    form = card("归属信息", f"""<div class="form-grid">
  {field("所属学校", inp("", "中南大学", readonly=True))}
  {field("所属学院", sel(COLLEGES, "计算机学院", True), True)}
  {field("所属团学组织", inp("请输入团学组织名称", NEW["org"], True, attrs='id="org-input"') + f'<div class="chips mt8">{chips_html}</div>', True, ORG_HINT)}
  <div class="full">{field("组织类别", radios("org_type", ORG_TYPES, NEW["org_type"], True), True, "校级学生组织、院级学生组织、班级团支部、社团组织")}</div>
  <div class="full">{field("平台管理层级", radios("lv", LEVELS, NEW["level"], True), True, "一级平台、二级平台、三级平台、社团平台")}</div>
</div>""")
    side = card("填写说明", alert("带 <span class='req'>*</span> 的为必填。所属团学组织可以手输，也可以点下面的提示词写入。", "info")
                + f'<div class="mt8"><b>{LEVEL_NOTE}</b></div>{levels}<div class="small muted mt12">下一步填写平台类型、账号名称、平台 ID，并确认第 10 至 13 项。</div>')
    content = shell(page_hd("新建备案申请", "发起人：李明 · 中南计算机青年 · 第 1 / 4 步"),
                    wiz(0) + f'<div class="split mt16">{form}{side}</div>',
                    bar("归属信息确认后进入平台信息", btn("保存草稿", None, "default", "file", toast="草稿已保存，可在我的申请中继续填写") + back_btn("apply.html", "取消") + submit_btn("下一步", "apply-create-platform.html")))
    page("apply-create-basic.html", "apply", "新建备案 · 归属信息", crumbs(("业务申请", "apply.html"), ("归属信息", None)), content, FILL_JS)


def create_platform():
    mechs = "".join(mech_row(m["no"], m["title"], m["body"], m["key"]) for m in MECHANISMS)
    body = (card("平台信息", f"""<div class="form-grid c3">
  {field("平台类型", sel(PLATFORM_TYPES, NEW["platform"], True), True, PLATFORM_TYPE_HINT)}
  {field("账号名称", inp(ACCOUNT_NAME_HINT, NEW["name"], True), True, ACCOUNT_NAME_HINT)}
  {field("曾用名", inp(FORMER_NAME_HINT), hint="非必填。" + FORMER_NAME_HINT)}
  <div class="span2">{field("平台 ID", inp(PID_HINT, NEW["pid"], True), True, PID_HINT)}</div>
  {field("是否认证", radios("verify", ["是", "否"], "否", True), True, "单选，是 / 否")}
  {field("粉丝数", inp(FANS_HINT, "0", True, "number"), True, FANS_HINT)}
  {field(TEAM_LABEL, inp("请输入人数", "6", True, "number"), True)}
  {field("开通时间", inp("", NEW["opened"], True, "date"), True)}
  <div class="full">{field("主页链接", inp("https://", "https://mp.weixin.qq.com/csu_cs_youth", True), True)}</div>
</div>""")
            + card("平台头像与二维码", f'<div class="grid g2">{field("平台头像", upload("上传平台头像", "jpg / png", ["中南计算机青年头像.png"]), True)}'
                   f'{field("二维码", upload("上传平台二维码", "jpg / png", []), hint=QR_HINT)}</div>', cls="mt16")
            + card("平台信息确认", mechs + alert("以下四项须逐条确认。说明文字为制度原文，请选择是否已经建立。", "info"), tag("（10）至（13）", "muted"), cls="mt16")
            + card("平台介绍与发布范围", f"""<div class="form-grid c1">
  {field("平台介绍", textarea(INTRO_HINT, INTRO_SHORT, True, 800, 5), True, INTRO_HINT + "。当前 " + str(SHORT_N) + " 字")}
  {field("信息发布范围", textarea("请填写信息发布范围", "学院团学活动相关信息。", True, 0, 2), True)}
  {field("备注", inp(""))}
</div>""", cls="mt16 grow"))
    content = shell(page_hd("新建备案申请", "发起人：李明 · 第 2 / 4 步"), wiz(1) + f'<div class="mt16">{body}</div>',
                    bar("二维码非必填。下一步自动做重复检查", back_btn("apply-create-basic.html", "上一步") + submit_btn("下一步", "apply-duplicate.html", toast="正在进行重复检查")))
    page("apply-create-platform.html", "apply", "新建备案 · 平台信息", crumbs(("业务申请", "apply.html"), ("平台信息", None)), content)


def duplicate():
    tiles_html = f"""<div class="grid g3">
  <div class="chk ok"><div class="flex gap8">{icon("check-circle")}{tag("通过", "success")}</div><b class="mt8" style="display:block">相同平台、相同 ID</b><div class="small sub mt4">微信公众号 · csu_cs_youth 在全校账号中没有重复</div></div>
  <div class="chk ok"><div class="flex gap8">{icon("check-circle")}{tag("通过", "success")}</div><b class="mt8" style="display:block">相同主页链接</b><div class="small sub mt4">主页链接没有被其他账号登记</div></div>
  <div class="chk warn"><div class="flex gap8">{icon("alert")}{tag("需确认", "warning")}</div><b class="mt8" style="display:block">高度相似账号名称</b><div class="small sub mt4">「中南计算机学院」已注销，相似度 82%</div></div>
</div>"""
    similar = card("相似账号", f"""<div class="flex gap12">{pf("微信公众号", "lg")}<div class="grow"><div class="flex gap8"><b class="fs16">中南计算机学院</b>{st("已注销")}</div>
      <div class="small muted mt4">微信公众号 · ID csu_jsjxy · 2019-06 注销 · 原归属计算机学院团委</div></div><b class="c-warning">82%</b></div>
      <div class="mt12">{alert("名称相似只作提示。确认不是同一账号后可以继续。若相同平台且相同 ID，则禁止新建，应改为认领。本次没有命中相同 ID。", "warning")}</div>""", cls="mt16 grow")
    content = shell(page_hd("重复检查结果", "提交前自动检查：相同平台相同 ID、相同主页链接、高度相似账号名称"),
                    tiles_html + similar + '<div class="mt16">' + tiles([
                        ("返回修改平台信息", "改名称或平台 ID", "apply-create-platform.html", "edit", ""),
                        ("确认后继续", "填写运行与负责人", "apply-create-staff.html", "arrow-right", "green"),
                        ("改为认领", "若其实是已有账号", "apply-claim.html", "hand", "purple"),
                        ("返回业务申请", "五类入口", "apply.html", "file-add", "orange"),
                    ]) + "</div>",
                    bar("未发现相同平台、相同 ID", back_btn("apply-create-platform.html", "返回修改") + btn("确认不是同一账号，继续", "apply-create-staff.html", "primary", "arrow-right")))
    page("apply-duplicate.html", "apply", "重复检查", crumbs(("业务申请", "apply.html"), ("重复检查", None)), content)


def create_staff():
    rm = '<button class="link" type="button" data-remove>删除</button>'
    admins = table(["姓名", "学号", "手机号", "所在班级", "操作"], [
        ["<b>陈可欣</b>", '<span data-no="8209230221">8209230221</span>', "137 7310 4418", "2023级软件工程1班", rm],
        ["<b>刘子涵</b>", '<span data-no="8209240133">8209240133</span>', "158 7312 6609", "2024级人工智能2班", rm],
    ], id_="admin-table")
    body = (card("运行信息", f"""<div class="form-grid c3">
  {field(PUBLISH_TIME_LABEL, inp("", "2026-09-22", True, "date"), True, "日期选择")}
  {field("更新频率", sel(UPDATE_FREQ, UPDATE_FREQ[0], True), True)}
  {field("运行状态", sel(RUN_STATUS, "正常运行", True), True, "正常运行、不活跃、整改中、暂停运行、申请注销、已注销")}
  <div class="full">{field("异常情况", textarea("请填写异常情况", "", False, 0, 2))}</div>
</div>""")
            + card("当前管理教师", f"""<div class="form-grid c3">
  {field("姓名", inp("", "王晓琳", True), True)}
  {field("工号", inp("", WX["no"], True), True)}
  {field("职务", inp("", "宣传工作辅导员", True), True)}
  {field("手机号", inp("", WX["phone"], True), True)}
  {field("是否为专职教师", radios("fulltime", ["是", "否"], "是", True), True)}
</div>""", cls="mt16")
            + card("当前学生运营负责人 · 具体负责人", f"""<div class="form-grid c3">
  {field("姓名", inp("", "李明", True), True)}
  {field("学号", inp("", LM["no"], True), True)}
  {field("手机号", inp("", LM["phone"], True), True)}
</div><div class="small muted mt8">本次由发起人李明担任具体负责人</div>""", cls="mt16")
            + card("当前学生运营负责人 · 管理员", admins + people_picker("pick-admin", "admin-table", "admin", 5),
                   add_people_btn("pick-admin", "admin-table", 5) + '<span class="small muted">检索学号或姓名加入，最多 5 人</span>', cls="mt16")
            + card("制度责任人", kv([("第一责任人", "张卫东 · 计算机学院党委副书记"), ("直接责任人", "周建华 · 学院团委书记"), ("带出规则", "按所属学院自动带出，二级、三级平台由所在单位党委统一指导", True)], 2)
                   + '<div class="mt12">' + alert("第一责任人、直接责任人不用手填，提交时随学院信息一并送审。", "info") + "</div>", cls="mt16 grow"))
    content = shell(page_hd("新建备案申请", "发起人：李明 · 第 3 / 4 步"), wiz(2) + f'<div class="mt16">{body}</div>',
                    bar("管理员最多 5 人，具体负责人为本申请人", back_btn("apply-duplicate.html", "上一步") + submit_btn("下一步", "apply-create-reviewer.html")))
    page("apply-create-staff.html", "apply", "新建备案 · 运行与负责人", crumbs(("业务申请", "apply.html"), ("运行与负责人", None)), content, STAFF_JS)


def create_reviewer():
    teachers = [("王晓琳", WX, True, "推荐 · 本组织指导教师"), ("刘洋", PEOPLE["刘洋"], False, "2023级辅导员"),
                ("周建华", ZJ, False, "学院团委书记，一般不作为一审"), ("张卫东", PEOPLE["张卫东"], False, "党委副书记"),
                ("陈静", CJ, False, "校团委宣传部，一般为终审")]
    choices = "".join(
        f'<div class="choice{" on" if on else ""}" data-choice data-cat="{esc(n + " " + p["no"] + " " + p["job"])}"><span class="ck"></span><div class="grow"><b>{n}</b>'
        f'<div class="small muted">工号 {p["no"]} · {p["job"]} · {p["phone"]}</div><div class="small c-primary mt4">{tip}</div></div></div>'
        for n, p, on, tip in teachers)
    summary = kv([("所属学院 / 组织", "计算机学院 · " + NEW["org"]), ("组织类别 / 层级", NEW["org_type"] + " · " + NEW["level"]),
                  ("平台", NEW["platform"] + " · " + NEW["name"]), ("平台 ID", NEW["pid"]),
                  ("管理教师 / 负责人", "王晓琳 / 李明"), ("管理员", "陈可欣、刘子涵", True)], 3)
    content = shell(
        page_hd("新建备案申请", "第 4 / 4 步 · 指导教师审核阶段可以指定审核老师"),
        wiz(3) + card("审核信息", '<div class="small muted mb8">一审可以改选。输入姓名或工号筛选。二审、三审按组织带出。</div>'
                     '<label class="top-search mb12" style="width:320px">' + icon("search") + '<input placeholder="搜索姓名 / 工号" data-search="#rev-list"></label>'
                     '<div class="field-label mb8"><span class="req">*</span>一审负责人</div><div class="choices" id="rev-list" data-single>' + choices + "</div>", cls="mt16")
        + f'<div class="grid g2 mt16">{card("二审负责人", kv([("姓名", "周建华"), ("工号", ZJ["no"]), ("职务", ZJ["job"]), ("手机号", ZJ["phone"])], 2))}'
        f'{card("三审负责人", kv([("姓名", "陈静"), ("工号", CJ["no"]), ("职务", CJ["job"]), ("手机号", CJ["phone"])], 2))}</div>'
        + card("审核流程", timeline([("now", "一审 · 指导教师", "默认王晓琳，可在上方改选", ""), ("wait", "二审 · 学院团委", "周建华", ""), ("wait", "三审 · 校团委", "陈静", "通过后建立档案")]), cls="mt16")
        + card("本申请摘要", summary, cls="mt16 grow")
        + '<label class="card mt16 field" style="display:flex;gap:8px;align-items:center;padding:14px 16px"><input type="checkbox" checked required style="accent-color:var(--c-primary)">本人承诺所填信息真实、准确、完整。<span class="err-msg">请勾选承诺</span></label>',
        bar("提交后通知一审老师", back_btn("apply-create-staff.html", "上一步") + submit_btn("提交申请", "apply-result.html", ic="send", toast="申请已提交")))
    page("apply-create-reviewer.html", "apply", "新建备案 · 审核人", crumbs(("业务申请", "apply.html"), ("审核人", None)), content)


def apply_result():
    content = shell(
        page_hd("申请已提交", NEW_NO),
        card("", result("ok", "新建备案已提交", "已通知指导教师王晓琳审核。你可以在我的申请里查看进度、催办或撤回。"))
        + card("审核流程", timeline([("done", "学生提交", "李明 · 刚刚", ""), ("now", "指导教师审核", "王晓琳", ""), ("wait", "学院团委审核", "周建华", ""), ("wait", "校团委审核", "陈静", "")]), cls="mt16")
        + '<div class="mt16">' + tiles([
            ("查看进度", "可撤回或催办", "application-detail.html", "eye", ""),
            ("我的申请", "审核中与退回", "apply.html", "clipboard", "orange"),
            ("返回业务申请", "继续办其他业务", "apply.html", "file-add", "green"),
            ("返回首页", "待办与账号", "home.html", "home", "purple"),
        ]) + "</div>",
        bar("编号 " + NEW_NO, btn("查看进度", "application-detail.html", "primary", "eye") + btn("我的申请", "apply.html", "default", "clipboard") + btn("返回首页", "home.html", "ghost")))
    page("apply-result.html", "apply", "提交成功", crumbs(("业务申请", "apply.html"), ("提交成功", None)), content)


def apply_id_change():
    opts = ["计院摄影协会 · 视频号", "中南计院团委 · 微信公众号", "计算机学院学生会 · 微博", "计院街舞社 · 抖音"]
    body = card("识别规则", alert("平台 ID 发生变化，不属于普通信息变更。同一平台类型下平台 ID 唯一。必须同时办成两件事：按<b>新 ID 新建备案</b>，并<b>注销原来的 ID</b>。只改名称、主页或二维码的，请返回信息变更。", "warning")
                + '<div class="guide mt16">' + "".join(f'<div><b>{t}</b><div class="small muted mt4">{d}</div></div>' for t, d in [
                    ("1. 选定原账号", "系统带出当前平台 ID"), ("2. 填写新 ID", "作为新建备案的唯一标识"), ("3. 新建备案", "走四步向导重新审核"), ("4. 注销原 ID", "原档案永久保留"),
                ]) + "</div>")
    select = '<select class="select" required onchange="syncOldPid(this)">' + "".join(
        f'<option{" selected" if o == opts[0] else ""}>{o}</option>' for o in opts) + "</select>"
    form = card("本次要变更的 ID", f"""<div class="idbox mb16"><div class="box"><div class="small muted">原平台 ID · 将注销</div><b class="c-danger fs18" id="old-pid-view">sph_csu_cs_photo</b><div class="small muted mt8">档案保留，状态改为已注销</div></div>
      <div class="mid">{icon("arrow-right", 22)}</div>
      <div class="box" style="border-color:var(--c-primary-border);background:#F7FBFE"><div class="small muted">新平台 ID · 须新建备案</div><div class="mt8 bold">在下方填写，不能与原 ID 相同</div><div class="small muted mt8">提交后走指导教师、学院、校团委三级审核</div></div></div>
      <div class="form-grid">
      {field("原账号", select, True)}
      {field("原平台 ID", inp("", "sph_csu_cs_photo", readonly=True, attrs='id="old-pid"'), True)}
      <div class="full">{field("新平台 ID", inp("请输入新的平台 ID", "", True, attrs='id="new-pid"'), True, PID_HINT)}</div>
    </div>""", cls="mt16 grow")
    content = shell(page_hd("平台 ID 变化", "不能按普通变更提交"), body + form,
                    bar("两项都要提交，没有先后", back_btn("apply.html", "返回业务申请") + btn("去注销原账号", "apply-cancel.html", "default", "power") + submit_btn("去新建备案", "apply-create-basic.html", ic="file-add", toast="请在新建备案中填写新的平台 ID")))
    page("apply-id-change.html", "apply", "平台 ID 变化", crumbs(("业务申请", "apply.html"), ("平台 ID 变化", None)), content, ID_JS)


def apply_change():
    choices = ('<div class="choices cols" data-single=".id-pane">'
               '<div class="choice on" data-choice=".pane-name"><span class="ck"></span><div><b>普通信息变更</b><div class="small muted">名称、主页、二维码等，平台 ID 不变</div></div></div>'
               '<div class="choice" data-choice=".pane-id"><span class="ck"></span><div><b>平台 ID 发生变化</b><div class="small muted">须新建备案，并注销原 ID</div></div></div></div>')
    name_form = f"""<div class="form-grid">
  {field("变更账号", inp("", "", readonly=True, attrs='id="chg-acct"'), True)}
  {field("账号名称 · 变更前", inp("", "", readonly=True, attrs='id="chg-before"'))}
  {field("账号名称 · 变更后", inp("请输入新名称", "", True, attrs='id="chg-after"'), True)}
  <div class="full">{field("变更说明", textarea("请说明变更原因", "", True, 200, 3, attrs='id="chg-reason"'), True)}</div>
  <div class="full">{field("佐证材料", upload("上传换届决议等", "jpg / png / pdf", ["学生会第十届换届决议.pdf"]))}</div>
</div>"""
    id_pane = alert("平台 ID 变化不会进入这条变更流程。下一步说明原 ID 与新 ID，并分别打开新建备案和注销。", "warning") + '<div class="guide mt12"><div><b>新建</b><div class="small muted">用新 ID 走四步备案</div></div><div><b>注销</b><div class="small muted">原 ID 停用并保留档案</div></div><div><b>名称变更</b><div class="small muted">请改回左侧「普通信息变更」</div></div><div><b>当前账号</b><div class="small muted" id="chg-id-label">选择账号后显示</div></div></div>'
    form = card("变更类型", choices) + f'<div class="id-pane pane-name mt16">{card("变更内容", name_form)}</div><div class="id-pane pane-id mt16 hidden">{card("平台 ID 不能在此修改", id_pane)}</div>'
    content = shell(
        page_hd("信息变更", '<span id="acct-sub">请先选择要办理的账号</span>'),
        _acct_step("信息变更", form),
        bar("未选择账号时不能提交", back_btn("apply.html", "取消")
            + '<span class="id-pane pane-name">' + submit_btn("下一步", "apply-change-confirm.html") + "</span>"
            + '<span class="id-pane pane-id hidden">' + submit_btn("按平台 ID 规则办理", "apply-id-change.html", toast="平台 ID 变化需新建并注销原号") + "</span>"))
    page("apply-change.html", "apply", "信息变更", crumbs(("业务申请", "apply.html"), ("信息变更", None)), content, page_js())


def change_confirm():
    content = shell(
        page_hd("确认变更", "审核通过后新名称生效，原名称记入曾用名"),
        card("变更前后", diff_table([
            ("账号名称", REN["name"], REN["new_name"]),
            ("平台类型", REN["platform"], REN["platform"]),
            ("平台 ID", REN["pid"], REN["pid"]),
            ("负责人", "李明", "李明"),
            ("所属组织", REN["org"], REN["org"]),
        ]) + '<div class="mt12">' + alert("平台 ID 两列相同，可以按普通变更提交。", "success") + "</div>", cls="grow"),
        bar("确认后提交指导教师王晓琳", back_btn("apply-change.html", "返回修改") + submit_btn("确认提交", "apply-change-result.html", ic="send", toast="变更申请已提交")))
    page("apply-change-confirm.html", "apply", "变更确认", crumbs(("信息变更", "apply-change.html"), ("确认", None)), content)


def change_result():
    content = shell(
        page_hd("变更申请已提交", FLOWS["rename"]["no"]),
        card("", result("ok", "名称变更已提交", "「" + REN["name"] + "」拟改为「" + REN["new_name"] + "」。已通知王晓琳审核。"))
        + card("审核流程", timeline([
            ("done", "学生提交名称变更", "李明 · 刚刚", FLOWS["rename"]["steps"][0][3]),
            ("now", "指导教师审核", "王晓琳", ""),
            ("wait", "学院团委审核", "周建华", "重要变更继续上报"),
            ("wait", "校团委审核", "陈静", "通过后原名称记入曾用名"),
        ]), cls="mt16 grow"),
        bar(FLOWS["rename"]["no"], btn("查看进度", "application-change.html", "primary", "eye") + btn("我的申请", "apply.html", "default") + btn("返回首页", "home.html", "ghost")))
    page("apply-change-result.html", "apply", "变更已提交", crumbs(("信息变更", "apply-change.html"), ("提交成功", None)), content)


def apply_handover():
    opener = '<button type="button" class="btn btn-light btn-sm" data-toggle="#pick-ho">' + icon("search") + "检索学生</button>"
    form = f"""<div class="form-grid">
    <div class="full">{field("交接账号", inp("", "", readonly=True, attrs='id="ho-acct"'), True)}</div>
    {field("姓名", inp("", "李四", True, attrs='id="ho-name"'), True)}
    {field("学号", inp("", LS["no"], True, attrs='id="ho-no"'), True)}
    {field("手机号", inp("", LS["phone"], True, attrs='id="ho-phone"'), True)}
    {field("职务", inp("", LS["job"]))}
    {field("生效时间", inp("", "2026-10-01", True, "date"), True)}
  </div>{successor_picker()}"""
    inner = (f'<div class="grid g2">{card("原负责人", kv([("姓名", "李明"), ("学号", LM["no"]), ("手机号", LM["phone"]), ("任期", "2024-09-10 起")], 2))}{card("新负责人", form, opener)}</div>'
             + card("交接说明", field("交接说明", textarea("请说明交接原因", FLOWS["handover"]["steps"][0][3], True, 200, 3), True), cls="mt16 grow")
             + f'<div class="mt16">{alert("学生提交后由具体管理教师王晓琳审核，通过即生效。原负责人任职起止时间保留在账号历史中。", "info")}</div>')
    content = shell(
        page_hd("负责人交接", '<span id="acct-sub">请先选择要办理的账号</span>'),
        _acct_step("负责人交接", inner),
        bar("未选择账号时不能提交", back_btn("apply.html", "取消") + submit_btn("提交申请", "apply-handover-result.html", ic="send", toast="交接申请已提交")),
        )
    page("apply-handover.html", "apply", "负责人交接", crumbs(("业务申请", "apply.html"), ("负责人交接", None)), content, PERSON_JS + page_js())


def handover_result():
    content = shell(
        page_hd("交接申请已提交", FLOWS["handover"]["no"]),
        card("", result("ok", "负责人交接已提交", HO["name"] + "拟由李明交接给李四，生效时间 2026-10-01。"))
        + card("审核流程", timeline([
            ("done", "学生提交", "李明 · 刚刚", FLOWS["handover"]["steps"][0][3]),
            ("now", "指导教师审核", "王晓琳 · 通过即生效", ""),
        ]), cls="mt16 grow"),
        bar("只需指导教师审核", btn("返回账号", "account-handover.html", "primary", "archive") + btn("我的申请", "apply.html", "default") + btn("返回首页", "home.html", "ghost")))
    page("apply-handover-result.html", "apply", "交接已提交", crumbs(("负责人交接", "apply-handover.html"), ("提交成功", None)), content)


def apply_cancel():
    form = card("注销信息", f"""<div class="form-grid">
  {field("注销账号", inp("", "", readonly=True, attrs='id="cancel-acct"'), True)}
  {field("平台 ID", inp("", "", readonly=True, attrs='id="cancel-pid"'), True)}
  <div class="full">{field("注销原因", radios("why", CANCEL_REASONS, "重复账号", True), True)}</div>
  <div class="full">{field("注销说明", textarea("请说明注销原因", "该视频号长期未更新，协会已改用其他平台发布，申请注销。", True, 300, 3), True)}</div>
  <div class="full">{field("佐证材料", upload("上传决议或停更说明", "jpg / png / pdf"))}</div>
</div>""") + '<div class="mt16">' + alert('注销后状态转为已注销，档案与历史永久保留。如果实际是平台 ID 换了，不要只注销旧号，还要按新 ID 新建备案。<a class="link" href="apply-id-change.html">按平台 ID 变化办理</a>', "warning") + "</div>"
    content = shell(
        page_hd("账号注销", '<span id="acct-sub">请先选择要办理的账号</span>'),
        _acct_step("账号注销", form),
        bar("未选择账号时不能提交", back_btn("apply.html", "取消") + submit_btn("提交申请", "apply-cancel-result.html", ic="send", toast="注销申请已提交")))
    page("apply-cancel.html", "apply", "账号注销", crumbs(("业务申请", "apply.html"), ("账号注销", None)), content, page_js())


def cancel_result():
    content = shell(
        page_hd("注销申请已提交", "ZX20260930021"),
        card("", result("ok", "注销申请已提交", "默认账号为计院摄影协会（视频号）。审核完成前账号仍可查询，通过后状态改为已注销，数据永久保留。"))
        + card("审核流程", timeline([("done", "学生提交注销", "李明 · 刚刚", "重复账号 / 长期未更新"), ("now", "指导教师审核", "王晓琳", ""), ("wait", "学院团委审核", "周建华", ""), ("wait", "校团委确认", "陈静", "")]), cls="mt16 grow"),
        bar("ZX20260930021", btn("返回账号", "account-photo.html", "primary", "archive") + btn("我的申请", "apply.html", "default") + btn("返回首页", "home.html", "ghost")))
    page("apply-cancel-result.html", "apply", "注销已提交", crumbs(("账号注销", "apply-cancel.html"), ("提交成功", None)), content)


def apply_claim():
    rows = [
        ("计院篮球协会", "抖音", "csu_cs_basketball", "缺负责教师"),
        ("2022级计算机科学2班团支部", "QQ", "2230617785", "缺学生负责人"),
        ("计院辩论队", "哔哩哔哩", "csu_cs_debate", "缺负责教师"),
        ("计算机学院研究生会", "微信公众号", "csu_cs_gs", "缺学生负责人"),
    ]
    body = []
    for n, p, pid, miss in rows:
        js = "var i=document.getElementById('claim-name');if(i){i.value='" + n + "';}toast('已选择：" + n + "');"
        body.append([acct(n, p, pid), p, f'<span class="num">{pid}</span>', tag(miss, "warning"),
                     f'<button class="btn btn-light btn-sm" type="button" onclick="{js}">{icon("hand")}认领</button>'])
    content = shell(
        page_hd("账号认领", "学校已导入、尚未绑定到本人的历史账号"),
        '<label class="top-search mb12" style="width:320px">' + icon("search") + '<input placeholder="搜索账号名称 / 平台 ID" data-search="#claim-tbl"></label>'
        + card("可认领账号", table(["账号", "平台", "平台 ID", "缺失", "操作"], body, id_="claim-tbl") + pager(4, 1))
        + card("认领说明", f"""<div class="form-grid">
  {field("认领账号", inp("请先在上方点击认领", "", True, attrs='id="claim-name" readonly'), True)}
  <div class="full">{field("认领说明", textarea("请说明你与该账号的关系", "我是该组织现任宣传负责人，申请认领并补全责任人信息。", True, 200, 3), True)}</div>
</div>""", cls="mt16 grow"),
        bar("未选择账号时不能提交", back_btn("apply.html", "取消") + submit_btn("提交认领申请", "apply-claim-result.html", ic="send", toast="认领申请已提交，等待指导教师确认")))
    page("apply-claim.html", "apply", "账号认领", crumbs(("业务申请", "apply.html"), ("账号认领", None)), content)


def claim_result():
    content = shell(
        page_hd("认领申请已提交", "RL20260930015"),
        card("", result("ok", "认领申请已提交", "指导教师王晓琳将确认你与所选账号的责任关系。确认通过后，该账号出现在我的账号中。"))
        + card("后续", timeline([("done", "学生提交认领", "李明 · 刚刚", ""), ("now", "指导教师确认", "王晓琳", ""), ("wait", "写入责任人", "通过后可办理年审与变更", "")]), cls="mt16 grow"),
        bar("RL20260930015", btn("返回认领", "apply-claim.html", "default", "hand") + btn("我的账号", "accounts.html", "primary", "database") + btn("返回首页", "home.html", "ghost")))
    page("apply-claim-result.html", "apply", "认领已提交", crumbs(("账号认领", "apply-claim.html"), ("提交成功", None)), content)


# ---------------------------------------------------------------- 我的申请
SCOPE_SHORT = "学院团学活动相关信息。"
SCOPE_FULL = "限于计算机学院团学工作相关内容：思想引领、团学活动、学术科创、评优公示。"
REJECT_INTRO = "计院学生会拟开设抖音账号，用于发布招新通知、活动预告和院会信息。"
REJECT_SCOPE = "计算机学院学生会活动通知与招新信息。"


def _attach(names):
    return "".join(
        '<button class="btn btn-text btn-sm" type="button" data-toast="正在预览：' + n + '">' + icon("file", 14) + n + "</button>"
        for n in names)


def _intro_html(text, warn=False):
    cls = "intro-box warn" if warn else "intro-box"
    return '<div class="' + cls + '">' + text + '</div><div class="small muted mt8">共 ' + str(len(text)) + " 字</div>"


def _mechs():
    return kv([(m["no"] + " " + m["title"], tag("已建立", "success")) for m in MECHANISMS], 2)


def _people_run():
    return kv([
        (PUBLISH_TIME_LABEL, "2026-09-22"),
        ("更新频率", UPDATE_FREQ[0]),
        ("运行状态", "正常运行"),
        ("异常情况", "无"),
        ("管理教师", "王晓琳 · " + WX["no"]),
        ("职务 / 手机", "宣传工作辅导员 · " + WX["phone"]),
        ("是否专职教师", "是"),
        ("具体负责人", "李明 · " + LM["no"] + " · " + LM["phone"]),
        ("管理员", "陈可欣（8209230221）、刘子涵（8209240133）", True),
        ("第一责任人", "张卫东 · 学院党委副书记"),
        ("一审", "王晓琳"),
        ("二审", "周建华 · " + ZJ["job"]),
        ("三审", "陈静 · " + CJ["job"]),
    ], 2)


def _new_filled(a, intro, scope, warn=False, fans="0", team="6", home="https://mp.weixin.qq.com/csu_cs_youth", former="—", run_kv=None):
    belong = card("归属信息", kv([
        ("所属学校", "中南大学"), ("所属学院", "计算机学院"), ("所属团学组织", a["org"]),
        ("组织类别", a["org_type"]), ("平台管理层级", a["level"]), ("开通时间", a["opened"]),
    ], 2))
    platform = card("平台信息", kv([
        ("平台类型", a["platform"]), ("账号名称", a["name"]), ("曾用名", former),
        ("平台 ID", '<span class="num">' + a["pid"] + "</span>" + copy_btn(a["pid"])),
        ("是否认证", "否"), ("粉丝数", fans), (TEAM_LABEL, team),
        ("主页链接", home, True), ("平台头像", "已上传"), ("二维码", "未上传（非必填）"),
    ], 2) + '<div class="divider"></div><div class="field-label mb8">平台介绍</div>' + _intro_html(intro, warn)
        + '<div class="mt12"><div class="field-label mb8">信息发布范围</div><div class="intro-box">' + scope + "</div></div>"
        + '<div class="mt16"><div class="field-label mb8">平台信息确认</div>' + _mechs() + "</div>", cls="mt16")
    run = card("运行与负责人", run_kv if run_kv is not None else _people_run(), cls="mt16")
    return belong + platform + run


def _change_filled():
    diff = card("变更内容", diff_table([
        ("账号名称", REN["name"], REN["new_name"]),
        ("平台类型", REN["platform"], REN["platform"]),
        ("平台 ID", REN["pid"], REN["pid"]),
        ("所属团学组织", REN["org"], REN["org"]),
        ("平台层级", REN["level"], REN["level"]),
        ("学生负责人", "李明", "李明"),
        ("管理教师", "王晓琳", "王晓琳"),
    ]))
    reason = card("变更说明与材料", kv([
        ("变更原因", FLOWS["rename"]["steps"][0][3], True),
        ("详细说明", "2026 年 9 月学生会完成换届，学院各新媒体平台统一使用「中南计院」品牌前缀，微博名称调整为「中南计院学生会」，账号主体与运营团队不变。", True),
        ("佐证材料", _attach(["学生会第十届换届决议.pdf", "微博改名预览截图.png"]), True),
    ], 2), cls="mt16")
    base = card("账号原信息", kv([
        ("所属学校", "中南大学"), ("所属学院", "计算机学院"), ("所属团学组织", REN["org"]),
        ("组织类别", REN["org_type"]), ("平台管理层级", REN["level"]), ("开通时间", REN["opened"]),
        ("粉丝数", REN["fans"]), ("主页链接", "https://weibo.com/" + REN["pid"]),
    ], 2), cls="mt16")
    return diff + reason + base


def _handover_filled():
    pair = '<div class="grid g2">' + card("原负责人", kv([
        ("姓名", "李明"), ("学号", LM["no"]), ("手机号", LM["phone"]),
        ("班级", LM["grade"]), ("职务", "街舞社原宣传负责人"), ("任期", "2024-09-10 ~ 2026-09-30"),
    ], 2)) + card("新负责人", kv([
        ("姓名", "李四"), ("学号", LS["no"]), ("手机号", LS["phone"]),
        ("班级", LS["grade"]), ("职务", LS["job"]), ("生效时间", "2026-10-01"),
    ], 2)) + "</div>"
    note = card("交接说明", kv([
        ("交接账号", HO["name"] + " · " + HO["platform"]),
        ("平台 ID", HO["pid"]),
        ("所属组织", HO["org"]),
        ("平台层级", HO["level"]),
        ("交接原因", FLOWS["handover"]["steps"][0][3], True),
        ("已确认事项", "密码已更换、绑定手机已变更、素材已移交、新负责人已签承诺书", True),
        ("佐证材料", _attach(["街舞社换届名单.pdf", "交接清单（双方签字）.pdf"]), True),
    ], 2), cls="mt16")
    return pair + note


def _cancel_filled(a, reason, note, files):
    return card("注销申请", kv([
        ("注销账号", a["name"]), ("平台类型", a["platform"]), ("平台 ID", a["pid"]),
        ("所属组织", a["org"]), ("平台层级", a["level"]), ("开通时间", a["opened"]),
        ("注销原因", reason), ("最近发布", a.get("last_post", "—")),
        ("注销说明", note, True),
        ("佐证材料", _attach(files), True),
    ], 2))


def _chart(nodes):
    boxes = ['<div class="wf-end">开始</div>']
    for n, h, s in nodes:
        boxes.append('<i class="wf-arrow ' + s + '"></i><div class="wf-node ' + s + '">' + icon("user", 16) + "<b>" + n + "</b><small>" + h + "</small></div>")
    boxes.append('<i class="wf-arrow wait"></i><div class="wf-end">结束</div>')
    zoom_m = WF_ZOOM.format(d="-.1")
    zoom_p = WF_ZOOM.format(d=".1")
    return ('<div class="flow-box"><div class="wf-chart" data-s="1"><div class="wf-zoom">'
            '<button type="button" onclick="' + zoom_m + '" aria-label="缩小">' + icon("zoom-out") + "</button>"
            '<span class="wf-pct">100%</span>'
            '<button type="button" onclick="' + zoom_p + '" aria-label="放大">' + icon("zoom-in") + "</button></div>"
            '<div class="wf-flow">' + "".join(boxes) + "</div>"
            '<div class="wf-legend"><span class="done">已完成</span><span class="now">当前环节</span><span class="wait">未开始</span></div></div></div>')


def _rec_table(spec):
    rows = []
    for i, r in enumerate(spec["records"]):
        rows.append([str(i + 1), r[0], r[1], tag(r[3], WF_OP_KIND.get(r[3], "primary")), r[4] or "—", r[5]])
    for a in spec["approvers"]:
        now = next((n for n, _, s in spec["nodes"] if s == "now"), "")
        rows.append([str(len(rows) + 1), now, a[1], tag("审批中", "primary"), "—", "—"])
    return table(["序号", "流程环节", "实际审批人", "审批操作", "审批意见", "处理时间"], rows)


def _flow_block(spec, ended="流程已结束"):
    now = [(n, h) for n, h, s in spec["nodes"] if s == "now"]
    if now:
        line = alert("<b>当前节点：</b>" + now[0][0] + " · " + now[0][1] + "　流程：" + spec["name"], "info")
    else:
        line = alert("<b>当前节点：</b>" + ended + "　流程：" + spec["name"], "success")
    return '<div class="mt16">' + line + "</div>" + card("流程图", _chart(spec["nodes"]), cls="mt16") + card("审批记录", _rec_table(spec), cls="mt16")


def application_table():
    rows = [
        dict(cells=[NEW_NO, "新建备案", NEW["name"], "学院团委审核", st("审核中"), "09-26 重提", btn("查看", "application-detail.html", "text", "eye", "sm")], cat="ing"),
        dict(cells=[FLOWS["rename"]["no"], "信息变更", REN["name"], "指导教师审核", st("审核中"), "09-26 提交", btn("查看", "application-change.html", "text", "eye", "sm")], cat="ing"),
        dict(cells=[NEW_NO, "新建备案", NEW["name"], "退回修改", st("已退回"), "09-25 退回", btn("查看", "application-returned.html", "text", "eye", "sm")], cat="back"),
        dict(cells=[NEW_NO, "新建备案", NEW["name"], "校团委通过", st("已通过"), "09-30 完成", btn("查看", "application-approved.html", "text", "eye", "sm")], cat="ok"),
        dict(cells=[FLOWS["handover"]["no"], "负责人交接", HO["name"], "已生效", st("已通过"), "09-28 完成", btn("查看", "application-handover.html", "text", "eye", "sm")], cat="ok"),
        dict(cells=["XJ20260912006", "新建备案", "计院学生会", "不予备案", st("已驳回"), "09-13 驳回", btn("查看", "application-rejected.html", "text", "eye", "sm")], cat="no"),
    ]
    return (
        '<div class="apply-list-hd mt16"><b>我的申请</b><span class="small muted">同一申请的退回、审核中、通过会同时列出，分别对应那个阶段</span></div>'
        + filter_bar([
            field("关键词", inp("编号 / 账号", attrs='data-search="#app-tbl"')),
            field("业务类型", sel(["新建备案", "信息变更", "负责人交接"], ph="全部")),
            field("当前节点", sel(["指导教师", "学院团委", "校团委"], ph="全部")),
        ])
        + '<div class="card"><div class="card-bd"><div class="toolbar">'
        + seg([("全部", "all"), ("审核中", "ing"), ("已退回", "back"), ("已通过", "ok"), ("已驳回", "no")], target="#app-tbl")
        + "</div>"
        + table(["编号", "类型", "账号", "当前节点", "状态", "时间", "操作"], rows, id_="app-tbl")
        + pager(6, 1)
        + '<div class="small muted mt12">「中南计算机青年」的退回、审核中、通过是同一份新建申请的三个阶段。退回后可以修改重提；驳回则流程终止。</div></div></div>'
    )


def application_detail():
    spec = flow_spec("new", 4, 2)
    content = shell(
        page_hd("申请进度", NEW_NO + " · " + NEW["name"], st("审核中")),
        alert("当前查看的是 09-26 重新提交的稿。历史退回 1 次，下面是当时填写的内容，只读。", "info")
        + '<div class="bold mt16">填报内容</div>'
        + _new_filled(NEW, INTRO_FULL, SCOPE_FULL)
        + _flow_block(spec)
        + '<div id="undo-done" class="hidden mt16">' + card("", result("ok", "申请已撤回", "可修改后重新提交。", btn("去修改", "application-edit.html", "primary", "edit") + btn("返回我的申请", "apply.html", "ghost"))) + "</div>",
        bar("审核中可撤回或催办", '<button class="btn btn-default" type="button" data-toggle="#dlg-undo">' + icon("undo") + "撤回申请</button>" + btn("催办", None, "primary", "bell", toast="已向学院团委周建华发送催办")),
        dialog("dlg-undo", "撤回这条申请？", "撤回后可修改内容再提交，当前审核节点将停止。", '<button class="btn btn-primary" type="button" data-toggle="#dlg-undo,#undo-done" data-toast="申请已撤回，可修改后重新提交">确认撤回</button>'))
    page("application-detail.html", "apply", "申请进度", crumbs(("业务申请", "apply.html"), ("审核中", None)), content)


def application_change():
    spec = flow_spec("rename", 1, 1, "change")
    content = shell(
        page_hd("变更进度", FLOWS["rename"]["no"] + " · " + REN["name"], st("审核中")),
        '<div class="bold">填报内容</div>' + _change_filled() + _flow_block(spec),
        bar("可催办当前节点", btn("返回我的申请", "apply.html", "default") + btn("催办", None, "primary", "bell", toast="已向王晓琳发送催办")))
    page("application-change.html", "apply", "变更进度", crumbs(("业务申请", "apply.html"), ("信息变更", None)), content)


def application_returned():
    spec = custom_spec(
        "new", NEW["name"] + " · " + NEW_NO, "李明",
        [("提交申请", "李明"), ("指导教师审核", "王晓琳"), ("申请人修改", "李明"), ("学院团委审核", "周建华"), ("校团委审核", "陈静")],
        [("提交申请", "李明", "", "提交", "", "2026-09-24 10:12"),
         ("指导教师审核", "王晓琳", "", "退回", FLOWS["new"]["steps"][1][3], "2026-09-25 09:30")],
        2)
    content = shell(
        page_hd("申请已退回", NEW["name"], st("已退回")),
        card("退回意见", alert(FLOWS["new"]["steps"][1][3], "danger") + '<div class="small muted mt8">王晓琳 · 2026-09-25 09:30 · 当前 ' + str(SHORT_N) + " 字，不足 100 字</div>")
        + alert("下面是 09-24 首次提交、后来被退回的填报内容。平台介绍需要补充后才能重提。", "warning")
        + '<div class="bold mt16">填报内容</div>'
        + _new_filled(NEW, INTRO_SHORT, SCOPE_SHORT, warn=True)
        + _flow_block(spec)
        + '<div id="cancel-done" class="hidden mt16">' + card("", result("warn", "申请已撤销", "流程已终止。如需备案请重新发起。", btn("重新发起", "apply-create-basic.html", "primary") + btn("返回我的申请", "apply.html", "ghost"))) + "</div>",
        bar("按意见修改后可重新提交", '<button class="btn btn-danger" type="button" data-toggle="#dlg-cancel">撤销申请</button>' + btn("修改并重新提交", "application-edit.html", "primary", "edit")),
        dialog("dlg-cancel", "撤销这条申请？", "撤销后流程终止。如仍需备案，需重新发起。", '<button class="btn btn-danger" type="button" data-toggle="#dlg-cancel,#cancel-done" data-toast="申请已撤销，流程终止">确认撤销</button>'))
    page("application-returned.html", "apply", "申请已退回", crumbs(("业务申请", "apply.html"), ("已退回", None)), content)


def application_edit():
    content = shell(
        page_hd("修改后重新提交", "只需修改被退回的字段"),
        alert(FLOWS["new"]["steps"][1][3], "danger")
        + card("平台介绍", field("平台介绍", textarea(INTRO_HINT, INTRO_FULL, True, 800, 8), True, INTRO_HINT + "。当前 " + str(FULL_N) + " 字"), cls="mt16")
        + card("信息发布范围", field("信息发布范围", textarea("请填写信息发布范围", "限于计算机学院团学工作相关内容：思想引领、团学活动、学术科创、评优公示。", True, 0, 3), True), cls="mt16 grow"),
        bar("重新提交后回到指导教师审核", back_btn("application-returned.html", "取消") + submit_btn("重新提交", "application-detail.html", ic="send", toast="已重新提交")))
    page("application-edit.html", "apply", "修改后重新提交", crumbs(("已退回", "application-returned.html"), ("修改", None)), content)


def application_approved():
    spec = flow_spec("new", 6, 4)
    content = shell(
        page_hd("备案完成", NEW_NO + " · " + FILING_OK, st("已通过")),
        card("", result("ok", "已准予备案", "账号档案已建立，备案表已生成。"))
        + card("审核结论", kv([("备案编号", FILING_OK), ("申请编号", NEW_NO), ("终审", "陈静 · 校团委宣传部"), ("备案时间", "2026-09-30 10:05"), ("意见", FLOWS["new"]["steps"][5][3], True)], 2), cls="mt16")
        + alert("下面是终审通过的那一稿，与 09-26 重提内容一致，只读。", "success")
        + '<div class="bold mt16">填报内容</div>'
        + _new_filled(NEW, INTRO_FULL, SCOPE_FULL)
        + _flow_block(spec, "校团委已通过，流程结束"),
        bar(FILING_OK, btn("查看账号档案", "account-youth.html", "primary", "archive") + btn("下载备案表", None, "default", "download", toast="备案表已开始下载") + btn("返回我的申请", "apply.html", "ghost")))
    page("application-approved.html", "apply", "备案完成", crumbs(("业务申请", "apply.html"), ("已通过", None)), content)


def application_handover():
    spec = flow_spec("handover", 2, 2)
    content = shell(
        page_hd("交接已生效", FLOWS["handover"]["no"] + " · " + HO["name"], st("已通过")),
        card("", result("ok", "指导教师已通过，交接生效", "生效时间 2026-10-01。李明的任职记入历史，李四成为新负责人。"))
        + '<div class="bold mt16">填报内容</div>'
        + _handover_filled()
        + _flow_block(spec, "交接已生效"),
        bar("填写过程仍可打开", btn("查看账号", "account-handover.html", "primary", "archive") + btn("打开交接表", "apply-handover.html", "default", "edit") + btn("返回我的申请", "apply.html", "ghost")))
    page("application-handover.html", "apply", "交接已生效", crumbs(("业务申请", "apply.html"), ("交接结果", None)), content)


def application_rejected():
    rej = dict(name="计院学生会", platform="抖音", pid="csu_cs_su", level="二级平台", org_type="院级学生组织",
               org="计算机学院学生会", opened="2026-09-08")
    run = kv([
        (PUBLISH_TIME_LABEL, "尚未发布"),
        ("更新频率", UPDATE_FREQ[5]),
        ("运行状态", "拟新开"),
        ("异常情况", "与已备案抖音号重复开设"),
        ("管理教师", "王晓琳 · " + WX["no"]),
        ("具体负责人", "李明 · " + LM["no"]),
        ("管理员", "暂无"),
        ("一审", "王晓琳"),
        ("二审", "周建华"),
        ("三审", "陈静"),
    ], 2)
    spec = custom_spec(
        "new", "计院学生会 · XJ20260912006", "李明",
        [("提交申请", "李明"), ("指导教师审核", "王晓琳")],
        [("提交申请", "李明", "", "提交", "", "2026-09-12 16:30"),
         ("指导教师审核", "王晓琳", "", "驳回", "与已备案账号重复，请通过认领办理。", "2026-09-13 09:10")],
        2)
    content = shell(
        page_hd("申请已驳回", "不予备案，流程终止", st("已驳回")),
        card("驳回原因", alert("与已备案账号重复开设，不予备案。如该账号确属本组织，请走认领，不要重新新建。", "danger"))
        + alert("下面是这条新建备案当时提交的内容，账号是计院学生会，不是中南计算机青年。", "info")
        + '<div class="bold mt16">填报内容</div>'
        + _new_filled(rej, REJECT_INTRO, REJECT_SCOPE, warn=True, fans="0", team="4",
                      home="https://www.douyin.com/csu_cs_su", run_kv=run)
        + _flow_block(spec, "不予备案，流程已终止"),
        bar("退回可改，驳回不可改", btn("返回我的申请", "apply.html", "default") + btn("改为认领", "apply-claim.html", "primary", "hand")))
    page("application-rejected.html", "apply", "申请已驳回", crumbs(("业务申请", "apply.html"), ("已驳回", None)), content)


# ---------------------------------------------------------------- 年审 / 整改 / 僵尸号
def annual():
    rows = [
        dict(cells=[acct(AN["name"], AN["platform"], AN["org"]), AN["platform"], st("待填报"), T["stu_end"], btn("去填报", "annual-fill.html", "primary", "edit", "sm")], cat="fill"),
        dict(cells=[acct(HO["name"], HO["platform"], HO["org"]), HO["platform"], st("待填报"), T["stu_end"], btn("去填报", "annual-fill-dance.html", "light", "edit", "sm")], cat="fill"),
        dict(cells=[acct(PH["name"], PH["platform"], "停更 " + str(PH["idle_days"]) + " 天"), PH["platform"], st("疑似僵尸号"), "先核实", btn("去核实", "zombie-verify.html", "light", "ghost", "sm")], cat="risk"),
        dict(cells=[acct(REN["name"], REN["platform"], REN["org"]), REN["platform"], st("待指导教师审核"), "09-22 已提交", btn("查看", "annual-ren.html", "text", "eye", "sm")], cat="ing"),
        dict(cells=[acct(RE["name"], RE["platform"], "管理员协助"), RE["platform"], st("待整改"), "10-20 截止", btn("去整改", "rectify-detail.html", "light", "wrench", "sm")], cat="fix"),
        dict(cells=[acct(NEW["name"], NEW["platform"], "2026-09-20 新开通"), NEW["platform"], st("备案申请中"), "不参与本年", btn("查看申请", "application-detail.html", "text", "eye", "sm")], cat="skip"),
    ]
    content = f"""{page_hd(T["name"], f"学生填报截止 {T['stu_end']} · 历史数据自动继承 · 待填报 2、待核实 1", btn("从团委开始填", "annual-fill.html", "primary", "edit"))}
<div class="grid g4 mb12">{stat("待填报", 2, "团委、街舞社", "edit", href="annual-fill.html")}
{stat("待核实", 1, "摄影协会先核实", "ghost", "orange", href="zombie-verify.html")}
{stat("审核中", 1, "学生会已提交", "clock", href="annual-ren.html")}
{stat("待整改", 1, "青协，见整改任务", "wrench", "red", href="rectify.html")}</div>
{filter_bar([field("关键词", inp("账号名称", attrs='data-search="#an-tbl"')), field("平台", sel(PLATFORM_TYPES, ph="全部"))])}
<div class="card"><div class="card-bd"><div class="toolbar">{seg([("全部", "all"), ("待填报", "fill"), ("审核中", "ing"), ("待核实", "risk"), ("整改", "fix")], target="#an-tbl")}</div>
{table(["账号", "平台", "状态", "截止 / 进度", "操作"], rows, id_="an-tbl")}{pager(6, 1)}</div></div>
<div class="mt16">{alert("计院摄影协会停更已超过预警天数，年审入口改为核实，避免在未核实的情况下直接填「正常运营」。中南计算机青年本年新建，不参加这次年审。", "info")}</div>"""
    page("annual.html", "annual", "我的年审", crumbs(("我的年审", None)), content)


def _annual_fill(file, a, last, nxt, crumb):
    content = shell(
        page_hd("年审填报", a["name"] + " · " + a["platform"]),
        card("上年度信息（自动继承）", kv([("平台 ID", a["pid"]), ("平台管理层级", a["level"]), ("所属团学组织", a["org"]), ("指导教师", a["teacher"]), ("运营负责人", "李明"), ("粉丝数", a["fans"])], 3))
        + card("本年度确认", '<div class="form-grid">' + annual_fields(last) + "</div><div class=\"mt12\">" + alert("年度异动由以上确认项自动判定。按当前选项，本账号为无异动。", "info") + "</div>", cls="mt16")
        + card("佐证材料", field("账号主页截图", upload("上传主页截图", "需包含账号名称与最近发布时间", [a["name"] + "_主页.png"]), True), cls="mt16 grow"),
        bar("提交后进入指导教师审核", btn("暂存", None, "default", "file", toast="已暂存，可稍后继续填写") + back_btn("annual.html", "返回") + submit_btn("提交年审", nxt, ic="send", toast="年审已提交")))
    page(file, "annual", "年审填报", crumbs(("我的年审", "annual.html"), (crumb, None)), content)


def annual_fill():
    _annual_fill("annual-fill.html", AN, "2026-09-17", "annual-result.html", "团委填报")


def annual_fill_dance():
    _annual_fill("annual-fill-dance.html", HO, "2026-09-12", "annual-dance-result.html", "街舞社填报")


def annual_result():
    content = shell(
        page_hd("年审已提交", FLOWS["annual"]["no"] + " · " + AN["name"]),
        card("", result("ok", "年审已提交", "等待指导教师王晓琳审核，教师审核截止 " + T["teacher_end"] + "。"))
        + card("后续节点", timeline([
            ("done", "学生确认无异动并提交", "李明 · 刚刚", "最近发布 2026-09-17"),
            ("now", "指导教师审核", "王晓琳", ""),
            ("wait", "学院统一提交", "周建华", ""),
            ("wait", "校团委审核", "陈静", ""),
        ]), cls="mt16 grow"),
        bar(FLOWS["annual"]["no"], btn("返回年审列表", "annual.html", "primary") + btn("返回首页", "home.html", "ghost")))
    page("annual-result.html", "annual", "年审提交成功", crumbs(("我的年审", "annual.html"), ("提交成功", None)), content)


def annual_dance_result():
    content = shell(
        page_hd("年审已提交", "NS2026-CS-0044 · " + HO["name"]),
        card("", result("ok", "街舞社年审已提交", "已按无异动提交，等待王晓琳审核。"))
        + card("后续节点", timeline([("done", "学生确认并提交", "李明 · 刚刚", "最近发布 2026-09-12"), ("now", "指导教师审核", "王晓琳", "")]), cls="mt16 grow"),
        bar("NS2026-CS-0044", btn("返回年审列表", "annual.html", "primary") + btn("查看账号", "account-handover.html", "default", "archive")))
    page("annual-dance-result.html", "annual", "年审提交成功", crumbs(("我的年审", "annual.html"), ("街舞社已提交", None)), content)


def annual_ren():
    content = shell(
        page_hd("年审审核中", REN["name"] + " · 微博"),
        card("提交摘要", kv([("提交时间", "2026-09-22 21:05"), ("年度异动", "无异动"), ("最近发布", "2026-09-18"), ("当前节点", "指导教师 · 王晓琳")], 2))
        + card("进度", timeline([("done", "学生确认并提交", "李明 · 2026-09-22", "名称变更另行申请，年审确认账号仍在运营"), ("now", "指导教师审核", "王晓琳", "")]), cls="mt16 grow"),
        bar("已提交，无需重复填报", btn("催办", None, "primary", "bell", toast="已向王晓琳发送年审催办") + btn("返回年审列表", "annual.html", "default")))
    page("annual-ren.html", "annual", "年审审核中", crumbs(("我的年审", "annual.html"), ("学生会年审", None)), content)


def rectify():
    f = FLOWS["rectify"]
    rows = [
        dict(cells=[f'<span class="num">{f["no"]}</span>', acct(RE["name"], RE["platform"], "何雨桐负责，李明协助"),
                    "第 2 轮", "制度文件缺少签字盖章，审核记录不完整", f["deadline"], tag("待提交", "danger"),
                    btn("去办理", "rectify-detail.html", "primary", "arrow-right", "sm")],
             href="rectify-detail.html", cat="todo"),
        dict(cells=['<span class="num">ZG20260910003</span>', acct(PH["name"], PH["platform"], PH["org"]),
                    "第 1 次", "停更 212 天，需补全学生管理员并恢复更新", "2026-10-20", st("待指导教师审核"),
                    btn("查看", "rectify-photo.html", "text", "eye", "sm")],
             href="rectify-photo.html", cat="review"),
    ]
    content = f"""{page_hd("整改任务", "本人负责或协助的整改任务。先看列表，点一行进入该账号的整改详情", btn("我的待办", "todo.html", "default", "inbox"))}
{filter_bar([
    field("关键词", inp("账号 / 整改编号", attrs='data-search="#rf-tbl"')),
    field("状态", sel(["待提交", "待指导教师审核", "整改通过"], ph="全部")),
])}
<div class="grid g4 mb12">{stat("全部任务", 2, "负责或协助", "wrench")}
{stat("待提交", 1, RE["name"] + " · 第 2 轮", "upload", "red", href="rectify-detail.html")}
{stat("审核中", 1, PH["name"] + " · 材料已交", "clock", "orange", href="rectify-photo.html")}
{stat("最近截止", "10-20", "计院青年志愿者", "calendar", href="rectify-detail.html")}</div>
<div class="card"><div class="card-bd"><div class="toolbar">{seg([("全部", "all"), ("待提交", "todo"), ("审核中", "review")], target="#rf-tbl")}</div>
{table(["整改编号", "账号", "轮次", "问题", "截止时间", "状态", "操作"], rows, id_="rf-tbl")}{pager(2, 1)}</div></div>"""
    page("rectify.html", "rectify", "整改任务", crumbs(("整改任务", None)), content)


def rectify_detail():
    f = FLOWS["rectify"]
    content = shell(
        page_hd("整改任务", RE["name"] + " · 第 2 轮", tag("待提交", "danger")),
        card("整改要求", kv([("整改编号", f["no"]), ("账号", RE["name"] + " · " + RE["platform"]), ("负责人", "何雨桐（李明以管理员协助提交）"), ("截止时间", f["deadline"]), ("问题", f["steps"][0][3], True), ("上轮意见", f["steps"][3][3], True)], 2))
        + card("已发生的轮次", timeline([
            ("done", "年审要求整改", "王晓琳 · " + f["steps"][0][0], f["steps"][0][3]),
            ("done", "学院下发", "周建华 · " + f["steps"][1][0], f["steps"][1][3]),
            ("done", "第一次提交", "何雨桐 · " + f["steps"][2][0], f["steps"][2][3]),
            ("back", "继续整改", "周建华 · " + f["steps"][3][0], f["steps"][3][3]),
            ("now", "等待第 2 轮材料", "请于 " + f["deadline"] + " 前提交签字盖章件", ""),
        ]), cls="mt16 grow"),
        bar("请在截止前提交", btn("返回列表", "rectify.html", "default") + btn("联系学院", None, "default", "phone", toast="学院团委电话 " + ZJ["phone"]) + btn("提交整改", "rectify-submit.html", "primary", "upload")))
    page("rectify-detail.html", "rectify", "整改详情", crumbs(("整改任务", "rectify.html"), (RE["name"], None)), content)


def rectify_photo():
    a = PH
    content = shell(
        page_hd("整改任务", a["name"] + " · 第 1 次", st("待指导教师审核")),
        card("整改要求", kv([
            ("整改编号", "ZG20260910003"), ("账号", a["name"] + " · " + a["platform"]), ("负责人", "李明"),
            ("截止时间", "2026-10-20"),
            ("问题", "停更 212 天；学生管理员信息缺失；未提交信息发布审查机制", True),
            ("整改要求", "恢复更新，补全管理员，并提交经指导教师签字的作品发布审核办法", True),
        ], 2))
        + card("已提交材料", kv([
            ("提交人", "李明 · 2026-09-26 18:30"),
            ("整改说明", "9 月 26 日、28 日已发布 2 条作品，并制定第四季度内容计划", True),
            ("证明材料", "近期作品截图.png、第四季度内容计划.xlsx、作品发布审核办法（签字版）.pdf", True),
        ], 2), cls="mt16")
        + card("已发生的轮次", timeline([
            ("done", "学院下发整改任务", "周建华 · 2026-09-10 10:00", "10 月 20 日前恢复更新并补全负责人信息。"),
            ("done", "学生提交整改材料", "李明 · 2026-09-26 18:30", "已恢复更新，补全管理员并制定审核办法。"),
            ("now", "指导教师审核", "王晓琳", ""),
            ("wait", "学院复核", "周建华", ""),
        ]), cls="mt16 grow"),
        bar("材料已提交，等待王晓琳审核", btn("返回列表", "rectify.html", "default") + btn("查看账号", "account-photo.html", "primary", "archive")))
    page("rectify-photo.html", "rectify", "整改详情", crumbs(("整改任务", "rectify.html"), (a["name"], None)), content)


def rectify_submit():
    content = shell(
        page_hd("提交整改材料", RE["name"] + " · 第 2 轮"),
        card("整改填报", f"""<div class="form-grid c1">
  {field("整改说明", textarea("请说明整改措施", "已补充指导教师签字及学院盖章，并附 7-9 月审核台账。", True, 400, 4), True)}
  {field("是否建立信息发布审查机制", radios("u1", ["是", "否"], "是", True), True)}
  {field("证明材料", upload("上传制度与审核记录", "pdf / jpg", ["信息发布三审制度（签字盖章）.pdf", "7-9月审核台账.xlsx"]), True)}
</div>""", cls="grow"),
        bar("提交后由学院复核，不会直接回到待提交状态", back_btn("rectify-detail.html", "取消") + submit_btn("提交整改", "rectify-done.html", ic="send", toast="已提交，等待学院审核")))
    page("rectify-submit.html", "rectify", "提交整改", crumbs(("整改任务", "rectify.html"), (RE["name"], "rectify-detail.html"), ("提交", None)), content)


def rectify_done():
    content = shell(
        page_hd("整改材料已提交", FLOWS["rectify"]["no"]),
        card("", result("ok", "第 2 轮材料已提交", "等待学院团委周建华复核。复核前任务保持「已提交」。"))
        + card("进度", timeline([
            ("back", "上轮继续整改", "周建华 · 2026-09-24", FLOWS["rectify"]["steps"][3][3]),
            ("done", "提交签字盖章材料", "李明 · 刚刚", "制度文件与 7-9 月审核台账"),
            ("now", "学院复核", "周建华", ""),
        ]), cls="mt16 grow"),
        bar(FLOWS["rectify"]["no"], btn("返回整改说明", "rectify-detail.html", "default") + btn("返回列表", "rectify.html", "ghost") + btn("返回待办", "todo.html", "primary", "inbox")))
    page("rectify-done.html", "rectify", "整改已提交", crumbs(("整改任务", "rectify.html"), ("已提交", None)), content)


def zombie_verify():
    a = PH
    choices = "".join(
        f'<div class="choice{" on" if on else ""}" data-choice="{sel}"><span class="ck"></span><div><b>{t}</b><div class="small muted">{d}</div></div></div>'
        for t, d, sel, on in [
            ("仍在正常运营", "核实为正常，学院审核后解除预警", ".zv-normal", True),
            ("需要整改", "由学院下发整改任务", ".zv-fix", False),
            ("申请注销", "转入注销流程，数据永久保留", ".zv-cancel", False),
        ])
    content = shell(
        page_hd("僵尸号核实", a["name"] + " · 停更 " + str(a["idle_days"]) + " 天"),
        alert("系统只做预警，不会直接注销。最近发布 " + a["last_post"] + "。", "warning")
        + card("账号", kv([("平台", a["platform"] + " · " + a["pid"]), ("组织", a["org"]), ("负责人", "李明"), ("停更", str(a["idle_days"]) + " 天")], 2), cls="mt16")
        + card("核实结论", '<div class="choices" data-single=".zv-tip">' + choices + '</div><div class="zv-tip zv-normal mt12">' + alert("需上传近期发布截图，并更新最近发布时间。", "success") + '</div><div class="zv-tip zv-fix mt12 hidden">' + alert("学院审核后将另行下发整改，不会直接改这个账号的年审状态。", "warning") + '</div><div class="zv-tip zv-cancel mt12 hidden">' + alert('提交核实后可继续填写注销申请。<a class="link" href="apply-cancel.html?acct=photo">去填写注销</a>', "danger") + "</div>", cls="mt16")
        + card("核实说明", f"""<div class="form-grid">
  <div class="full">{field("情况说明", textarea("请说明停更原因及后续计划", "已于 9 月恢复更新，9 月 27 日发布迎新作品，后续每月不少于 2 次。", True, 300, 3), True)}</div>
  {field(PUBLISH_TIME_LABEL, inp("", "2026-09-27", True, "date"), True, "日期选择")}
  <div class="full">{field("近期发布截图", upload("上传截图", "需包含发布日期", ["视频号主页截图_0927.jpg"]), True)}</div>
</div>""", cls="mt16 grow"),
        bar("默认按「仍在正常运营」提交", back_btn("todo.html", "稍后处理") + submit_btn("提交核实", "zombie-result.html", ic="send", toast="核实结果已提交，等待学院审核")))
    page("zombie-verify.html", "todo", "僵尸号核实", crumbs(("我的待办", "todo.html"), ("僵尸号核实", None)), content)


def zombie_result():
    content = shell(
        page_hd("核实已提交", PH["name"]),
        card("", result("ok", "已按「仍在正常运营」提交", "学院审核通过后解除预警。系统没有因此注销账号。"))
        + card("进度", timeline([
            ("done", "学生核实", "李明 · 刚刚", "最近发布更新为 2026-09-27，已附截图"),
            ("now", "学院审核", "周建华", ""),
        ]), cls="mt16")
        + f'<div class="mt16">{alert("若实际应注销或整改，可从账号档案重新进入对应办理，不必等这条核实被退回。", "info")}</div>',
        bar("等待学院审核", btn("查看账号", "account-photo.html", "primary", "archive") + btn("返回待办", "todo.html", "default", "inbox")))
    page("zombie-result.html", "todo", "核实已提交", crumbs(("我的待办", "todo.html"), ("核实结果", None)), content)


def build():
    home()
    messages()
    accounts()
    account_detail()
    account_history()
    account_annual()
    account_handover()
    account_photo()
    account_youth()
    apply_hub()
    create_basic()
    create_platform()
    duplicate()
    create_staff()
    create_reviewer()
    apply_result()
    apply_id_change()
    apply_change()
    change_confirm()
    change_result()
    apply_handover()
    handover_result()
    apply_cancel()
    cancel_result()
    apply_claim()
    claim_result()
    application_detail()
    application_change()
    application_returned()
    application_edit()
    application_approved()
    application_handover()
    application_rejected()
    annual()
    annual_fill()
    annual_fill_dance()
    annual_result()
    annual_dance_result()
    annual_ren()
    rectify()
    rectify_detail()
    rectify_photo()
    rectify_submit()
    rectify_done()
    zombie_verify()
    zombie_result()
