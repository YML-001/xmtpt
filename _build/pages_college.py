"""PC 端 · 学院管理员（计算机学院团委）页面。

演示视角：学院管理员 周建华（计算机学院团委书记）。
数据范围：计算机学院及所属 / 直属 / 指导组织；负责学院层面审核、统筹教师审核结果并统一提交校团委。
"""
from datetime import date
from urllib.parse import quote

from base import *  # noqa: F401,F403
from data import (ACCOUNTS, FLOWS, PEOPLE, COLLEGE_STATS as CS, ANNUAL_TASK as T, PLATFORM_TYPES, LEVELS,
                  RUN_STATUS, ANNUAL_STATUS, UPDATE_FREQ)

D = "pc/college/"
HOME = ("学院工作台", "workbench.html")
TODAY = date(2026, 9, 30)

# ---------------------------------------------------------------- 本模块样式
CSS = """
.ap-tbl td:nth-child(6),.ap-tbl td:last-child{white-space:nowrap}
.ap-tbl td:nth-child(5){min-width:200px}
/* 工作台欢迎区 */
.wb-hero{position:relative;overflow:hidden;display:flex;align-items:center;gap:18px;padding:22px 26px;border-radius:12px;margin-bottom:16px;color:#fff;background:linear-gradient(115deg,#0A416F 0%,#0E5E9E 45%,#2A8DC7 100%)}
.wb-hero::after{content:"";position:absolute;right:-70px;top:-90px;width:280px;height:280px;border-radius:50%;background:rgba(255,255,255,.07)}
.wb-hero::before{content:"";position:absolute;right:160px;bottom:-130px;width:220px;height:220px;border-radius:50%;background:rgba(255,255,255,.05)}
.wb-hero h1{font-size:20px;font-weight:700}
.wb-hero .avatar{border:2px solid rgba(255,255,255,.6)}
.hero-meta{font-size:13px;opacity:.85;margin-top:2px}
.hero-pill{display:inline-flex;align-items:center;gap:6px;height:24px;padding:0 10px;border-radius:12px;background:rgba(255,255,255,.14);font-size:12px}
.hero-btn{position:relative;z-index:1;display:inline-flex;align-items:center;gap:6px;height:34px;padding:0 14px;border-radius:8px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.28);color:#fff;font-size:13px;white-space:nowrap}
.hero-btn:hover{background:rgba(255,255,255,.24)}
.hero-btn.solid{background:#fff;color:var(--c-primary-dark);border-color:#fff;font-weight:600}
/* 年审节点 */
.nodes{display:flex;align-items:stretch;gap:6px}
.node{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px;padding:12px 14px;border-radius:8px;border:1px solid var(--c-line);background:#FAFCFE;transition:border-color .15s,box-shadow .15s}
.node:hover{border-color:var(--c-primary-border);box-shadow:var(--shadow-md)}
.node b{font-size:24px;line-height:1.2;font-variant-numeric:tabular-nums}
.node.primary b{color:var(--c-primary)}.node.warning b{color:var(--c-warning)}.node.danger b{color:var(--c-danger)}.node.success b{color:var(--c-success)}
.node.success{background:var(--c-success-bg);border-color:var(--c-success-bd)}
.node-arrow{display:flex;align-items:center;color:var(--c-border)}
.countdown{border-radius:10px;padding:16px 18px;background:linear-gradient(160deg,#FFF5E5,#FFFBF4);border:1px solid var(--c-warning-bd);height:100%}
.countdown .big{font-size:34px;font-weight:700;color:var(--c-warning);line-height:1.1;font-variant-numeric:tabular-nums}
.dl{display:flex;justify-content:space-between;font-size:12px;color:var(--c-text-2);padding:5px 0;border-bottom:1px dashed var(--c-warning-bd)}
.dl:last-child{border-bottom:none}.dl.cur{color:var(--c-warning);font-weight:600}
/* 待办与消息 */
.todo-row{display:flex;align-items:center;gap:12px;padding:11px 0;border-bottom:1px solid var(--c-line)}
.todo-row:last-child{border-bottom:none}.todo-row:hover .bold{color:var(--c-primary)}
.ic-box{width:34px;height:34px;border-radius:9px;display:grid;place-items:center;flex:none;background:var(--c-primary-light);color:var(--c-primary)}
.ic-box.orange{background:var(--c-warning-bg);color:var(--c-warning)}.ic-box.red{background:var(--c-danger-bg);color:var(--c-danger)}
.ic-box.green{background:var(--c-success-bg);color:var(--c-success)}.ic-box.gray{background:var(--c-muted-bg);color:var(--c-muted)}
.msg{display:flex;align-items:center;gap:14px;padding:14px 20px;border-bottom:1px solid var(--c-line);transition:background .15s}
.msg:hover{background:#F7FBFE}.msg:last-child{border-bottom:none}
.msg .dot{width:7px;height:7px;border-radius:50%;background:var(--c-danger);flex:none}
.msg.read .dot{background:transparent}
/* 演示下一步 */
.scene-next{display:inline-flex;align-items:center;gap:6px;height:32px;padding:0 14px;border-radius:16px;background:#F0EDFB;color:#6B5BD2;border:1px dashed #C9C0F0;font-size:13px;font-weight:500;white-space:nowrap}
.scene-next:hover{background:#E6E1FA}
/* 批量操作条 */
.batchbar{display:flex;align-items:center;gap:10px;padding:8px 14px;margin-bottom:12px;border-radius:8px;background:#F3F9FD;border:1px solid var(--c-primary-border);font-size:13px;color:var(--c-text-2)}
.batchbar b{color:var(--c-primary)}
/* 审核意见高亮 */
.opinion{border:1px solid var(--c-success-bd);background:linear-gradient(180deg,#F3FDF8,#fff);border-radius:var(--radius);padding:16px 18px 16px 22px;position:relative}
.opinion::before{content:"";position:absolute;left:0;top:14px;bottom:14px;width:3px;border-radius:2px;background:var(--c-success)}
.opinion.warn{border-color:var(--c-warning-bd);background:linear-gradient(180deg,#FFF9EF,#fff)}.opinion.warn::before{background:var(--c-warning)}
.opinion.info{border-color:var(--c-primary-border);background:linear-gradient(180deg,#F3F9FD,#fff)}.opinion.info::before{background:var(--c-primary)}
.quote{font-size:15px;color:var(--c-text);margin-top:8px;line-height:1.7}
/* 人员 */
.ini{width:32px;height:32px;border-radius:50%;display:grid;place-items:center;flex:none;background:var(--c-primary-light);color:var(--c-primary);font-weight:600;font-size:13px}
.ini.sm{width:24px;height:24px;font-size:11px}.ini.lg{width:56px;height:56px;font-size:20px}
.person{display:inline-flex;align-items:center;gap:8px;white-space:nowrap}
.t-card{display:flex;align-items:center;gap:12px;padding:12px 14px;border:1px solid var(--c-line);border-radius:8px;background:#fff;transition:border-color .15s,box-shadow .15s}
.t-card:hover{border-color:var(--c-primary-border);box-shadow:var(--shadow-md)}
.t-card.warn{background:var(--c-danger-bg);border-color:var(--c-danger-bd)}
.id-card{padding:14px 16px;border-radius:8px;border:1px solid var(--c-primary-border);background:#F7FBFE}
/* 清单与承诺 */
.check-item{display:flex;align-items:center;gap:12px;padding:14px 16px;border:1px solid var(--c-line);border-radius:8px;background:#fff}
.ok-ic{width:30px;height:30px;border-radius:50%;display:grid;place-items:center;flex:none;background:var(--c-success-bg);color:var(--c-success)}
.commit{display:flex;align-items:flex-start;gap:10px;padding:14px 16px;border-radius:8px;background:#F7F9FB;border:1px solid var(--c-line);cursor:pointer;font-size:13px;color:var(--c-text-2);line-height:1.7}
.commit input{accent-color:var(--c-primary);width:16px;height:16px;margin-top:3px;flex:none}
.commit.invalid{border-color:var(--c-danger);background:var(--c-danger-bg);color:#B3161C}
.mini-stat{padding:14px 16px;border-radius:8px;background:#F7F9FB;border:1px solid var(--c-line)}
.mini-stat b{display:block;font-size:22px;font-variant-numeric:tabular-nums;line-height:1.3}
/* 组织树 */
.org-name{display:flex;align-items:center;gap:8px}
.org-d1{padding-left:18px}
.org-d1::before{content:"";width:10px;height:10px;border-left:1.5px solid var(--c-border);border-bottom:1.5px solid var(--c-border);margin-top:-8px;flex:none}
tr.warn-row td{background:#FFF8EC}
/* 分配规则 */
.rule-row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.3fr) 20px minmax(0,1fr) 32px;gap:10px;align-items:center;padding:10px 12px;border:1px solid var(--c-line);border-radius:8px;background:#FAFCFE}
.shot{border-radius:10px;overflow:hidden;border:1px solid var(--c-line);background:#F7F9FB}
.shot img{width:100%;height:240px;object-fit:cover}
button.choice{width:100%;text-align:left}
.stat-value.c-primary{color:var(--c-primary)}.stat-value.c-warning{color:var(--c-warning)}
.stat-value.c-danger{color:var(--c-danger)}.stat-value.c-success{color:var(--c-success)}
.ledger{display:flex;flex-direction:column;gap:10px;padding:18px 20px}
.ledger .ic-box{width:40px;height:40px;border-radius:10px}
.tbl-sm .table td{padding:9px 12px}
.cb{display:inline-flex;align-items:center;gap:8px;font-size:13px;cursor:pointer;color:var(--c-text)}
.cb input{accent-color:var(--c-primary);width:15px;height:15px;cursor:pointer}
"""

# 提交承诺必须勾选：捕获阶段拦截 data-submit
COMMIT_JS = r"""
document.addEventListener('click',function(e){var b=e.target.closest('[data-submit]');if(!b)return;var c=document.getElementById('commit-ck');
if(c&&!c.checked){e.stopImmediatePropagation();e.preventDefault();c.closest('.commit').classList.add('invalid');window.toast('请先阅读并勾选提交承诺');}},true);
document.addEventListener('change',function(e){if(e.target.id==='commit-ck'){e.target.closest('.commit').classList.toggle('invalid',!e.target.checked);}});
"""

# ---------------------------------------------------------------- 本院固定数据
# 6 名业务教师；nodes 为其负责账号的年审节点分布：待填报、待教师审核、待学院审核、整改中、已完成
TEACHERS = [
    dict(name="王晓琳", job="宣传工作辅导员 / 2021级辅导员 / 街舞社指导教师", scope="学院团委直属组织、2021级团支部、计院街舞社等",
         total=11, nodes=[4, 2, 2, 1, 2], zombie=3, rectify=1),
    dict(name="刘洋", job="2023级辅导员", scope="2023级各班团支部", total=6, nodes=[0, 0, 0, 1, 5], zombie=0, rectify=1),
    dict(name="陈思远", job="2024级辅导员", scope="2024级各班团支部", total=5, nodes=[0, 1, 1, 0, 3], zombie=0, rectify=0),
    dict(name="赵敏", job="志愿服务负责老师", scope="青年志愿者服务队、支教队", total=4, nodes=[0, 0, 0, 0, 4], zombie=0, rectify=0),
    dict(name="孙浩", job="社团工作辅导员", scope="计院学生社团（街舞社等单独指定的除外）", total=5, nodes=[0, 1, 1, 0, 3], zombie=0, rectify=0),
    dict(name="林雪", job="2025级辅导员", scope="2025级各班团支部", total=3, nodes=[0, 0, 0, 0, 3], zombie=0, rectify=0),
]
UNASSIGNED_NODES = [1, 0, 0, 0, 1]
TEACHER_NAMES = [t["name"] for t in TEACHERS]

# 年审节点（合计 36，与 COLLEGE_STATS 已完成 21 / 待完成 15 一致）
NODES = [("待填报", 5, "primary", "annual-progress.html", "学生尚未提交"),
         ("待教师审核", 4, "warning", "annual-progress.html", "3 名教师处理中"),
         ("待学院审核", 4, "warning", "annual-review.html", "需本人处理"),
         ("整改中", 2, "danger", "rectify.html", "含复核中 1 个"),
         ("已完成", 21, "success", "annual-review.html", "学院已确认")]

# 按组织统计年审节点：组织, 账号数, [待填报, 待教师审核, 待学院审核, 整改中, 已完成]
ORG_PROGRESS = [
    ("学院团委及直属组织", 5, [1, 0, 2, 0, 2]),
    ("青年志愿者协会及服务队", 5, [0, 0, 0, 1, 4]),
    ("学生社团", 9, [3, 1, 1, 0, 4]),
    ("2021级团支部", 2, [0, 2, 0, 0, 0]),
    ("2023级团支部", 6, [0, 0, 0, 1, 5]),
    ("2024级团支部", 5, [0, 1, 1, 0, 3]),
    ("2025级团支部", 4, [1, 0, 0, 0, 3]),
]

# 本院账号清单：剧本账号 + 其他本院账号
EXTRA_ACCTS = [
    dict(name="计算机学院研究生会", platform="微信公众号", pid="csu_cs_gsu", org="计算机学院研究生会", level="二级平台",
         teacher="王晓琳", student="陈卓", run="正常运行", filing="已备案", annual="待学校审核"),
    dict(name="2021级计算机科学3班团支部", platform="QQ", pid="1136620871", org="2021级计算机科学3班团支部", level="三级平台",
         teacher="王晓琳", student="—（已毕业）", run="不活跃", filing="已备案", annual="待指导教师审核"),
    dict(name="2023级网络工程1班团支部", platform="QQ", pid="2330915647", org="2023级网络工程1班团支部", level="三级平台",
         teacher="刘洋", student="周可欣", run="整改中", filing="已备案", annual="待整改"),
    dict(name="2024级计算机科学1班团支部", platform="微信公众号", pid="csu_cs2401", org="2024级计算机科学1班团支部", level="三级平台",
         teacher="陈思远", student="吴嘉怡", run="正常运行", filing="已备案", annual="待学院审核"),
    dict(name="2025级软件工程2班团支部", platform="QQ", pid="3350228716", org="2025级软件工程2班团支部", level="三级平台",
         teacher="未分配", student="王一鸣", run="正常运行", filing="已备案", annual="待填报"),
    dict(name="计院人工智能协会", platform="哔哩哔哩", pid="1685520394", org="计院人工智能协会", level="社团平台",
         teacher="未分配", student="张子涵", run="正常运行", filing="已备案", annual="待学校审核"),
    dict(name="计院篮球协会", platform="抖音", pid="csu_cs_basketball", org="计院篮球协会", level="社团平台",
         teacher="孙浩", student="刘子豪", run="正常运行", filing="已备案", annual="待学院审核"),
]
SCENE_KEYS = ["annual", "new", "rename", "idchange", "rectify", "handover", "proxy", "photo", "zombie"]
ZOMBIE_NAMES = {ACCOUNTS["zombie"]["name"], ACCOUNTS["photo"]["name"], "2021级计算机科学3班团支部"}
LEVEL_CAT = {"二级平台": "l2", "三级平台": "l3", "社团平台": "club"}
PLATFORM_DIST = [("微信公众号", 15), ("QQ", 8), ("抖音", 4), ("微博", 3), ("哔哩哔哩", 3), ("小红书", 2), ("视频号", 1)]


def college_accounts():
    rows = []
    for k in SCENE_KEYS:
        a = ACCOUNTS[k]
        rows.append(dict(name=a["name"], platform=a["platform"], pid=a["pid"], org=a["org"], level=a["level"],
                         teacher=a["teacher"], student=a["student"], run=a["run"], filing=a["filing"], annual=a["annual"]))
    return rows + EXTRA_ACCTS


# ---------------------------------------------------------------- 本模块小组件
def cr(*items):
    return [HOME] + list(items)


def page(file, key, title, crumbs, content, js=""):
    pc_page(D + file, "college", key, title, crumbs, content, css=CSS, js=js)


def go(text, href, kind="primary", ic=None, toast=None, size=""):
    """跳转按钮：可先给出 toast 再跳转（<a> 带 data-toast 会被拦截，故用 button + data-href）。"""
    cls = "btn btn-" + kind + (" btn-" + size if size else "")
    t = ' data-toast="%s"' % esc(toast) if toast else ""
    i = icon(ic) if ic else ""
    return f'<button class="{cls}" type="button" data-href="{href}"{t}>{i}{text}</button>'


def scene_next(text, href):
    return f'<a class="scene-next" href="{href}">{icon("route", 14)}演示下一步：{text}{icon("arrow-right", 14)}</a>'


def st2(x):
    return st(x) if x and x != "—" else '<span class="muted">—</span>'


def person(name, size="sm", sub=""):
    if name in AVATARS:
        av = avatar(name, size)
    else:
        av = f'<span class="ini {size}">{name[0]}</span>'
    s = f'<span class="small muted">{sub}</span>' if sub else ""
    return f'<span class="person">{av}<span>{name}</span>{s}</span>'


def teacher_cell(name):
    return tag("未分配", "danger") if name == "未分配" else person(name)


def teacher_href(name):
    if name == "王晓琳":
        return "teacher-detail.html"
    return "teacher-detail.html?t=" + quote(name)


def annual_open(name, cs):
    """年审列表进入能办完的页面：整改、注销、名称变更不落到同一个无异动审核页。"""
    if name == ACCOUNTS["zombie"]["name"]:
        return "zombie-verify-detail.html"
    if name == ACCOUNTS["rectify"]["name"]:
        return "rectify-detail.html"
    if name == ACCOUNTS["rename"]["name"]:
        return "approval-change.html"
    if cs == "待整改":
        return "rectify.html"
    return "annual-review-detail.html"


def ic_box(ic, color=""):
    return f'<span class="ic-box {color}">{icon(ic)}</span>'


def flow_items(key, n):
    """取剧本时间线前 n 步（原文照录），退回类节点标为 back。"""
    out = []
    for when, who, title, cmt in FLOWS[key]["steps"][:n]:
        state = "back" if ("退回" in title or "继续整改" in title) else "done"
        out.append((state, title, when + " · " + who, cmt))
    return out


def pct_cell(done, total):
    p = round(done / total * 100) if total else 0
    color = "green" if p >= 80 else ("orange" if p < 50 else "")
    return f'<div class="flex gap8" style="min-width:130px">{progress(p, color)}<span class="num small">{p}%</span></div>'


def annual_tabs(active):
    return ptabs([("年审进度", "annual-progress.html"), ("学院审核", "annual-review.html"), ("提交校团委", "annual-submit.html")], active)


def acct_head(a, extra_tags="", meta=""):
    """详情页顶部账号概要。"""
    m = meta or f'{a["platform"]} · 平台ID {a["pid"]} · {a["org"]}'
    return (f'<div class="flex gap16">{pf(a["platform"], "lg")}<div class="grow"><div class="flex gap8 wrap">'
            f'<span class="fs18 bold">{a["name"]}</span>{extra_tags}</div><div class="small muted mt4">{m}</div></div></div>')


# ---------------------------------------------------------------- 1 学院工作台
def workbench():
    days_left = (date(2026, 11, 5) - TODAY).days
    hero = f"""<div class="wb-hero">
  {avatar('周建华', 'lg')}
  <div class="grow" style="position:relative;z-index:1">
    <h1>下午好，周建华老师</h1>
    <div class="hero-meta">计算机学院团委书记 · 学院管理员 ｜ 数据范围：计算机学院及所属、直属、指导组织（{CS['total']} 个账号 · 28 个组织 · {CS['teachers']} 名业务教师）</div>
    <div class="flex gap8 mt8 wrap"><span class="hero-pill">{icon('calendar', 14)}{T['name']}进行中</span>
    <span class="hero-pill">{icon('inbox', 14)}今日待办 5 项</span><span class="hero-pill">{icon('clock', 14)}距学院提交截止 {days_left} 天</span></div>
  </div>
  <a class="hero-btn" href="approvals.html">{icon('file-check', 14)}学院审核</a>
  <a class="hero-btn" href="rectify-create.html">{icon('wrench', 14)}下发整改</a>
  <a class="hero-btn solid" href="annual-progress.html">{icon('calendar', 14)}年审统筹</a>
</div>"""
    kpis = "".join([
        stat("本院账号", CS["total"], "三级平台 17 个", "database", href="accounts.html"),
        stat("已完成年审", CS["done"], "完成率 %.1f%%" % (CS["done"] / CS["total"] * 100), "check-circle", "green", href="annual-progress.html"),
        stat("待完成年审", CS["todo"], f"距截止 {days_left} 天", "calendar", "orange", href="annual-progress.html"),
        stat("疑似僵尸号", CS["zombie"], "1 个待学院审核", "ghost", "red", href="zombie.html"),
        stat("待整改", CS["rectify"], "1 个待审核", "wrench", "orange", href="rectify.html"),
        stat("待学院审核", 4, "4 类业务待办", "file-check", href="approvals.html"),
    ])
    parts = []
    for i, (label, v, kind, href, hint) in enumerate(NODES):
        if i:
            parts.append(f'<span class="node-arrow">{icon("chevron-right")}</span>')
        parts.append(f'<a class="node {kind}" href="{href}"><span class="small sub">{label}</span><b>{v}</b><span class="small muted">{hint}</span></a>')
    nodes = f'<div class="nodes">{"".join(parts)}</div>'
    dls = "".join(
        f'<div class="dl{" cur" if cur else ""}"><span>{k}</span><span class="num">{v}</span></div>'
        for k, v, cur in [("学生填报截止", T["stu_end"], False), ("教师审核截止", T["teacher_end"], False),
                          ("学院提交截止", T["college_end"], True), ("学校审核截止", T["school_end"], False)])
    countdown = (f'<div class="countdown"><div class="small" style="color:#A86400">距学院提交截止</div>'
                 f'<div class="flex gap8 mt4" style="align-items:baseline"><span class="big">{days_left}</span><span class="c-warning bold">天</span></div>'
                 f'<div class="small muted mb8">截止日期 {T["college_end"]}</div>{dls}</div>')
    done_pct = CS["done"] / CS["total"] * 100
    annual_body = f"""{nodes}
<div class="grid mt16" style="grid-template-columns:minmax(0,1fr) 220px">
  <div>
    <div class="flex gap12"><span class="small sub nowrap">整体完成率</span>{progress(done_pct, 'green')}<span class="bold num">{done_pct:.1f}%</span><span class="small muted nowrap">{CS['done']} / {CS['total']}</span></div>
    <div class="mt16">{alert('全部 36 个账号完成教师审核与学院审核后，才能统一提交校团委。当前仍有 <b>5</b> 个账号学生未填报，建议优先催办。', 'warning')}</div>
    <div class="flex gap8 mt16">{btn('查看本院年审进度', 'annual-progress.html', 'default', 'chart', 'sm')}{btn('学院审核（4）', 'annual-review.html', 'light', 'file-check', 'sm')}{btn('一键催办未填报', None, 'default', 'bell', 'sm', toast='已向 5 个待填报账号的学生负责人发送催办提醒')}</div>
  </div>
  {countdown}
</div>"""
    todos = [
        ("新建备案 · 中南计算机青年", "指导教师王晓琳已通过 · 2026-09-27 11:20", "file-add", "", "approval-detail.html", "新建"),
        ("名称变更 · 计算机学院学生会", "拟改名“中南计院学生会” · 教师已通过", "file-edit", "orange", "approval-change.html", "变更"),
        ("僵尸号审核 · 2021级软件工程1班团支部", "辅导员核实建议注销 · 停更 412 天", "ghost", "red", "zombie-verify-detail.html", "僵尸号"),
        ("整改审核 · 计院青年志愿者", "第 1 轮整改材料 · 何雨桐 2026-09-23 提交", "wrench", "orange", "rectify-detail.html", "整改"),
        ("代办交接 · 计院ACM协会", "教师代办 · 赵磊（已毕业）→ 孙悦", "hand", "", "approval-proxy.html", "交接"),
    ]
    todo_html = "".join(
        f'<a class="todo-row" href="{h}">{ic_box(ic, c)}<div class="grow"><div class="bold fs13 ellipsis">{t}</div>'
        f'<div class="small muted ellipsis">{m}</div></div>{tag(k, "primary")}{icon("chevron-right")}</a>'
        for t, m, ic, c, h, k in todos)
    trows = []
    for t in TEACHERS:
        href = teacher_href(t["name"])
        trows.append(dict(cells=[person(t["name"]), f'<span class="num">{t["total"]}</span>',
                                 f'<span class="num {"c-warning bold" if t["nodes"][1] else "muted"}">{t["nodes"][1]}</span>',
                                 pct_cell(t["nodes"][4], t["total"])], href=href))
    teacher_tbl = table(["教师", "负责账号", "待审核", "年审完成率"], trows, cls="tbl-sm")
    content = f"""{hero}
<div class="grid g6">{kpis}</div>
<div class="grid mt16" style="grid-template-columns:minmax(0,1.7fr) minmax(0,1fr)">
  {card('本院年审进度 · 按节点', annual_body, btn('提交校团委', 'annual-submit.html', 'primary', 'send', 'sm'))}
  {card('我的待办', todo_html, btn('消息待办', 'messages.html', 'text', size='sm'))}
</div>
<div class="grid mt16" style="grid-template-columns:minmax(0,1.7fr) minmax(0,1fr)">
  {card('教师工作量', teacher_tbl, btn('全部教师', 'teachers.html', 'text', size='sm') + btn('任务分派', 'assign.html', 'light', 'route', 'sm'))}
  {card('本院平台类型分布', hbars(PLATFORM_DIST) + '<div class="small muted mt8">微信公众号与 QQ 占比 63.9%，班级团支部以 QQ 为主</div>', btn('本院账号', 'accounts.html', 'text', size='sm'))}
</div>"""
    page("workbench.html", "workbench", "学院工作台", [("学院工作台", None)], content)


# ---------------------------------------------------------------- 2 消息待办
def messages():
    items = [
        ("todo unread", "file-add", "", "【待审核】新建备案 · 中南计算机青年", "指导教师王晓琳已审核通过，请进行学院审核", "2026-09-27 11:20", "approval-detail.html"),
        ("todo unread", "file-edit", "orange", "【待审核】名称变更 · 计算机学院学生会", "拟变更为“中南计院学生会”，属重要变更，学院审核后报校团委", "2026-09-27 09:15", "approval-change.html"),
        ("todo unread", "hand", "", "【待审核】教师代办交接 · 计院ACM协会", "王晓琳代办负责人交接：赵磊（已毕业）→ 孙悦", "2026-09-30 09:20", "approval-proxy.html"),
        ("todo unread", "ghost", "red", "【待审核】僵尸号核实结果 · 2021级软件工程1班团支部", "辅导员王晓琳核实：团支部已毕业，建议注销", "2026-09-22 15:30", "zombie-verify-detail.html"),
        ("todo unread", "wrench", "orange", "【待审核】整改材料 · 计院青年志愿者", "何雨桐提交第 1 轮整改材料，请判定整改结果", "2026-09-23 22:10", "rectify-detail.html"),
        ("todo", "calendar", "green", "【待确认】年审学院审核 · 4 个账号", "教师审核已完成，待学院确认后纳入提交清单", "2026-09-29 09:00", "annual-review.html"),
        ("todo", "upload", "", "【待确认】校团委导入历史数据 · 13 条待处理", "请补全负责教师、学生负责人等缺失信息并确认", "2026-09-16 10:00", "import-confirm.html"),
        ("urge unread", "bell", "orange", "【催办】校团委：计算机学院年审完成率低于全校平均", "当前完成率 58.3%，请督促 5 个待填报账号尽快提交", "2026-09-28 15:00", "annual-progress.html"),
        ("notice", "radar", "red", "【预警】本院新增疑似僵尸号 3 个", "系统按“停更 ≥ 180 天”“团支部已毕业”等规则自动预警", "2026-09-01 02:00", "zombie.html"),
        ("notice", "check-circle", "green", "【结果】负责人交接已生效 · 计院街舞社", "李明 → 李四，生效时间 2026-10-01，历任记录已保留", "2026-09-28 10:05", "../common/archive-staff.html"),
        ("notice", "calendar", "", "【通知】2026年度团学组织新媒体平台年审已启动", "学生填报截止 2026-10-15，学院提交截止 2026-11-05", "2026-09-15 09:00", "annual-progress.html"),
    ]
    rows = []
    for cat, ic, c, t, d, when, h in items:
        unread = "unread" in cat
        cls = "msg" if unread else "msg read"
        weight = "bold" if unread else ""
        rows.append(f'<a class="{cls}" href="{h}" data-cat="{cat}"><span class="dot"></span>{ic_box(ic, c)}'
                    f'<div class="grow"><div class="fs13 {weight}">{t}</div><div class="small muted mt4">{d}</div></div>'
                    f'<span class="small muted nowrap">{when}</span>{icon("chevron-right")}</a>')
    n_todo = sum(1 for x in items if "todo" in x[0])
    n_notice = sum(1 for x in items if "notice" in x[0])
    n_urge = sum(1 for x in items if "urge" in x[0])
    n_unread = sum(1 for x in items if "unread" in x[0])
    tabs = seg([(f"全部 {len(items)}", "all"), (f"待办 {n_todo}", "todo"), (f"通知 {n_notice}", "notice"),
                (f"催办 {n_urge}", "urge"), (f"未读 {n_unread}", "unread")], target="#msg-list")
    content = f"""{page_hd('消息待办', '学院层面的待审核、待确认事项与系统通知，点击直接进入办理页面',
                   btn('全部已读', None, 'default', 'check', toast=f'已将 {n_unread} 条未读消息标记为已读') + btn('去学院审核', 'approvals.html', 'primary', 'file-check'))}
<div class="grid g4 mb16">
  {stat('待我办理', n_todo, '审核 5 · 确认 2', 'inbox', href='approvals.html')}
  {stat('未读消息', n_unread, '最近 7 天', 'bell', 'red')}
  {stat('校团委催办', n_urge, '年审进度', 'flag', 'orange', href='annual-progress.html')}
  {stat('系统通知', n_notice, '预警 / 结果 / 任务', 'info', 'gray')}
</div>
{card('消息列表', f'<div id="msg-list">{"".join(rows)}</div>', tabs, bd_cls='')}
{pager(len(items), 1)}"""
    page("messages.html", "messages", "消息待办", cr(("消息待办", None)), content)


# ---------------------------------------------------------------- 3 本院账号
def accounts():
    rows = []
    for a in college_accounts():
        cats = [LEVEL_CAT.get(a["level"], "l2")]
        if a["name"] in ZOMBIE_NAMES:
            cats.append("zombie")
        if a["teacher"] == "未分配":
            cats.append("unassigned")
        name_extra = " " + tag("疑似僵尸号", "danger") if a["name"] in ZOMBIE_NAMES else ""
        rows.append(dict(cells=[
            acct(a["name"], a["platform"], f'{a["platform"]} · {a["pid"]}'),
            f'<div class="fs13">{a["org"]}</div><div class="small muted">{a["level"]}{name_extra}</div>',
            teacher_cell(a["teacher"]), a["student"], st2(a["run"]), st2(a["filing"]), st2(a["annual"]),
            ops(("档案", "../common/archive-basic.html"), ("分配教师", "assign.html")),
        ], href="../common/archive-basic.html", cat=" ".join(cats)))
    all_rows = college_accounts()
    n_zombie = sum(1 for a in all_rows if a["name"] in ZOMBIE_NAMES)
    n_un = sum(1 for a in all_rows if a["teacher"] == "未分配")
    quick = chips([(f"全部 {len(all_rows)}", "all"), ("二级平台", "l2"), ("三级平台", "l3"), ("社团平台", "club"),
                   (f"疑似僵尸号 {n_zombie}", "zombie"), (f"未分配教师 {n_un}", "unassigned")], target="#acct-table")
    filters = filter_bar([
        field("账号名称 / 平台ID", inp("请输入关键字")),
        field("平台类型", sel(PLATFORM_TYPES)),
        field("平台层级", sel(LEVELS)),
        field("所属组织", sel(["计算机学院团委", "计算机学院学生会", "计算机学院研究生会", "计算机学院青年志愿者协会", "学生社团", "班级团支部"])),
        field("负责教师", sel(TEACHER_NAMES + ["未分配"])),
        field("运行状态", sel(RUN_STATUS)),
        field("年审状态", sel(ANNUAL_STATUS)),
    ])
    content = f"""{page_hd('本院账号', f'计算机学院及所属、直属、指导组织全部新媒体账号，共 {CS["total"]} 个；一账号一档案',
                   btn('导入确认', 'import-confirm.html', 'default', 'upload') + btn('导出', 'export.html', 'default', 'download') + btn('新建账号', '../common/apply-create-basic.html', 'primary', 'plus'))}
{filters}
<div class="card card-bd">
  <div class="toolbar">{quick}<span class="small muted">数据范围：本学院 · 更新于 2026-09-30 09:00</span></div>
  <div class="batchbar">{icon('check-circle')}已选 <b data-checked-count="#acct-table">0</b> 个账号
    <span class="ml-auto flex gap8">{btn('批量分配教师', 'assign-batch.html', 'light', 'route', 'sm')}{btn('导出所选', 'export.html', 'default', 'download', 'sm')}</span></div>
  {table(['账号', '所属组织 / 层级', '负责教师', '学生负责人', '运行状态', '备案状态', '年审状态', '操作'], rows, check=True, id_='acct-table')}
  {pager(CS['total'], 3)}
</div>"""
    page("accounts.html", "accounts", "本院账号", cr(("账号管理", None), ("本院账号", None)), content)


# ---------------------------------------------------------------- 4 本院组织
ORG_JS = """
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-oname]');if(!b)return;
  window._orgRow=b.closest('tr');
  document.getElementById('f-name').value=b.getAttribute('data-oname');
  document.getElementById('f-type').value=b.getAttribute('data-otype');
  document.getElementById('f-parent').value=b.getAttribute('data-oparent');
  document.getElementById('f-status').value=b.getAttribute('data-ostatus');
  document.getElementById('f-teacher').value=b.getAttribute('data-oteacher');
});
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-graduate]');if(!b)return;
  var tr=b.closest('tr');var st=tr&&tr.querySelector('[data-status]');
  if(st)st.innerHTML='<span class="tag tag-muted tag-dot">已毕业</span>';
});
function saveOrg(){
  var tr=window._orgRow;if(!tr)return;
  var name=document.getElementById('f-name').value.trim();
  if(!name){toast('请填写组织名称');return;}
  var nm=tr.querySelector('.bold');if(nm)nm.textContent=name;
  var tds=tr.children;
  tds[1].textContent=document.getElementById('f-type').value;
  tds[2].innerHTML='<span class="sub">'+document.getElementById('f-parent').value+'</span>';
  var status=document.getElementById('f-status').value;
  var kind=status==='已毕业'?'tag-muted':'tag-success';
  tds[3].innerHTML='<span data-status><span class="tag '+kind+' tag-dot">'+status+'</span></span>';
  tds[4].textContent=document.getElementById('f-teacher').value;
  var btn=tr.querySelector('[data-oname]');
  if(btn){btn.setAttribute('data-oname',name);btn.setAttribute('data-otype',document.getElementById('f-type').value);
    btn.setAttribute('data-oparent',document.getElementById('f-parent').value);btn.setAttribute('data-ostatus',status);
    btn.setAttribute('data-oteacher',document.getElementById('f-teacher').value);}
  document.getElementById('org-edit').classList.add('hidden');
  toast('组织信息已保存');
}
function addOrg(){
  var name=document.getElementById('n-name').value.trim();
  if(!name){toast('请填写组织名称');return;}
  var tb=document.querySelector('#org-table tbody');
  var typ=document.getElementById('n-type').value,parent=document.getElementById('n-parent').value;
  var status=document.getElementById('n-status').value,teacher=document.getElementById('n-teacher').value.trim()||'未配置';
  var tr=document.createElement('tr');
  tr.innerHTML='<td><div class="org-name org-d1"><span class="bold fs13">'+name+'</span></div></td><td>'+typ+'</td><td><span class="sub">'+parent+'</span></td><td><span data-status><span class="tag tag-success tag-dot">'+status+'</span></span></td><td>'+teacher+'</td><td><span class="num bold">0</span></td><td><div class="ops"><button class="link" type="button" data-toggle="#org-edit" data-oname="'+name+'" data-otype="'+typ+'" data-oparent="'+parent+'" data-ostatus="'+status+'" data-oteacher="'+teacher+'">编辑</button><a class="link" href="accounts.html">查看账号</a></div></td>';
  tb.insertBefore(tr,tb.firstChild);
  document.getElementById('org-new').classList.add('hidden');
  document.getElementById('n-name').value='';
  toast('已新增组织：'+name);
}
function loadImportSample(){
  document.getElementById('import-preview').classList.remove('hidden');
  toast('已载入模板中的 2 条组织');
}
function confirmImport(){
  var box=document.getElementById('import-preview');
  if(box.classList.contains('hidden')){toast('请先选择文件或载入模板示例');return;}
  var tb=document.querySelector('#org-table tbody');
  var rows=box.querySelectorAll('tbody tr');
  rows.forEach(function(src){
    var cells=src.children;var name=cells[0].textContent.trim();
    var tr=document.createElement('tr');
    tr.innerHTML='<td><div class="org-name org-d1"><span class="bold fs13">'+name+'</span></div></td><td>'+cells[1].textContent+'</td><td><span class="sub">'+cells[2].textContent+'</span></td><td><span data-status><span class="tag tag-success tag-dot">存续</span></span></td><td>'+cells[3].textContent+'</td><td><span class="num bold">0</span></td><td><span class="tag tag-success">刚导入</span></td>';
    tb.insertBefore(tr,tb.firstChild);
  });
  document.getElementById('org-import').classList.add('hidden');
  toast('已导入 '+rows.length+' 个组织');
}
"""


def organizations():
    # 名称, 类别, 上级, 存续状态, 指导教师, 账号数, 层级深度, 分类, 提示
    orgs = [
        ("计算机学院团委", "学院团委", "计算机学院党委", "存续", "周建华", 1, 0, "college", ""),
        ("计算机学院团委新媒体中心", "院级学生组织", "计算机学院团委", "存续", "王晓琳", 1, 1, "college", ""),
        ("计算机学院学生会", "院级学生组织", "计算机学院团委", "存续", "王晓琳", 1, 1, "college", ""),
        ("计算机学院研究生会", "院级学生组织", "计算机学院团委", "存续", "王晓琳", 1, 1, "college", ""),
        ("计算机学院青年志愿者协会", "院级学生组织", "计算机学院团委", "存续", "王晓琳 / 赵敏", 5, 1, "college", ""),
        ("计算机学院大学生科学技术协会", "院级学生组织", "计算机学院团委", "存续", "王晓琳", 1, 1, "college", ""),
        ("计院街舞社", "社团组织", "计算机学院团委（指导）", "存续", "王晓琳", 1, 1, "club", ""),
        ("计院ACM协会", "社团组织", "计算机学院团委（指导）", "存续", "王晓琳", 1, 1, "club", ""),
        ("计院摄影协会", "社团组织", "计算机学院团委（指导）", "存续", "王晓琳", 1, 1, "club", ""),
        ("计院篮球协会", "社团组织", "计算机学院团委（指导）", "存续", "孙浩", 2, 1, "club", ""),
        ("计院人工智能协会", "社团组织", "计算机学院团委（指导）", "存续", "未配置", 1, 1, "club", ""),
        ("2021级软件工程1班团支部", "班级团支部", "计算机学院团委", "已毕业", "王晓琳", 1, 1, "branch grad", "zombie"),
        ("2021级计算机科学3班团支部", "班级团支部", "计算机学院团委", "已毕业", "王晓琳", 1, 1, "branch grad", "zombie"),
        ("2021级计算机科学2班团支部", "班级团支部", "计算机学院团委", "已毕业", "王晓琳", 0, 1, "branch grad", ""),
        ("2023级软件工程2班团支部", "班级团支部", "计算机学院团委", "存续", "刘洋", 1, 1, "branch", ""),
        ("2023级网络工程1班团支部", "班级团支部", "计算机学院团委", "存续", "刘洋", 1, 1, "branch", ""),
        ("2024级计算机科学1班团支部", "班级团支部", "计算机学院团委", "存续", "陈思远", 1, 1, "branch", ""),
        ("2025级软件工程2班团支部", "班级团支部", "计算机学院团委", "存续", "林雪", 1, 1, "branch", ""),
    ]
    rows = []
    for name, typ, parent, status, teacher, n, depth, cat, flag in orgs:
        d = " org-d1" if depth else ""
        ic_ = "building" if depth == 0 else ("users" if typ == "社团组织" else ("flag" if typ == "班级团支部" else "hierarchy"))
        note = ""
        if flag == "zombie":
            note = f' <a class="tag tag-danger" href="zombie.html">{icon("alert", 12)}账号未注销 · 去核实</a>'
        status_tag = f'<span data-status>{tag(status, "muted" if status == "已毕业" else "success", True)}</span>'
        teacher_html = tag("未配置", "warning") if teacher == "未配置" else teacher
        edit = (f'<button class="link" type="button" data-toggle="#org-edit" data-oname="{esc(name)}" data-otype="{esc(typ)}" '
                f'data-oparent="{esc(parent)}" data-ostatus="{esc(status)}" data-oteacher="{esc(teacher)}">编辑</button>')
        view = '<a class="link" href="accounts.html">查看账号</a>'
        if status == "已毕业":
            op = f'<div class="ops">{edit}{view}</div>'
        else:
            grad = (f'<button class="link" type="button" data-graduate data-toast="已将“{name}”标记为已毕业，名下账号将进入僵尸号核实">标记毕业</button>')
            op = f'<div class="ops">{edit}{grad}{view}</div>'
        rows.append(dict(cells=[f'<div class="org-name{d}">{icon(ic_)}<span class="bold fs13">{name}</span>{note}</div>',
                                typ, f'<span class="sub">{parent}</span>', status_tag, teacher_html,
                                f'<span class="num bold">{n}</span>', op],
                         cat=cat, cls="warn-row" if flag else ""))
    tabs = seg([("全部", "all"), ("院级组织", "college"), ("学生社团", "club"), ("班级团支部", "branch"), ("已毕业", "grad")],
               target="#org-table")
    content = f"""{page_hd('本院组织', '学院团委—团学组织树；班级团支部毕业后标记“已毕业”，名下未注销账号自动进入僵尸号核实',
                   '<button class="btn btn-default" type="button" data-toggle="#org-import">' + icon('upload') + '批量导入组织</button>'
                   + '<button class="btn btn-primary" type="button" data-toggle="#org-new">' + icon('plus') + '新增组织</button>')}
{alert('<b>2021级软件工程1班团支部</b> 已于 2025 年 6 月毕业，但名下账号“2021级软件工程1班团支部”（微信公众号）仍未注销，已停更 412 天，辅导员已核实建议注销。<a class="link" href="zombie.html">前往僵尸号核实</a>', 'warning')}
<div class="grid g4 mt16 mb16">
  {stat('组织总数', 28, '院级 6 · 社团 9 · 团支部 13', 'hierarchy')}
  {stat('存续组织', 24, '正常开展活动', 'check-circle', 'green')}
  {stat('已毕业团支部', 4, '2021 级 4 个班', 'flag', 'gray')}
  {stat('毕业仍有账号', 2, '需转注销处置', 'alert', 'red', href='zombie.html')}
</div>
<div class="card card-bd">
  <div class="toolbar">{tabs}<span class="small muted">带“账号未注销”标记的组织已毕业，但名下账号仍在册</span></div>
  {table(['组织名称', '组织类别', '上级组织', '存续状态', '指导教师', '账号数', '操作'], rows, id_='org-table')}
  {pager(28, 2)}
</div>"""
    types = ["院级学生组织", "社团组织", "班级团支部", "学院团委"]
    type_opts = "".join(f"<option>{t}</option>" for t in types)
    edit_body = f"""<div class="form-grid">
  {field('组织名称', '<input class="input" id="f-name" required>', True)}
  {field('组织类别', f'<select class="select" id="f-type">{type_opts}</select>', True)}
  {field('上级组织', '<input class="input" id="f-parent">')}
  {field('存续状态', '<select class="select" id="f-status"><option>存续</option><option>已毕业</option><option>已撤销</option></select>', True)}
  {field('指导教师', '<input class="input" id="f-teacher">')}
</div>"""
    new_body = f"""<div class="form-grid">
  {field('组织名称', '<input class="input" id="n-name" placeholder="请输入组织全称" required>', True)}
  {field('组织类别', f'<select class="select" id="n-type">{type_opts}</select>', True)}
  {field('上级组织', '<input class="input" id="n-parent" value="计算机学院团委">')}
  {field('存续状态', '<select class="select" id="n-status"><option>存续</option><option>已毕业</option><option>已撤销</option></select>', True)}
  {field('指导教师', '<input class="input" id="n-teacher" placeholder="请输入指导教师姓名">')}
</div>"""
    sample = table(["组织名称", "组织类别", "上级组织", "指导教师"], [
        ["2026级人工智能1班团支部", "班级团支部", "计算机学院团委", "林雪"],
        ["计院机器人协会", "社团组织", "计算机学院团委（指导）", "王晓琳"],
    ])
    import_body = f"""<div class="small sub mb12">按模板填写组织名称、组织类别、上级组织、指导教师后上传。也可先载入模板中的 2 条示例，确认后写入本院组织列表。</div>
<label class="upload">{icon('upload', 22)}<div class="mt4">选择 Excel 文件</div><div class="small muted">支持 .xlsx</div><input type="file" accept=".xlsx,.xls,.csv" onchange="loadImportSample()"></label>
<div class="mt12"><button type="button" class="btn btn-light btn-sm" onclick="loadImportSample()">载入模板示例</button></div>
<div id="import-preview" class="hidden mt12"><div class="field-label mb8">待导入</div>{sample}</div>"""
    content += (
        f'<div class="mask hidden" id="org-edit"><div class="modal"><div class="modal-hd">编辑组织'
        f'<button class="x-btn" type="button" data-toggle="#org-edit" aria-label="关闭">{icon("x")}</button></div>'
        f'<div class="modal-bd">{edit_body}</div><div class="modal-ft">'
        f'<button class="btn btn-default" type="button" data-toggle="#org-edit">取消</button>'
        f'<button class="btn btn-primary" type="button" onclick="saveOrg()">保存</button></div></div></div>'
        f'<div class="mask hidden" id="org-new"><div class="modal"><div class="modal-hd">新增组织'
        f'<button class="x-btn" type="button" data-toggle="#org-new" aria-label="关闭">{icon("x")}</button></div>'
        f'<div class="modal-bd">{new_body}</div><div class="modal-ft">'
        f'<button class="btn btn-default" type="button" data-toggle="#org-new">取消</button>'
        f'<button class="btn btn-primary" type="button" onclick="addOrg()">确认新增</button></div></div></div>'
        f'<div class="mask hidden" id="org-import"><div class="modal lg"><div class="modal-hd">批量导入组织'
        f'<button class="x-btn" type="button" data-toggle="#org-import" aria-label="关闭">{icon("x")}</button></div>'
        f'<div class="modal-bd">{import_body}</div><div class="modal-ft">'
        f'<button class="btn btn-default" type="button" data-toggle="#org-import">取消</button>'
        f'<button class="btn btn-primary" type="button" onclick="confirmImport()">确认导入</button></div></div></div>'
    )
    page("organizations.html", "organizations", "本院组织", cr(("账号管理", None), ("本院组织", None)), content, ORG_JS)


# ---------------------------------------------------------------- 5 学院审核列表
# ---------------------------------------------------------------- 6 新建备案 · 学院审核（剧本一）
def approval_detail():
    a, f = ACCOUNTS["new"], FLOWS["new"]
    t_when, _, _, t_cmt = f["steps"][3]
    head = acct_head(a, st(a["filing"]) + tag("新建", "primary") + tag("二级平台", "muted"))
    summary = kv([("申请编号", f'<span class="num">{f["no"]}</span>'), ("业务类型", "新建备案"), ("申请人", "李明（8209230117）"),
                  ("发起方式", "学生发起"), ("首次提交", f["steps"][0][0]), ("当前节点", tag("学院团委审核", "warning", True))], 3)
    teacher_op = f"""<div class="opinion">
  <div class="flex gap12">{avatar('王晓琳')}<div class="grow"><div class="bold">指导教师意见 · 王晓琳 {tag('同意', 'success')}</div>
  <div class="small muted">计算机学院宣传工作辅导员 · {t_when}</div></div>{tag('第 2 次审核', 'muted')}</div>
  <div class="quote">“{t_cmt}”</div>
  <div class="small muted mt8">首次审核（2026-09-25）曾退回修改：平台介绍不足 100 字；学生已补充至 326 字后重新提交。</div>
</div>"""
    belong = kv([("所属学院", "计算机学院"), ("所属团学组织", a["org"]), ("组织类别", a["org_type"]), ("平台管理层级", a["level"])], 2)
    platform = kv([("平台类型", a["platform"]), ("账号名称", a["name"]), ("曾用名", "无"), ("平台ID", a["pid"]),
                   ("是否认证", "否"), ("粉丝数", "0"), ("开通时间", a["opened"]), ( "运营团队规模（单位：人）", "6"),
                   ("主页链接", "mp.weixin.qq.com/csu_cs_youth"), ("平台头像", "已上传"), ("二维码", "未上传（非必填）"),
                   ("信息发布范围", "学院团学活动相关信息。")], 2)
    running = kv([("最近一次公开内容发布时间", "2026-09-22"), ("更新频率", "每周更新（≥1次/周）"), ("运行状态", "正常运行"),
                  ("异常情况", "无"), ("备注", "无")], 2)
    staff = kv([("当前管理教师", "王晓琳"), ("工号", "T20180427"), ("职务", "宣传工作辅导员"), ("手机号", PEOPLE["王晓琳"]["phone"]),
                ("是否为专职教师", "是"), ("具体负责人", "李明"), ("学号", "8209230117"), ("手机号", PEOPLE["李明"]["phone"]),
                ("管理员", "陈可欣（8209230221）、刘子涵（8209240133）", True),
                ("一审负责人", "王晓琳 · T20180427 · 宣传工作辅导员 · " + PEOPLE["王晓琳"]["phone"]),
                ("二审负责人", "周建华 · " + PEOPLE["周建华"]["no"] + " · " + PEOPLE["周建华"]["job"] + " · " + PEOPLE["周建华"]["phone"]),
                ("三审负责人", "陈静 · " + PEOPLE["陈静"]["no"] + " · " + PEOPLE["陈静"]["job"] + " · " + PEOPLE["陈静"]["phone"])], 2)
    intro = ("“中南计算机青年”是计算机学院团委新媒体中心主办的官方微信公众号，面向本院全体团员青年及校友。平台定位为学院共青团思想引领、"
             "青年服务与文化传播的主阵地，设置“院团动态”“青春榜样”“学业帮”三个固定栏目：院团动态发布团学活动通知与活动报道；"
             "青春榜样展示优秀团员、竞赛获奖与志愿服务典型；学业帮提供课程资源、竞赛信息与升学就业经验分享。信息发布范围限于学院团学工作相关内容，"
             "不发布商业推广信息。所有推文执行“学生编辑初审、新媒体中心主任复审、指导教师终审”的三审制度，涉及重大主题与敏感信息须报学院团委书记审定。")
    mechanisms = mechanism_blocks()
    files = "".join(f'<span class="file-chip">{icon("file")}{x}</span>' for x in
                    ["新媒体平台备案申请表（签字版）.pdf", "信息发布三审制度.pdf", "账号后台认证截图.png", "运营团队名单.xlsx"])
    tl = flow_items("new", 4) + [("now", "学院团委审核", "当前节点 · 周建华", ""), ("wait", "校团委审核", "待流转 · 陈静", "")]
    left = f"""{card('', head + '<div class="divider"></div>' + summary)}
<div class="mt16">{teacher_op}</div>
<div class="grid g2 mt16">
  {card('归属信息', belong)}
  {card('平台信息', platform)}
  {card('运行信息', running)}
  {card('责任人员', staff)}
</div>
{card('平台介绍', f'<p class="fs13 sub" style="line-height:1.9">{intro}</p>', tag('326 字 · 已按退回意见补充', 'success'), cls='mt16')}
<div class="grid g2 mt16">
  {card('平台信息确认', mechanisms)}
  {card('附件材料', f'<div class="upload-list" style="margin-top:0">{files}</div>')}
</div>
<div class="mt16">{alert('重复检查：系统发现 1 个名称相似账号“中南大学计算机学院青年”（已注销，2023-06），申请人已确认非重复账号。', 'info')}</div>"""
    right = f"""<div class="sticky col gap16">
  {card('审核流程', timeline(tl), tag(f['no'], 'muted'))}
  {card('学院审核意见', field('审核意见', textarea('请输入学院审核意见', '同意，报校团委审核。', maxlen=200, rows=3), req=True) +
        '<div class="chips mt12">' + ''.join(f'<button type="button" class="chip" data-toast="已插入常用意见：{x}">{x}</button>' for x in ['同意，报校团委审核。', '材料齐全', '请补充佐证材料']) + '</div>')}
</div>"""
    content = f"""{page_hd('新建备案 · 学院审核', '剧本一：指导教师已通过（含一次退回重提），学院审核通过后流转至校团委终审',
                   back_btn('approvals.html') + scene_next('校级终审', '../school/approval-detail.html'))}
<div class="split" data-form>
  <div>{left}</div>
  {right}
</div>
<div class="actbar"><span class="grow">{icon('info', 14)} 通过后流转至校团委审核；驳回则流程终止；退回修改将返回学生本人</span>
  {btn('驳回', '../common/modal-reject.html', 'danger', 'x-circle')}
  {btn('退回修改', '../common/modal-return.html', 'warning', 'undo')}
  {go('通过并报校团委', '../school/approval-detail.html', 'primary', 'send', toast='已通过，流转至校团委审核')}
</div>"""
    page("approval-detail.html", "approvals", "新建备案 · 学院审核", cr(("学院审核", "approvals.html"), ("新建备案 · " + a["name"], None)), content)


# ---------------------------------------------------------------- 7 名称变更 · 学院审核（剧本二）
def approval_change():
    a, f = ACCOUNTS["rename"], FLOWS["rename"]
    head = acct_head(a, st(a["filing"]) + tag("重要变更", "danger") + tag("二级平台", "muted"),
                     f'{a["platform"]} · 平台ID {a["pid"]} · 粉丝 {a["fans"]} · 开通于 {a["opened"]}')
    summary = kv([("申请编号", f'<span class="num">{f["no"]}</span>'), ("变更类型", "账号名称变更"), ("申请人", "李明（8209230117）"),
                  ("发起方式", "学生发起"), ("提交时间", f["steps"][0][0]), ("变更原因", f["steps"][0][3])], 3)
    diff = diff_table([("账号名称", a["name"], a["new_name"]), ("平台类型", a["platform"], a["platform"]),
                       ("平台 ID", a["pid"], a["pid"]), ("所属组织", a["org"], a["org"]), ("平台层级", a["level"], a["level"]),
                       ("管理教师", a["teacher"], a["teacher"]), ("学生负责人", "李明", "李明")])
    t_when, _, _, t_cmt = f["steps"][1]
    teacher_op = f"""<div class="opinion">
  <div class="flex gap12">{avatar('王晓琳')}<div class="grow"><div class="bold">指导教师意见 · 王晓琳 {tag('同意', 'success')}</div>
  <div class="small muted">{t_when}</div></div></div>
  <div class="quote">“{t_cmt}”</div>
</div>"""
    effects = kv([("生效方式", "校团委审核通过后生效"), ("曾用名", "“计算机学院学生会”自动记入档案曾用名"),
                  ("平台侧改名", "需学生在微博后台同步提交改名"), ("备案表", "生效后自动更新备案表")], 2)
    files = "".join(f'<span class="file-chip">{icon("file")}{x}</span>' for x in ["学生会换届决议.pdf", "新名称视觉规范.png"])
    tl = flow_items("rename", 2) + [("now", "学院团委审核", "当前节点 · 周建华", ""), ("wait", "校团委审核", "待流转 · 陈静", "")]
    left = f"""{card('', head + '<div class="divider"></div>' + summary)}
<div class="mt16">{alert('<b>账号名称变更属重要变更，学院审核后需报校团委。</b>名称变更生效后，原名称记入曾用名，历史年审与备案记录保持关联。', 'warning')}</div>
{card('变更前后对比', diff, tag('1 项变更', 'warning'), cls='mt16')}
<div class="grid g2 mt16">
  <div>{teacher_op}</div>
  {card('变更影响', effects)}
</div>
{card('佐证材料', f'<div class="upload-list" style="margin-top:0">{files}</div>', cls='mt16')}"""
    right = f"""<div class="sticky col gap16">
  {card('审核流程', timeline(tl), tag(f['no'], 'muted'))}
  {card('学院审核意见', field('审核意见', textarea('请输入学院审核意见', '属重要变更，报校团委审核。', maxlen=200, rows=3), req=True))}
</div>"""
    content = f"""{page_hd('名称变更 · 学院审核', '剧本二：计算机学院学生会 → 中南计院学生会，教师已通过，学院审核后报校团委',
                   back_btn('approvals.html') + scene_next('校级审核', '../school/approval-change.html'))}
<div class="split" data-form>
  <div>{left}</div>
  {right}
</div>
<div class="actbar"><span class="grow">{icon('info', 14)} 重要变更须经校团委审核后生效；退回将返回学生修改</span>
  {btn('驳回', '../common/modal-reject.html', 'danger', 'x-circle')}
  {btn('退回修改', '../common/modal-return.html', 'warning', 'undo')}
  {go('通过并报校团委', '../school/approval-change.html', 'primary', 'send', toast='已通过，流转至校团委审核')}
</div>"""
    page("approval-change.html", "approvals", "名称变更 · 学院审核", cr(("学院审核", "approvals.html"), ("名称变更 · " + a["name"], None)), content)


# ---------------------------------------------------------------- 7b 教师代办交接 · 学院审核（剧本八）
def approval_proxy():
    a, f = ACCOUNTS["proxy"], FLOWS["proxy"]
    zl, sy = PEOPLE["赵磊"], PEOPLE["孙悦"]
    head = acct_head(a, st("教师代办") + tag("负责人交接", "primary") + st(a["filing"]),
                     f'{a["platform"]} · 平台ID {a["pid"]} · {a["org"]} · 申请编号 {f["no"]}')
    summary = kv([("申请编号", f'<span class="num">{f["no"]}</span>'), ("业务类型", "负责人交接"),
                  ("发起方式", st("教师代办")), ("代办人", "王晓琳 · 宣传工作辅导员"),
                  ("提交时间", f["steps"][0][0]), ("生效方式", "学院审核通过后立即生效")], 3)
    reason = f["steps"][0][3]
    opinion_cmt = f["steps"][1][3]

    def who_box(title, name, meta, badge):
        return (f'<div class="id-card"><div class="flex between"><span class="small muted bold">{title}</span>{badge}</div>'
                f'<div class="flex gap12 mt8">{avatar(name)}<div><div class="bold">{name}</div><div class="small sub">{meta}</div></div></div></div>')

    pair = (f'<div class="grid g2">{who_box("原负责人", "赵磊", zl["grade"] + " · " + zl["job"] + " · " + zl["no"], tag("已毕业", "muted"))}'
            f'{who_box("新负责人", "孙悦", sy["grade"] + " · " + sy["job"] + " · " + sy["no"], tag("接任", "success"))}</div>')
    diff = diff_table([("学生负责人", "赵磊", "孙悦"), ("学号", zl["no"], sy["no"]), ("班级", zl["grade"], sy["grade"]),
                       ("手机号", zl["phone"], sy["phone"]), ("任期", "2023-09 ~ 2025-06", "审核通过后起"),
                       ("管理教师", a["teacher"], a["teacher"]), ("账号名称", a["name"], a["name"])])
    teacher_op = f"""<div class="opinion warn">
  <div class="flex gap12">{avatar('王晓琳')}<div class="grow"><div class="bold">代办说明 · 王晓琳 {tag('教师代办', 'primary')}</div>
  <div class="small muted">宣传工作辅导员 · {f["steps"][0][0]}</div></div></div>
  <div class="quote">“{reason}”</div>
</div>"""
    files = "".join(f'<span class="file-chip">{icon("file")}{x}</span>' for x in ["赵磊学籍状态截图（已毕业）.png", "ACM协会换届决议.pdf"])
    tl = flow_items("proxy", 1) + [("now", "学院管理员审核", "当前节点 · 周建华", ""), ("wait", "交接生效", "孙悦成为学生负责人", "")]
    chip_js = "var t=document.getElementById('px-cmt');if(t)t.value=this.textContent.trim()"
    chips = "".join(f'<button type="button" class="chip" onclick="{chip_js}">{x}</button>'
                    for x in [opinion_cmt, "原负责人已毕业，同意代办交接。", "请补充换届决议"])
    left = f"""{card('', head + '<div class="divider"></div>' + summary)}
<div class="mt16">{alert('<b>发起方式：教师代办。</b>学生负责人赵磊已毕业无法本人办理，由指导教师王晓琳代为发起。学院审核通过后交接即时生效，原负责人任期记入历任记录，操作日志保留“教师代办”。', 'info')}</div>
{card('交接双方', pair, cls='mt16')}
{card('变更前后', diff, tag('负责人变更', 'warning'), cls='mt16')}
<div class="mt16">{teacher_op}</div>
{card('佐证材料', f'<div class="upload-list" style="margin-top:0">{files}</div>', cls='mt16')}"""
    right = f"""<div class="sticky col gap16">
  {card('审核流程', timeline(tl), tag(f['no'], 'muted'))}
  {card('学院审核意见', field('审核意见', textarea('请输入学院审核意见', opinion_cmt, maxlen=200, rows=3, attrs='id="px-cmt"'), req=True)
        + f'<div class="chips mt12">{chips}</div>')}
</div>"""
    content = f"""{page_hd('教师代办交接 · 学院审核', '剧本八：计院ACM协会负责人赵磊（已毕业）→ 孙悦，教师代办，学院审核通过后即时生效',
                   back_btn('approvals.html') + scene_next('查看代办日志', '../school/log-detail.html'))}
<div class="split" data-form>
  <div>{left}</div>
  {right}
</div>
<div class="actbar"><span class="grow">{icon('info', 14)} 通过后孙悦立即成为学生负责人；退回则回到代办教师补充材料</span>
  {btn('驳回', '../common/modal-reject.html', 'danger', 'x-circle')}
  {btn('退回教师', '../common/modal-return.html', 'warning', 'undo')}
  {go('通过并生效', '../common/archive-logs.html', 'primary', 'check', toast='已通过，孙悦接任负责人，交接即时生效')}
</div>"""
    page("approval-proxy.html", "approvals", "教师代办交接 · 学院审核",
         cr(("学院审核", "approvals.html"), ("代办交接 · " + a["name"], None)), content)


# ---------------------------------------------------------------- 8 本院年审进度
def annual_progress():
    days_left = (date(2026, 11, 5) - TODAY).days
    node_cards = "".join(
        f'<a class="card card-hover stat" href="{h}"><div class="grow"><div class="stat-label">{label}</div>'
        f'<div class="stat-value c-{"primary" if kind == "primary" else kind}">{v}</div><div class="stat-sub">{hint}</div></div></a>'
        for label, v, kind, h, hint in NODES)
    org_rows = []
    for name, n, nd in ORG_PROGRESS:
        cells = [f'<b>{name}</b>', n] + [f'<span class="num {"muted" if x == 0 else ""}">{x}</span>' for x in nd]
        cells += [pct_cell(nd[4], n), ops(("明细", "accounts.html"), ("催办", None, f"已向“{name}”未完成账号的负责人发送催办"))]
        org_rows.append(cells)
    t_rows = []
    for t in TEACHERS:
        nd = t["nodes"]
        cells = [person(t["name"]), f'<span class="small sub">{t["job"]}</span>', t["total"]]
        cells += [f'<span class="num {"muted" if x == 0 else ""}">{x}</span>' for x in nd]
        cells += [pct_cell(nd[4], t["total"]), ops(("查看", teacher_href(t["name"])),
                                                  ("催办", None, f'已向{t["name"]}老师发送年审催办提醒'))]
        t_rows.append(cells)
    un = UNASSIGNED_NODES
    t_rows.append([tag("未分配教师", "danger"), '<span class="small sub">需先分派负责教师</span>', sum(un)]
                  + [f'<span class="num {"muted" if x == 0 else ""}">{x}</span>' for x in un]
                  + [pct_cell(un[4], sum(un)), ops(("去分派", "assign.html"))])
    heads_node = ["待填报", "待教师审核", "待学院审核", "整改中", "已完成"]
    org_tbl = table(["组织", "账号数"] + heads_node + ["完成率", "操作"], org_rows)
    t_tbl = table(["教师", "岗位", "负责账号"] + heads_node + ["完成率", "操作"], t_rows)
    total_row = f'<div class="flex gap16 small sub mt12">合计 {CS["total"]} 个账号：' + " · ".join(f"{l} {v}" for l, v, _, _, _ in NODES) + "</div>"
    view = seg([("按组织", "org"), ("按教师", "teacher")], target="#ap-views")
    content = f"""{page_hd('本院年审进度', f'{T["name"]} · 学生填报截止 {T["stu_end"]} · 教师审核截止 {T["teacher_end"]} · 学院提交截止 {T["college_end"]}',
                   btn('导出进度表', None, 'default', 'download', toast='已生成《计算机学院年审完成情况》Excel') + btn('一键催办未完成', None, 'primary', 'bell', toast='已向 15 个未完成账号的学生负责人及 3 名教师发送催办'))}
{annual_tabs('年审进度')}
{alert(f'距学院提交截止（{T["college_end"]}）还有 <b>{days_left}</b> 天。本院当前完成率 58.3%，低于全校平均 71.6%；校团委已于 2026-09-28 发出催办。', 'warning', 'clock')}
<div class="grid g5 mt16">{node_cards}</div>
<div class="card card-bd mt16">
  <div class="toolbar"><div class="flex gap12"><span class="card-title">完成情况明细</span>{view}</div>
  <div class="flex gap8">{btn('学院审核', 'annual-review.html', 'light', 'file-check', 'sm')}{btn('提交校团委', 'annual-submit.html', 'primary', 'send', 'sm')}</div></div>
  <div id="ap-views"><div data-cat="org">{org_tbl}</div><div data-cat="teacher" class="hidden">{t_tbl}</div></div>
  {total_row}
</div>"""
    page("annual-progress.html", "annual", "本院年审进度", cr(("年审统筹", "annual-progress.html"), ("年审进度", None)), content)


# ---------------------------------------------------------------- 9 学院年审审核（剧本五）
def annual_review():
    items = [
        (ACCOUNTS["annual"]["name"], "微信公众号", "计算机学院团委", "王晓琳", "无异动", "教师已通过", "待学院审核", "nochg"),
        ("计院篮球协会", "抖音", "计院篮球协会", "孙浩", "无异动", "教师已通过", "待学院审核", "nochg"),
        ("计算机学院研究生会", "微信公众号", "计算机学院研究生会", "王晓琳", "无异动", "教师已通过", "已确认", "nochg"),
        ("计院支教队", "微信公众号", "计算机学院青年志愿者协会", "赵敏", "无异动", "教师已通过", "已确认", "nochg"),
        ("2023级软件工程2班团支部", "微信公众号", "2023级软件工程2班团支部", "刘洋", "无异动", "教师已通过", "已确认", "nochg"),
        (ACCOUNTS["rename"]["name"], "微博", "计算机学院学生会", "王晓琳", "变更", "教师已通过 · 名称变更", "待学院审核", "change"),
        ("2024级计算机科学1班团支部", "微信公众号", "2024级计算机科学1班团支部", "陈思远", "变更", "教师已通过 · 负责人变更", "待学院审核", "change"),
        ("计院人工智能协会", "哔哩哔哩", "计院人工智能协会", "未分配", "新建", "学院代审 · 本年度新建", "已确认", "change"),
        (ACCOUNTS["rectify"]["name"], "小红书", "计算机学院青年志愿者协会", "王晓琳", "无异动", "要求整改", "整改复核中", "abn"),
        ("2023级网络工程1班团支部", "QQ", "2023级网络工程1班团支部", "刘洋", "无异动", "要求整改", "待整改", "abn"),
        (ACCOUNTS["zombie"]["name"], "微信公众号", "2021级软件工程1班团支部", "王晓琳", "注销", "建议注销", "本年度注销", "cancel"),
    ]
    teacher_kind = {"要求整改": "danger", "建议注销": "muted"}
    rows = []
    for name, p, org, t, chg, tr, cs, cat in items:
        tk = teacher_kind.get(tr, "success")
        h = annual_open(name, cs)
        if name == ACCOUNTS["rectify"]["name"]:
            arch = "../common/archive-rectify.html"
        elif name == ACCOUNTS["zombie"]["name"]:
            arch = "../common/archive-cancel.html"
        elif name == ACCOUNTS["rename"]["name"]:
            arch = "../common/archive-changes.html"
        else:
            arch = "../common/archive-audit.html"
        if cat in ("abn", "cancel") or name == ACCOUNTS["rename"]["name"]:
            op = ops(("审核", h), ("档案", arch))
        elif cs == "已确认":
            op = ops(("查看", h), ("撤回确认", None, f"已撤回“{name}”的学院确认"))
        else:
            op = ops(("审核", h), ("确认", None, f"已确认“{name}”年审通过"))
        rows.append(dict(cells=[acct(name, p, org), teacher_cell(t), st(chg), tag(tr, tk), st(cs if cs != "已确认" else "已确认"), op],
                         href=h, cat=cat))
    cnt = {}
    for x in items:
        cnt[x[7]] = cnt.get(x[7], 0) + 1
    tabs = seg([(f"全部 {len(items)}", "all"), (f"无异动 {cnt['nochg']}", "nochg"), (f"有变更 {cnt['change']}", "change"),
                (f"异常·整改 {cnt['abn']}", "abn"), (f"本年度注销 {cnt['cancel']}", "cancel")], target="#ar-table")
    content = f"""{page_hd('学院年审审核', '汇总各教师审核结果：无异动账号可批量确认；变更、整改、注销账号逐一审核',
                   scene_next('统一提交校团委', 'annual-submit.html') + btn('全部审核完成，去提交', 'annual-submit.html', 'primary', 'send'))}
{annual_tabs('学院审核')}
<div class="grid g4 mb16">
  {stat('教师已审核', 32, '共 36 个账号', 'file-check')}
  {stat('待学院审核', 4, '无异动 2 · 变更 2', 'inbox', 'orange')}
  {stat('异常 / 整改', 2, '整改复核中 1 · 待整改 1', 'wrench', 'red', href='rectify.html')}
  {stat('本年度注销', 1, '僵尸号核实转注销', 'ban', 'gray', href='zombie.html')}
</div>
<div class="card card-bd">
  <div class="toolbar">{tabs}{alert('无异动且教师已通过的账号，可勾选后批量确认', 'info')}</div>
  <div class="batchbar">{icon('check-circle')}已选 <b data-checked-count="#ar-table">0</b> 个账号
    <span class="ml-auto flex gap8">{btn('批量确认通过', None, 'primary', 'check', 'sm', toast='已批量确认所选账号，已纳入提交校团委清单')}
    {btn('批量退回教师', None, 'default', 'undo', 'sm', toast='已将所选账号退回指导教师重新审核')}</span></div>
  {table(['账号 / 所属组织', '负责教师', '年度异动', '教师审核结果', '学院审核', '操作'], rows, check=True, id_='ar-table')}
  {pager(36, 4)}
</div>"""
    page("annual-review.html", "annual", "学院年审审核", cr(("年审统筹", "annual-progress.html"), ("学院审核", None)), content)


# ---------------------------------------------------------------- 10 年审单账号审核
def annual_review_detail():
    a, f = ACCOUNTS["annual"], FLOWS["annual"]
    head = acct_head(a, st("无异动") + tag("教师已通过", "success") + st("待学院审核"),
                     f'{a["platform"]} · 平台ID {a["pid"]} · 粉丝 {a["fans"]} · 年审编号 {f["no"]}')
    checks = [
        ("账号是否仍存在", "是"), ("是否正常运营", "是，正常运营"), ("账号能否正常访问", "能正常访问"),
        ("最近发布时间", "2026-09-17"), ("当前学生负责人", "李明（8209230117）"), ("指导教师是否变化", "否（王晓琳）"),
        ("账号名称是否变化", "否"), ("是否申请注销", "否"), ("其他异常情况", "无"),
    ]
    rows = [[f'<span class="bold fs13">{k}</span>', v, tag(icon("check", 12) + "与档案一致", "success")] for k, v in checks]
    t_when, _, _, t_cmt = f["steps"][2]
    s_when, _, _, s_cmt = f["steps"][1]
    teacher_op = f"""<div class="opinion">
  <div class="flex gap12">{avatar('王晓琳')}<div class="grow"><div class="bold">指导教师审核意见 {tag('通过', 'success')}</div>
  <div class="small muted">王晓琳 · {t_when}</div></div></div>
  <div class="quote">“{t_cmt}”</div>
</div>"""
    tl = flow_items("annual", 3) + [("now", "学院审核确认", "当前节点 · 周建华", ""),
                                    ("wait", "学院统一提交校团委", "本院全部账号完成后统一提交", ""),
                                    ("wait", "校团委审核", "陈静", "")]
    left = f"""{card('', head)}
{card('学生确认事项', table(['核对项', '学生确认', '系统比对'], rows, cls='tbl-sm') + f'<div class="small muted mt12">学生李明于 {s_when} 提交：{s_cmt}</div>', tag('9 项全部确认', 'success'), cls='mt16')}
<div class="mt16">{teacher_op}</div>
<div class="grid g2 mt16">
  {card('本年度运营数据', kv([('本年度发布', '86 篇'), ('月均发布', '9.6 篇'), ('粉丝增长', '+2,318'), ('最高阅读', '1.2 万')], 2))}
  {card('平台信息确认', mechanism_blocks())}
</div>"""
    right = f"""<div class="sticky col gap16">
  {card('账号主页截图', f'<div class="shot"><img src="{PHOTOS["screenshot"]}" alt="中南计院团委公众号主页截图"></div><div class="small muted mt8">学生上传于 2026-09-18 · 截图显示最近发布 2026-09-17</div>')}
  {card('审核流程', timeline(tl), tag(f['no'], 'muted'))}
</div>"""
    content = f"""{page_hd('年审单账号审核', '学院层面审核单个账号：可确认通过、退回、要求整改或建议不通过',
                   back_btn('annual-review.html') + btn('查看账号档案', '../common/archive-audit.html', 'default', 'archive'))}
<div class="split">
  <div>{left}</div>
  {right}
</div>
<div class="actbar"><span class="grow">{icon('info', 14)} 确认通过后纳入本院提交清单；要求整改将生成整改任务</span>
  {btn('建议不通过', '../common/modal-reject.html', 'danger', 'x-circle')}
  {btn('退回', '../common/modal-return.html', 'warning', 'undo')}
  {btn('要求整改', 'rectify-create.html', 'default', 'wrench')}
  {go('学院确认通过', 'annual-review.html', 'primary', 'check', toast='已确认通过，已纳入提交校团委清单')}
</div>"""
    page("annual-review-detail.html", "annual", "年审单账号审核", cr(("年审统筹", "annual-progress.html"), ("学院审核", "annual-review.html"), (a["name"], None)), content)


# ---------------------------------------------------------------- 11 提交校团委（剧本五）
CHANGE_SUMMARY = [("无异动", 22), ("新建", 3), ("变更", 9), ("注销", 2)]


def annual_submit():
    checks = [
        ("所有账号已完成教师审核", "36 / 36 个账号，6 名教师全部完成"),
        ("学院审核完成", "36 / 36 个账号已由学院确认"),
        ("待整改账号已下发整改任务", "2 个账号，整改任务 ZG20260920001 等已下发"),
        ("注销账号已处置", "2 个账号已转注销并报校团委确认"),
    ]
    check_html = "".join(
        f'<div class="check-item"><span class="ok-ic">{icon("check")}</span><div class="grow"><div class="bold fs13">{t}</div>'
        f'<div class="small muted">{d}</div></div>{tag("已满足", "success")}</div>' for t, d in checks)
    total = sum(v for _, v in CHANGE_SUMMARY)
    kinds = {"无异动": "c-primary", "新建": "c-primary", "变更": "c-warning", "注销": "c-danger"}
    minis = "".join(f'<div class="mini-stat"><span class="small sub">{k}</span><b class="{kinds[k]}">{v}</b>'
                    f'<span class="small muted">占比 {v / total * 100:.1f}%</span></div>' for k, v in CHANGE_SUMMARY)
    by_level = table(["平台层级", "账号数", "无异动", "新建", "变更", "注销"], [
        ["二级平台", 10, 6, 1, 3, 0], ["三级平台", 17, 10, 1, 4, 2], ["社团平台", 9, 6, 1, 2, 0],
        ['<b>合计</b>', f'<b>{total}</b>', "<b>22</b>", "<b>3</b>", "<b>9</b>", "<b>2</b>"]], cls="tbl-sm")
    commit = ('<label class="commit"><input type="checkbox" id="commit-ck">'
              '<span>本人承诺：计算机学院已按《中南大学团学组织新媒体平台管理办法》完成本年度全部账号的年审工作，所提交数据真实、准确、完整；'
              '对存在问题的账号已督促整改或依规注销。提交后本院年审数据将锁定，如需修改须由校团委退回。</span></label>')
    content = f"""{page_hd('提交校团委', '剧本五：全部账号完成教师审核与学院审核后，由学院统一提交校团委',
                   back_btn('annual-review.html') + scene_next('校级批量审核（学校管理员）', '../school/annual-review.html'))}
{annual_tabs('提交校团委')}
{alert(f'以下为提交时点数据：计算机学院 {total} 个账号已全部完成本年度年审（教师审核 + 学院审核），满足提交条件。', 'success')}
<div class="grid mt16" style="grid-template-columns:minmax(0,1.2fr) minmax(0,1fr)">
  {card('提交前检查清单', f'<div class="col gap12">{check_html}</div>', tag('4 / 4 通过', 'success'))}
  {card('按异动类型汇总', f'<div class="grid g4">{minis}</div><div class="mt16">{donut(CHANGE_SUMMARY, total, "账号总数")}</div>', tag(f'合计 {total}', 'primary'))}
</div>
{card('按平台层级明细', by_level, btn('导出汇总表', None, 'text', size='sm', toast='已生成《计算机学院2026年度年审汇总表》'), cls='mt16')}
{card('提交承诺', commit + '<div class="small muted mt8">提交人：周建华（计算机学院团委书记） · 提交后通知校团委宣传部陈静</div>', cls='mt16')}
<div class="actbar"><span class="grow">{icon('lock', 14)} 提交后本院年审数据锁定，校团委审核截止 {T['school_end']}</span>
  {back_btn('annual-review.html', '返回学院审核')}
  {btn('预览提交内容', None, 'default', 'eye', toast='已生成提交预览：36 个账号，无异动 22 / 新建 3 / 变更 9 / 注销 2')}
  {submit_btn('确认提交校团委', 'annual-submit-success.html', 'primary', 'send', toast='已提交校团委')}
</div>"""
    page("annual-submit.html", "annual", "提交校团委", cr(("年审统筹", "annual-progress.html"), ("提交校团委", None)), content, js=COMMIT_JS)


def annual_submit_success():
    total = sum(v for _, v in CHANGE_SUMMARY)
    info = kv([("提交编号", '<span class="num">NS2026-CS-SUB</span>'), ("提交人", "周建华 · 学院管理员"), ("提交时间", "2026-09-29 17:00"),
               ("账号总数", f"{total} 个"), ("异动汇总", " · ".join(f"{k} {v}" for k, v in CHANGE_SUMMARY)), ("下一节点", f"校团委审核（截止 {T['school_end']}）")], 3)
    tl = flow_items("annual", 4) + [("now", "校团委审核", "陈静 · 审核中", "")]
    actions = (btn("返回工作台", "workbench.html", "default", "home") + btn("查看年审进度", "annual-progress.html", "ghost", "chart")
               + btn("查看校级审核（演示下一角色）", "../school/annual-review.html", "primary", "arrow-right"))
    body = result("ok", "本院年审已提交校团委",
                  f"计算机学院 2026 年度年审已于 2026-09-29 17:00 提交校团委，共 {total} 个账号；数据已锁定，校团委审核结果将通过消息通知。",
                  actions)
    content = f"""{card('', body)}
<div class="grid mt16" style="grid-template-columns:minmax(0,1.4fr) minmax(0,1fr)">
  {card('提交信息', info)}
  {card('年审流程（剧本五）', timeline(tl))}
</div>"""
    page("annual-submit-success.html", "annual", "提交成功", cr(("年审统筹", "annual-progress.html"), ("提交成功", None)), content)


# ---------------------------------------------------------------- 12 任务分派
ASSIGN_ROWS = [
    ("2025级软件工程2班团支部", "QQ", "2025级软件工程2班团支部", "班级团支部", "未分配", "l3 unassigned"),
    ("计院人工智能协会", "哔哩哔哩", "计院人工智能协会", "社团组织", "未分配", "club unassigned"),
    (ACCOUNTS["annual"]["name"], "微信公众号", "计算机学院团委", "院级学生组织", "王晓琳", "l2"),
    (ACCOUNTS["rename"]["name"], "微博", "计算机学院学生会", "院级学生组织", "王晓琳", "l2"),
    (ACCOUNTS["rectify"]["name"], "小红书", "计算机学院青年志愿者协会", "院级学生组织", "王晓琳", "l2"),
    (ACCOUNTS["handover"]["name"], "抖音", "计院街舞社", "社团组织", "王晓琳", "club"),
    (ACCOUNTS["photo"]["name"], "视频号", "计院摄影协会", "社团组织", "王晓琳", "club"),
    ("计院篮球协会", "抖音", "计院篮球协会", "社团组织", "孙浩", "club"),
    ("2023级网络工程1班团支部", "QQ", "2023级网络工程1班团支部", "班级团支部", "刘洋", "l3"),
    ("2024级计算机科学1班团支部", "微信公众号", "2024级计算机科学1班团支部", "班级团支部", "陈思远", "l3"),
    ("计院支教队", "微信公众号", "计算机学院青年志愿者协会", "院级学生组织", "赵敏", "l2"),
]
RULE_EXAMPLES = "2024级团支部 → 2024级辅导员（陈思远）；学生社团 → 社团工作辅导员（孙浩）；志愿者协会 → 志愿服务负责老师（赵敏）"


def assign_content():
    cards = []
    for t in TEACHERS:
        href = teacher_href(t["name"])
        done_p = round(t["nodes"][4] / t["total"] * 100)
        av = avatar(t["name"]) if t["name"] in AVATARS else f'<span class="ini">{t["name"][0]}</span>'
        cards.append(f'<a class="t-card" href="{href}">{av}'
                     f'<div class="grow"><div class="flex between"><span class="bold">{t["name"]}</span><span class="small sub">负责 <b class="c-primary num">{t["total"]}</b> 个</span></div>'
                     f'<div class="small muted ellipsis">{t["job"]}</div><div class="flex gap8 mt4">{progress(done_p, "green")}<span class="small muted num">{done_p}%</span></div></div></a>')
    cards.append(f'<a class="t-card warn" href="assign-batch.html">{ic_box("alert", "red")}<div class="grow"><div class="bold c-danger">未分配账号 2 个</div>'
                 f'<div class="small muted">新建团支部、新成立社团尚未指定负责教师</div></div>{icon("chevron-right")}</a>')
    rows = []
    for name, p, org, typ, t, cat in ASSIGN_ROWS:
        op = (f'<div class="ops"><button class="link" type="button" onclick="assignRow(this)">分配</button>'
              f'<a class="link" href="../common/archive-staff.html">档案</a></div>')
        rows.append(dict(cells=[acct(name, p, org), typ, f'<span data-col="teacher">{teacher_cell(t)}</span>',
                                f'<div style="width:150px">{sel(TEACHER_NAMES, None if t == "未分配" else t, ph="选择教师")}</div>',
                                op],
                         cat=cat))
    quick = chips([("全部", "all"), ("未分配 2", "unassigned"), ("院级组织", "l2"), ("学生社团", "club"), ("班级团支部", "l3")], target="#as-table")
    return f"""{page_hd('任务分派', '将本院账号分配给具体教师负责审核；支持单个调整与按规则批量分配，分配变更全程留痕',
                   btn('分配记录', '../common/archive-logs.html', 'default', 'history') + btn('按规则批量分配', 'assign-batch.html', 'primary', 'route'))}
{alert('<b>分配规则示例：</b>' + RULE_EXAMPLES + '。按规则分配后，新建账号将自动归属对应教师。', 'info')}
<div class="grid mt16" style="grid-template-columns:300px minmax(0,1fr)">
  {card('本院业务教师（6）', '<div class="col gap8">' + ''.join(cards) + '</div>', btn('工作量', 'teachers.html', 'text', size='sm'))}
  <div class="card card-bd">
    <div class="toolbar">{quick}<span class="small muted">在“变更为”中选择教师后点击“分配”生效</span></div>
    {table(['账号', '组织类别', '当前负责教师', '变更为', '操作'], rows, id_='as-table')}
    {pager(36, 3)}
  </div>
</div>"""


ASSIGN_JS = r"""
function assignRow(btn){
  var tr=btn.closest('tr');
  var s=tr&&tr.querySelector('select');
  var name=s?s.value:'';
  if(!name){toast('请先在“变更为”中选择教师');return;}
  var cell=tr.querySelector('[data-col="teacher"]');
  if(cell)cell.textContent=name;
  toast('已更新负责教师为 '+name+'，并通知新旧教师');
  btn.textContent='已分配';
}
function addRule(){
  var tpl=document.querySelector('#rule-tpl .rule-row');
  var box=document.getElementById('rule-list');
  if(!tpl||!box)return;
  var row=tpl.cloneNode(true);
  row.querySelectorAll('select').forEach(function(s){s.selectedIndex=0;});
  box.appendChild(row);
  toast('已添加一条规则，请选择条件与教师');
}
"""


def assign():
    page("assign.html", "assign", "任务分派", cr(("任务与人员", None), ("任务分派", None)), assign_content(), ASSIGN_JS)


def assign_batch():
    types = [("按年级", "如 2024级团支部 → 2024级辅导员", True), ("按组织类别", "如 学生社团 → 社团工作辅导员", False),
             ("按学生组织", "如 志愿者协会 → 志愿服务负责老师", False), ("指定账号", "勾选具体账号分配给某位教师", False)]
    choice_html = "".join(
        f'<button type="button" class="choice{" on" if on else ""}" data-choice=""><span class="ck"></span>'
        f'<div class="grow"><div class="bold fs13">{t}</div><div class="small muted">{d}</div></div></button>' for t, d, on in types)
    rules = [("按年级", "2024级团支部（3）", "陈思远"), ("按组织类别", "学生社团（8）", "孙浩"), ("按学生组织", "青年志愿者协会（1）", "赵敏")]
    rule_opts_k = ["按年级", "按组织类别", "按学生组织", "指定账号"]
    rule_opts_c = ["2024级团支部（3）", "2025级团支部（4）", "学生社团（8）", "青年志愿者协会（1）", "院级学生组织（5）"]

    def rule_row(k=None, c=None, t=None, req=False):
        return (f'<div class="rule-row">{sel(rule_opts_k, k, ph="规则类型")}'
                f'{sel(rule_opts_c, c, ph="选择条件")}'
                f'<span class="muted">{icon("arrow-right")}</span>{sel(TEACHER_NAMES, t, ph="选择教师", req=req)}'
                f'<button type="button" class="x-btn" data-remove=".rule-row" aria-label="删除规则">{icon("trash")}</button></div>')

    rule_html = "".join(rule_row(k, c, t, True) for k, c, t in rules)
    preview = table(["账号范围", "数量", "将分配给"], [
        ["2024级团支部", "3", "陈思远"], ["学生社团", "8", "孙浩"], ["青年志愿者协会", "1", "赵敏"],
    ], cls="tbl-sm")
    body = f"""<div data-form>
  <div class="form-section">规则类型</div>
  <div class="choices g4 grid" data-single="">{choice_html}</div>
  <div class="form-section mt20">分配规则 <span class="small muted" style="font-weight:400">条件 → 负责教师，按顺序匹配</span></div>
  <div id="rule-tpl" class="hidden">{rule_row(req=True)}</div>
  <div id="rule-list" class="col gap8">{rule_html}</div>
  <div class="mt12"><button class="btn btn-light btn-sm" type="button" onclick="addRule()">{icon('plus')}添加规则</button></div>
  <div id="rule-preview" class="hidden mt12"><div class="field-label mb8">受影响账号（12）</div>{preview}</div>
  <div class="divider"></div>
  <div class="flex between"><div class="flex gap12"><span class="switch on" role="switch" aria-label="覆盖已分配账号"></span><span class="fs13">覆盖已分配账号的负责教师</span></div>
  <div class="flex gap8"><span class="switch on" role="switch" aria-label="新建账号自动匹配"></span><span class="fs13">后续新建账号自动匹配规则</span></div></div>
  <div class="mt16">{alert('预览：<b>将影响 12 个账号</b> —— 2024级团支部 3 个 → 陈思远；学生社团 8 个 → 孙浩；青年志愿者协会 1 个 → 赵敏。分配完成后将通知相关教师，原负责教师的在办事项保留至办结。', 'warning')}</div>
</div>"""
    footer = (btn("取消", "assign.html", "default")
              + btn("预览明细", None, "ghost", "eye", toast="已展开 12 个受影响账号", attrs='data-toggle="#rule-preview"')
              + submit_btn("确认分配", "assign.html", "primary", "check", toast="已按规则完成分配，共 12 个账号"))
    content = f'<div class="backdrop">{assign_content()}</div>' + modal("按规则批量分配", body, footer, "lg", close_href="assign.html")
    page("assign-batch.html", "assign", "批量分配规则", cr(("任务分派", "assign.html"), ("批量分配规则", None)), content, ASSIGN_JS)


# ---------------------------------------------------------------- 13 教师工作量
def teachers():
    rows = []
    for t in TEACHERS:
        nd = t["nodes"]
        href = teacher_href(t["name"])
        rows.append(dict(cells=[
            person(t["name"], ""), f'<div class="fs13">{t["job"]}</div><div class="small muted">{t["scope"]}</div>',
            f'<b class="num">{t["total"]}</b>',
            f'<span class="num {"c-warning bold" if nd[1] else "muted"}">{nd[1]}</span>',
            f'<span class="num">{nd[4]}</span>',
            f'<span class="num {"c-danger bold" if t["zombie"] else "muted"}">{t["zombie"]}</span>',
            f'<span class="num {"c-warning bold" if t["rectify"] else "muted"}">{t["rectify"]}</span>',
            pct_cell(nd[4], t["total"]),
            ops(("查看", href), ("催办", None, f'已向{t["name"]}老师发送待审核事项催办')),
        ], href=href))
    tot = sum(t["total"] for t in TEACHERS)
    content = f"""{page_hd('教师工作量', '每名教师负责账号数、待审核、已完成、疑似僵尸号与待整改情况；点击查看其负责账号',
                   btn('导出教师负责账号清单', 'export.html', 'default', 'download') + btn('一键催办', None, 'primary', 'bell', toast='已向有待审核事项的 3 名教师发送催办'))}
<div class="grid g4 mb16">
  {stat('业务教师', CS['teachers'], '辅导员 4 · 专项负责 2', 'users')}
  {stat('已分配账号', tot, '未分配 2 个', 'route', href='assign.html')}
  {stat('教师待审核', 4, '王晓琳 2 · 陈思远 1 · 孙浩 1', 'inbox', 'orange')}
  {stat('人均负责', '%.1f' % (tot / len(TEACHERS)), '最多：王晓琳 11 个', 'chart', 'gray')}
</div>
<div class="card card-bd">
  <div class="toolbar"><span class="card-title">教师列表</span>{btn('任务分派', 'assign.html', 'light', 'route', 'sm')}</div>
  {table(['教师', '岗位 / 授权范围', '负责账号总数', '待审核数', '已完成数', '疑似僵尸号', '待整改', '年审完成率', '操作'], rows)}
</div>"""
    page("teachers.html", "teachers", "教师工作量", cr(("任务与人员", None), ("教师工作量", None)), content)


def xfer_ops(name):
    return (f'<div class="ops"><a class="link" href="../common/archive-basic.html">档案</a>'
            f'<button class="link" type="button" data-toggle="#xfer-modal" data-xfer="{esc(name)}">更换负责教师</button></div>')


def other_teacher_panels():
    parts = []
    for t in TEACHERS:
        if t["name"] == "王晓琳":
            continue
        owned = [a for a in college_accounts() if a["teacher"] == t["name"]]
        if owned:
            body_rows = [dict(cells=[acct(a["name"], a["platform"], a["org"]), tag(a["level"], "muted"), a["student"],
                                     st2(a["run"]), st2(a["annual"]), xfer_ops(a["name"])]) for a in owned]
            table_html = table(["账号", "平台层级", "学生负责人", "运行状态", "年审状态", "操作"], body_rows, check=True)
        else:
            table_html = alert(f'{t["name"]}老师负责范围内的账号尚未在本院清单中单列。可在任务分派中查看或调整。', "info") + '<div class="mt12">' + btn("去任务分派", "assign.html", "light", "route", "sm") + "</div>"
        av = avatar(t["name"], "lg") if t["name"] in AVATARS else f'<span class="ini lg">{t["name"][0]}</span>'
        nd = t["nodes"]
        profile = f"""<div class="flex gap16">{av}<div class="grow">
  <div class="flex gap8"><span class="fs18 bold">{t["name"]}</span>{tag("业务教师", "primary")}</div>
  <div class="small muted mt4">{t["job"]}</div>
  <div class="small sub mt4">{t["scope"]}</div></div>
  <div class="flex gap8">{btn("调整授权", "users.html", "default", "key")}<button class="btn btn-ghost" type="button" data-toggle="#xfer-modal" data-xfer-batch="1">{icon("swap")}批量移交</button></div></div>"""
        kpis = "".join([
            stat("负责账号", t["total"], "授权范围内", "database"),
            stat("待审核", nd[1], "年审节点", "inbox", "orange"),
            stat("已完成年审", nd[4], "完成率 %d%%" % round(nd[4] / t["total"] * 100), "check-circle", "green"),
            stat("疑似僵尸号", t["zombie"], "待核实或已处置", "ghost", "red", href="zombie.html"),
            stat("待整改", t["rectify"], "整改任务", "wrench", "orange", href="rectify.html"),
        ])
        listed = len(owned)
        head_n = ("清单中的账号（%d / %d）" % (listed, t["total"])) if listed else ("负责账号（%d）" % t["total"])
        parts.append(f"""<div data-teacher-panel="{esc(t["name"])}" class="hidden">
{page_hd("教师负责账号", t["name"] + "老师的授权范围与负责账号；可更换负责教师或批量移交", back_btn("teachers.html") + btn("任务分派", "assign.html", "primary", "route"))}
{card("", profile)}
<div class="grid g5 mt16">{kpis}</div>
<div class="card card-bd mt16">
  <div class="toolbar"><span class="card-title">{head_n}</span>
  <div class="flex gap8"><span class="small sub">已选 <b class="c-primary" data-checked-count="#td-table">0</b> 个</span><button class="btn btn-light btn-sm" type="button" data-toggle="#xfer-modal" data-xfer-batch="1">{icon("swap")}批量移交</button></div></div>
  {table_html}
</div></div>""")
    return "".join(parts)


def xfer_modal():
    opts = "".join(f"<option>{n}</option>" for n in TEACHER_NAMES)
    body = f"""<div class="bold mb8" id="xfer-title">更换负责教师</div>
<div class="small sub mb12">选择接收教师后，账号及未办结事项一并移交，操作记入日志。</div>
{field("接收教师", f'<select class="select" id="xfer-teacher"><option value="">请选择接收教师</option>{opts}</select>', True)}"""
    return (f'<div class="mask hidden" id="xfer-modal"><div class="modal"><div class="modal-hd">移交负责教师'
            f'<button class="x-btn" type="button" data-toggle="#xfer-modal" aria-label="关闭">{icon("x")}</button></div>'
            f'<div class="modal-bd">{body}</div><div class="modal-ft">'
            f'<button class="btn btn-default" type="button" data-toggle="#xfer-modal">取消</button>'
            f'<button class="btn btn-primary" type="button" onclick="saveXfer()">确认移交</button></div></div></div>')


TEACHER_JS = r"""
(function(){
  var q=location.search.match(/[?&]t=([^&]+)/);
  var name=q?decodeURIComponent(q[1]):'王晓琳';
  var panels=document.querySelectorAll('[data-teacher-panel]');
  var hit=false;
  panels.forEach(function(p){
    var on=p.getAttribute('data-teacher-panel')===name;
    if(on)hit=true;
    p.classList.toggle('hidden',!on);
    var tb=p.querySelector('table');
    if(tb){if(on)tb.id='td-table';else tb.removeAttribute('id');}
  });
  if(!hit&&panels[0]){panels[0].classList.remove('hidden');var tb0=panels[0].querySelector('table');if(tb0)tb0.id='td-table';name='王晓琳';}
  var tab=document.querySelector('.zx-tab.on');
  if(tab&&tab.firstChild&&tab.firstChild.nodeType===3)tab.firstChild.textContent=name;
})();
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-xfer]');
  if(b){window._xferRow=b.closest('tr');window._xferBatch=false;
    var title=document.getElementById('xfer-title');if(title)title.textContent='更换负责教师 · '+b.getAttribute('data-xfer');}
  var batch=e.target.closest('[data-xfer-batch]');
  if(batch){window._xferRow=null;window._xferBatch=true;
    var title2=document.getElementById('xfer-title');if(title2)title2.textContent='批量移交负责教师';}
});
function saveXfer(){
  var sel=document.getElementById('xfer-teacher');
  var who=sel?sel.value:'';
  if(!who){toast('请选择接收教师');return;}
  function mark(tr){
    if(!tr)return;
    var cb=tr.querySelector('input[type=checkbox]');
    if(cb){cb.checked=false;cb.disabled=true;}
    var last=tr.lastElementChild;
    if(last)last.innerHTML='<span class="tag tag-success">已移交 '+who+'</span>';
  }
  if(window._xferBatch){
    var tb=document.getElementById('td-table');
    var rows=tb?[].slice.call(tb.querySelectorAll('tbody tr')).filter(function(tr){var c=tr.querySelector('input[type=checkbox]');return c&&c.checked;}):[];
    if(!rows.length){toast('请先勾选要移交的账号');return;}
    rows.forEach(mark);
    toast('已将 '+rows.length+' 个账号移交给 '+who+'，待办同步转移');
  }else if(window._xferRow){
    mark(window._xferRow);
    toast('已移交给 '+who+'，待办同步转移');
  }else{toast('请从账号行进入移交');return;}
  document.querySelectorAll('[data-checked-count]').forEach(function(n){n.textContent='0';});
  document.getElementById('xfer-modal').classList.add('hidden');
}
"""


def teacher_detail():
    p = PEOPLE["王晓琳"]
    scopes = [("宣传工作辅导员", "学院团委直属组织：团委、新媒体中心、学生会、研究生会、科协、青年志愿者协会", 6),
              ("2021级辅导员", "2021级各班团支部（已毕业，待注销处置）", 2),
              ("街舞社等社团指导教师", "计院街舞社、计院ACM协会、计院摄影协会", 3)]
    scope_html = "".join(f'<div class="id-card"><div class="flex between">{tag(s, "primary")}<span class="small sub">{n} 个账号</span></div>'
                         f'<div class="small sub mt8">{d}</div></div>' for s, d, n in scopes)
    profile = f"""<div class="flex gap16">{avatar('王晓琳', 'lg')}<div class="grow">
  <div class="flex gap8"><span class="fs18 bold">王晓琳</span>{tag('业务教师', 'primary')}{tag('一人三身份', 'warning')}</div>
  <div class="small muted mt4">工号 {p['no']} · {p['org']} · {p['phone']}</div>
  <div class="small sub mt4">{p['job']}</div></div>
  <div class="flex gap8">{btn('调整授权', 'users.html', 'default', 'key')}<button class="btn btn-ghost" type="button" data-toggle="#xfer-modal" data-xfer-batch="1">{icon('swap')}批量移交</button></div></div>
<div class="grid g3 mt16">{scope_html}</div>"""
    keys = ["annual", "new", "rename", "idchange", "rectify", "handover", "proxy", "photo", "zombie"]
    source = {"annual": "宣传工作辅导员", "new": "宣传工作辅导员", "rename": "宣传工作辅导员", "idchange": "宣传工作辅导员",
              "rectify": "宣传工作辅导员", "handover": "社团指导教师", "proxy": "社团指导教师", "photo": "社团指导教师", "zombie": "2021级辅导员"}
    rows = []
    for k in keys:
        a = ACCOUNTS[k]
        rows.append([acct(a["name"], a["platform"], a["org"]), tag(source[k], "muted"), a["student"], st2(a["run"]), st2(a["annual"]),
                     xfer_ops(a["name"])])
    for a in EXTRA_ACCTS:
        if a["teacher"] == "王晓琳":
            src = "2021级辅导员" if a["name"].startswith("2021") else "宣传工作辅导员"
            rows.append([acct(a["name"], a["platform"], a["org"]), tag(src, "muted"), a["student"], st2(a["run"]), st2(a["annual"]),
                         xfer_ops(a["name"])])
    t = TEACHERS[0]
    kpis = "".join([stat("负责账号", t["total"], "三类身份授权", "database"), stat("待审核", t["nodes"][1], "年审 2", "inbox", "orange"),
                    stat("已完成年审", t["nodes"][4], "完成率 %d%%" % round(t["nodes"][4] / t["total"] * 100), "check-circle", "green"),
                    stat("疑似僵尸号", t["zombie"], "2021级团支部 2", "ghost", "red", href="zombie.html"),
                    stat("待整改", t["rectify"], "计院青年志愿者", "wrench", "orange", href="rectify.html")])
    content = f"""{page_hd('教师负责账号', '王晓琳老师的授权范围与负责账号；可逐个更换负责教师或批量移交',
                   back_btn('teachers.html') + btn('任务分派', 'assign.html', 'primary', 'route'))}
{card('', profile)}
<div class="grid g5 mt16">{kpis}</div>
<div class="card card-bd mt16">
  <div class="toolbar"><span class="card-title">负责账号（{len(rows)}）</span>
  <div class="flex gap8"><span class="small sub">已选 <b class="c-primary" data-checked-count="#td-table">0</b> 个</span><button class="btn btn-light btn-sm" type="button" data-toggle="#xfer-modal" data-xfer-batch="1">{icon('swap')}批量移交</button></div></div>
  {table(['账号', '授权来源', '学生负责人', '运行状态', '年审状态', '操作'], rows, check=True, id_='td-table')}
</div>"""
    content = f'<div data-teacher-panel="王晓琳">{content}</div>' + other_teacher_panels() + xfer_modal()
    page("teacher-detail.html", "teachers", "教师负责账号", cr(("教师工作量", "teachers.html"), ("王晓琳", None)), content, TEACHER_JS)


# ---------------------------------------------------------------- 14 僵尸号核实
def zombie():
    z, ph = ACCOUNTS["zombie"], ACCOUNTS["photo"]
    rows = [
        dict(cells=[acct(z["name"], z["platform"], "三级平台 · 组织已毕业"), z["last_post"], f'<b class="c-danger num">{z["idle_days"]} 天</b>',
                    '<div class="flex gap4 wrap">' + tag("停更 ≥ 180 天", "danger") + tag("团支部已毕业", "danger") + '</div>', st("高风险"),
                    f'{tag("辅导员已核实", "success")}<div class="small muted mt4">待学院审核 · 建议注销</div>', person("王晓琳"),
                    ops(("审核", "zombie-verify-detail.html"))], href="zombie-verify-detail.html", cat="todo college"),
        dict(cells=[acct(ph["name"], ph["platform"], "社团平台 · 组织存续"), ph["last_post"], f'<b class="c-warning num">{ph["idle_days"]} 天</b>',
                    tag("停更 ≥ 180 天", "warning"), st("中风险"), f'{tag("学生核实中", "primary")}<div class="small muted mt4">李明 · 截止 2026-10-08</div>',
                    person("李明"), ops(("催办", None, "已向李明发送核实催办"), ("档案", "../common/archive-basic.html"))], cat="todo"),
        dict(cells=[acct("2021级计算机科学3班团支部", "QQ", "三级平台 · 组织已毕业"), "2025-05-28", '<b class="c-danger num">490 天</b>',
                    '<div class="flex gap4 wrap">' + tag("停更 ≥ 180 天", "danger") + tag("团支部已毕业", "danger") + '</div>', st("高风险"),
                    f'{tag("待教师核实", "warning")}<div class="small muted mt4">已分派 2026-09-01</div>', person("王晓琳"),
                    ops(("催办", None, "已向王晓琳老师发送核实催办"), ("档案", "../common/archive-basic.html"))], cat="todo"),
        dict(cells=[acct("2020级计算机科学1班团支部", "QQ", "三级平台 · 已注销"), "2024-07-02", '<span class="muted num">—</span>',
                    tag("团支部已毕业", "muted"), st("已处置"), tag("已注销 · 2026-06-30", "muted"), person("王晓琳"),
                    ops(("查看", "../common/archive-cancel.html"))], href="../common/archive-cancel.html", cat="done"),
        dict(cells=[acct("计院书画协会", "微信公众号", "社团平台 · 核实正常"), "2026-04-26", '<span class="muted num">—</span>',
                    tag("停更 ≥ 180 天", "muted"), st("已处置"), tag("核实正常 · 2026-05-12", "success"), person("孙浩"),
                    ops(("查看", "../common/archive-logs.html"))], href="../common/archive-logs.html", cat="done"),
        dict(cells=[acct("2022级网络工程2班团支部", "微信公众号", "三级平台 · 整改完成"), "2026-02-11", '<span class="muted num">—</span>',
                    tag("信息不完整", "muted"), st("已处置"), tag("转整改 · 已通过", "success"), person("刘洋"),
                    ops(("查看", "../common/archive-rectify.html"))], href="../common/archive-rectify.html", cat="done"),
    ]
    tabs = seg([("全部 6", "all"), ("待处理 3", "todo"), ("待学院审核 1", "college"), ("已处置 3", "done")], target="#zb-table")
    flow = steps(["系统预警", "学生 / 教师核实", "学院审核", "正常 / 整改 / 注销", "必要时报校团委确认"], 2)
    content = f"""{page_hd('僵尸号核实', '系统按规则自动预警本院疑似僵尸号，经核实与学院审核后处置',
                   btn('预警规则说明', None, 'default', 'help', toast='停更 ≥ 180 天、组织已毕业 / 撤销、负责人离校、账号无法访问等规则，由校团委统一配置') + btn('一键催办核实', None, 'primary', 'bell', toast='已向 2 名核实人发送催办'))}
<div class="grid g4 mb16">
  {stat('疑似僵尸号', CS['zombie'], '占本院账号 8.3%', 'ghost', 'red')}
  {stat('待学院审核', 1, '辅导员已核实', 'inbox', 'orange', href='zombie-verify-detail.html')}
  {stat('核实中', 2, '学生 1 · 教师 1', 'search')}
  {stat('本年度已处置', 3, '注销 1 · 正常 1 · 整改 1', 'check-circle', 'green')}
</div>
{card('处置流程', flow + '<div class="mt16">' + alert('处置流程：<b>预警 → 学生或教师核实 → 学院审核 → 正常 / 整改 / 注销 → 必要时报校团委</b>。系统只做预警，<b>不直接注销账号</b>；注销须经学院审核并报校团委确认，数据永久保留。', 'info') + '</div>')}
<div class="card card-bd mt16">
  <div class="toolbar">{tabs}<span class="small muted">数据截至 2026-09-30 02:00 自动巡检</span></div>
  {table(['账号', '最近发布', '停更天数', '命中规则', '风险等级', '核实进度', '核实人', '操作'], rows, id_='zb-table')}
</div>"""
    page("zombie.html", "zombie", "僵尸号核实", cr(("风险治理", None), ("僵尸号核实", None)), content)


def zombie_verify_detail():
    z, f = ACCOUNTS["zombie"], FLOWS["zombie"]
    head = acct_head(z, st(z["run"]) + st(z["filing"]) + st("疑似僵尸号") + st("高风险"))
    info = kv([("平台 ID", z["pid"]), ("所属组织", f'{z["org"]} {tag("已毕业", "muted")}'), ("平台层级", z["level"]),
               ("开通时间", z["opened"]), ("最近发布", f'<b>{z["last_post"]}</b>'), ("停更天数", f'<b class="c-danger">{z["idle_days"]} 天</b>'),
               ("粉丝数", z["fans"]), ("管理教师", z["teacher"]), ("学生负责人", z["student"])], 3)
    rules = table(["预警规则", "阈值", "实际情况", "结果"], [
        ["停更时长", "≥ 180 天", "412 天（最近发布 2025-08-14）", tag("命中", "danger")],
        ["组织存续状态", "已毕业 / 已撤销", "2021级软件工程1班团支部 · 2025-06 毕业", tag("命中", "danger")],
        ["学生负责人状态", "毕业 / 离校", "原团支书已毕业，无接任人", tag("命中", "danger")],
        ["账号可访问性", "无法访问", "可正常访问", tag("未命中", "muted")],
    ], cls="tbl-sm")
    v_when, _, v_title, v_cmt = f["steps"][1]
    evidence = "".join(f'<span class="file-chip">{icon("file")}{x}</span>' for x in
                       ["2025届软件工程1班毕业名单.pdf", "公众号后台发布记录截图.png", "原团支书确认聊天记录.jpg"])
    verify = f"""<div class="opinion warn">
  <div class="flex gap12">{avatar('王晓琳')}<div class="grow"><div class="bold">辅导员核实结果 · 王晓琳 {tag('建议注销', 'warning')}</div>
  <div class="small muted">2021级辅导员 · {v_when}</div></div></div>
  <div class="quote">“团支部已于 2025 年 6 月毕业，建议注销。{v_cmt}”</div>
  <div class="small muted mt12">核实佐证</div><div class="upload-list">{evidence}</div>
</div>"""
    choices = [("转注销", "团支部已毕业、无人运营，报校团委确认后注销，数据永久保留", True),
               ("转整改", "仍有组织需要保留，指定新负责人并限期恢复更新", False),
               ("核实正常", "账号仍在正常运营，解除预警", False)]
    ch_html = "".join(
        f'<button type="button" class="choice{" on" if on else ""}" data-choice=""><span class="ck"></span><div class="grow">'
        f'<div class="bold fs13">{t}</div><div class="small muted">{d}</div></div></button>' for t, d, on in choices)
    c_cmt = f["steps"][2][3]
    decide = (f'<div class="grid g3" data-single="">{ch_html}</div>'
              f'<div class="mt16">{field("学院审核意见", textarea("请输入学院审核意见", c_cmt, maxlen=200, rows=3), req=True)}</div>'
              f'<div class="mt12">{alert("转注销后由校团委确认，账号状态转为“已注销”，历史发布记录、年审与操作日志永久保留，不可删除。", "info")}</div>')
    tl = flow_items("zombie", 2) + [("now", "学院审核", "当前节点 · 周建华", ""), ("wait", "校团委确认", "待流转 · 陈静", "")]
    left = f"""{card('', head + '<div class="divider"></div>' + info)}
{card('触发规则', rules, tag('命中 3 / 4', 'danger'), cls='mt16')}
<div class="mt16">{verify}</div>
{card('学院处置', decide, cls='mt16')}"""
    right = f"""<div class="sticky col gap16">
  {card('处置流程', timeline(tl), tag(f['no'], 'muted'))}
  {card('关联信息', kv([('关联组织', '2021级软件工程1班团支部'), ('组织状态', tag('已毕业', 'muted')), ('本年度年审', st(z['annual'])), ('同班其他账号', '无')], 2) + '<div class="mt12">' + btn('查看账号档案', '../common/archive-basic.html', 'default', 'archive', 'sm') + '</div>')}
</div>"""
    content = f"""{page_hd('僵尸号 · 学院审核', '剧本七：辅导员已核实团支部毕业并建议注销，学院审核后报校团委确认',
                   back_btn('zombie.html') + scene_next('校团委确认注销', '../school/zombie-detail.html'))}
<div class="split" data-form>
  <div>{left}</div>
  {right}
</div>
<div class="actbar"><span class="grow">{icon('info', 14)} 系统不直接注销账号；学院审核转注销后须报校团委确认</span>
  {btn('退回教师重核', '../common/modal-return.html', 'default', 'undo')}
  {go('核实正常', 'zombie.html', 'default', 'check-circle', toast='已核实正常，解除僵尸号预警')}
  {btn('转整改', 'rectify-create.html', 'warning', 'wrench')}
  {go('转注销并报校团委', '../school/zombie-detail.html', 'primary', 'send', toast='已转注销，报校团委确认')}
</div>"""
    page("zombie-verify-detail.html", "zombie", "僵尸号 · 学院审核", cr(("僵尸号核实", "zombie.html"), (z["name"], None)), content)


# ---------------------------------------------------------------- 15 整改管理
def rectify():
    r, f = ACCOUNTS["rectify"], FLOWS["rectify"]
    rows = [
        dict(cells=[f'<span class="num">{f["no"]}</span>', acct(r["name"], r["platform"], r["org"]), tag("年审整改", "primary"),
                    '<div class="small">未建立信息发布审查机制；内容未执行“先审后发”</div>', person("何雨桐"), f["deadline"],
                    tag("第 1 轮", "muted"), st("待审核"), ops(("审核", "rectify-detail.html"))], href="rectify-detail.html", cat="doing review"),
        dict(cells=['<span class="num">ZG20260918002</span>', acct("2023级网络工程1班团支部", "QQ", "2023级网络工程1班团支部"), tag("年审整改", "primary"),
                    '<div class="small">账号信息不完整，缺学生管理员及认证信息</div>', person("周可欣"), "2026-10-15",
                    tag("第 1 轮", "muted"), st("进行中"), ops(("催办", None, "已向周可欣发送整改催办"), ("档案", "../common/archive-rectify.html"))],
             cat="doing"),
        dict(cells=['<span class="num">ZG20260910003</span>', acct(ACCOUNTS["photo"]["name"], ACCOUNTS["photo"]["platform"], "计院摄影协会"), tag("年审整改", "primary"),
                    '<div class="small">停更 212 天，学生管理员信息缺失；当前在指导教师复核</div>', person("李明"), "2026-10-20",
                    tag("第 1 轮", "muted"), tag("教师复核中", "primary", True),
                    ops(("催办", None, "已向王晓琳老师发送复核催办"), ("查看进度", "../teacher/review-rectify.html"))],
             href="../teacher/review-rectify.html", cat="doing"),
        dict(cells=['<span class="num">ZG20260612004</span>', acct("计院篮球协会", "抖音", "计院篮球协会"), tag("内容巡查", "warning"),
                    '<div class="small">内容未执行“先审后发”</div>', person("刘子豪"), "2026-06-30", tag("第 1 轮", "muted"), st("整改通过"),
                    ops(("查看", "../common/archive-rectify.html"))], href="../common/archive-rectify.html", cat="done"),
        dict(cells=['<span class="num">ZG20260315003</span>', acct("2022级网络工程2班团支部", "微信公众号", "2022级网络工程2班团支部"), tag("僵尸号转整改", "danger"),
                    '<div class="small">长期未更新（停更 196 天）</div>', person("黄思琪"), "2026-04-15", tag("第 2 轮", "muted"), st("整改通过"),
                    ops(("查看", "../common/archive-rectify.html"))], href="../common/archive-rectify.html", cat="done"),
        dict(cells=['<span class="num">ZG20251120006</span>', acct(ACCOUNTS["photo"]["name"], "视频号", "计院摄影协会"), tag("年审整改", "primary"),
                    '<div class="small">负责人信息缺失</div>', person("李明"), "2025-12-10", tag("第 1 轮", "muted"), st("整改通过"),
                    ops(("查看", "../common/archive-rectify.html"))], href="../common/archive-rectify.html", cat="done"),
        dict(cells=['<span class="num">ZG20251108005</span>', acct("计院人工智能协会", "哔哩哔哩", "计院人工智能协会"), tag("数据异常", "warning"),
                    '<div class="small">未备案先运营，补办备案</div>', person("张子涵"), "2025-11-30", tag("第 1 轮", "muted"), st("整改通过"),
                    ops(("查看", "../common/archive-rectify.html"))], href="../common/archive-rectify.html", cat="done"),
    ]
    def ncat(key):
        return sum(1 for r in rows if key in r["cat"].split())
    tabs = seg([(f"全部 {len(rows)}", "all"), (f"进行中 {ncat('doing')}", "doing"), (f"待我审核 {ncat('review')}", "review"),
                (f"已完成 {ncat('done')}", "done")], target="#rf-table")
    content = f"""{page_hd('本院整改', '跟踪本院整改任务：下发 → 学生提交 → 学院审核（整改通过 / 继续整改 / 转注销），全部轮次永久留痕',
                   btn('导出整改台账', 'export.html', 'default', 'download') + btn('下发整改', 'rectify-create.html', 'primary', 'plus'))}
<div class="grid g4 mb16">
  {stat('进行中', ncat('doing'), '含教师复核中 1 个', 'wrench', 'orange')}
  {stat('待学院审核', 1, '第 1 轮材料已提交', 'inbox', href='rectify-detail.html')}
  {stat('临近截止', 1, '7 天内到期', 'clock', 'red')}
  {stat('本年度已整改', 4, '一次通过率 75%', 'check-circle', 'green')}
</div>
<div class="card card-bd">
  <div class="toolbar">{tabs}<label class="top-search" style="width:260px">{icon('search')}<input placeholder="搜索任务编号 / 账号" data-search="#rf-table"></label></div>
  {table(['任务编号', '整改账号', '来源', '整改问题', '整改责任人', '截止时间', '轮次', '状态', '操作'], rows, id_='rf-table')}
</div>"""
    page("rectify.html", "rectify", "本院整改", cr(("风险治理", None), ("本院整改", None)), content)


def rectify_create():
    r, f = ACCOUNTS["rectify"], FLOWS["rectify"]
    src_when, _, _, src_cmt = f["steps"][0]
    req_cmt = f["steps"][1][3]
    issues = [("未建立信息发布审查机制", True), ("内容未执行“先审后发”", True), ("账号信息不完整", False), ("长期未更新", False),
              ("负责人信息缺失", False), ("四项机制不健全", False), ("其他", False)]
    issue_html = "".join(f'<button type="button" class="chip{" on" if on else ""}" data-choice="">{t}</button>' for t, on in issues)
    target = (f'<div class="flex gap12" style="padding:12px 14px;border:1px solid var(--c-line);border-radius:8px;background:#FAFCFE">'
              f'{acct(r["name"], r["platform"], r["org"] + " · " + r["level"])}<span class="ml-auto flex gap8">{st(r["run"])}{st("待整改")}</span></div>')
    form = f"""<div class="form-section">整改对象</div>
<div class="form-grid">
  {field('整改账号', target, req=True, cls='full')}
  {field('整改来源', inp(val='年审整改 · 年审编号 NS2026-CS-0019', readonly=True))}
  {field('发起依据', inp(val='王晓琳老师年审审核意见（' + src_when + '）', readonly=True))}
</div>
<div class="form-section mt24">整改内容</div>
<div class="form-grid c1">
  {field('整改问题', '<div class="chips">' + issue_html + '</div>', req=True, hint='可多选；已按教师年审意见预选')}
  {field('整改要求', textarea('请填写具体整改要求', req_cmt, req=True, maxlen=300, rows=3), req=True)}
</div>
<div class="form-section mt24">责任与时限</div>
<div class="form-grid">
  {field('学生整改责任人', sel(['何雨桐（8209230509）', '李明（8209230117）'], '何雨桐（8209230509）', req=True), req=True)}
  {field('指导教师', sel(TEACHER_NAMES, '王晓琳', req=True), req=True)}
  {field('截止时间', inp(val=f['deadline'], typ='date', req=True), req=True, hint='距今 20 天；逾期未提交将自动提醒学院')}
  {field('审核层级', radios('level', ['学院审核', '报校团委审核'], '学院审核'), hint='一般整改由学院审核办结；重大问题可报校团委')}
  {field('附件', upload('上传整改参考材料', '如制度模板、问题截图等', files=['新媒体信息发布审查制度（参考模板）.docx', '问题内容截图.png']), cls='full')}
</div>
<div class="mt16"><div class="field-label mb8">通知方式</div><label class="cb"><input type="checkbox" checked>站内信</label><div class="mt8"><label class="cb"><input type="checkbox" checked>ITS 消息</label></div></div>"""
    tl = flow_items("rectify", 1) + [("now", "学院下发整改任务", "当前 · 周建华", ""), ("wait", "学生提交整改材料", "何雨桐", ""),
                                     ("wait", "学院审核整改结果", "整改通过 / 继续整改 / 转注销", "")]
    right = f"""<div class="sticky col gap16">
  <div class="opinion warn"><div class="flex gap12">{avatar('王晓琳')}<div class="grow"><div class="bold">教师年审意见 {tag('要求整改', 'danger')}</div>
  <div class="small muted">王晓琳 · {src_when}</div></div></div><div class="quote fs13">“{src_cmt}”</div></div>
  {card('整改流程', timeline(tl))}
</div>"""
    content = f"""{page_hd('下发整改任务', '剧本六：依据指导教师年审意见，向账号学生负责人下发整改任务',
                   back_btn('rectify.html') + scene_next('学生端查看整改任务', '../../app/student/rectify.html'))}
<div data-form>
{alert(f'来源：王晓琳老师年审审核要求整改（{src_when[:10]}）。已自动带入整改账号、问题与责任人，请确认后下发。', 'warning')}
<div class="split mt16">
  {card('整改任务信息', form)}
  {right}
</div>
<div class="actbar"><span class="grow">{icon('info', 14)} 下发后学生将在移动端收到整改待办；整改期间账号运行状态为“整改中”</span>
  {back_btn('rectify.html', '取消')}
  {btn('保存草稿', None, 'default', 'file', toast='已保存为草稿')}
  {submit_btn('下发整改任务', 'rectify.html', 'primary', 'send', toast='整改任务已下发，已通知何雨桐')}
</div>
</div>"""
    page("rectify-create.html", "rectify", "下发整改任务", cr(("本院整改", "rectify.html"), ("下发整改任务", None)), content)


def rectify_detail():
    r, f = ACCOUNTS["rectify"], FLOWS["rectify"]
    s_when, _, _, s_cmt = f["steps"][2]
    judge_cmt = f["steps"][3][3]
    task = kv([("任务编号", f'<span class="num">{f["no"]}</span>'), ("整改账号", r["name"] + "（小红书）"), ("整改来源", "年审整改 · 王晓琳 2026-09-19"),
               ("整改问题", tag("未建立信息发布审查机制", "danger") + " " + tag("内容未执行“先审后发”", "danger"), True),
               ("整改要求", f["steps"][1][3], True),
               ("整改责任人", "何雨桐（学生） / 王晓琳（指导教师）"), ("截止时间", f'{f["deadline"]} <span class="small c-warning">剩 20 天</span>'),
               ("当前轮次", tag("第 1 轮 · 待学院审核", "warning"))], 3)
    files = "".join(f'<span class="file-chip">{icon("file")}{x}</span>' for x in
                    ["信息发布三审制度.pdf", "9月推文审核记录.xlsx", "审核流程截图.png"])
    submission = f"""<div class="flex gap12 mb16">{avatar('何雨桐')}<div class="grow"><div class="bold">何雨桐 · 计院青年志愿者协会宣传部部长</div>
<div class="small muted">第 1 次提交 · {s_when}</div></div>{tag('第 1 轮', 'primary')}</div>
{kv([('整改说明', s_cmt + '由宣传部起草，经协会会长审阅后执行，规定所有笔记发布前须经三级审核。', True),
     ('整改结果', '已建立审查机制；9 月 20 日起所有笔记执行“编辑初审、部长复审、指导教师终审”。', True),
     ('更新后信息', '信息审核人：王晓琳；审核流程：学生编辑初审 → 宣传部长复审 → 指导教师终审', True),
     ('证明材料', f'<div class="upload-list" style="margin-top:0">{files}</div>', True)], 3)}
<div class="mt12">{alert('材料核验：制度文件未见指导教师签字及学院盖章；审核记录仅覆盖 9 月，未包含 7-8 月。', 'danger')}</div>"""
    choices = [("整改通过", "材料齐全，问题已整改到位，年审恢复流转", ".rd-pass", False),
               ("继续整改", "材料不完整或整改不到位，退回学生继续整改", ".rd-cont", True),
               ("转注销", "拒不整改或无法整改，转入注销流程", ".rd-cancel", False)]
    ch_html = "".join(
        f'<button type="button" class="choice{" on" if on else ""}" data-choice="{sel_}"><span class="ck"></span><div class="grow">'
        f'<div class="bold fs13">{t}</div><div class="small muted">{d}</div></div></button>' for t, d, sel_, on in choices)
    panes = f"""<div class="rd-pane rd-cont mt16">
  {field('继续整改意见', textarea('请说明需继续整改的内容', judge_cmt, req=True, maxlen=300, rows=3), req=True)}
  <div class="form-grid mt12">{field('第 2 轮截止时间', inp(val=f['deadline'], typ='date'))}{field('补充要求', inp(val='补充签字盖章版制度及 7-9 月审核台账'))}</div>
</div>
<div class="rd-pane rd-pass mt16 hidden">
  {field('审核意见', textarea('请输入审核意见', '材料齐全，整改通过。', maxlen=300, rows=3))}
  <div class="mt12">{alert('整改通过后，该账号年审状态恢复为“待学院审核”，运行状态恢复为“正常运行”。', 'success')}</div>
</div>
<div class="rd-pane rd-cancel mt16 hidden">
  {alert('转注销需发起账号注销申请，填写注销原因与佐证材料，经校团委确认后账号转为“已注销”，数据永久保留。', 'warning')}
</div>"""
    tl = flow_items("rectify", 3) + [("now", "学院审核第 1 轮整改材料", "当前节点 · 周建华", ""),
                                     ("wait", "学生第二次提交整改材料", "何雨桐", ""), ("wait", "学院复核整改结果", "周建华", "")]
    left = f"""{card('整改任务', task)}
{card('第 1 轮提交材料', submission, cls='mt16')}
{card('整改审核结果', f'<div class="grid g3" data-single=".rd-pane">{ch_html}</div>{panes}', cls='mt16')}
<div class="mt16">{alert('全部历史整改记录（每一轮的提交材料与审核意见）永久保留，可在 <a class="link" href="../common/archive-rectify.html">账号档案 · 整改记录</a> 中查看。', 'info', 'archive')}</div>"""
    right = f"""<div class="sticky col gap16">
  {card('整改轮次', timeline(tl), tag(f['no'], 'muted'))}
  {card('历史整改', '<div class="small sub">该账号近 3 年无其他整改记录。</div>')}
</div>"""
    content = f"""{page_hd('整改审核', '剧本六：审核学生第 1 轮整改材料 —— 判定继续整改',
                   back_btn('rectify.html') + scene_next('第二轮提交后移动端审核', '../../app/college/rectify.html'))}
<div class="split" data-form>
  <div>{left}</div>
  {right}
</div>
<div class="actbar"><span class="grow">{icon('info', 14)} 选择审核结果后提交；继续整改将生成第 2 轮整改待办</span>
  {btn('查看档案整改记录', '../common/archive-rectify.html', 'default', 'archive')}
  <span class="rd-pane rd-cont flex gap8">{submit_btn('提交：继续整改', 'rectify.html', 'danger-solid', 'undo', toast='已退回继续整改，学生将收到待办')}</span>
  <span class="rd-pane rd-pass flex gap8 hidden">{submit_btn('提交：整改通过', 'rectify.html', 'success', 'check', toast='整改通过，年审恢复流转')}</span>
  <span class="rd-pane rd-cancel flex gap8 hidden">{btn('转注销：发起注销申请', '../common/apply-cancel.html', 'danger', 'ban')}</span>
</div>"""
    page("rectify-detail.html", "rectify", "整改审核", cr(("本院整改", "rectify.html"), ("整改审核 · " + r["name"], None)), content)


# ---------------------------------------------------------------- 16 导入数据确认
FILL_JS = """
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-fname]');if(!b)return;
  window._fillRow=b.closest('tr');
  document.getElementById('fill-title').textContent='补全 · '+b.getAttribute('data-fname');
  document.getElementById('fill-miss').textContent='缺失：'+b.getAttribute('data-fmiss');
  document.getElementById('fill-org').value=b.getAttribute('data-forg')||'';
  document.getElementById('fill-teacher').value=b.getAttribute('data-fteacher')||'';
  document.getElementById('fill-student').value=b.getAttribute('data-fstudent')||'';
});
function saveFill(){
  var tr=window._fillRow;if(!tr)return;
  var org=document.getElementById('fill-org').value.trim();
  var teacher=document.getElementById('fill-teacher').value.trim();
  var student=document.getElementById('fill-student').value.trim();
  if(!org||!teacher||!student){toast('请补全所属组织、负责教师和学生负责人');return;}
  var orgCell=tr.querySelector('[data-col="org"]');
  var tCell=tr.querySelector('[data-col="teacher"]');
  var sCell=tr.querySelector('[data-col="student"]');
  var miss=tr.querySelector('[data-col="miss"]');
  var stc=tr.querySelector('[data-st]');
  if(orgCell)orgCell.textContent=org;
  if(tCell)tCell.textContent=teacher;
  if(sCell)sCell.textContent=student;
  if(miss)miss.innerHTML='<span class="small c-success">信息完整</span>';
  if(stc)stc.innerHTML='<span class="tag tag-warning tag-dot">待确认</span>';
  document.getElementById('fill-modal').classList.add('hidden');
  toast('已保存补全信息，状态改为待确认');
}
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-mark]');if(!b)return;
  var stc=b.closest('tr').querySelector('[data-st]');if(!stc)return;
  stc.innerHTML=b.getAttribute('data-mark')==='ok'
    ?'<span class="tag tag-success tag-dot">已确认</span>'
    :'<span class="tag tag-danger tag-dot">信息有误</span>';
});
"""


def import_confirm():
    items = [
        ("IM2025-CS-003", ACCOUNTS["rename"]["name"], "微博", ACCOUNTS["rename"]["pid"], "计算机学院学生会", "王晓琳", "李明", [], "待确认", "pending"),
        ("IM2025-CS-021", "2023级软件工程2班团支部", "微信公众号", "csu_se2302", "2023级软件工程2班团支部", "刘洋", "黄子轩", [], "待确认", "pending"),
        ("IM2025-CS-030", "计算机学院研究生会", "微信公众号", "csu_cs_gsu", "计算机学院研究生会", "王晓琳", "陈卓", [], "待确认", "pending"),
        ("IM2025-CS-011", "计院篮球协会", "抖音", "csu_cs_basketball", "计院篮球协会", "", "刘子豪", ["缺负责教师"], "待补全", "missing"),
        ("IM2025-CS-014", "2022级计算机科学2班团支部", "QQ", "2230617785", "2022级计算机科学2班团支部", "刘洋", "", ["缺学生负责人", "缺更新频率"], "待补全", "missing"),
        ("IM2025-CS-017", "计院书画协会", "微信公众号", "csu_cs_art", "计院书画协会", "", "", ["缺负责教师", "缺学生负责人"], "待补全", "missing claim"),
        ("IM2025-CS-022", "2024级人工智能1班团支部", "QQ", "2415538920", "2024级人工智能1班团支部", "陈思远", "孙悦", ["缺开通时间"], "待补全", "missing"),
        ("IM2025-CS-026", "计院电竞社", "哔哩哔哩", "2046631178", "", "", "", ["缺所属组织", "缺负责教师", "缺学生负责人"], "待补全", "missing claim"),
        ("IM2025-CS-001", ACCOUNTS["annual"]["name"], "微信公众号", ACCOUNTS["annual"]["pid"], "计算机学院团委", "王晓琳", "李明", [], "已确认", "done"),
        ("IM2025-CS-005", ACCOUNTS["rectify"]["name"], "小红书", ACCOUNTS["rectify"]["pid"], "计算机学院青年志愿者协会", "王晓琳", "何雨桐", [], "已确认", "done"),
    ]
    rows = []
    for no, name, p, pid, org, t, s, miss, status, cat in items:
        miss_html = '<div class="flex gap4 wrap">' + "".join(tag(m, "danger") for m in miss) + "</div>" if miss else '<span class="small c-success">信息完整</span>'
        fill = (f'<button class="link" type="button" data-toggle="#fill-modal" data-fname="{esc(name)}" '
                f'data-fmiss="{esc("、".join(miss) or "请核对字段")}" data-fteacher="{esc(t)}" data-fstudent="{esc(s)}" '
                f'data-forg="{esc(org)}">补全</button>')
        if "claim" in cat:
            op = f'<div class="ops">{fill}<a class="link" href="../common/apply-claim.html">认领</a></div>'
        elif status == "待补全":
            op = f'<div class="ops">{fill}</div>'
        elif status == "待确认":
            op = (f'<div class="ops"><button class="link" type="button" data-mark="ok" data-toast="已确认“{esc(name)}”导入信息无误">确认</button>'
                  f'<button class="link" type="button" data-mark="bad" data-toast="已标记为信息有误，退回校团委核对">有误</button></div>')
        else:
            op = ops(("档案", "../common/archive-basic.html"))
        empty = '<span class="muted">—</span>'
        st_html = st(status) if status != "待补全" else tag("待补全", "danger", True)
        rows.append(dict(cells=[f'<span class="num small nowrap">{no}</span>', acct(name, p, pid),
                                f'<span data-col="org">{org or empty}</span>', f'<span data-col="teacher">{t or empty}</span>',
                                f'<span data-col="student">{s or empty}</span>', f'<span data-col="miss">{miss_html}</span>',
                                f'<span data-st>{st_html}</span>', op], cat=cat))
    tabs = seg([("全部", "all"), ("待确认 8", "pending"), ("待补全 5", "missing"), ("已确认 23", "done")], target="#im-table")
    content = f"""{page_hd('导入数据确认', '从本院账号进入。校团委以 2025 年度台账为基础导入的历史数据，由学院补全缺失字段并逐条确认',
                   btn('下载本院导入明细', None, 'default', 'download', toast='已下载《计算机学院导入数据明细》Excel') + btn('批量确认', None, 'primary', 'check', toast='请先勾选需要确认的记录'))}
{alert('校团委宣传部于 2026-09-16 导入 2025 年度台账，计算机学院共 36 条。请于 <b>2026-10-10</b> 前完成补全与确认；无人认领的账号可由学生或教师通过“账号认领”补录。', 'info')}
<div class="grid g4 mt16 mb16">
  {stat('导入总数', 36, '来源：2025 年度台账', 'upload')}
  {stat('待确认', 8, '信息完整，待学院核对', 'inbox', 'orange')}
  {stat('待补全', 5, '缺负责教师 3 · 缺学生负责人 3', 'alert', 'red')}
  {stat('已确认', 23, '已建立账号档案', 'check-circle', 'green')}
</div>
<div class="card card-bd">
  <div class="toolbar">{tabs}<span class="small sub">已选 <b class="c-primary" data-checked-count="#im-table">0</b> 条</span></div>
  {table(['导入编号', '账号 / 平台ID', '所属组织', '负责教师', '学生负责人', '缺失字段', '状态', '操作'], rows, check=True, id_='im-table')}
  {pager(36, 4)}
</div>"""
    fill_body = f"""<div class="bold mb8" id="fill-title">补全导入信息</div>
<div class="small c-danger mb12" id="fill-miss"></div>
<div class="form-grid">
  {field('所属组织', '<input class="input" id="fill-org" placeholder="请输入所属组织">', True)}
  {field('负责教师', '<input class="input" id="fill-teacher" placeholder="请输入负责教师">', True)}
  {field('学生负责人', '<input class="input" id="fill-student" placeholder="请输入学生负责人">', True)}
  {field('更新频率', '<select class="select" id="fill-freq">' + ''.join(f'<option>{x}</option>' for x in UPDATE_FREQ) + '</select>')}
  {field('开通时间', '<input class="input" id="fill-opened" type="date" value="2026-09-01">')}
</div>"""
    content += (
        f'<div class="mask hidden" id="fill-modal"><div class="modal"><div class="modal-hd">补全缺失字段'
        f'<button class="x-btn" type="button" data-toggle="#fill-modal" aria-label="关闭">{icon("x")}</button></div>'
        f'<div class="modal-bd">{fill_body}</div><div class="modal-ft">'
        f'<button class="btn btn-default" type="button" data-toggle="#fill-modal">取消</button>'
        f'<button class="btn btn-primary" type="button" onclick="saveFill()">保存</button></div></div></div>'
    )
    page("import-confirm.html", "accounts", "导入数据确认", cr(("本院账号", "accounts.html"), ("导入数据确认", None)), content, FILL_JS)


# ---------------------------------------------------------------- 17 本院数据导出
def export():
    ledgers = [
        ("学院账号明细表", "本院全部账号的归属、平台、运行、责任人与四套状态", "36 条 · 42 个字段", "database", ""),
        ("本院疑似僵尸号清单", "预警规则、停更天数、核实进度与处置结果", "3 条待处置 · 3 条已处置", "ghost", "red"),
        ("本院年审完成情况", "按组织 / 教师统计各节点数量与完成率", "36 条 · 2026 年度", "calendar", "green"),
        ("教师负责账号清单", "每名教师负责账号、授权来源与待办数量", "6 名教师 · 34 个账号", "users", ""),
        ("学生运营负责人清单", "学生负责人、学号、联系方式与任职起止时间", "31 人", "user", "orange"),
        ("注销 / 新建清单", "本年度新建、注销账号及审核结果", "新建 3 · 注销 2", "file", "gray"),
    ]
    cards = "".join(
        f'<div class="card ledger"><div class="flex gap12">{ic_box(ic, c)}<div class="grow"><div class="bold">{t}</div>'
        f'<div class="small muted">{n}</div></div></div><div class="fs13 sub">{d}</div>'
        f'<div class="flex gap8 mt4">{btn("导出 Excel", None, "primary", "download", "sm", toast="已生成《计算机学院" + t + "》Excel，可在导出记录中下载")}'
        f'{btn("导出 PDF", None, "default", "print", "sm", toast="已生成《计算机学院" + t + "》PDF")}</div></div>'
        for t, d, n, ic, c in ledgers)
    records = table(["导出时间", "台账", "条件", "格式", "导出人", "操作"], [
        ["2026-09-29 16:40", "本院年审完成情况", "2026 年度 · 全部组织", "Excel", "周建华", ops(("下载", None, "已开始下载"))],
        ["2026-09-25 10:12", "本院疑似僵尸号清单", "风险等级：全部", "Excel", "周建华", ops(("下载", None, "已开始下载"))],
        ["2026-09-18 09:30", "教师负责账号清单", "全部教师", "PDF", "周建华", ops(("下载", None, "已开始下载"))],
        ["2026-09-10 14:05", "学院账号明细表", "运行状态：全部", "Excel", "周建华", ops(("下载", None, "已开始下载"))],
    ], cls="tbl-sm")
    content = f"""{page_hd('本院数据导出', '按台账类型导出本学院数据；每次导出均记录导出人、时间与条件',
                   btn('导出记录', '../common/archive-logs.html', 'default', 'history'))}
{alert('导出范围仅限<b>计算机学院</b>及所属、直属、指导组织；全校台账由校团委导出。导出文件含个人信息，请妥善保管，不得外传。', 'warning', 'lock')}
<div class="grid g3 mt16">{cards}</div>
{card('最近导出', records, cls='mt16')}"""
    page("export.html", "export", "本院数据导出", cr(("数据与系统", None), ("本院数据导出", None)), content)


# ---------------------------------------------------------------- 18 本院授权
AUTH_JS = """
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-aname]');if(!b)return;
  document.getElementById('auth-name').value=b.getAttribute('data-aname')||'';
  document.getElementById('auth-no').value=b.getAttribute('data-ano')||'';
  document.getElementById('auth-scope').value=b.getAttribute('data-ascope')||'';
  var who=b.getAttribute('data-aname');
  document.getElementById('auth-title').textContent=who?('授权 · '+who):'新增授权';
  window._authRow=who?b.closest('tr'):null;
});
function saveAuth(){
  var name=document.getElementById('auth-name').value.trim();
  var no=document.getElementById('auth-no').value.trim();
  var scope=document.getElementById('auth-scope').value.trim();
  if(!name||!no||!scope){toast('请填写人员、工号 / 学号和授权范围');return;}
  if(window._authRow){
    var cell=window._authRow.querySelector('[data-col="scope"]');
    if(cell)cell.textContent=scope;
    toast('已保存 '+name+' 的授权范围');
  }else{
    var tb=document.querySelector('#us-table tbody');
    var tr=document.createElement('tr');
    tr.innerHTML='<td><b>'+name+'</b></td><td><span class="num small">'+no+'</span></td><td><span class="tag tag-primary">新授权</span></td><td><span class="fs13" data-col="scope">'+scope+'</span></td><td><span class="tag tag-success tag-dot">启用</span></td><td><span class="small muted">刚刚</span></td><td><span class="small muted">已保存</span></td>';
    if(tb)tb.insertBefore(tr,tb.firstChild);
    toast('已新增授权：'+name);
  }
  document.getElementById('auth-modal').classList.add('hidden');
}
"""


def users():
    data = [
        ("周建华", "T20090315", [("学院管理员", "primary")], "计算机学院全部数据（本学院及所属 / 直属 / 指导组织）", "2026-09-30 13:40"),
        ("王晓琳", "T20180427", [("宣传工作辅导员", "warning"), ("2021级辅导员", "warning"), ("街舞社指导教师", "warning")],
         "学院团委直属组织 6 · 2021级团支部 2 · 社团 3（共 11 个账号）", "2026-09-30 09:20"),
        ("刘洋", "T20200611", [("2023级辅导员", "warning")], "2023级各班团支部（6 个账号）", "2026-09-29 18:02"),
        ("陈思远", "T20210903", [("2024级辅导员", "warning")], "2024级各班团支部（5 个账号）", "2026-09-29 11:26"),
        ("赵敏", "T20170512", [("志愿服务负责老师", "warning")], "青年志愿者服务队、支教队（4 个账号）", "2026-09-27 15:44"),
        ("孙浩", "T20190218", [("社团工作辅导员", "warning")], "计院学生社团（5 个账号）", "2026-09-28 20:15"),
        ("林雪", "T20250701", [("2025级辅导员", "warning")], "2025级各班团支部（3 个账号）", "2026-09-26 08:57"),
        ("李明", "8209230117", [("学生负责人", "success")], "中南计院团委 · 中南计算机青年 · 计算机学院学生会", "2026-09-30 08:12"),
        ("何雨桐", "8209230509", [("学生负责人", "success")], "计院青年志愿者 · 计院科协", "2026-09-27 20:45"),
        ("李四", "8209240208", [("学生负责人", "success")], "计院街舞社（2026-10-01 生效）", "2026-09-28 12:30"),
        ("孙悦", "8209240315", [("学生负责人", "success")], "计院ACM协会（代办交接审核中）", "2026-09-30 10:02"),
    ]
    rows = []
    for name, no, ids, scope, last in data:
        is_student = no.startswith("82")
        cat = "student" if is_student else ("admin" if name == "周建华" else "teacher")
        id_html = '<div class="flex gap4 wrap">' + "".join(tag(t, k) for t, k in ids) + "</div>"
        op = (f'<div class="ops"><button class="link" type="button" data-toggle="#auth-modal" data-aname="{esc(name)}" '
              f'data-ano="{esc(no)}" data-ascope="{esc(scope)}">授权</button>'
              f'<button class="link" type="button" data-toggle="#auth-modal" data-aname="{esc(name)}" '
              f'data-ano="{esc(no)}" data-ascope="{esc(scope)}">调整范围</button></div>')
        rows.append(dict(cells=[person(name), f'<span class="num small">{no}</span>', id_html, f'<span class="fs13" data-col="scope">{scope}</span>',
                                st("启用"), f'<span class="small muted">{last}</span>', op], cat=cat))
    tabs = seg([("全部 11", "all"), ("学院管理员 1", "admin"), ("业务教师 6", "teacher"), ("学生负责人 4", "student")], target="#us-table")
    multi = "".join(
        f'<div class="id-card"><div class="flex between">{tag(t, "warning")}<span class="small sub">{n} 个账号</span></div>'
        f'<div class="small sub mt8">{d}</div></div>'
        for t, d, n in [("宣传工作辅导员", "学院团委、新媒体中心、学生会、研究生会、科协、青年志愿者协会", 6),
                        ("2021级辅导员", "2021级软件工程1班、计算机科学3班等团支部", 2),
                        ("街舞社指导教师", "计院街舞社（兼指导 ACM 协会、摄影协会）", 3)])
    multi_body = (f'<div class="flex gap12 mb12">{avatar("王晓琳")}<div class="grow"><div class="bold">王晓琳 · 一人多身份示例</div>'
                  f'<div class="small muted">登录后可在“身份切换”中选择，数据范围为三个身份授权的并集</div></div>'
                  f'{btn("身份切换", "../common/identity-switch.html", "default", "user-switch", "sm")}</div><div class="grid g3">{multi}</div>')
    content = f"""{page_hd('本院授权', '为本院教师与学生负责人授予身份与数据范围；授权范围不超出本学院',
                   btn('授权记录', 'logs.html', 'default', 'history') + '<button class="btn btn-primary" type="button" data-toggle="#auth-modal" data-aname="" data-ano="" data-ascope="">' + icon('user-add') + '新增授权</button>')}
{card('多身份授权说明', multi_body)}
<div class="card card-bd mt16">
  <div class="toolbar">{tabs}<span class="small muted">学院管理员仅可授权本学院范围；跨学院授权请联系校团委</span></div>
  {table(['用户', '工号 / 学号', '身份', '授权范围', '状态', '最近登录', '操作'], rows, id_='us-table')}
</div>"""
    auth_body = f"""<div class="bold mb8" id="auth-title">授权设置</div>
<div class="form-grid">
  {field('人员', '<input class="input" id="auth-name" placeholder="输入姓名检索本院人员">', True)}
  {field('工号 / 学号', '<input class="input" id="auth-no" placeholder="输入工号或学号">', True)}
  {field('身份', radios('auth-role', ['学院管理员', '业务教师', '学生负责人'], '业务教师'), True)}
  {field('组织 / 账号范围', '<input class="input" id="auth-scope" placeholder="例如：2024级各班团支部">', True)}
</div>
<div class="mt12">{''.join(f'<label class="cb" style="display:flex;margin-top:6px"><input type="checkbox" checked> {x}</label>' for x in ['查看账号', '审核申请', '审核年审', '代办业务'])}</div>"""
    content += (
        f'<div class="mask hidden" id="auth-modal"><div class="modal"><div class="modal-hd">授权设置'
        f'<button class="x-btn" type="button" data-toggle="#auth-modal" aria-label="关闭">{icon("x")}</button></div>'
        f'<div class="modal-bd">{auth_body}</div><div class="modal-ft">'
        f'<button class="btn btn-default" type="button" data-toggle="#auth-modal">取消</button>'
        f'<button class="btn btn-primary" type="button" onclick="saveAuth()">保存授权</button></div></div></div>'
    )
    page("users.html", "users", "本院授权", cr(("数据与系统", None), ("本院授权", None)), content, AUTH_JS)


# ---------------------------------------------------------------- 19 操作日志
def logs():
    type_of = {"new": "新建备案", "rename": "信息变更", "handover": "负责人交接", "idchange": "平台ID变更", "annual": "年审",
               "rectify": "整改", "zombie": "僵尸号处置", "proxy": "负责人交接"}
    role_of = {"李明": "学生用户", "何雨桐": "学生用户", "王晓琳": "业务教师", "周建华": "学院管理员", "陈静": "学校管理员", "系统": "系统"}
    kind_of = {"学生用户": "success", "业务教师": "warning", "学院管理员": "primary", "学校管理员": "primary", "系统": "muted"}
    events = []
    for k, f in FLOWS.items():
        for when, who, title, cmt in f["steps"]:
            events.append((when, who, k, title, cmt))
    events.sort(reverse=True)
    rows = []
    for when, who, k, title, cmt in events[:15]:
        role = role_of.get(who, "—")
        summary = f'<div class="fs13">{title}</div>' + (f'<div class="small muted ellipsis" style="max-width:360px">{cmt}</div>' if cmt else "")
        if k == "proxy":
            summary += f'<div class="mt4">{tag("发起方式：教师代办", "primary")}</div>'
        rows.append(dict(cells=[f'<span class="num small">{when}</span>', person(who) if who != "系统" else tag("系统", "muted"),
                                tag(role, kind_of.get(role, "muted")), type_of[k], f'<span class="bold fs13">{ACCOUNTS[k]["name"]}</span>',
                                summary, ops(("详情", "../common/archive-logs.html"))],
                         href="../common/archive-logs.html"))
    filters = filter_bar([
        field("操作时间", inp(val="2026-09-01 至 2026-09-30")),
        field("操作人", inp("姓名 / 工号 / 学号")),
        field("身份", sel(["学生用户", "业务教师", "学院管理员", "学校管理员", "系统"])),
        field("业务类型", sel(["新建备案", "信息变更", "负责人交接", "平台ID变更", "年审", "整改", "僵尸号处置", "注销"])),
        field("账号", inp("账号名称 / 平台ID")),
        field("发起方式", sel(["本人发起", "教师代办", "系统自动"])),
        field("操作结果", sel(["成功", "退回", "驳回"])),
    ])
    content = f"""{page_hd('操作日志', f'本学院范围内全部业务操作留痕（共 {len(events)} 条），日志不可修改、不可删除',
                   btn('导出日志', None, 'default', 'download', toast='已导出本院 2026 年 9 月操作日志'))}
{filters}
<div class="card card-bd">
  {table(['时间', '操作人', '身份', '业务类型', '对象', '操作摘要', '操作'], rows)}
  {pager(len(events), 3)}
</div>"""
    page("logs.html", "logs", "操作日志", cr(("数据与系统", None), ("操作日志", None)), content)


def build():
    workbench()
    messages()
    accounts()
    organizations()
    approval_detail()
    approval_change()
    approval_proxy()
    annual_progress()
    annual_review()
    annual_review_detail()
    annual_submit()
    annual_submit_success()
    assign()
    assign_batch()
    teachers()
    teacher_detail()
    zombie()
    zombie_verify_detail()
    rectify()
    rectify_create()
    rectify_detail()
    import_confirm()
    export()
    users()
    logs()
