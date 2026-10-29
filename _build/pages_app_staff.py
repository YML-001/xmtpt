"""移动端 · 业务教师（王晓琳）与学院管理员（周建华）页面。

教师可以使用移动端完成主要审核工作；PC 和移动端同一账号体系、同一数据库、同一业务状态。
"""
from base import *  # noqa: F401,F403
from data import ACCOUNTS, PEOPLE, FLOWS, COLLEGE_STATS as CS, ANNUAL_TASK as T
from mobile_archive import ARCH_JS, ARCHIVE_CSS, action_row, render_archive

DT = "app/teacher/"
DC = "app/college/"

# ---------------------------------------------------------------- 本模块样式
STAFF_CSS = """
.hero-tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px;position:relative;z-index:1}
.hero-tag{height:22px;padding:0 9px;border-radius:11px;background:rgba(255,255,255,.18);font-size:11px;display:inline-flex;align-items:center;gap:4px;white-space:nowrap}
.hero-tag .i{width:12px;height:12px}
.hero-stats{display:grid;grid-template-columns:repeat(4,1fr);margin-top:14px;position:relative;z-index:1;text-align:center;background:rgba(255,255,255,.12);border-radius:12px;padding:10px 0}
.hero-stats.c3{grid-template-columns:repeat(3,1fr)}
.hero-stats a+a{border-left:1px solid rgba(255,255,255,.18)}
.hero-stats b{display:block;font-size:20px;font-weight:700;line-height:1.3;font-variant-numeric:tabular-nums}
.hero-stats b small{font-size:12px;font-weight:500;opacity:.8}
.hero-stats span{font-size:11px;opacity:.85}
.sec-t{font-size:15px;font-weight:600;display:flex;align-items:center;gap:8px;margin-bottom:10px}
.sec-t::before{content:"";width:3px;height:14px;border-radius:2px;background:var(--c-primary);flex:none}
.sec-t .ml-auto{font-weight:400;font-size:12px}
.row{display:flex;justify-content:space-between;gap:12px;padding:8px 0;font-size:14px;border-bottom:1px dashed #EEF0F3}
.row:last-child{border-bottom:none;padding-bottom:0}
.row>span:first-child{color:var(--c-text-3);flex:none}
.row>span:last-child{text-align:right;color:var(--c-text);word-break:break-all}
.row.stack{flex-direction:column;gap:2px}
.row.stack>span:last-child{text-align:left;font-size:13px;line-height:1.7;color:var(--c-text-2)}
.fold-hd{width:100%;display:flex;align-items:center;gap:8px;font-size:15px;font-weight:600;text-align:left}
.fold-hd::before{content:"";width:3px;height:14px;border-radius:2px;background:var(--c-primary);flex:none}
.fold-tx{font-size:12px;font-weight:400;color:var(--c-text-3);display:inline-flex;align-items:center;gap:2px}
.fold-bd{margin-top:8px}
.intro{margin-top:6px;padding:10px 12px;background:#F7F9FB;border-radius:8px;font-size:13px;line-height:1.75;color:var(--c-text-2)}
.mech{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-top:8px}
.mech span{display:flex;align-items:center;gap:6px;padding:8px 10px;border-radius:8px;background:var(--c-success-bg);color:#0E8A55;font-size:12px}
.tc-top{display:flex;align-items:center;gap:10px}
.tc-meta{font-size:12px;color:var(--c-text-3);margin-top:8px;display:flex;flex-wrap:wrap;gap:2px 12px}
.tc-note{margin-top:8px;padding:8px 10px;background:#F7F9FB;border-radius:8px;font-size:13px;color:var(--c-text-2)}
.tc-ft{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:10px;padding-top:10px;border-top:1px solid #F0F2F5;font-size:12px;color:var(--c-text-3)}
.tc-ft .go{color:var(--c-primary);font-weight:500;display:inline-flex;align-items:center;gap:2px}
.batch-entry{display:flex;align-items:center;gap:12px;background:linear-gradient(135deg,#EAF5FC,#F4FAFE);border:1px solid var(--c-primary-border)}
.person{border:1px solid var(--c-line);border-radius:12px;padding:12px 8px;text-align:center;background:#FAFBFC;min-width:0}
.person.new{border-color:var(--c-primary-border);background:#F3F9FD}
.person .avatar{margin:0 auto 6px}
.person .small{line-height:1.7}
.arrow-c{width:28px;height:28px;border-radius:50%;background:var(--c-primary);color:#fff;display:grid;place-items:center;align-self:center}
.arrow-c .i{width:16px;height:16px}
.cmp{border-radius:12px;padding:12px;border:1px solid var(--c-line)}
.cmp.old{background:#FAFBFC}.cmp.new{background:#F2FBF7;border-color:var(--c-success-bd)}
.cmp .v{font-size:16px;font-weight:600;margin-top:2px}
.cmp.old .v{color:var(--c-text-3);text-decoration:line-through;text-decoration-color:rgba(223,32,39,.5)}
.cmp.new .v{color:var(--c-success)}
.cmp-arrow{display:flex;justify-content:center;margin:-6px 0;position:relative;z-index:1}
.ok-list{display:grid;gap:2px}
.ok-list div{display:flex;align-items:center;gap:8px;padding:7px 0;font-size:13px;border-bottom:1px dashed #EEF0F3}
.ok-list div:last-child{border-bottom:none}
.ok-list .i{color:var(--c-success);width:16px;height:16px}
.ok-list em{font-style:normal;margin-left:auto;color:var(--c-text-3);font-size:12px}
.shot{border-radius:10px;overflow:hidden;position:relative}
.shot img{width:100%;height:150px;object-fit:cover}
.shot span{position:absolute;left:8px;bottom:8px;padding:2px 8px;border-radius:6px;background:rgba(0,0,0,.55);color:#fff;font-size:11px}
.mini3{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.mini3>div{background:var(--c-bg);border-radius:10px;padding:10px 8px;text-align:center}
.mini3 b{display:block;font-size:17px;font-variant-numeric:tabular-nums}
.mini3 small{display:block;font-size:11px;color:var(--c-text-3)}
.mini3 .up{font-size:11px}
.dlg-hd{padding:18px 18px 4px;font-size:17px;font-weight:600;text-align:center}
.dlg-bd{padding:6px 18px 16px;font-size:13px;color:var(--c-text-2)}
.dlg-bd .cell{padding:0;border:none;min-height:0;margin-top:10px}
.dlg-bd .m-textarea{min-height:84px}
.dlg-ft{display:flex;border-top:1px solid var(--c-line)}
.dlg-ft button{flex:1;height:48px;font-size:16px;color:var(--c-text-2)}
.dlg-ft button+button{border-left:1px solid var(--c-line)}
.dlg-ft .ok{color:var(--c-primary);font-weight:600}.dlg-ft .ok.danger{color:var(--c-danger)}
.sheet-hd{font-size:16px;font-weight:600;text-align:center;margin-bottom:6px}
.sheet-item{display:flex;align-items:center;gap:12px;padding:12px 2px;border-bottom:1px solid #F0F2F5}
.sheet-item .qi{width:38px;height:38px;border-radius:11px;display:grid;place-items:center;background:var(--c-primary-light);color:var(--c-primary);flex:none}
.sheet-item .qi.orange{background:var(--c-warning-bg);color:var(--c-warning)}.sheet-item .qi.red{background:var(--c-danger-bg);color:var(--c-danger)}
.sheet-item .qi.green{background:var(--c-success-bg);color:var(--c-success)}.sheet-item .qi.purple{background:#F0EDFB;color:#6B5BD2}
.sheet-cancel{display:block;width:100%;height:46px;margin-top:12px;border-radius:10px;background:var(--c-bg);font-size:16px}
.bottom-bar .btn.wide{flex:1.8}
.bottom-bar .btn.slim{flex:.9}
.bk-row{display:flex;align-items:center;gap:10px;padding:11px 14px;border-bottom:1px solid #F0F2F5;cursor:pointer;transition:background .15s}
.bk-row:last-child{border-bottom:none}
.bk-row.on{background:#F7FBFE}
.bk-row input,.bk-all input{width:18px;height:18px;accent-color:var(--c-primary);flex:none}
.bk-all{display:flex;align-items:center;gap:10px;padding:12px 14px;background:#fff;border-radius:12px;margin-bottom:10px;position:sticky;top:-12px;z-index:5;box-shadow:0 1px 2px rgba(0,0,0,.04);cursor:pointer}
.chip-group{display:flex;flex-wrap:wrap;gap:8px}
.chip-group .chip{height:30px}
.funnel{display:flex;height:12px;border-radius:6px;overflow:hidden;margin:10px 0 12px}
.funnel i{display:block;height:100%}
.fn-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:4px;text-align:center}
.fn-grid>div{padding:8px 2px;border-radius:10px;background:var(--c-bg)}
.fn-grid b{display:block;font-size:18px;font-variant-numeric:tabular-nums}
.fn-grid small{display:flex;align-items:center;justify-content:center;gap:4px;font-size:11px;color:var(--c-text-2)}
.fn-grid small i{width:8px;height:8px;border-radius:2px;display:inline-block}
.p-row{display:flex;align-items:center;gap:10px;padding:12px 0;border-bottom:1px solid #F0F2F5}
.p-row:last-child{border-bottom:none}
.seg.full{display:flex;width:100%}.seg.full button{flex:1;justify-content:center}
.risk-tile{display:flex;align-items:center;gap:10px;padding:12px}
.msg-dot{width:8px;height:8px;border-radius:50%;background:var(--c-danger);flex:none}
.msg-dot.read{background:transparent}
.pc-hint{display:flex;align-items:center;gap:12px;border:1px dashed var(--c-primary-border);background:#F7FBFE}
.res-card{text-align:left;margin-top:16px}
.search-box{display:flex;align-items:center;gap:8px;height:38px;padding:0 12px;border-radius:19px;background:#fff;color:var(--c-text-3);margin-bottom:10px}
.search-box input{border:none;outline:none;background:none;flex:1;min-width:0;font-size:14px}
.chips.scroll-x{flex-wrap:nowrap;overflow-x:auto;margin-bottom:12px;-webkit-overflow-scrolling:touch}
.chips.scroll-x::-webkit-scrollbar{height:0}
.chips.scroll-x .chip{flex:none}
.req-item{padding:10px 0;border-bottom:1px dashed #EEF0F3}
.req-item:last-child{border-bottom:none;padding-bottom:0}
.req-q{display:flex;gap:8px;font-size:13px;color:var(--c-text-2)}
.req-a{margin-top:6px;padding:8px 10px;border-radius:8px;background:var(--c-success-bg);color:#0E8A55;font-size:13px;display:flex;gap:6px}
.req-a .i{margin-top:3px}
"""


# ---------------------------------------------------------------- 本模块小组件
def jump(text, href, kind="primary", toast=None, ic=None, cls="", attrs=""):
    """跳转按钮：可先提示再跳转（<a data-toast> 会被通用脚本拦截，故用 button + data-href）。"""
    t = f' data-toast="{esc(toast)}"' if toast else ""
    i = icon(ic) if ic else ""
    return f'<button class="btn btn-{kind} {cls}" type="button" data-href="{href}"{t} {attrs}>{i}{text}</button>'


def badge(n):
    return f'<span class="badge">{n}</span>' if n else ""


def toggle_btn(text, target, kind="default", ic=None, cls=""):
    i = icon(ic) if ic else ""
    return f'<button class="btn btn-{kind} {cls}" type="button" data-toggle="{target}">{i}{text}</button>'


def sec(title, body, extra="", cls=""):
    ex = f'<span class="ml-auto">{extra}</span>' if extra else ""
    return f'<div class="m-card {cls}"><div class="sec-t">{title}{ex}</div>{body}</div>'


def rows(items):
    """键值行：值较长时改为上下排列，避免右对齐多行换行难以阅读。"""
    out = []
    for k, v in items:
        cls = "row stack" if len(re_strip(v)) > 18 else "row"
        out.append(f'<div class="{cls}"><span>{k}</span><span>{v}</span></div>')
    return "".join(out)


def fold(key, title, body, open_=True):
    """可折叠信息分区：点击标题切换内容与“收起/展开”提示。"""
    bd, up, dn = ("", "", " hidden") if open_ else (" hidden", " hidden", "")
    return (f'<div class="m-card"><button class="fold-hd" type="button" data-toggle="#{key}, #{key}-up, #{key}-dn">'
            f'<span class="grow">{title}</span>'
            f'<span class="fold-tx{up}" id="{key}-up">收起{icon("chevron-down", 14)}</span>'
            f'<span class="fold-tx{dn}" id="{key}-dn">展开{icon("chevron-right", 14)}</span></button>'
            f'<div class="fold-bd{bd}" id="{key}">{body}</div></div>')


def head(name, platform, meta, tags=""):
    return (f'<div class="m-card"><div class="flex gap12">{pf(platform, "lg")}<div class="grow">'
            f'<div class="fs16 bold ellipsis">{name}</div><div class="small muted ellipsis">{meta}</div>'
            f'<div class="flex gap6 wrap mt4">{tags}</div></div></div></div>')


def flow_tl(key, done_n, now_title="", now_meta="", back_idx=()):
    """按 FLOWS 输出前 done_n 步已完成节点，并追加当前节点。"""
    items = []
    for i, (when, who, title, cm) in enumerate(FLOWS[key]["steps"][:done_n]):
        items.append(("back" if i in back_idx else "done", title, f"{who} · {when}", cm))
    if now_title:
        items.append(("now", now_title, now_meta, ""))
    return timeline(items)


def opinion(val="", label="审核意见", ph="请输入审核意见（选填）"):
    return f'<div class="m-group">{m_textarea(label, ph, val, maxlen=200)}</div>'


def dialog(id_, title, desc, ph, ok_text, target, toast, danger=True, val=""):
    """手机内对话框：data-form 限定校验范围，原因为必填。"""
    ok_cls = "ok danger" if danger else "ok"
    return (f'<div class="m-dialog-mask hidden" id="{id_}"><div class="m-dialog" data-form>'
            f'<div class="dlg-hd">{title}</div><div class="dlg-bd">{desc}'
            f'<div class="cell col-cell"><textarea class="m-textarea" placeholder="{ph}" required>{esc(val)}</textarea>'
            f'<div class="err-msg">请填写原因</div></div></div>'
            f'<div class="dlg-ft"><button type="button" data-toggle="#{id_}">取消</button>'
            f'<button type="button" class="{ok_cls}" data-submit="{target}" data-toast="{esc(toast)}">{ok_text}</button></div></div></div>')


def choices(group, items):
    """单选卡片：items 为 (标题, 说明, 联动选择器, 是否选中)；联动元素需带 group 类名。"""
    out = []
    for title, desc, target, on in items:
        c = " on" if on else ""
        out.append(f'<div class="choice{c}" data-choice="{target}"><span class="ck"></span><div class="grow">'
                   f'<div class="bold fs13">{title}</div><div class="small muted">{desc}</div></div></div>')
    return f'<div class="choices" data-single="{group}">{"".join(out)}</div>'


def todo_card(cat, href, name, platform, kind_tag, meta, note, foot_l, foot_r="去审核"):
    meta_html = "".join(f"<span>{m}</span>" for m in meta)
    return (f'<a class="m-card" href="{href}" data-cat="{cat}" style="display:block">'
            f'<div class="tc-top">{pf(platform, "sm")}<div class="grow bold ellipsis">{name}</div>{kind_tag}</div>'
            f'<div class="tc-meta">{meta_html}</div><div class="tc-note">{note}</div>'
            f'<div class="tc-ft"><span>{foot_l}</span><span class="go">{foot_r}{icon("chevron-right", 14)}</span></div></a>')


def list_item(href, ic, color, title, meta, right=""):
    return (f'<a class="todo-item" href="{href}"><span class="stat-ic {color}" style="width:38px;height:38px;border-radius:11px">{icon(ic, 20)}</span>'
            f'<div class="grow" style="min-width:0"><div class="bold fs13 ellipsis">{title}</div><div class="small muted ellipsis">{meta}</div></div>{right}</a>')


def pc_hint(title, desc, href):
    return (f'<a class="m-card pc-hint" href="{href}"><span class="stat-ic" style="width:38px;height:38px;border-radius:11px">{icon("monitor", 20)}</span>'
            f'<div class="grow"><div class="bold fs13">{title}</div><div class="small muted">{desc}</div></div>{icon("chevron-right", cls="arrow")}</a>')


def page_t(role, path, title, content, notes, flow, **kw):
    """统一加上本模块样式。"""
    css = STAFF_CSS + kw.pop("css", "")
    app_page(path, role, title, content, notes=notes, flow=flow, css=css, **kw)


A_NEW, A_REN, A_HO, A_AN, A_RE, A_ZB, A_PH = (ACCOUNTS[k] for k in ("new", "rename", "handover", "annual", "rectify", "zombie", "photo"))
F_NEW, F_REN, F_HO, F_AN, F_RE, F_ZB = (FLOWS[k] for k in ("new", "rename", "handover", "annual", "rectify", "zombie"))

INTRO = ("“中南计算机青年”是计算机学院团委新媒体中心主办的微信公众号，定位为学院共青团思想引领与青年服务平台。"
         "主要栏目包括“青春计院”“学术前沿”“榜样力量”“就业指南”“团务通知”五个板块：青春计院报道学院团学活动与志愿服务；"
         "学术前沿介绍学院科研成果、学科竞赛与创新创业项目；榜样力量宣传优秀学生、优秀团员与先进集体事迹；"
         "就业指南发布实习招聘、升学深造与职业规划信息；团务通知发布团员教育管理、主题团日与“青年大学习”等工作通知。"
         "信息发布范围限于计算机学院团学工作相关内容，不发布商业广告及与学院无关的信息。"
         "所有推文执行“学生编辑初审、新媒体中心主任复审、指导教师终审”的三审制度，重大活动报道须经学院团委书记审定后发布。"
         "平台原则上每周更新不少于 2 次，由新媒体中心 12 名学生编辑轮值运营。")


# ================================================================ 业务教师
def t_home():
    me = PEOPLE["王晓琳"]
    scopes = [("tag", "宣传工作辅导员 · 10"), ("users", "2021级辅导员 · 7"), ("star", "街舞社指导教师 · 1")]
    tags_html = "".join(f'<span class="hero-tag">{icon(ic)}{t}</span>' for ic, t in scopes)
    quick = "".join(
        f'<a href="{h}"><span class="qi {c}">{icon(ic)}{badge(n)}</span>{t}</a>'
        for t, ic, c, n, h in [
            ("新建", "file-add", "", 1, "review-detail.html"), ("变更", "file-edit", "orange", 1, "review-change.html"),
            ("交接", "user-switch", "green", 1, "review-handover.html"), ("注销", "power", "red", 1, "todo.html"),
            ("年审", "calendar", "", 3, "review-annual.html"), ("僵尸号", "ghost", "red", 1, "review-zombie.html"),
            ("整改", "wrench", "orange", 1, "review-rectify.html"),
        ])
    urgent = "".join([
        list_item("review-handover.html", "user-switch", "green", "计院街舞社 · 负责人交接", "李明 → 李四 · 拟 2026-10-01 生效", tag("明日生效", "danger")),
        list_item("review-detail.html", "file-add", "", "中南计算机青年 · 新建备案", "学生已按退回意见修改并重新提交", tag("二次提交", "warning")),
        list_item("review-annual.html", "calendar", "", "中南计院团委 · 年度年审", "学生确认无异动 · 2026-09-18 提交", st("无异动", False)),
        list_item("review-zombie.html", "ghost", "red", "2021级软件工程1班团支部", "停更 412 天 · 待辅导员核实", st("待核实", False)),
    ])
    content = f"""
<div class="m-hero">
  <div class="flex gap12" style="position:relative;z-index:1">{avatar('王晓琳', 'lg')}
    <div class="grow"><div class="fs18 bold">王老师，下午好</div><div class="small" style="opacity:.85">{me['org']} · 业务教师</div></div>
    <a href="messages.html" style="position:relative" aria-label="消息">{icon('bell', 22)}<span class="badge" style="position:absolute;top:-6px;right:-8px">3</span></a>
  </div>
  <div class="hero-tags">{tags_html}</div>
  <div class="hero-stats">
    <a href="todo.html"><b>9</b><span>待审核</span></a>
    <a href="accounts.html"><b>18</b><span>负责账号</span></a>
    <a href="review-zombie.html"><b>2</b><span>疑似僵尸号</span></a>
    <a href="review-rectify.html"><b>1</b><span>待整改</span></a>
  </div>
</div>
<div class="alert alert-warning mt12">{icon('clock')}<div class="grow"><b>{T['name']}</b>：教师审核截止 <b>{T['teacher_end']}</b>，剩余 25 天，请及时处理年审记录。</div></div>
<div class="m-card mt12"><div class="sec-t">待审分类<span class="ml-auto"><a class="muted" href="todo.html">共 9 项</a></span></div><div class="quick pack7">{quick}</div></div>
<a class="m-card batch-entry" href="review-batch.html"><span class="stat-ic green" style="width:40px;height:40px;border-radius:12px">{icon('check-circle', 22)}</span>
  <div class="grow"><div class="bold">批量审核年审（无异动 12 个）</div><div class="small muted">仅无异动、无风险且信息完整的账号可批量通过</div></div>{icon('chevron-right', cls='arrow')}</a>
<div class="m-title">紧急待办<a href="todo.html">全部{icon('chevron-right', 14)}</a></div>
<div class="m-card" style="padding:4px 14px">{urgent}</div>"""
    page_t("teacher", DT + "home.html", "工作台", content, tab="home", nav_title="教师工作台",
           notes=["顶部三个身份标签对应王晓琳的三个授权范围，数据按授权范围自动汇总（共 18 个账号）",
                  "统计数字可点击：待审核进入待审列表，疑似僵尸号、待整改直达核实与整改审核页",
                  "7 类待审分类快捷入口带角标，年审无异动账号可一键进入批量审核",
                  "PC 与移动端同一账号体系、同一数据库、同一业务状态，任一端处理后另一端同步"],
           flow=[("剧本三：交接审核", "review-handover.html"), ("剧本五：年审审核", "review-annual.html"),
                 ("剧本五：无异动批量通过", "review-batch.html"), ("PC 端教师工作台", "../../pc/teacher/workbench.html")])


def t_todo():
    cards = "".join([
        todo_card("apply", "review-detail.html", A_NEW["name"], A_NEW["platform"], tag("新建备案", "primary"),
                  [F_NEW["no"], "李明 · 2026-09-26 20:05 重新提交"], "已按退回意见补充平台介绍（326 字）及信息发布范围",
                  f'{tag("二次提交", "warning")}'),
        todo_card("apply", "review-change.html", A_REN["name"], A_REN["platform"], tag("名称变更", "warning"),
                  [F_REN["no"], "李明 · 2026-09-26 14:30"], f"拟更名为“{A_REN['new_name']}”，属重要变更，需报校团委",
                  "当前节点：指导教师审核"),
        todo_card("apply", "review-handover.html", A_HO["name"], A_HO["platform"], tag("负责人交接", "success"),
                  [F_HO["no"], "李明 · 2026-09-27 19:40"], "负责人由李明交接给李四，拟 2026-10-01 生效；教师通过即生效",
                  f'{tag("明日生效", "danger")}'),
        todo_card("apply", "../../pc/teacher/review-cancel.html", "2021级网络工程2班团支部", "QQ", tag("账号注销", "danger"),
                  ["ZX20260928002", "原团支书 · 2026-09-28 16:12"], "团支部已于 2025 年 6 月毕业，申请注销账号",
                  "需核验佐证材料", "PC 审核"),
        todo_card("annual", "review-annual.html", A_AN["name"], A_AN["platform"], st("无异动", False),
                  [F_AN["no"], "李明 · 2026-09-18 21:16"], "学生确认 9 项全部正常，最近发布 2026-09-17", "可批量通过"),
        todo_card("annual", "review-annual.html", "计院研究生会", "视频号", st("无异动", False),
                  ["NS2026-CS-0015", "刘佳宁 · 2026-09-21 18:02"], "学生确认无异动，最近发布 2026-09-25", "可批量通过"),
        todo_card("annual", "../../pc/teacher/review-annual.html", ACCOUNTS["idchange"]["name"], "哔哩哔哩", st("变更", False),
                  ["NS2026-CS-0018", "何雨桐 · 2026-09-29 20:31"], "年度内平台 ID 发生变化，需逐条审核", "有异动，不可批量", "PC 审核"),
        todo_card("zombie", "review-zombie.html", A_ZB["name"], A_ZB["platform"], st("疑似僵尸号", False),
                  ["系统预警 · 2026-09-01"], "停更 412 天，命中“停更 ≥ 180 天”“团支部已毕业”两条规则", "请辅导员核实", "去核实"),
        todo_card("rectify", "review-rectify.html", A_PH["name"], A_PH["platform"], tag("整改审核", "warning"),
                  ["ZG20260915003", "李明 · 2026-09-28 22:05"], "已提交整改材料：补全学生负责人、恢复更新", "截止 2026-10-15"),
    ])
    content = f"""
<div class="m-tabs" data-target="#todo-list">
  <button type="button" class="on" data-seg="all">全部 9</button><button type="button" data-seg="apply">申请 4</button>
  <button type="button" data-seg="annual">年审 3</button><button type="button" data-seg="zombie">僵尸号 1</button>
  <button type="button" data-seg="rectify">整改 1</button>
</div>
<a class="m-card batch-entry" href="review-batch.html" style="position:sticky;top:34px;z-index:6">
  <span class="stat-ic green" style="width:36px;height:36px;border-radius:10px">{icon('check-circle', 20)}</span>
  <div class="grow"><div class="bold fs13">批量审核 · 无异动年审 12 个</div><div class="small muted">无风险且信息完整，可一键通过</div></div>
  <span class="btn btn-primary btn-sm">批量审核</span></a>
<div id="todo-list">{cards}</div>
<div class="small muted" style="text-align:center;padding:4px 0 8px">已加载全部待审事项 · 按提交时间倒序</div>"""
    page_t("teacher", DT + "todo.html", "待审", content, tab="todo", nav_title="待我审核",
           right='<a href="done.html">已审</a>',
           notes=["顶部页签按申请 / 年审 / 僵尸号 / 整改筛选，数量与工作台一致（共 9 项）",
                  "吸顶的“批量审核”入口汇总 12 个无异动年审，一键进入批量通过",
                  "注销、有异动年审等需核验材料的事项标注“PC 审核”，点击直达 PC 审核页",
                  "右上角“已审”查看本人审核记录"],
           flow=[("新建备案审核", "review-detail.html"), ("剧本三：交接审核", "review-handover.html"),
                 ("剧本五：年审审核", "review-annual.html"), ("批量审核", "review-batch.html"),
                 ("PC 端待我审核", "../../pc/teacher/todo.html")])


def t_done():
    recs = [
        ("pass", A_HO["name"], "抖音", "负责人交接", "已通过", "2026-09-28 10:05", "同意交接，生效时间 2026-10-01。", "review-result.html"),
        ("pass", "计院心理协会", "微博", "年度年审", "已通过", "2026-09-26 09:12", "无异动，信息完整。", "review-annual.html"),
        ("back", A_NEW["name"], "微信公众号", "新建备案", "已退回", "2026-09-25 09:30", F_NEW["steps"][1][3], "../student/application-returned.html"),
        ("other", A_ZB["name"], "微信公众号", "僵尸号核实", "建议注销", "2026-09-22 15:30", F_ZB["steps"][1][3], "../../pc/college/zombie-verify-detail.html"),
        ("other", A_RE["name"], "小红书", "年度年审", "要求整改", "2026-09-19 16:00", F_RE["steps"][0][3], "../../pc/common/archive-rectify.html"),
        ("reject", "计院编程兴趣小组", "抖音", "新建备案", "已驳回", "2026-09-17 14:48", "与“计院ACM协会”账号定位重复，且未取得组织成立批复。", "../student/application-rejected.html"),
        ("pass", "计院创新创业协会", "抖音", "信息变更", "已通过", "2026-09-16 11:05", "更换管理员手机号，同意。", "../../pc/common/archive-changes.html"),
    ]
    kinds = {"已通过": "success", "已退回": "danger", "已驳回": "danger", "建议注销": "warning", "要求整改": "danger"}
    items = "".join(
        f'<a class="m-card" href="{h}" data-cat="{c}" style="display:block"><div class="tc-top">{pf(p, "sm")}<div class="grow" style="min-width:0">'
        f'<div class="bold ellipsis">{n}</div><div class="small muted">{k} · {w}</div></div>{tag(r, kinds[r], True)}</div>'
        f'<div class="tc-note">{cm}</div></a>'
        for c, n, p, k, r, w, cm, h in recs)
    content = f"""
<div class="m-card"><div class="mini3">
  <div><b>23</b><small>本月已审</small></div><div><b class="c-success">19</b><small>通过</small></div><div><b class="c-danger">4</b><small>退回 / 驳回 / 整改</small></div>
</div></div>
{chips([('全部', 'all'), ('已通过', 'pass'), ('已退回', 'back'), ('已驳回', 'reject'), ('其他处置', 'other')], target='#done-list').replace('class="chips"', 'class="chips scroll-x"')}
<div id="done-list">{items}</div>
<button class="btn btn-default" type="button" style="width:100%" data-toast="已加载更早的 16 条审核记录">{icon('history')}加载更早记录</button>"""
    page_t("teacher", DT + "done.html", "已审", content, back="todo.html", nav_title="已审核记录",
           notes=["展示本人全部审核记录，结果标签统一配色：通过绿色、退回 / 驳回红色、建议注销橙色",
                  "筛选标签按审核结果过滤记录，点击记录查看该业务当前进展（跨端跳转）",
                  "审核记录同步写入账号档案与操作日志，PC 端“已审核”看到相同数据"],
           flow=[("学生查看退回意见", "../student/application-returned.html"), ("学院审核僵尸号核实结果", "../../pc/college/zombie-verify-detail.html"),
                 ("PC 端已审核", "../../pc/teacher/done.html")])


def t_messages():
    msgs = [
        ("audit", False, "user-switch", "green", "新的交接申请待审核", "李明提交“计院街舞社”负责人交接，拟 2026-10-01 生效", "2026-09-27 19:40", "review-handover.html"),
        ("audit", False, "file-add", "", "学生已重新提交新建申请", "“中南计算机青年”已按退回意见修改，请再次审核", "2026-09-26 20:05", "review-detail.html"),
        ("risk", False, "ghost", "red", "疑似僵尸号预警", "“2021级软件工程1班团支部”停更 412 天，请尽快核实", "2026-09-01 02:00", "review-zombie.html"),
        ("audit", True, "wrench", "orange", "整改材料已提交", "“计院摄影协会”已提交整改材料，等待您审核", "2026-09-28 22:05", "review-rectify.html"),
        ("risk", True, "clock", "orange", "年审截止提醒", f"教师审核截止 {T['teacher_end']}，您还有 3 条年审待审核", "2026-09-28 09:00", "todo.html"),
        ("sys", True, "hierarchy", "", "学院下发整改任务", "周建华已向“计院青年志愿者”下发整改任务 ZG20260920001", "2026-09-20 10:00", "../../pc/teacher/messages.html"),
        ("sys", True, "calendar", "", "年审任务已发布", f"{T['name']}已发布，系统已为您负责的账号生成年审记录", "2026-09-15 09:00", "todo.html"),
    ]
    items = "".join(
        f'<a class="m-card flex gap12 top-align" href="{h}" data-cat="{c}"><span class="stat-ic {col}" style="width:38px;height:38px;border-radius:11px">{icon(ic, 20)}</span>'
        f'<div class="grow" style="min-width:0"><div class="flex gap6"><span class="msg-dot{" read" if rd else ""}"></span><span class="bold fs13 grow ellipsis">{t}</span></div>'
        f'<div class="small sub mt4">{d}</div><div class="small muted mt4">{w}</div></div></a>'
        for c, rd, ic, col, t, d, w, h in msgs)
    content = f"""
{chips([('全部 7', 'all'), ('审核待办', 'audit'), ('风险预警', 'risk'), ('系统通知', 'sys')], target='#msg-list')}
<div id="msg-list" class="mt12">{items}</div>"""
    page_t("teacher", DT + "messages.html", "消息", content, back="home.html", nav_title="消息提醒",
           right='<button type="button" data-toast="已将 3 条未读消息标记为已读">全部已读</button>',
           notes=["消息按身份与授权范围生成：审核待办、风险预警、系统通知三类，可筛选",
                  "红点表示未读，点击消息直达对应审核 / 核实页面办理",
                  "年审截止等提醒保留在消息列表中，点击进入对应办理页"],
           flow=[("剧本三：交接审核", "review-handover.html"), ("僵尸号核实", "review-zombie.html")])


def t_mine():
    me = PEOPLE["王晓琳"]
    scopes = "".join(
        f'<div class="p-row"><span class="stat-ic {c}" style="width:36px;height:36px;border-radius:10px">{icon(ic, 18)}</span>'
        f'<div class="grow"><div class="bold fs13">{t}</div><div class="small muted">{d}</div></div><span class="bold num">{n}<span class="small muted"> 个</span></span></div>'
        for t, d, ic, c, n in [
            ("宣传工作辅导员", "计算机学院团委、学生会、科协及学院社团", "tag", "", 10),
            ("2021级辅导员", "2021级各班团支部", "users", "green", 7),
            ("街舞社指导教师", "计院街舞社", "star", "orange", 1),
        ])
    content = f"""
<div class="m-card flex gap12">{avatar('王晓琳', 'lg')}
  <div class="grow"><div class="fs18 bold">王晓琳</div><div class="small muted">工号 {me['no']} · {me['phone']}</div>
  <div class="flex gap6 mt4">{tag('业务教师', 'primary')}{tag('计算机学院', 'muted')}</div></div>
</div>
{sec('我的授权范围', scopes, '<span class="muted">共 18 个账号</span>')}
<div class="m-group">
  {cell(icon('file-check') + ' 已审核记录', '23 条', 'done.html')}
  {cell(icon('bell') + ' 消息提醒', '<span class="badge">3</span>', 'messages.html')}
</div>
<div class="alert alert-info">{icon('info')}<div class="grow">PC 和移动端同一账号体系、同一数据库、同一业务状态；移动端可完成主要审核工作。</div></div>"""
    page_t("teacher", DT + "mine.html", "我的", content, tab="mine", nav_title="我的",
           notes=["展示一人多身份：宣传工作辅导员、2021级辅导员、街舞社指导教师及各自授权账号数",
                  "已审核记录和消息提醒可从本页进入"],
           flow=[("已审核记录", "done.html"), ("消息提醒", "messages.html"),
                 ("PC 端教师工作台", "../../pc/teacher/workbench.html")])


def teacher_rows():
    """教师手机账号清单。状态与原来的卡片一致，档案正文另按同一账号补全。"""
    def rec(key, cat, name, platform, meta, run, sub, href, act, src=None, **over):
        src = src or {}
        level = over.get("level") or src.get("level") or meta.split(" · ")[0]
        return dict(
            key=key, cat=cat, name=name, platform=platform, pid=over.get("pid") or src.get("pid") or "—",
            org=over.get("org") or src.get("org") or name, level=level,
            org_type=over.get("org_type") or src.get("org_type") or "",
            college="计算机学院", teacher=over.get("teacher") or src.get("teacher") or "王晓琳",
            student=over.get("student") or src.get("student") or "—",
            run=run, filing=over.get("filing") or src.get("filing") or "已备案",
            annual=sub or src.get("annual") or "—", last=over.get("last") or src.get("last_post") or "",
            opened=src.get("opened") or "", fans=src.get("fans") or "",
            change=src.get("change") or "", idle_days=over.get("idle_days", src.get("idle_days")),
            meta=meta, act=act, href=href,
        )
    return [
        rec("an", "xc", A_AN["name"], A_AN["platform"], "二级平台 · 院级学生组织", "正常运行", "待指导教师审核", "review-annual.html", "审核年审", A_AN, last="2026-09-17"),
        rec("nw", "xc", A_NEW["name"], A_NEW["platform"], "二级平台 · 院级学生组织", "备案申请中", "", "review-detail.html", "审核新建", A_NEW),
        rec("rn", "xc", A_REN["name"], A_REN["platform"], "二级平台 · 院级学生组织", "正常运行", "变更申请中", "review-change.html", "审核变更", A_REN, last="2026-09-18"),
        rec("id", "xc", ACCOUNTS["idchange"]["name"], "哔哩哔哩", "二级平台 · 院级学生组织", "正常运行", "待填报", "", "", ACCOUNTS["idchange"]),
        rec("re", "xc", A_RE["name"], A_RE["platform"], "二级平台 · 院级学生组织", "整改中", "整改复核中", "", "", A_RE, last="2026-09-26"),
        rec("ph", "xc", A_PH["name"], A_PH["platform"], "社团平台 · 社团组织", "不活跃", "整改复核中", "review-rectify.html", "审核整改", A_PH),
        rec("px", "xc", ACCOUNTS["proxy"]["name"], "QQ", "社团平台 · 负责人已毕业", "正常运行", "待填报", "../../pc/teacher/proxy.html", "PC 代办", ACCOUNTS["proxy"], last="2026-09-24"),
        rec("gs", "xc", "计院研究生会", "视频号", "二级平台 · 院级学生组织", "正常运行", "待指导教师审核", "review-annual.html", "审核年审", student="刘佳宁"),
        rec("xl", "xc", "计院心理协会", "微博", "社团平台 · 社团组织", "正常运行", "待学院审核", "", ""),
        rec("cx", "xc", "计院创新创业协会", "抖音", "社团平台 · 社团组织", "正常运行", "待学院审核", "", ""),
        rec("zb", "fd", A_ZB["name"], A_ZB["platform"], "三级平台 · 停更 412 天", "不活跃", "疑似僵尸号", "review-zombie.html", "去核实", A_ZB),
        rec("ne", "fd", "2021级网络工程2班团支部", "QQ", "三级平台 · 班级团支部", "申请注销", "注销申请中", "../../pc/teacher/review-cancel.html", "PC 审核", org="2021级网络工程2班团支部", level="三级平台", org_type="班级团支部"),
        rec("ai", "fd", "2021级人工智能1班团支部", "QQ", "三级平台 · 停更 236 天", "不活跃", "疑似僵尸号", "", "", org="2021级人工智能1班团支部", level="三级平台", org_type="班级团支部", idle_days=236),
        rec("cs2", "fd", "2021级计算机科学2班团支部", "QQ", "三级平台 · 班级团支部", "不活跃", "待填报", "", "", org="2021级计算机科学2班团支部", level="三级平台", org_type="班级团支部"),
        rec("is", "fd", "2021级信息安全1班团支部", "微信公众号", "三级平台 · 班级团支部", "申请注销", "注销申请中", "", "", org="2021级信息安全1班团支部", level="三级平台", org_type="班级团支部"),
        rec("cs1", "fd", "2021级计算机科学1班团支部", "微信公众号", "三级平台 · 班级团支部", "已注销", "本年度注销", "", "", org="2021级计算机科学1班团支部", level="三级平台", org_type="班级团支部", filing="已注销"),
        rec("se2", "fd", "2021级软件工程2班团支部", "微信公众号", "三级平台 · 班级团支部", "已注销", "本年度注销", "", "", org="2021级软件工程2班团支部", level="三级平台", org_type="班级团支部", filing="已注销"),
        rec("ho", "jw", A_HO["name"], A_HO["platform"], "社团平台 · 社团组织", "正常运行", "交接审核中", "review-handover.html", "审核交接", A_HO, last="2026-09-12"),
    ]


def t_accounts():
    items = []
    for r in teacher_rows():
        sub = r["annual"] if r["annual"] != "—" else ""
        sub_tag = st(sub, False) if sub in STATUS_KIND else tag(sub, "warning")
        action = btn(r["act"], r["href"], "light", size="sm") if r["href"] else ""
        items.append(
            '<div class="m-card" data-cat="' + r["cat"] + '"><div class="tc-top top-align">' + pf(r["platform"])
            + '<div class="grow" style="min-width:0"><div class="bold ellipsis">' + r["name"] + '</div>'
            + '<div class="small muted ellipsis">' + r["platform"] + " · " + r["meta"] + '</div>'
            + '<div class="flex gap6 wrap mt4">' + st(r["run"]) + (sub_tag if sub else "") + '</div></div></div>'
            + '<div class="tc-ft" style="justify-content:flex-end">'
            + btn("查看档案", "archive.html?c=" + r["key"], "default", size="sm") + action + '</div></div>'
        )
    content = (
        '<label class="search-box">' + icon("search") + '<input placeholder="搜索账号名称 / 组织" data-search="#acct-list" aria-label="搜索账号"></label>'
        + chips([("全部 18", "all"), ("宣传工作 10", "xc"), ("2021级 7", "fd"), ("街舞社 1", "jw")], target="#acct-list").replace('class="chips"', 'class="chips scroll-x"', 1)
        + '<div id="acct-list">' + "".join(items) + '</div>'
    )
    page_t("teacher", DT + "accounts.html", "负责账号", content, tab="accounts", nav_title="我负责的账号",
           notes=["按授权范围（宣传工作 / 2021级 / 街舞社）筛选，搜索框按名称实时过滤",
                  "每个账号展示运行状态与当前业务状态，有待办的账号可直接进入审核",
                  "查看档案打开与 PC 相同分区的手机档案，原有审核和代办按钮仍留在卡片上",
                  "毕业学生负责的账号（如计院ACM协会）仍可进入教师代办"],
           flow=[("手机档案", "archive.html?c=rn"), ("教师代办（剧本八）", "../../pc/teacher/proxy.html"),
                 ("PC 我负责的账号", "../../pc/teacher/accounts.html")])


def t_archive():
    cases = []
    for i, r in enumerate(teacher_rows()):
        flags = st(r["run"])
        if r["annual"] and r["annual"] != "—":
            flags += st(r["annual"], False) if r["annual"] in STATUS_KIND else tag(r["annual"], "warning")
        act = action_row([(r["act"], r["href"], "primary")]) if r["href"] else ""
        cls = "hidden" if i else ""
        cases.append(
            '<div data-case="' + r["key"] + '" class="' + cls + '">'
            + head(r["name"], r["platform"], r["org"], flags)
            + render_archive(r) + act + "</div>"
        )
    page_t("teacher", DT + "archive.html", "账号档案", "".join(cases), back="accounts.html",
           css=ARCHIVE_CSS, js=ARCH_JS, nav_title="账号档案",
           notes=["分区与 PC 账号档案一致：基本信息、平台信息、归属、负责人与管理员、年审、变更、整改、操作记录",
                  "从负责账号进入，状态与那张卡片一致",
                  "卡片上原有的审核、核实、代办按钮在档案底部保留"],
           flow=[("返回负责账号", "accounts.html"), ("审核年审", "review-annual.html"),
                 ("审核交接", "review-handover.html"), ("PC 账号档案", "../../pc/common/archive-staff.html")])


def _review_bottom(pass_text, pass_href, pass_toast, reject_id="#dlg-reject", return_href="review-return.html"):
    return (toggle_btn("驳回", reject_id, "danger", cls="slim")
            + jump("退回", return_href, "warning", cls="slim")
            + jump(pass_text, pass_href, "primary", pass_toast, cls="wide"))


def _reject_dialog(case_desc):
    return dialog("dlg-reject", "确认驳回该申请？", f"驳回即不予办理，流程终止，申请人需重新发起。{case_desc}",
                  "请填写驳回原因（必填），将通知申请人", "确认驳回", "review-result.html?c=reject", "已驳回，已通知申请人")


def t_review_detail():
    org = rows([("所属学院", "计算机学院"), ("所属团学组织", A_NEW["org"]), ("组织类别", A_NEW["org_type"]), ("平台管理层级", A_NEW["level"])])
    plat = rows([("平台类型", A_NEW["platform"]), ("账号名称", A_NEW["name"]), ("曾用名", "无"), ("平台ID", A_NEW["pid"]),
                 ("是否认证", "否"), ("粉丝数", "0"), ("运营团队规模（单位：人）", "6"),
                 ("开通时间", A_NEW["opened"]), ("主页链接", "mp.weixin.qq.com/csu_cs_youth"),
                 ("平台头像", "已上传"), ("二维码", "未上传（非必填）"), ("信息发布范围", "学院团学活动相关信息。")])
    plat += (f'<div class="flex between mt8"><span class="small muted">平台介绍</span>{tag("本次修改 · 326 字", "warning")}</div>'
             f'<div class="intro">{INTRO}</div>'
             f'<div class="small muted mt8">平台信息确认</div>{mechanism_blocks()}')
    run = rows([("最近一次公开内容发布时间", "2026-09-22"), ("更新频率", "每周更新（≥1次/周）"),
                ("运行状态", "正常运行"), ("异常情况", "无"), ("备注", "无")])
    lm, wx, zw = PEOPLE["李明"], PEOPLE["王晓琳"], PEOPLE["张卫东"]
    zj, cj = PEOPLE["周建华"], PEOPLE["陈静"]
    staff = rows([("当前管理教师", f"王晓琳 · {wx['no']} · 宣传工作辅导员 · 专职 · {wx['phone']}"),
                  ("具体负责人", f"李明 · {lm['no']} · {lm['phone']}"),
                  ("管理员", "陈可欣（8209230221）、刘子涵（8209240133）"),
                  ("一审负责人", f"王晓琳 · {wx['no']} · {wx['phone']}"),
                  ("二审负责人", f"周建华 · {zj['no']} · {zj['phone']}"),
                  ("三审负责人", f"陈静 · {cj['no']} · {cj['phone']}"),
                  ("第一责任人", f"张卫东 · {zw['job']}")])
    content = f"""
{head(A_NEW['name'], A_NEW['platform'], F_NEW['no'] + ' · 李明 2026-09-26 重新提交', tag('新建备案', 'primary') + tag('二次提交', 'warning') + st('待审核'))}
{m_steps(['学生提交', '教师审核', '学院审核', '校级审核'], 1)}
<div class="alert alert-info mb12">{icon('refresh')}<div class="grow">退回后重新提交：{F_NEW['steps'][2][3]}</div></div>
{fold('f-org', '归属信息', org, False)}
{fold('f-plat', '平台信息', plat)}
{fold('f-run', '运行信息', run, False)}
{fold('f-staff', '责任人', staff, False)}
{sec('审核流程', flow_tl('new', 3, '指导教师审核', '王晓琳 · 待审核（当前节点）', back_idx=(1,)))}
{opinion(F_NEW['steps'][3][3])}"""
    page_t("teacher", DT + "review-detail.html", "新建备案审核", content, back="todo.html",
           bottom=_review_bottom("通过", "review-result.html?c=new", "已通过，流转至学院审核"),
           overlay=_reject_dialog(""),
           notes=["本单为退回后重新提交的版本，顶部提示学生本次补充的内容，平台介绍标注“本次修改 · 326 字”",
                  "归属 / 平台 / 运行 / 责任人分区可点击标题折叠展开，默认展开平台信息",
                  "底部三种处理：驳回（手机内弹窗，原因必填，流程终止）、退回（选择需修改字段）、通过（流转学院审核）",
                  "时间线中第一次退回节点以橙色标识，审核意见预填可修改"],
           flow=[("通过 → 审核完成", "review-result.html?c=new"), ("退回 → 填写退回原因", "review-return.html"),
                 ("学院移动端审核", "../college/review-detail.html"), ("学院 PC 审核", "../../pc/college/approval-detail.html")])


def t_review_change():
    same = rows([("平台类型", A_REN["platform"]), ("平台 ID", A_REN["pid"]), ("所属组织", A_REN["org"]),
                 ("管理教师", "王晓琳"), ("学生负责人", "李明")])
    files = "".join(f'<span class="file-chip">{icon("file")}{x}</span>' for x in ["学生会换届决议.pdf", "新名称品牌说明.docx"])
    reason = f'<div class="fs13 sub">{F_REN["steps"][0][3]}</div><div class="upload-list">{files}</div>'
    content = f"""
{head(A_REN['name'], A_REN['platform'], F_REN['no'] + ' · 李明 2026-09-26 14:30', tag('名称变更', 'warning') + tag('重要变更', 'danger') + st('待审核'))}
{m_steps(['学生提交', '教师审核', '学院审核', '校级审核'], 1)}
<div class="m-card"><div class="sec-t">变更对比<span class="ml-auto">{tag('1 项变更', 'warning')}</span></div>
  <div class="cmp old"><div class="small muted">变更前 · 账号名称</div><div class="v">{A_REN['name']}</div></div>
  <div class="cmp-arrow"><span class="arrow-c" style="transform:rotate(90deg)">{icon('arrow-right')}</span></div>
  <div class="cmp new"><div class="small muted">变更后 · 账号名称</div><div class="v">{A_REN['new_name']}</div></div>
  <div class="small muted mt12">未变更字段</div>{same}
</div>
{sec('变更原因', reason)}
<div class="alert alert-warning mb12">{icon('alert')}<div class="grow"><b>重要变更报校团委：</b>账号名称变更须经教师、学院审核后报校团委审核；生效后原名称“{A_REN['name']}”记入曾用名。</div></div>
{sec('审核流程', flow_tl('rename', 1, '指导教师审核', '王晓琳 · 待审核（当前节点）'))}
{opinion(F_REN['steps'][1][3])}"""
    page_t("teacher", DT + "review-change.html", "变更审核", content, back="todo.html",
           bottom=_review_bottom("通过", "review-result.html?c=change", "已通过，流转至学院审核"),
           overlay=_reject_dialog(""),
           notes=["变更前后对比卡片突出显示名称变化，未变更字段折叠在下方供核对",
                  "名称变更属重要变更：教师 → 学院 → 校团委三级审核，生效后保留曾用名",
                  "驳回为手机内确认弹窗，退回进入退回原因页，通过流转学院审核"],
           flow=[("通过 → 审核完成", "review-result.html?c=change"), ("退回 → 填写退回原因", "review-return.html"),
                 ("学院审核（剧本二）", "../../pc/college/approval-change.html"), ("PC 端变更审核", "../../pc/teacher/review-change.html")])


def t_review_handover():
    lm, ls = PEOPLE["李明"], PEOPLE["李四"]
    persons = f"""
<div style="display:grid;grid-template-columns:1fr 28px 1fr;gap:8px">
  <div class="person">{avatar('李明')}<div class="bold">李明</div>{tag('原负责人', 'muted')}
    <div class="small muted mt4">学号 {lm['no']}<br>任期 2024-09-10<br>~ 2026-09-30</div></div>
  <span class="arrow-c">{icon('arrow-right')}</span>
  <div class="person new">{avatar('李四')}<div class="bold">李四</div>{tag('新负责人', 'primary')}
    <div class="small muted mt4">学号 {ls['no']}<br>{ls['phone']}<br>{ls['job']}</div></div>
</div>"""
    checks = "".join(f'<div>{icon("check-circle")}{t}<em>{e}</em></div>' for t, e in [
        ("新负责人已实名认证", "统一身份认证"), ("新负责人已确认接收", "2026-09-27 20:02"),
        ("账号密码与绑定手机已移交", "学生声明"), ("新负责人无其他在任冲突", "系统校验")])
    content = f"""
{head(A_HO['name'], A_HO['platform'], F_HO['no'] + ' · ' + A_HO['pid'] + ' · 粉丝 ' + A_HO['fans'], tag('负责人交接', 'success') + st('正常运行') + st('待审核'))}
{sec('交接信息', persons + rows([('生效时间', '<b class="c-primary">2026-10-01</b>'), ('新负责人班级', ls['grade']), ('交接原因', F_HO['steps'][0][3])]))}
<div class="alert alert-info mb12">{icon('info')}<div class="grow"><b>规则：</b>教师审核通过即生效，原负责人任职起止时间保留，记入责任人员历史。</div></div>
{sec('交接核验', f'<div class="ok-list">{checks}</div>')}
{sec('审核流程', flow_tl('handover', 1, '指导教师审核（通过即生效）', '王晓琳 · 待审核（当前节点）'))}
{opinion(F_HO['steps'][1][3])}"""
    page_t("teacher", DT + "review-handover.html", "交接审核", content, back="todo.html",
           bottom=_review_bottom("通过并生效", "review-result.html", "审核通过，交接已生效"),
           overlay=_reject_dialog(""),
           notes=["剧本三第 3 步：原负责人与新负责人卡片左右对照，显示学号、任期与联系方式",
                  "交接只需指导教师一级审核，通过即生效（2026-10-01），无需学院 / 校团委审核",
                  "原负责人李明的任职起止时间（2024-09-10 ~ 2026-09-30）保留在责任人员历史中",
                  "驳回为手机内弹窗（原因必填），退回进入退回原因页"],
           flow=[("剧本三下一步：审核完成即生效", "review-result.html"), ("退回 → 填写退回原因", "review-return.html"),
                 ("学生端提交成功页（上一步）", "../student/apply-result.html")])


def t_review_annual():
    confirms = "".join(f'<div>{icon("check-circle")}{t}<em>{e}</em></div>' for t, e in [
        ("账号仍在运营", "正常"), ("账号名称无变化", "正常"), ("平台 ID 无变化", "正常"), ("所属组织无变化", "正常"),
        ("管理教师无变化", "正常"), ("学生负责人无变化", "正常"), ("四项机制运行正常", "正常"),
        ("本年度无违规违纪记录", "正常"), ("更新频率：每周更新", "最近发布 2026-09-17")])
    compare = f"""
<div class="mini3">
  <div><small>粉丝数</small><b>36,512</b><span class="up">较 2025 +11.1%</span></div>
  <div><small>年度发布</small><b>156</b><span class="up">较 2025 +14 篇</span></div>
  <div><small>2025 年审</small><b class="c-success" style="font-size:14px;line-height:1.9">年审通过</b><span class="small muted">无整改</span></div>
</div>"""
    sheet_items = "".join(
        f'<a class="sheet-item" href="{h}"><span class="qi {c}">{icon(ic, 20)}</span><div class="grow"><div class="bold fs13">{t}</div>'
        f'<div class="small muted">{d}</div></div>{icon("chevron-right", cls="arrow")}</a>'
        for t, d, ic, c, h in [
            ("退回修改", "退回学生补充或更正填报内容", "undo", "orange", "review-return.html"),
            ("修改后确认", "教师直接修正信息后确认通过（PC 端）", "file-edit", "", "../../pc/teacher/review-annual-edit.html"),
            ("标记疑似僵尸号", "进入僵尸号核实流程", "ghost", "red", "review-zombie.html"),
            ("要求整改", "提交学院下发整改任务（PC 端）", "wrench", "orange", "../../pc/college/rectify-create.html"),
            ("建议注销", "发起账号注销申请（PC 端）", "power", "red", "../../pc/common/apply-cancel.html"),
        ])
    overlay = (f'<div class="sheet-mask hidden" id="more-sheet"><div class="sheet"><div class="sheet-hd">其他处理方式</div>'
               f'<div class="small muted" style="text-align:center;margin-bottom:4px">年审共 6 种教师操作，通过为主操作</div>'
               f'{sheet_items}<button class="sheet-cancel" type="button" data-toggle="#more-sheet">取消</button></div></div>')
    content = f"""
{head(A_AN['name'], A_AN['platform'], F_AN['no'] + ' · ' + A_AN['pid'] + ' · 粉丝 ' + A_AN['fans'], st('无异动') + st('待指导教师审核') + st('正常运行'))}
{m_steps(['学生填报', '教师审核', '学院审核', '校级审核'], 1)}
{sec('学生确认事项', f'<div class="ok-list">{confirms}</div>', '<span class="c-success">9 / 9 正常</span>')}
{sec('年度异动', rows([('异动类型', st('无异动')), ('填报人', '李明 · 2026-09-18 21:16'), ('填报说明', F_AN['steps'][1][3])]))}
{sec('账号主页截图', f'<div class="shot"><img src="{PHOTOS["screenshot"]}" alt="中南计院团委公众号主页截图"><span>2026-09-18 上传 · 1/1</span></div>')}
{sec('与 2025 年度对比', compare)}
{sec('审核流程', flow_tl('annual', 2, '指导教师审核', '王晓琳 · 待审核（当前节点）'))}
{opinion(F_AN['steps'][2][3])}
<a class="m-card batch-entry" href="review-batch.html"><span class="stat-ic green" style="width:36px;height:36px;border-radius:10px">{icon('check-circle', 20)}</span>
  <div class="grow"><div class="bold fs13">其余 11 个无异动年审可批量通过</div><div class="small muted">剧本五下一步：批量审核</div></div>{icon('chevron-right', cls='arrow')}</a>"""
    page_t("teacher", DT + "review-annual.html", "年审审核", content, back="todo.html",
           bottom=(toggle_btn("更多操作", "#more-sheet", "default", "more")
                   + jump("通过", "review-result.html?c=annual", "primary", "年审已通过，流转至学院审核", "check", cls="wide")),
           overlay=overlay,
           notes=["剧本五第 6 步：学生确认的 9 项全部正常、无异动，最近发布 2026-09-17",
                  "展示账号主页截图与 2025 年度对比，辅助判断是否真实运营",
                  "教师 6 种操作：“通过”为主操作；“更多操作”底部面板提供退回修改、修改后确认、标记疑似僵尸号、要求整改、建议注销",
                  "修改后确认、要求整改、建议注销涉及较多表单，跳转 PC 端办理"],
           flow=[("剧本五下一步：无异动批量通过", "review-batch.html"), ("通过 → 审核完成", "review-result.html?c=annual"),
                 ("修改后确认（PC）", "../../pc/teacher/review-annual-edit.html"), ("要求整改（剧本六）", "../../pc/college/rectify-create.html")])


def t_review_zombie():
    rules = "".join(f'<div>{icon("alert-circle")}{t}<em>{e}</em></div>' for t, e in [
        ("停更 ≥ 180 天", "命中 · 412 天"), ("团支部已毕业", "命中 · 2025-06"), ("学生负责人为空", "命中 · 已毕业")])
    hints = (f'<div class="zv zv-ok hidden mt8">{alert("核实为仍正常运营：需补充近期运营截图，解除预警后恢复年审流转。", "success")}</div>'
             f'<div class="zv zv-fix hidden mt8">{alert("需整改：将提交学院下发整改任务，整改期间状态为“整改中”。", "warning")}</div>'
             f'<div class="zv zv-cancel mt8">{alert("建议注销：提交学院审核，学院转注销后由校团委确认，账号数据永久保留。", "danger")}</div>')
    content = f"""
{head(A_ZB['name'], A_ZB['platform'], F_ZB['no'] + ' · ' + A_ZB['pid'] + ' · 粉丝 ' + A_ZB['fans'], st('疑似僵尸号') + st('高风险') + st('不活跃'))}
<div class="m-card"><div class="mini3">
  <div><b class="c-danger">{A_ZB['idle_days']}</b><small>停更天数</small></div>
  <div><b style="font-size:13px;line-height:2;white-space:nowrap">{A_ZB['last_post']}</b><small>最近发布</small></div>
  <div><b style="font-size:14px;line-height:1.9">已毕业</b><small>团支部状态</small></div>
</div></div>
{sec('触发规则', f'<div class="ok-list" style="--ok:var(--c-danger)">{rules}</div><div class="tc-note">{F_ZB["steps"][0][3]}</div>', '<span class="c-danger">3 条命中</span>')}
<div class="m-card"><div class="sec-t">核实结论<span class="req" style="margin-left:-4px">*</span></div>
  {choices('.zv', [('仍正常运营', '账号仍有学生运营，解除预警', '.zv-ok', False), ('需整改', '存在问题，需限期整改', '.zv-fix', False), ('建议注销', '无人运营或组织已撤销', '.zv-cancel', True)])}
  {hints}
</div>
<div class="m-group">{m_textarea('核实说明', '请填写核实情况', F_ZB['steps'][1][3], req=True, maxlen=200)}</div>
{sec('佐证材料', upload('上传佐证材料', '毕业名单、团支部撤销说明等，支持图片 / PDF', ['2021级软件工程1班毕业名单.pdf']))}
<div class="alert alert-warning">{icon('shield')}<div class="grow"><b>系统不直接注销：</b>辅导员核实结论提交学院审核，学院转注销后由校团委确认。</div></div>"""
    page_t("teacher", DT + "review-zombie.html", "僵尸号核实", content, back="todo.html",
           bottom=submit_btn("提交核实结果", "review-result.html?c=zombie", toast="核实结果已提交学院审核"),
           css=".ok-list .i{color:var(--ok,var(--c-success))}",
           notes=["展示停更天数、最近发布时间与命中规则，辅助辅导员核实",
                  "核实结论三选一（默认“建议注销”），切换结论时下方提示对应的后续流程",
                  "核实说明必填（已按剧本七预填），可上传佐证材料",
                  "系统不直接注销：结论提交学院审核，再由校团委确认"],
           flow=[("剧本七下一步：学院审核转注销", "../../pc/college/zombie-verify-detail.html"),
                 ("提交 → 审核完成", "review-result.html?c=zombie"), ("PC 端僵尸号核实", "../../pc/teacher/review-zombie.html")])


def t_review_rectify():
    reqs = f"""
<div class="req-item"><div class="req-q">{tag('要求 1', 'danger')}<span>补全学生负责人：当前学生负责人信息缺失，需补录并完成实名认证</span></div>
  <div class="req-a">{icon('check-circle', 14)}<span>已补录学生负责人 李明（{PEOPLE['李明']['no']}），并新增管理员 1 名</span></div></div>
<div class="req-item"><div class="req-q">{tag('要求 2', 'danger')}<span>恢复更新：停更 212 天，需于截止前恢复正常更新（≥ 2 条）</span></div>
  <div class="req-a">{icon('check-circle', 14)}<span>2026-09-26、2026-09-28 已发布 2 条作品，并制定 10 月更新计划</span></div>
  <div class="shot mt8"><img src="{PHOTOS['phone']}" alt="视频号近期作品截图" style="height:120px"><span>近期作品截图</span></div></div>"""
    hints = (f'<div class="rf rf-pass mt8">{alert("整改通过：结束整改任务，账号恢复“正常运行”，年审恢复流转。", "success")}</div>'
             f'<div class="rf rf-cont hidden mt8">{alert("继续整改：将退回学生补充材料，整改轮次 +1。", "warning")}</div>'
             f'<div class="rf rf-cancel hidden mt8">{alert("转注销：整改无望时转入注销流程，需学院与校团委审核。", "danger")}</div>')
    content = f"""
{head(A_PH['name'], A_PH['platform'], 'ZG20260915003 · 第 1 轮 · 截止 2026-10-15', tag('整改审核', 'warning') + st('整改复核中') + st('不活跃'))}
{sec('整改要求与提交情况', reqs, '<span class="c-success">2 / 2 已响应</span>')}
{sec('整改说明', f'<div class="fs13 sub">负责人已补录，社团已恢复运营并安排专人每周更新。</div><div class="upload-list"><span class="file-chip">{icon("file")}学生负责人补录表.pdf</span><span class="file-chip">{icon("image")}近期作品截图.png</span></div><div class="small muted mt8">李明 · 2026-09-28 22:05 提交</div>')}
<div class="m-card"><div class="sec-t">审核结论</div>
  {choices('.rf', [('整改通过', '整改要求均已落实', '.rf-pass', True), ('继续整改', '材料不全或未落实', '.rf-cont', False), ('转注销', '无法整改，转注销流程', '.rf-cancel', False)])}
  {hints}
</div>
{opinion('负责人已补全，已恢复更新，同意整改通过。')}"""
    page_t("teacher", DT + "review-rectify.html", "整改审核", content, back="todo.html",
           bottom=submit_btn("提交审核结论", "review-result.html?c=rectify", toast="整改审核结论已提交"),
           notes=["逐条对照整改要求与学生提交情况：补全学生负责人、恢复更新",
                  "审核结论三选一：整改通过 / 继续整改 / 转注销，切换后提示对应后续流程",
                  "教师审核结论同步至学院整改跟踪，整改记录写入账号档案"],
           flow=[("提交 → 审核完成", "review-result.html?c=rectify"), ("学院整改跟踪", "../college/rectify.html"),
                 ("档案整改记录", "../../pc/common/archive-rectify.html")])


def t_review_return():
    fields = "".join(f'<button type="button" class="chip{" on" if on else ""}" data-choice="">{f}</button>' for f, on in [
        ("平台介绍", True), ("信息发布范围", True), ("平台名称", False), ("平台 ID", False), ("主要栏目", False),
        ("学生负责人", False), ("管理教师", False), ("四项机制", False), ("佐证材料", False)])
    quick = "".join(f'<button type="button" class="chip" onclick="addReason(this)">{q}</button>' for q in [
        "平台介绍不足 100 字", "信息填写不完整", "佐证材料不清晰", "负责人信息有误", "组织归属不正确"])
    content = f"""
<div class="m-card flex gap12">{pf(A_NEW['platform'])}<div class="grow"><div class="bold">{A_NEW['name']} · 新建备案</div>
  <div class="small muted">{F_NEW['no']} · 申请人 李明</div></div>{st('待审核')}</div>
<div class="m-card"><div class="sec-t">需修改的字段<span class="ml-auto muted">可多选</span></div><div class="chip-group">{fields}</div></div>
<div class="m-card"><div class="sec-t">常用退回原因<span class="ml-auto muted">点击填入</span></div><div class="chip-group">{quick}</div></div>
<div class="m-group"><div class="cell col-cell"><span class="cell-label"><span class="req">*</span>退回说明</span>
  <textarea class="m-textarea" id="ret-reason" placeholder="请说明需要修改的内容，将通知申请人" required maxlength="300" data-count>{F_NEW['steps'][1][3]}</textarea>
  <div class="count-tip">{len(F_NEW['steps'][1][3])} / 300</div><div class="err-msg">请填写退回说明</div></div></div>
<div class="alert alert-info">{icon('info')}<div class="grow">退回后申请回到申请人，修改后重新提交，将再次由您审核；原审核记录保留在流程时间线中。</div></div>"""
    js = r"""
function addReason(el){var ta=document.getElementById('ret-reason');var v=el.textContent.trim();
  if(ta.value.indexOf(v)<0){ta.value=(ta.value?ta.value.replace(/[。；\s]+$/,'')+'；':'')+v+'。';}
  el.classList.add('on');ta.dispatchEvent(new Event('input',{bubbles:true}));}
"""
    page_t("teacher", DT + "review-return.html", "退回原因", content, back="review-detail.html",
           bottom=back_btn("review-detail.html", "取消") + submit_btn("确认退回", "review-result.html?c=return", "warning", "undo", "已退回，已通知申请人"),
           js=js,
           notes=["需修改字段可多选，申请人重新编辑时仅高亮这些字段",
                  "常用退回原因点击即追加到说明中，退回说明为必填，清空后提交将标红提示",
                  "确认退回后通知申请人（学生李明），申请进入“已退回”状态"],
           flow=[("学生查看退回意见", "../student/application-returned.html"), ("退回完成", "review-result.html?c=return"),
                 ("PC 端退回弹窗", "../../pc/common/modal-return.html")])


def t_review_batch():
    recs = [
        (A_AN["name"], "微信公众号", "李明", "09-17"),
        ("计院研究生会", "视频号", "刘佳宁", "09-25"),
        ("计院心理协会", "微博", "陈雨萱", "09-22"),
        ("计院创新创业协会", "抖音", "黄子轩", "09-27"),
        ("计院网络安全协会", "微信公众号", "周子墨", "09-26"),
        ("计院辩论队", "哔哩哔哩", "林书瑶", "09-19"),
        ("计院新闻中心", "微博", "李明", "09-28"),
        ("计院红十字分会", "微信公众号", "唐可欣", "09-21"),
        ("计院羽毛球协会", "抖音", "邓浩然", "09-24"),
        ("计院书画协会", "小红书", "苏语桐", "09-18"),
        ("计院就业服务站", "微信公众号", "韩思远", "09-29"),
        ("计院科技创新中心", "视频号", "钱一鸣", "09-23"),
    ]
    rows_html = "".join(
        f'<label class="bk-row"><input type="checkbox" class="bk" checked aria-label="选择{n}">{pf(p, "sm")}'
        f'<div class="grow" style="min-width:0"><div class="bold fs13 ellipsis">{n}</div><div class="small muted ellipsis">{who} 确认 · 最近发布 {last}</div></div>'
        f'{st("无异动", False)}</label>' for n, p, who, last in recs)
    excluded = "".join([
        list_item("../../pc/teacher/review-annual.html", "swap", "orange", "计院科协（哔哩哔哩）", "有异动：平台 ID 变化，需逐条审核", tag("PC 审核", "muted")),
        list_item("review-zombie.html", "ghost", "red", A_ZB["name"], "疑似僵尸号，需先完成核实", tag("去核实", "danger")),
    ])
    content = f"""
<div class="alert alert-info mb12">{icon('shield')}<div class="grow"><b>批量规则：</b>仅无异动、无风险且信息完整的账号可批量通过；有异动、疑似僵尸号、待整改账号需逐条审核。</div></div>
<label class="bk-all"><input type="checkbox" id="bk-all" checked aria-label="全选"><span class="bold grow">全选无异动年审</span><span class="small muted">已选 <b class="c-primary" data-bk-count>12</b> / 12</span></label>
<div class="m-group">{rows_html}</div>
<div class="m-title">不可批量（需逐条审核）<span class="small muted" style="font-weight:400">2 个</span></div>
<div class="m-card" style="padding:4px 14px">{excluded}</div>
<a class="m-card pc-hint" href="../../pc/college/annual-review.html"><span class="stat-ic green" style="width:36px;height:36px;border-radius:10px">{icon('hierarchy', 18)}</span>
  <div class="grow"><div class="bold fs13">通过后进入学院年审审核</div><div class="small muted">剧本五下一步 · 学院 PC 端汇总确认</div></div>{icon('chevron-right', cls='arrow')}</a>"""
    js = r"""
(function(){
  var all=document.getElementById('bk-all'),go=document.getElementById('bk-go');
  function sync(){
    var bs=document.querySelectorAll('.bk'),n=0;
    bs.forEach(function(b){if(b.checked)n++;b.closest('.bk-row').classList.toggle('on',b.checked);});
    document.querySelectorAll('[data-bk-count]').forEach(function(x){x.textContent=n;});
    all.checked=n===bs.length;all.indeterminate=n>0&&n<bs.length;
    go.classList.toggle('disabled',n===0);go.dataset.toast='已批量通过 '+n+' 条无异动年审记录';
  }
  document.addEventListener('change',function(e){
    if(e.target===all){document.querySelectorAll('.bk').forEach(function(b){b.checked=all.checked;});}
    if(e.target===all||e.target.classList.contains('bk'))sync();
  });
  sync();
})();
"""
    bottom = (f'<div class="grow" style="flex:1;display:flex;flex-direction:column;justify-content:center"><div class="small muted">已选择</div>'
              f'<div class="bold"><span class="c-primary fs18" data-bk-count>12</span> 条年审</div></div>'
              f'<button class="btn btn-primary wide" type="button" id="bk-go" data-href="review-result.html?c=batch" '
              f'data-toast="已批量通过 12 条无异动年审记录">{icon("check")}批量通过（<span data-bk-count>12</span>）</button>')
    page_t("teacher", DT + "review-batch.html", "批量审核", content, back="todo.html", bottom=bottom, js=js,
           notes=["剧本五第 7 步：列出 12 个无异动年审记录（含中南计院团委），默认全选",
                  "全选框支持全选 / 取消 / 半选状态，底部实时显示已选数量，未选择时批量按钮置灰",
                  "有异动或疑似僵尸号的账号单独列出，不可批量，需逐条审核",
                  "批量通过后记录流转至学院年审审核"],
           flow=[("剧本五下一步：学院年审审核", "../../pc/college/annual-review.html"),
                 ("批量通过 → 审核完成", "review-result.html?c=batch"), ("返回单条年审审核", "review-annual.html")])


def t_review_result():
    def case(key, kind, title, desc, card_rows, links, hidden=True):
        h = " hidden" if hidden else ""
        lk = "".join(f'<a class="cell" href="{hh}"><span class="cell-label fs13 c-primary">{tt}</span><span class="cell-value"></span>'
                     f'{icon("chevron-right", cls="arrow")}</a>' for tt, hh in links)
        return (f'<div data-case="{key}" class="{h.strip()}"><div class="result" style="padding:28px 8px 8px">'
                f'<div class="result-ic {kind}">{icon("check" if kind == "ok" else ("undo" if kind == "warn" else "x"))}</div>'
                f'<h2>{title}</h2><p class="fs13">{desc}</p></div>'
                f'<div class="m-card res-card">{rows(card_rows)}</div><div class="m-group">{lk}</div></div>')
    cases = "".join([
        case("handover", "ok", "审核完成", "交接审核已通过，按规则即时生效",
             [("账号", f"{A_HO['name']}（抖音）"), ("处理结果", '<span class="c-success bold">通过，交接已生效</span>'),
              ("负责人", "李明 → <b>李四</b>"), ("生效时间", "2026-10-01"),
              ("原负责人任期", "2024-09-10 ~ 2026-09-30"), ("历史记录", "已记入责任人员历史"), ("通知", "已通知李明、李四")],
             [("查看责任人员历史（PC 档案）", "../../pc/common/archive-staff.html")], hidden=False),
        case("new", "ok", "审核完成", "已通过，流转至学院审核",
             [("账号", A_NEW["name"]), ("申请编号", F_NEW["no"]), ("处理结果", '<span class="c-success bold">指导教师审核通过</span>'),
              ("下一节点", "学院团委审核 · 周建华")],
             [("学院移动端审核", "../college/review-detail.html"), ("学院 PC 审核", "../../pc/college/approval-detail.html")]),
        case("change", "ok", "审核完成", "已通过，流转至学院审核；属重要变更将报校团委",
             [("账号", A_REN["name"]), ("变更内容", f"名称 → {A_REN['new_name']}"), ("下一节点", "学院团委审核 · 周建华")],
             [("学院变更审核（PC）", "../../pc/college/approval-change.html")]),
        case("annual", "ok", "审核完成", "年审已通过，流转至学院审核",
             [("账号", A_AN["name"]), ("年审编号", F_AN["no"]), ("异动类型", "无异动"), ("下一节点", "学院年审审核")],
             [("继续批量审核其余无异动年审", "review-batch.html")]),
        case("batch", "ok", "批量审核完成", "已批量通过 12 条无异动年审记录",
             [("通过数量", '<b class="c-success">12 条</b>'), ("审核意见", "无异动，信息完整。"), ("下一节点", "学院年审审核")],
             [("学院年审审核（剧本五下一步）", "../../pc/college/annual-review.html")]),
        case("zombie", "ok", "核实结果已提交", "建议注销，已提交学院审核",
             [("账号", A_ZB["name"]), ("核实结论", '<span class="c-danger bold">建议注销</span>'), ("下一节点", "学院审核 · 周建华")],
             [("学院审核转注销（剧本七下一步）", "../../pc/college/zombie-verify-detail.html")]),
        case("rectify", "ok", "整改审核已提交", "审核结论已同步学院整改跟踪",
             [("账号", A_PH["name"]), ("审核结论", '<span class="c-success bold">整改通过</span>'), ("下一节点", "学院确认")],
             [("档案整改记录", "../../pc/common/archive-rectify.html")]),
        case("return", "warn", "已退回", "已退回，已通知申请人",
             [("账号", A_NEW["name"]), ("需修改字段", "平台介绍、信息发布范围"), ("申请人", "李明（已发送消息提醒）")],
             [("学生端查看退回意见", "../student/application-returned.html")]),
        case("reject", "err", "已驳回", "流程终止，已通知申请人",
             [("处理结果", '<span class="c-danger bold">驳回（不予办理）</span>'), ("申请人", "李明（已发送消息提醒）")],
             [("学生端查看驳回结果", "../student/application-rejected.html")]),
    ])
    content = f"""
{cases}
<div class="m-card flex between"><span class="sub">剩余待审</span><a class="bold c-primary" href="todo.html">8 项{icon('chevron-right', 14)}</a></div>"""
    js = r"""
(function(){var m=location.search.match(/[?&]c=(\w+)/);if(!m)return;
  var box=document.querySelector('[data-case="'+m[1]+'"]');if(!box)return;
  document.querySelectorAll('[data-case]').forEach(function(x){x.classList.toggle('hidden',x!==box);});})();
"""
    page_t("teacher", DT + "review-result.html", "审核完成", content, back="todo.html",
           bottom=btn("返回待审", "todo.html", "default") + btn("处理下一条", "review-annual.html", "primary", "arrow-right", attrs='style="flex:1.6"'),
           js=js,
           notes=["剧本三第 4 步：交接审核通过即生效，负责人已变更为李四（2026-10-01 生效），原负责人任职时间保留",
                  "同一结果页按来源显示不同摘要：新建、变更、年审、批量、僵尸号、整改、退回、驳回",
                  "“处理下一条”进入下一条待审（年审），“返回待审”回到列表，剩余待审 8 项"],
           flow=[("剧本三下一步：责任人员历史", "../../pc/common/archive-staff.html"),
                 ("学院审核新建（剧本一）", "../../pc/college/approval-detail.html"), ("处理下一条：年审审核", "review-annual.html")])


# ================================================================ 学院管理员
def c_home():
    pct = round(CS["done"] / CS["total"] * 100)
    quick = "".join(f'<a href="{h}"><span class="qi {c}">{icon(ic)}{badge(n)}</span>{t}</a>'
                    for t, ic, c, n, h in [
                        ("年审进度", "chart", "green", 0, "annual-progress.html"),
                        ("提交校团委", "send", "purple", 0, "annual-submit.html"), ("整改跟踪", "wrench", "orange", 2, "rectify.html"),
                        ("僵尸号预警", "ghost", "red", 3, "zombie.html"), ("消息待办", "bell", "", 0, "../../pc/college/messages.html"),
                    ])
    colors = ["#ABB0BA", "#E6A23C", "#2A8DC7", "#F56C6C", "#67C23A"]
    nodes = [("待填报", 5), ("待教师审核", 4), ("待学院审核", 4), ("整改中", 2), ("已完成", 21)]
    funnel = "".join(f'<i style="width:{n / CS["total"] * 100:.1f}%;background:{c}"></i>' for (_, n), c in zip(nodes, colors))
    fn = "".join(f'<div><b>{n}</b><small><i style="background:{c}"></i>{t}</small></div>' for (t, n), c in zip(nodes, colors))
    todos = "".join([
        list_item("review-detail.html", "file-add", "", f"{A_NEW['name']} · 新建备案", "王晓琳已通过 · 2026-09-27", tag("待学院审核", "warning")),
        list_item("rectify.html", "wrench", "orange", f"{A_RE['name']} · 整改第 2 轮", "何雨桐 2026-09-27 提交材料", tag("待复核", "warning")),
        list_item("../../pc/college/zombie-verify-detail.html", "ghost", "red", A_ZB["name"], "辅导员建议注销 · 待学院审核", tag("PC", "muted")),
    ])
    content = f"""
<div class="m-hero">
  <div class="flex gap12" style="position:relative;z-index:1">{avatar('周建华', 'lg')}
    <div class="grow"><div class="fs18 bold">周老师，下午好</div><div class="small" style="opacity:.85">计算机学院团委 · 学院团委书记</div></div>
    <a href="todo.html" style="position:relative" aria-label="待审">{icon('bell', 22)}<span class="badge" style="position:absolute;top:-6px;right:-8px">4</span></a>
  </div>
  <div class="hero-stats c3">
    <a href="accounts.html"><b>{CS['total']}</b><span>本院账号</span></a>
    <a href="annual-progress.html"><b>{CS['done']}<small>/{CS['total']}</small></b><span>年审完成</span></a>
    <a href="todo.html"><b>4</b><span>待学院审核</span></a>
  </div>
</div>
<div class="grid g2 mt12" style="gap:10px">
  <a class="m-card risk-tile" href="zombie.html" style="margin:0"><span class="stat-ic red" style="width:38px;height:38px;border-radius:11px">{icon('ghost', 20)}</span><div><div class="fs18 bold num">{CS['zombie']}</div><div class="small muted">疑似僵尸号</div></div></a>
  <a class="m-card risk-tile" href="rectify.html" style="margin:0"><span class="stat-ic orange" style="width:38px;height:38px;border-radius:11px">{icon('wrench', 20)}</span><div><div class="fs18 bold num">{CS['rectify']}</div><div class="small muted">待整改</div></div></a>
</div>
<a class="m-card mt12" href="annual-progress.html" style="display:block">
  <div class="sec-t">年审进度<span class="ml-auto c-primary">详情{icon('chevron-right', 12)}</span></div>
  <div class="flex between"><span class="small sub">完成率 <b class="c-primary fs16">{pct}%</b></span><span class="small c-warning">{icon('clock', 12)} 学院提交截止 {T['college_end']}</span></div>
  <div class="funnel">{funnel}</div><div class="fn-grid">{fn}</div>
</a>
<div class="m-card"><div class="quick pack5">{quick}</div></div>
<div class="m-title">待我处理<a href="todo.html">全部{icon('chevron-right', 14)}</a></div>
<div class="m-card" style="padding:4px 14px">{todos}</div>"""
    page_t("college", DC + "home.html", "学院看板", content, tab="home", nav_title="学院看板",
           notes=["汇总本院 36 个账号：年审完成 21/36、待学院审核 4、疑似僵尸号 3、待整改 2，数字可点击下钻",
                  "年审进度条按节点分色（待填报 5 / 待教师审核 4 / 待学院审核 4 / 整改中 2 / 已完成 21），显示学院提交截止 2026-11-05",
                  "快捷入口含提交校团委、整改跟踪、僵尸号预警；手机上办理审核和进度查看"],
           flow=[("学院审核新建备案", "review-detail.html"), ("剧本六：整改第二次提交", "rectify.html"),
                 ("年审进度与催办", "annual-progress.html"), ("提交校团委", "annual-submit.html"), ("PC 学院工作台", "../../pc/college/workbench.html")])


def c_todo():
    cards = "".join([
        todo_card("apply", "review-detail.html", A_NEW["name"], A_NEW["platform"], tag("新建备案", "primary"),
                  [F_NEW["no"], "王晓琳 · 2026-09-27 11:20 通过"], f"教师意见：{F_NEW['steps'][3][3]}", tag("教师已通过", "success")),
        todo_card("apply", "../../pc/college/approval-change.html", A_REN["name"], A_REN["platform"], tag("名称变更", "warning"),
                  [F_REN["no"], "王晓琳 · 2026-09-27 09:15 通过"], f"拟更名为“{A_REN['new_name']}”，属重要变更",
                  tag("建议 PC 审核：含变更对比", "muted"), "PC 审核"),
        todo_card("zombie", "../../pc/college/zombie-verify-detail.html", A_ZB["name"], A_ZB["platform"], st("疑似僵尸号", False),
                  [F_ZB["no"], "王晓琳 · 2026-09-22 15:30 核实"], f"辅导员核实：{F_ZB['steps'][1][3]}", tag("建议注销", "danger"), "PC 审核"),
        todo_card("rectify", "rectify.html", A_RE["name"], A_RE["platform"], tag("整改第 2 轮", "warning"),
                  [F_RE["no"], "何雨桐 · 2026-09-27 20:45"], F_RE["steps"][4][3], f"截止 {F_RE['deadline']}", "去复核"),
    ])
    proxy = f"""
<div class="m-card" data-cat="proxy"><div class="tc-top">{pf('QQ', 'sm')}<div class="grow bold ellipsis">{ACCOUNTS['proxy']['name']}</div>{st('教师代办', False)}</div>
  <div class="tc-meta"><span>{FLOWS['proxy']['no']}</span><span>王晓琳 · 2026-09-30 09:20 代办</span></div>
  <div class="tc-note">负责人交接：赵磊（已毕业）→ 孙悦。{FLOWS['proxy']['steps'][0][3]}</div>
  <div class="tc-ft"><a class="go" href="../../pc/school/log-detail.html">{icon('log', 14)}查看代办日志</a>
    <a class="btn btn-primary btn-sm" href="../../pc/college/approval-proxy.html">{icon('file-check')}去审核</a></div></div>"""
    content = f"""
<div class="m-tabs" data-target="#c-todo">
  <button type="button" class="on" data-seg="all">全部 5</button><button type="button" data-seg="apply">申请 2</button>
  <button type="button" data-seg="zombie">僵尸号 1</button><button type="button" data-seg="rectify">整改 1</button>
  <button type="button" data-seg="proxy">代办 1</button>
</div>
<div class="alert alert-info mb12">{icon('info')}<div class="grow">待学院审核 4 项 · 教师代办 1 项；含变更对比等复杂材料建议在 PC 端审核。</div></div>
<div id="c-todo">{cards}{proxy}</div>"""
    page_t("college", DC + "todo.html", "待学院审核", content, tab="todo", nav_title="待学院审核",
           notes=["展示教师审核通过后流转到学院的事项，页签按申请 / 僵尸号 / 整改 / 代办筛选",
                  "新建备案可在移动端直接审核；名称变更含对比表、僵尸号核实含佐证，标注建议 PC 审核并直达 PC 页面",
                  "教师代办交接进入 PC 审核页，通过后交接生效并写入账号操作日志"],
           flow=[("学院审核新建备案", "review-detail.html"), ("剧本六：整改复核", "rectify.html"),
                 ("剧本二：学院变更审核（PC）", "../../pc/college/approval-change.html"),
                 ("剧本七：僵尸号学院审核（PC）", "../../pc/college/zombie-verify-detail.html"),
                 ("剧本八：学院审核代办交接", "../../pc/college/approval-proxy.html")])


def c_review_detail():
    info = "".join([
        cell("平台类型", A_NEW["platform"]), cell("平台 ID", A_NEW["pid"]), cell("所属组织", A_NEW["org"]),
        cell("组织类别 / 层级", f"{A_NEW['org_type']} · {A_NEW['level']}"), cell("第一责任人", "张卫东 · 党委副书记"),
        cell("管理教师", "王晓琳"), cell("学生负责人", f"李明 · {PEOPLE['李明']['no']}"),
        cell("四项机制", '<span class="c-success">已建立 4 / 4</span>'), cell("平台介绍", "326 字（已补充）"),
    ])
    when, who, _, cm = F_NEW["steps"][3]
    overlay = (dialog("dlg-reject", "确认驳回该申请？", "驳回即不予办理，流程终止。", "请填写驳回原因（必填）", "确认驳回",
                      "review-result.html?c=reject", "已驳回，已通知申请人与指导教师")
               + dialog("dlg-return", "退回修改", "退回后回到申请人修改，重新提交后需教师再次审核。", "请填写退回原因（必填）",
                        "确认退回", "review-result.html?c=return", "已退回，已通知申请人", danger=False))
    content = f"""
{head(A_NEW['name'], A_NEW['platform'], F_NEW['no'] + ' · 申请人 李明', tag('新建备案', 'primary') + st('待学院审核'))}
{m_steps(['学生提交', '教师审核', '学院审核', '校级审核'], 2)}
<div class="m-card" style="border-left:3px solid var(--c-success)">
  <div class="flex gap8">{avatar('王晓琳', 'sm')}<span class="bold fs13 grow">指导教师意见 · 王晓琳</span>{st('已通过')}</div>
  <div class="fs16 bold mt8" style="line-height:1.6">“{cm}”</div><div class="small muted mt4">{when}</div>
</div>
<div class="m-group-title">关键信息</div>
<div class="m-group">{info}</div>
{sec('审核流程', flow_tl('new', 4, '学院团委审核', '周建华 · 待审核（当前节点）', back_idx=(1,)))}
{opinion(F_NEW['steps'][4][3])}"""
    page_t("college", DC + "review-detail.html", "学院审核详情", content, back="todo.html",
           bottom=(toggle_btn("驳回", "#dlg-reject", "danger", cls="slim") + toggle_btn("退回", "#dlg-return", "warning", cls="slim")
                   + jump("通过并报校团委", "review-result.html", "primary", "已通过，已流转至校团委审核", cls="wide")),
           overlay=overlay,
           notes=["醒目展示指导教师王晓琳的审核意见，学院在教师意见基础上审核",
                  "关键信息以列表呈现，完整时间线含第一次退回节点（橙色）",
                  "驳回、退回均为手机内对话框，原因必填；通过后报校团委审核"],
           flow=[("通过 → 审核完成", "review-result.html"), ("校级终审（PC）", "../../pc/school/approval-detail.html"),
                 ("PC 端学院审核", "../../pc/college/approval-detail.html")])


def c_review_result():
    def case(key, kind, title, desc, items, hidden):
        h = ' class="hidden"' if hidden else ""
        ic = {"ok": "check", "warn": "undo", "err": "x"}[kind]
        return (f'<div data-case="{key}"{h}><div class="result" style="padding:28px 8px 8px"><div class="result-ic {kind}">{icon(ic)}</div>'
                f'<h2>{title}</h2><p class="fs13">{desc}</p></div><div class="m-card res-card">{rows(items)}</div></div>')
    cases = "".join([
        case("pass", "ok", "审核完成", "已通过，已流转至校团委审核",
             [("账号", A_NEW["name"]), ("申请编号", F_NEW["no"]), ("学院意见", F_NEW["steps"][4][3]),
              ("下一节点", "校团委审核 · 陈静"), ("通知", "已通知申请人李明、指导教师王晓琳")], False),
        case("return", "warn", "已退回", "已退回申请人修改",
             [("账号", A_NEW["name"]), ("通知", "已通知申请人李明、指导教师王晓琳")], True),
        case("reject", "err", "已驳回", "流程终止，已通知申请人",
             [("账号", A_NEW["name"]), ("处理结果", '<span class="c-danger bold">驳回（不予办理）</span>')], True),
        case("handover", "ok", "交接已生效", "代办交接审核通过，负责人即时更新",
             [("账号", ACCOUNTS["proxy"]["name"]), ("原负责人", "赵磊（已毕业）· 任期止 2026-09-30"),
              ("新负责人", "孙悦 · 任期起 2026-09-30"), ("发起方式", "教师代办 · 王晓琳"), ("通知", "已通知孙悦、王晓琳")], True),
        case("rectcont", "warn", "已判定继续整改", "整改任务回到“待提交”，截止时间不变",
             [("账号", A_RE["name"]), ("整改轮次", "第 3 轮 · 截止 2026-10-20"), ("学院意见", "请补充 7-9 月审核台账原件扫描件"),
              ("通知", "已通知何雨桐、王晓琳")], True),
    ])
    content = f"""
{cases}
<div class="m-group"><a class="cell" href="../../pc/school/approval-detail.html"><span class="cell-label fs13 c-primary">查看校团委终审（PC）</span><span class="cell-value"></span>{icon('chevron-right', cls='arrow')}</a></div>
<div class="m-card flex between"><span class="sub">剩余待学院审核</span><a class="bold c-primary" href="todo.html">3 项{icon('chevron-right', 14)}</a></div>"""
    js = r"""
(function(){var m=location.search.match(/[?&]c=(\w+)/);if(!m)return;
  var box=document.querySelector('[data-case="'+m[1]+'"]');if(!box)return;
  document.querySelectorAll('[data-case]').forEach(function(x){x.classList.toggle('hidden',x!==box);});})();
"""
    page_t("college", DC + "review-result.html", "审核完成", content, back="todo.html",
           bottom=btn("返回看板", "home.html", "default") + btn("继续审核", "todo.html", "primary", "arrow-right", attrs='style="flex:1.6"'),
           js=js,
           notes=["学院审核通过后流转至校团委审核，并通知申请人与指导教师",
                  "按来源显示通过 / 退回 / 驳回三种结果",
                  "“继续审核”回到待审列表（剩余 3 项），“返回看板”回到学院看板"],
           flow=[("校团委终审（剧本一）", "../../pc/school/approval-detail.html"), ("继续审核", "todo.html"), ("返回看板", "home.html")])


def c_annual_progress():
    colors = ["#ABB0BA", "#E6A23C", "#2A8DC7", "#F56C6C", "#67C23A"]
    nodes = [("待填报", 5), ("待教师审核", 4), ("待学院审核", 4), ("整改中", 2), ("已完成", 21)]
    funnel = "".join(f'<i style="width:{n / CS["total"] * 100:.1f}%;background:{c}"></i>' for (_, n), c in zip(nodes, colors))
    fn = "".join(f'<div><b>{n}</b><small><i style="background:{c}"></i>{t}</small></div>' for (t, n), c in zip(nodes, colors))
    teachers = [("王晓琳", "宣传工作辅导员", 18, 10), ("刘洋", "2023级辅导员", 8, 5), ("陈露", "2024级辅导员", 4, 3),
                ("张可", "2022级辅导员", 3, 2), ("李娜", "社团指导教师", 2, 1), ("马超", "2025级辅导员", 1, 0)]
    orgs = [("院级学生组织", "团委、学生会、科协等", 10, 8), ("班级团支部", "各年级团支部", 18, 9), ("社团组织", "学院社团", 8, 4)]

    def prow(lead, name, sub, total, done, who):
        p = round(done / total * 100)
        color = "green" if p == 100 else ("orange" if p < 50 else "")
        act = (tag("已完成", "success") if done == total
               else btn("催办", None, "light", size="sm", toast=f"已向{who}发送催办提醒"))
        return (f'<div class="p-row">{lead}<div class="grow" style="min-width:0"><div class="flex between"><span class="bold fs13">{name}</span>'
                f'<span class="small muted num">{done}/{total}</span></div><div class="small muted">{sub}</div>'
                f'<div class="flex gap8 mt4">{progress(p, color)}<span class="small num" style="width:34px;text-align:right">{p}%</span></div></div>{act}</div>')
    t_rows = "".join(prow(avatar(n) if n in ("王晓琳", "刘洋") else f'<span class="avatar" style="display:grid;place-items:center;font-size:13px;color:var(--c-primary);background:var(--c-primary-light)">{n[0]}</span>',
                          n, s, t, d, n + "老师") for n, s, t, d in teachers)
    o_rows = "".join(prow(f'<span class="stat-ic" style="width:32px;height:32px;border-radius:9px">{icon("hierarchy", 16)}</span>',
                          n, s, t, d, n + "负责人") for n, s, t, d in orgs)
    content = f"""
<div class="m-card">
  <div class="sec-t">节点分布<span class="ml-auto muted">共 {CS['total']} 个账号</span></div>
  <div class="flex between"><span class="small sub">完成率 <b class="c-primary fs16">{round(CS['done'] / CS['total'] * 100)}%</b></span>
    <span class="small c-warning">{icon('clock', 12)} 学院提交截止 {T['college_end']}</span></div>
  <div class="funnel">{funnel}</div><div class="fn-grid">{fn}</div>
</div>
<div class="flex between mb12" style="gap:10px">
  <div class="seg full" data-single=".pv" style="flex:1"><button type="button" class="on" data-choice=".pv-t">按教师</button><button type="button" data-choice=".pv-o">按组织</button></div>
  {btn('一键催办', None, 'primary', 'bell', 'sm', toast='已向 5 名未完成教师及相关学生负责人发送催办')}
</div>
<div class="m-card pv pv-t" style="padding:2px 14px">{t_rows}</div>
<div class="m-card pv pv-o hidden" style="padding:2px 14px">{o_rows}</div>
<div class="small muted" style="text-align:center">全部账号完成后方可提交校团委</div>"""
    page_t("college", DC + "annual-progress.html", "年审进度", content, back="home.html", nav_title="本院年审进度",
           bottom=btn("PC 查看明细", "../../pc/college/annual-progress.html", "default") + btn("去提交", "annual-submit.html", "primary", "send", attrs='style="flex:1.6"'),
           notes=["进度条按节点分色：待填报 5 / 待教师审核 4 / 待学院审核 4 / 整改中 2 / 已完成 21，合计 36",
                  "“按教师 / 按组织”切换两种视图，每行显示完成数、进度条和催办按钮",
                  "单个催办或一键催办均即时提示，消息推送至教师与学生负责人",
                  "“去提交”进入提交校团委检查清单"],
           flow=[("提交校团委", "annual-submit.html"), ("PC 本院年审进度", "../../pc/college/annual-progress.html"),
                 ("学院年审审核（PC）", "../../pc/college/annual-review.html")])


def c_annual_submit():
    checks = "".join(f'<div>{icon("check-circle")}{t}<em>{e}</em></div>' for t, e in [
        ("36 个账号年审记录全部审核完成", "36 / 36"), ("整改任务均已闭环", "2 项已复核"), ("疑似僵尸号均已核实处置", "3 / 3"),
        ("注销账号均已提交注销申请", "2 个"), ("数据异常已处理", "0 条待处理"), ("教师审核意见完整", "已校验")])
    types = [("无异动", 22, "#9096A2"), ("新建", 3, "#2A8DC7"), ("变更", 9, "#E6A23C"), ("注销", 2, "#F56C6C")]
    bar = "".join(f'<i style="width:{n / 36 * 100:.1f}%;background:{c}"></i>' for _, n, c in types)
    grid = "".join(f'<div><b style="color:{c}">{n}</b><small><i style="background:{c}"></i>{t}</small></div>' for t, n, c in types)
    content = f"""
<div class="m-card flex gap12"><span class="stat-ic green" style="width:44px;height:44px;border-radius:12px">{icon('shield', 22)}</span>
  <div class="grow"><div class="bold">计算机学院 · {T['year']} 年度年审</div><div class="small muted">提交截止 {T['college_end']} · 提交后由校团委审核</div></div></div>
{sec('提交前检查', f'<div class="ok-list">{checks}</div>', '<span class="c-success">6 / 6 通过</span>')}
{sec('按异动类型汇总', f'<div class="funnel">{bar}</div><div class="fn-grid">{grid}</div><div class="small muted mt8">合计 36 个账号，与本院在册账号一致</div>')}
<label class="m-card flex gap8 top-align" style="cursor:pointer"><input type="checkbox" id="commit" style="width:18px;height:18px;margin-top:2px;accent-color:var(--c-primary)"
  onchange="document.getElementById('sub-btn').classList.toggle('disabled',!this.checked)">
  <span class="fs13 sub"><span class="req">*</span>本人承诺：本院年审数据真实、完整，已逐一核对账号运营情况、责任人员及四项机制落实情况。</span></label>"""
    page_t("college", DC + "annual-submit.html", "提交校团委", content, back="annual-progress.html",
           bottom=(back_btn("annual-progress.html", "返回")
                   + f'<button class="btn btn-primary disabled" type="button" id="sub-btn" data-submit="home.html" data-toast="已提交校团委" style="flex:1.8">{icon("send")}确认提交</button>'),
           notes=["检查清单全部通过（✓）后方可提交；存在未完成项时对应行将标红并禁止提交",
                  "按异动类型汇总：无异动 22 / 新建 3 / 变更 9 / 注销 2，合计 36",
                  "必须勾选数据真实性承诺，“确认提交”按钮才可点击；提交后返回看板并提示“已提交校团委”"],
           flow=[("校级年审审核（PC）", "../../pc/school/annual-review.html"), ("PC 提交成功页", "../../pc/college/annual-submit-success.html"),
                 ("返回学院看板", "home.html")])


def c_zombie():
    items = [
        (A_ZB["name"], "微信公众号", "停更 412 天 · 最近发布 2025-08-14", "辅导员建议注销", "danger",
         btn("去审核（PC）", "../../pc/college/zombie-verify-detail.html", "primary", size="sm"), "cancel"),
        (A_PH["name"], "视频号", "停更 212 天 · 最近发布 2026-03-02", "学生核实中", "warning",
         btn("查看进度", "../student/zombie-verify.html", "light", size="sm"), "verify"),
        ("2021级计算机科学3班团支部", "QQ", "停更 268 天 · 团支部已毕业", "待教师核实", "primary",
         btn("催办", None, "light", "bell", "sm", toast="已向王晓琳老师发送核实催办"), "verify"),
    ]
    cards = "".join(
        f'<div class="m-card" data-cat="{cat}"><div class="tc-top">{pf(p)}<div class="grow" style="min-width:0"><div class="bold ellipsis">{n}</div>'
        f'<div class="small muted">{m}</div></div></div><div class="tc-ft"><span>{tag(s, k, True)}</span>{a}</div></div>'
        for n, p, m, s, k, a, cat in items)
    content = f"""
<div class="m-card"><div class="mini3">
  <div><b class="c-danger">3</b><small>疑似僵尸号</small></div><div><b class="c-warning">2</b><small>核实中</small></div><div><b class="c-primary">1</b><small>待学院审核</small></div>
</div></div>
<div class="alert alert-warning mb12">{icon('shield')}<div class="grow"><b>处置原则：</b>系统按“停更 ≥ {T['idle_days']} 天”等规则预警，经学生 / 教师核实、学院审核、校团委确认后处置，系统不自动注销，注销账号数据永久保留。</div></div>
{chips([('全部 3', 'all'), ('核实中', 'verify'), ('待学院审核', 'cancel')], target='#zb-list')}
<div id="zb-list" class="mt12">{cards}</div>"""
    page_t("college", DC + "zombie.html", "僵尸号预警", content, back="home.html", nav_title="僵尸号预警",
           notes=["本院 3 个疑似僵尸号，显示停更天数与核实进度",
                  "辅导员已建议注销的账号进入学院审核（PC 端查看佐证后转注销）",
                  "核实中的账号可查看进度或催办教师 / 学生，所有操作即时反馈",
                  "处置原则：系统不直接注销，逐级核实确认"],
           flow=[("剧本七：学院审核转注销", "../../pc/college/zombie-verify-detail.html"),
                 ("PC 僵尸号核实", "../../pc/college/zombie.html"), ("返回学院看板", "home.html")])


def c_rectify():
    sub_when, sub_who, _, sub_cm = F_RE["steps"][4]
    files = "".join(f'<span class="file-chip">{icon(ic)}{f}</span>' for ic, f in [
        ("file", "信息发布三审制度（签字盖章版）.pdf"), ("file", "7-9月内容审核台账.xlsx"), ("image", "先审后发记录截图.zip")])
    hints = (f'<div class="rc rc-pass mt8">{alert("整改通过：整改任务关闭，账号恢复正常运行，年审恢复流转至学院审核。", "success")}</div>'
             f'<div class="rc rc-cont hidden mt8">{alert("继续整改：退回何雨桐补充材料，进入第 3 轮整改。", "warning")}</div>'
             f'<div class="rc rc-cancel hidden mt8">{alert("转注销：整改无望时转入注销流程，需校团委确认。", "danger")}</div>')
    content = f"""
{head(A_RE['name'], A_RE['platform'], F_RE['no'] + ' · 第 2 轮 · 截止 ' + F_RE['deadline'], st('整改复核中') + st('整改中'))}
{sec('整改问题与要求', rows([('整改问题', F_RE['steps'][0][3]), ('整改要求', F_RE['steps'][1][3])]))}
<div class="m-card" style="border-left:3px solid var(--c-primary)"><div class="sec-t">第 2 次提交材料<span class="ml-auto">{tag('本轮', 'primary')}</span></div>
  <div class="flex gap8">{avatar('何雨桐', 'sm')}<span class="fs13 bold">{sub_who}</span><span class="small muted">{sub_when}</span></div>
  <div class="tc-note">{sub_cm}</div><div class="upload-list">{files}</div>
  <div class="small muted mt8">对照第 1 轮意见：{F_RE['steps'][3][3]}</div>
</div>
{sec('整改轮次记录', flow_tl('rectify', 5, '学院复核第 2 次提交', '周建华 · 待判定（当前节点）'))}
<div class="m-card"><div class="sec-t">判定结果</div>
  {choices('.rc', [('整改通过', '材料齐全，问题已整改到位', '.rc-pass', True), ('继续整改', '仍有问题，退回再次整改', '.rc-cont', False), ('转注销', '无法整改，转注销流程', '.rc-cancel', False)])}
  {hints}
</div>
{opinion(F_RE['steps'][5][3], '判定意见')}"""
    bottom = (jump("确认：整改通过", "../../pc/common/archive-rectify.html", "success", "整改通过，年审恢复流转", "check", cls="rc rc-pass")
              + f'<button class="btn btn-warning rc rc-cont hidden" type="button" data-href="review-result.html?c=rectcont" data-toast="已判定继续整改，已通知何雨桐">{icon("refresh")}确认：继续整改</button>'
              + jump("确认：转注销", "../../pc/common/apply-cancel.html", "danger-solid", "已转注销，请填写注销申请", "power", cls="rc rc-cancel hidden"))
    page_t("college", DC + "rectify.html", "整改跟踪", content, back="home.html",
           bottom=bottom,
           notes=["剧本六第 6 步：何雨桐第二次提交签字盖章版制度及 7-9 月审核台账，附件可查看",
                  "整改轮次时间线展示两轮提交与第一次“继续整改”判定，当前为学院复核节点",
                  "判定结果三选一（默认整改通过），底部确认按钮随选择切换：整改通过进入档案整改记录；继续整改即时提示；转注销进入注销申请",
                  "整改通过后年审恢复流转"],
           flow=[("剧本六下一步：档案整改记录", "../../pc/common/archive-rectify.html"),
                 ("上一步：第一次判定继续整改（PC）", "../../pc/college/rectify-detail.html"),
                 ("转注销申请", "../../pc/common/apply-cancel.html")])


def c_mine():
    me = PEOPLE["周建华"]
    content = f"""
<div class="m-card flex gap12">{avatar('周建华', 'lg')}
  <div class="grow"><div class="fs18 bold">周建华</div><div class="small muted">工号 {me['no']} · {me['phone']}</div>
  <div class="flex gap6 mt4">{tag('学院管理员', 'primary')}{tag(me['job'], 'muted')}</div></div>
</div>
{sec('管理范围', f'<div class="mini3"><div><b>{CS["total"]}</b><small>本院账号</small></div><div><b>{CS["teachers"]}</b><small>业务教师</small></div><div><b>28</b><small>团学组织</small></div></div>', '<span class="muted">计算机学院团委</span>')}
<div class="m-group">
  {cell(icon('chart') + ' 年审进度', f'{CS["done"]}/{CS["total"]}', 'annual-progress.html')}
</div>"""
    page_t("college", DC + "mine.html", "我的", content, tab="mine", nav_title="我的",
           notes=["展示学院管理员身份与管理范围（本院 36 个账号、6 名业务教师）",
                  "年审进度可从本页进入"],
           flow=[("年审进度", "annual-progress.html"), ("PC 学院工作台", "../../pc/college/workbench.html")])


def c_accounts():
    from pages_college import college_accounts
    cards = []
    for a in college_accounts():
        key = a["pid"]
        act = ""
        if a["name"] == A_NEW["name"]:
            act = btn("审核新建", "review-detail.html", "light", size="sm")
        elif a["name"] == A_RE["name"]:
            act = btn("整改跟踪", "rectify.html", "light", size="sm")
        flags = st(a["run"]) + st(a["filing"]) + st(a["annual"])
        cards.append(
            '<div class="m-card"><a href="archive.html?c=' + key + '" style="display:block"><div class="tc-top">'
            + pf(a["platform"], "sm") + '<div class="grow" style="min-width:0"><div class="bold ellipsis">' + a["name"]
            + '</div><div class="small muted">' + a["org"] + " · " + a["level"] + '</div>'
            + '<div class="small muted">' + a["platform"] + " · " + a["teacher"] + " · " + a["student"] + '</div>'
            + '<div class="flex gap6 wrap mt4">' + flags + '</div></div></div></a>'
            + '<div class="tc-ft" style="justify-content:flex-end">'
            + btn("查看档案", "archive.html?c=" + key, "default", size="sm") + act + '</div></div>'
        )
    content = (
        '<div class="alert alert-info">' + icon("info") + '<div class="grow">本院在册 <b>' + str(CS["total"])
        + '</b> 个账号。这里列出重点账号，点进档案查看与 PC 相同的分区。</div></div>'
        + '<label class="search-box">' + icon("search")
        + '<input placeholder="搜索账号名称、组织或负责人" data-search="#acct-list" aria-label="搜索账号"></label>'
        + '<div id="acct-list">' + "".join(cards) + '</div>'
    )
    page_t("college", DC + "accounts.html", "本院账号", content, back="home.html", nav_title="本院账号",
           notes=["首页“本院账号”进入本页，口径仍是本院 " + str(CS["total"]) + " 个",
                  "重点账号可搜索，点进档案看到与 PC 相同的分区",
                  "新建备案、整改跟踪仍从本页进入原来的办理页"],
           flow=[("账号档案", "archive.html?c=" + A_NEW["pid"]), ("学院审核", "review-detail.html"),
                 ("返回看板", "home.html")])


def c_archive():
    from pages_college import college_accounts
    cases = []
    for i, a in enumerate(college_accounts()):
        rec = dict(a)
        rec["college"] = "计算机学院"
        rec["key"] = a["pid"]
        act = ""
        if a["name"] == A_NEW["name"]:
            act = action_row([("审核新建", "review-detail.html", "primary")])
        elif a["name"] == A_RE["name"]:
            act = action_row([("整改跟踪", "rectify.html", "primary")])
        cls = "hidden" if i else ""
        cases.append(
            '<div data-case="' + a["pid"] + '" class="' + cls + '">'
            + head(a["name"], a["platform"], a["org"], st(a["run"]) + st(a["filing"]) + st(a["annual"]))
            + render_archive(rec) + act + "</div>"
        )
    page_t("college", DC + "archive.html", "账号档案", "".join(cases), back="accounts.html",
           css=ARCHIVE_CSS, js=ARCH_JS, nav_title="账号档案",
           notes=["学院手机档案与 PC 账号档案同一套分区，字段来自同一份演示数据",
                  "新建备案和整改跟踪的原有入口留在档案底部",
                  "本页查看档案，不在这里做导入、导出或分配教师"],
           flow=[("返回本院账号", "accounts.html"), ("审核新建", "review-detail.html"),
                 ("整改跟踪", "rectify.html")])


def build():
    for fn in (t_home, t_todo, t_done, t_messages, t_mine, t_accounts, t_archive, t_review_detail, t_review_change, t_review_handover,
               t_review_annual, t_review_zombie, t_review_rectify, t_review_return, t_review_batch, t_review_result,
               c_home, c_todo, c_review_detail, c_review_result, c_annual_progress, c_annual_submit, c_zombie, c_rectify, c_mine,
               c_accounts, c_archive):
        fn()
