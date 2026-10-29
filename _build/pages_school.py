"""PC 端 · 学校管理员（校团委）页面。

视角：学校管理员 陈静（校团委宣传部），全校范围，负责校级终审、年审发起、风险监管与系统配置。
"""
from base import *  # noqa: F401,F403
from data import (ACCOUNTS, SCHOOL_STATS as S, PLATFORM_STATS, COLLEGES, ANNUAL_TASK as T, FLOWS, PEOPLE,
                  PLATFORM_TYPES, ORG_TYPES, LEVELS, RUN_STATUS, FILING_STATUS, ANNUAL_STATUS, CANCEL_REASONS, UPDATE_FREQ,
                  MECHANISMS)

D = "pc/school/"

# ---------------------------------------------------------------- 本模块样式
CSS = """
.scene{display:flex;align-items:center;gap:12px;padding:12px 16px;border-radius:var(--radius);background:linear-gradient(90deg,#EAF4FB,#F7FBFE);border:1px dashed var(--c-primary-border);font-size:13px;color:#1F5F92}
.scene-no{height:24px;padding:0 10px;border-radius:12px;background:var(--c-primary);color:#fff;font-size:12px;font-weight:600;display:inline-flex;align-items:center;flex:none}
.hd-card{display:flex;align-items:center;gap:16px;padding:18px 20px}
.hd-card h2{font-size:18px;font-weight:700;line-height:1.3}
.hd-meta{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:12px;color:var(--c-text-3);margin-top:6px}
.hd-side{margin-left:auto;text-align:right;flex:none}
.cb{display:inline-flex;align-items:center;gap:8px;font-size:13px;cursor:pointer;color:var(--c-text)}
.cb input{accent-color:var(--c-primary);width:15px;height:15px;cursor:pointer}
.tree-item{display:flex;align-items:center;gap:8px;width:100%;padding:8px 10px;border-radius:6px;font-size:14px;color:var(--c-text-2);text-align:left}
.tree-item:hover{background:var(--c-bg);color:var(--c-primary)}
.tree-item.on{background:var(--c-primary-light);color:var(--c-primary);font-weight:600}
.tree-item .cnt{margin-left:auto;font-size:12px;color:var(--c-text-3);font-weight:400}
.tree-sub{margin:2px 0 6px 18px;padding-left:10px;border-left:1px dashed var(--c-border)}
.tree-sub .tree-item{font-size:13px;padding:6px 10px}
.msg-item{display:flex;gap:14px;padding:14px 20px;border-bottom:1px solid var(--c-line);align-items:flex-start;transition:background .15s}
.msg-item:last-child{border-bottom:none}
.msg-item:hover{background:#F7FBFE}
.msg-ic{width:38px;height:38px;border-radius:10px;display:grid;place-items:center;flex:none;background:var(--c-primary-light);color:var(--c-primary)}
.msg-ic.orange{background:var(--c-warning-bg);color:var(--c-warning)}.msg-ic.red{background:var(--c-danger-bg);color:var(--c-danger)}
.msg-ic.green{background:var(--c-success-bg);color:var(--c-success)}.msg-ic.gray{background:var(--c-muted-bg);color:var(--c-muted)}
.msg-t{font-weight:600;font-size:14px}
.msg-item.unread .msg-t::after{content:"";display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--c-danger);margin-left:8px;vertical-align:middle}
.ntl{display:flex;padding:6px 0 2px}
.ntl-node{flex:1;position:relative;text-align:center;padding-top:26px;min-width:0}
.ntl-node::before{content:"";position:absolute;top:8px;left:-50%;right:50%;height:2px;background:var(--c-primary-border)}
.ntl-node:first-child::before{display:none}
.ntl-node>i{position:absolute;top:2px;left:50%;transform:translateX(-50%);width:14px;height:14px;border-radius:50%;background:#fff;border:3px solid var(--c-primary);z-index:1}
.ntl-node.done>i{background:var(--c-primary)}
.ntl-node.done::before{background:var(--c-primary)}
.ntl-node.now>i{box-shadow:0 0 0 4px rgba(42,141,199,.18)}
.ntl-node b{display:block;font-size:13px;font-weight:600}
.ntl-node span{display:block;font-size:12px;color:var(--c-text-3)}
.node-chip{display:inline-flex;align-items:center;gap:4px;height:26px;padding:0 10px;border-radius:13px;background:var(--c-primary-light);color:var(--c-primary);font-size:12px;white-space:nowrap}
.node-chip.gray{background:var(--c-muted-bg);color:var(--c-text-2)}.node-chip.green{background:var(--c-success-bg);color:var(--c-success)}
.node-arrow{color:var(--c-border);display:inline-flex}
.node-arrow .i{width:14px;height:14px}
.ns{display:inline-flex;align-items:center;gap:4px;font-size:12px;white-space:nowrap}
.ns .i{width:14px;height:14px}
.ns.done{color:var(--c-success)}.ns.now{color:var(--c-warning)}.ns.wait{color:var(--c-placeholder)}.ns.back{color:var(--c-danger)}
.ledger{padding:18px;display:flex;flex-direction:column;gap:10px}
.ledger-ic{width:40px;height:40px;border-radius:10px;display:grid;place-items:center;background:var(--c-primary-light);color:var(--c-primary);flex:none}
.ledger-ic.orange{background:var(--c-warning-bg);color:var(--c-warning)}.ledger-ic.red{background:var(--c-danger-bg);color:var(--c-danger)}
.ledger-ic.green{background:var(--c-success-bg);color:var(--c-success)}
.rule-card{padding:16px 18px;display:flex;flex-direction:column;gap:12px}
.rule-hd{display:flex;align-items:center;gap:12px}
.rule-ic{width:38px;height:38px;border-radius:10px;display:grid;place-items:center;flex:none;background:var(--c-danger-bg);color:var(--c-danger)}
.rule-ic.orange{background:var(--c-warning-bg);color:var(--c-warning)}.rule-ic.blue{background:var(--c-primary-light);color:var(--c-primary)}
.inline-inp{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--c-text-2)}
.inline-inp .input{width:90px;height:32px}
.hit-chip{display:flex;align-items:center;gap:10px;padding:12px 14px;border-radius:var(--radius);background:#fff;border:1px solid var(--c-line)}
.hit-chip b{font-size:20px;font-variant-numeric:tabular-nums;margin-left:auto}
.hit-v{flex-direction:column;align-items:flex-start;gap:8px}
.stat-value .fs18{font-size:20px}
.perm-col{display:flex;flex-direction:column;gap:6px}
.perm-row{display:flex;align-items:center;gap:8px;padding:8px 10px;border-radius:6px;border:1px solid var(--c-line);background:#fff}
.perm-row.on{border-color:var(--c-primary-border);background:#F5FAFD}
.perm-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
.dict-item{display:flex;align-items:center;gap:10px;width:100%;padding:10px 12px;border-radius:8px;font-size:14px;color:var(--c-text-2);text-align:left}
.dict-item:hover{background:var(--c-bg);color:var(--c-primary)}
.dict-item.on{background:var(--c-primary-light);color:var(--c-primary);font-weight:600}
.dict-item .cnt{margin-left:auto;font-size:12px;color:var(--c-text-3);font-weight:400}
.shot{border-radius:10px;overflow:hidden;border:1px solid var(--c-line);position:relative}
.shot img{width:100%;height:220px;object-fit:cover}
.shot span{position:absolute;left:8px;bottom:8px;background:rgba(0,0,0,.55);color:#fff;font-size:12px;padding:2px 8px;border-radius:4px}
.ck-list{display:grid;gap:8px}
.ck-list div{display:flex;align-items:center;gap:8px;font-size:13px;padding:8px 12px;border-radius:6px;background:var(--c-success-bg);color:#0E8A55}
.tpl{display:flex;align-items:center;gap:12px;padding:14px 16px;border:1px solid var(--c-line);border-radius:var(--radius);background:#fff}
.tpl-ic{width:40px;height:40px;border-radius:10px;display:grid;place-items:center;background:#E8F6EE;color:#1D8F4E;flex:none;font-weight:700;font-size:13px}
.mini-list{display:flex;flex-wrap:wrap;gap:6px}
.mini-list span{height:26px;padding:0 10px;border-radius:6px;background:var(--c-bg);font-size:12px;color:var(--c-text-2);display:inline-flex;align-items:center}
.task-card{padding:20px;display:flex;flex-direction:column;gap:14px}
.task-card.on{border-color:var(--c-primary-border);box-shadow:0 6px 20px rgba(42,141,199,.10)}
/* 备案表 */
.doc-wrap{background:#E9EDF2;border-radius:var(--radius);padding:28px 0}
.a4{width:794px;max-width:100%;margin:0 auto;background:#fff;padding:56px 64px 48px;box-shadow:0 6px 24px rgba(15,40,80,.12);font-family:'Songti SC','SimSun','STSong',serif;color:#1d1d1f;position:relative}
.a4 h1{text-align:center;font-size:22px;letter-spacing:1px;margin-bottom:6px;font-weight:700}
.a4 .doc-no{display:flex;justify-content:space-between;font-size:13px;margin:18px 0 8px}
.ftable{width:100%;border-collapse:collapse;font-size:14px;line-height:1.7}
.ftable td{border:1px solid #333;padding:8px 10px;vertical-align:middle}
.ftable td.k{width:108px;text-align:center;font-weight:700;background:#FAFAFA}
.ftable td.op{height:120px;vertical-align:top;position:relative}
.sign{position:absolute;right:16px;bottom:10px;text-align:right;font-size:13px}
.seal{position:absolute;right:230px;bottom:8px;width:104px;height:104px;border:3px solid rgba(223,32,39,.85);border-radius:50%;color:rgba(223,32,39,.85);display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(-14deg);font-size:12px;font-weight:700;line-height:1.3;text-align:center;font-family:var(--font)}
.seal .i{width:22px;height:22px;fill:rgba(223,32,39,.85);stroke:none;margin:2px 0}
.doc-foot{font-size:12px;color:#666;margin-top:14px;line-height:1.8}
"""


# ---------------------------------------------------------------- 通用小组件
def page(file, menu, title, crumbs, content, css="", js=""):
    pc_page(D + file, "school", menu, title, [("首页", "dashboard.html")] + crumbs, content, css=CSS + css, js=js)


def go(text, href, kind="primary", ic=None, toast=None, size=""):
    """带反馈的跳转按钮：先 toast 再跳转。"""
    cls = f"btn btn-{kind}" + (f" btn-{size}" if size else "")
    t = f' data-toast="{esc(toast)}"' if toast else ""
    i = icon(ic) if ic else ""
    return f'<button class="{cls}" type="button" data-href="{href}"{t}>{i}{text}</button>'


def cb(text, checked=False):
    c = " checked" if checked else ""
    return f'<label class="cb"><input type="checkbox"{c}>{text}</label>'


def sw(on=True, label="开关"):
    c = " on" if on else ""
    return f'<button type="button" class="switch{c}" aria-label="{label}"></button>'


def fchip(name, ic="file"):
    return f'<span class="file-chip">{icon(ic)}{name}</span>'


def sec(title):
    return f'<div class="form-section">{title}</div>'


def scene(no, text, href, label):
    return (f'<div class="scene"><span class="scene-no">演示剧本{no}</span><div class="grow">{text}</div>'
            f'<a class="btn btn-primary btn-sm" href="{href}">{label}{icon("arrow-right")}</a></div>')


def dash(v):
    return '<span class="muted">—</span>' if v in ("—", "", None) else v


def sts(v):
    return dash(v) if v in ("—", "", None) else st(v)


def person(name, meta=""):
    m = f'<div class="small muted">{meta}</div>' if meta else ""
    return f'<div class="flex gap8">{avatar(name, "sm")}<div><div class="nowrap">{name}</div>{m}</div></div>'


def ns(state, text=""):
    """年审节点状态：done 已完成 / now 进行中 / wait 未开始 / back 退回。"""
    ic = {"done": "check-circle", "now": "clock", "wait": "more", "back": "undo"}[state]
    txt = text or {"done": "已完成", "now": "进行中", "wait": "未开始", "back": "已退回"}[state]
    return f'<span class="ns {state}">{icon(ic)}{txt}</span>'


def node_flow(nodes):
    """审核节点链：nodes 为 (文字, 样式)。"""
    out = []
    for i, (t, c) in enumerate(nodes):
        if i:
            out.append(f'<span class="node-arrow">{icon("arrow-right")}</span>')
        out.append(f'<span class="node-chip {c}">{t}</span>')
    return f'<div class="flex gap6 wrap">{"".join(out)}</div>'


def ntl(nodes):
    """横向时间节点：nodes 为 (名称, 日期, 状态 done/now/"")。"""
    out = "".join(f'<div class="ntl-node {s}"><i></i><b>{n}</b><span>{d}</span></div>' for n, d, s in nodes)
    return f'<div class="ntl">{out}</div>'


def who_meta(who, t):
    role = PEOPLE.get(who, {}).get("role", "")
    r = f"（{role}）" if role and who != "系统" else ""
    return f"{who}{r} · {t}"


def flow_tl(key, now=None, now_title="", now_meta="", now_comment=""):
    """按 FLOWS 生成审核时间线；now 为当前节点下标（该节点及之后显示为待处理）。"""
    items = []
    for i, (t, who, title, cm) in enumerate(FLOWS[key]["steps"]):
        if now is not None and i == now:
            items.append(("now", now_title or title, now_meta or f"{who} · 待处理", now_comment))
            continue
        if now is not None and i > now:
            items.append(("wait", title, "未开始", ""))
            continue
        back = any(k in title for k in ("退回", "继续整改", "要求整改"))
        items.append(("back" if back else "done", title, who_meta(who, t), cm))
    return timeline(items)


def acct_head(a, extra_tags="", side=""):
    name, platform = a["name"], a["platform"]
    return (f'<div class="card hd-card">{pf(platform, "lg")}<div class="grow"><div class="flex gap8 wrap"><h2>{name}</h2>{extra_tags}</div>'
            f'<div class="hd-meta"><span>{platform} · ID {a["pid"]}</span><span>{a["org"]}</span><span>{a["level"]}</span>'
            f'<span>开通 {a["opened"]}</span></div></div><div class="hd-side">{side}</div></div>')


def backdrop(content):
    return f'<div class="backdrop">{content}</div>'


ANNUAL_TABS = [("年审任务", "annual-tasks.html"), ("全校进度", "annual-progress.html"), ("校级审核", "annual-review.html")]
SETTINGS_TABS = [("审核流程", "settings-workflow.html"), ("数据字典", "settings-dictionary.html"), ("风险规则", "settings-rules.html")]


# ================================================================ 工作台
def dashboard():
    kpis = "".join([
        stat("全校在册账号", f"{S['total']}", f"覆盖 {S['colleges']} 个二级团组织", "database", href="accounts.html"),
        stat("正常运行", f"{S['normal']}", f"占比 {S['normal'] / S['total'] * 100:.1f}%", "check-circle", "green", href="accounts.html"),
        stat("疑似僵尸号", f"{S['zombie']}", "停更 ≥ 180 天等规则命中", "ghost", "red", href="zombie.html"),
        stat("整改中", f"{S['rectifying']}", "3 项临近截止", "wrench", "orange", href="rectify.html"),
        stat("待校级审核", "12", "新建 5 · 变更 4 · 注销 3", "file-check", href="approvals.html"),
        stat("数据异常", "18", "负责人为空 9 · 组织为空 6", "alert", "orange", href="anomalies.html"),
    ])
    total = S["total"]
    levels = "".join(
        f'<a class="card card-hover" href="accounts.html" style="padding:16px 18px"><div class="small muted">{k}</div>'
        f'<div class="flex between mt4"><span class="fs18 bold num">{v}</span>{tag("%.1f%%" % (v / total * 100), "primary")}</div>'
        f'<div class="mt8">{progress(min(100, v / total * 140))}</div></a>'
        for k, v in [("一级平台", S["level1"]), ("二级平台", S["level2"]), ("三级平台", S["level3"]), ("社团平台", S["club"])])
    yearly = kv([("本年度新建", f'<span class="fs18 bold c-primary num">{S["new"]}</span>'),
                 ("本年度变更", f'<span class="fs18 bold c-warning num">{S["change"]}</span>'),
                 ("本年度注销", f'<span class="fs18 bold c-danger num">{S["cancel"]}</span>')], 3)
    annual_rows = [
        ("计算机学院", 36, 21, 58), ("商学院", 42, 38, 90), ("文学院", 28, 28, 100), ("机电工程学院", 51, 30, 59),
        ("湘雅医学院", 64, 41, 64), ("法学院", 22, 9, 41),
    ]
    annual_tbl = table(
        ["学院", "账号数", "已完成", "完成率", "操作"],
        [dict(cells=[f'<b>{c}</b>', n, d, f'<div class="flex gap8" style="min-width:140px">{progress(p, "green" if p == 100 else ("orange" if p < 60 else ""))}<span class="num small">{p}%</span></div>',
                     ops(("明细", "annual-college-detail.html"), ("催办", None, f"已向{c}发送催办提醒"))],
              href="annual-college-detail.html") for c, n, d, p in annual_rows])
    risk_rows = [
        dict(cells=[acct(ACCOUNTS["zombie"]["name"], "微信公众号", "计算机学院 · 三级平台"), "停更 412 天", st("高风险"), '<span class="muted">学院审核中</span>'], href="zombie-detail.html"),
        dict(cells=[acct("文学院书法协会", "抖音", "文学院 · 社团平台"), "负责人为空", st("中风险"), '<span class="muted">待教师核实</span>'], href="zombie.html"),
        dict(cells=[acct("2020级土木3班团支部", "QQ", "土木工程学院 · 三级平台"), "团支部已毕业", st("高风险"), '<span class="muted">待教师核实</span>'], href="zombie.html"),
        dict(cells=[acct("机电创客空间", "哔哩哔哩", "机电工程学院 · 二级平台"), "无法正常访问", st("中风险"), '<span class="muted">待学院审核</span>'], href="zombie.html"),
    ]
    todo_items = "".join(
        f'<a class="flex gap12" href="{h}" style="padding:10px 0;border-bottom:1px solid var(--c-line)">'
        f'<span class="stat-ic {c}" style="width:34px;height:34px;border-radius:9px">{icon(ic)}</span>'
        f'<div class="grow"><div class="bold fs13">{t}</div><div class="small muted">{m}</div></div>{icon("chevron-right")}</a>'
        for t, m, ic, c, h in [
            ("新建备案待终审 · 中南计算机青年", "计算机学院 · 学院已通过 · 2026-09-28", "file-add", "", "approval-detail.html"),
            ("名称变更待审核 · 计算机学院学生会", "拟改名“中南计院学生会” · 2026-09-29", "file-edit", "orange", "approval-change.html"),
            ("僵尸号待确认注销 · 2021级软件工程1班团支部", "学院已审核转注销 · 2026-09-29", "ghost", "red", "zombie-detail.html"),
            ("年审批量审核 · 计算机学院已提交", "无异动 18 个账号可批量通过", "calendar", "green", "annual-review.html"),
        ])
    content = f"""
{page_hd('数据驾驶舱', f'数据截至 2026-09-30 09:00 · {T["name"]}进行中（学生填报截止 {T["stu_end"]}）',
         btn('导出驾驶舱报表', None, 'default', 'download', toast='已生成《全校新媒体账号总览》报表，可在导出记录中下载') + btn('查看年审进度', 'annual-progress.html', 'primary', 'calendar'))}
<div class="grid g6">{kpis}</div>
<div class="grid mt16" style="grid-template-columns:2fr 1fr">
  {card('平台层级分布', f'<div class="grid g4">{levels}</div><div class="divider"></div>{yearly}', seg([('本年度', 'y'), ('上年度', 'l')]))}
  {card('平台类型分布', donut(PLATFORM_STATS[:6] + [('其他', 66)], S['total'], '在册账号'))}
</div>
<div class="grid mt16" style="grid-template-columns:3fr 2fr">
  {card('各学院年审完成情况', annual_tbl, btn('全部学院', 'annual-progress.html', 'text', size='sm') + btn('一键催办未完成学院', None, 'light', 'bell', 'sm', toast='已向 14 个未完成学院发送催办提醒'))}
  {card('我的待办', todo_items, btn('消息中心', 'messages.html', 'text', size='sm'))}
</div>
<div class="grid mt16" style="grid-template-columns:3fr 2fr">
  {card('风险预警 · 最新', table(['账号', '触发规则', '风险等级', '处置进度'], risk_rows), btn('僵尸号排查中心', 'zombie.html', 'text', size='sm'))}
  {card('近 6 个月账号异动', bars([('4月', 18), ('5月', 26), ('6月', 41), ('7月', 12), ('8月', 9), ('9月', 34)]) + '<div class="small muted mt8">6 月团支部毕业集中注销；9 月新学期新建集中</div>')}
</div>"""
    pc_page(D + "dashboard.html", "school", "dashboard", "数据驾驶舱", [("首页", "dashboard.html"), ("数据驾驶舱", None)], content)


def messages():
    items = [
        ("audit", "file-add", "", "新建备案待校级终审 · 中南计算机青年", "计算机学院团委已审核通过（周建华：同意，报校团委审核。），请进行校级终审。", "2026-09-28 16:40", "approval-detail.html", True),
        ("audit", "file-edit", "orange", "名称变更待校级审核 · 计算机学院学生会", "拟变更为“中南计院学生会”，属重要变更，学院已同意报送。", "2026-09-29 15:20", "approval-change.html", True),
        ("audit", "ban", "red", "账号注销待校级审核 · 2022级市场营销2班团支部", "商学院 · 注销原因：团支部毕业，佐证材料 2 份。", "2026-09-27 17:05", "approval-cancel.html", True),
        ("audit", "calendar", "green", "计算机学院已统一提交年审", "共 36 个账号，其中无异动无风险 18 个可批量通过。", "2026-09-29 17:00", "annual-review.html", True),
        ("handle", "ghost", "red", "僵尸号待校团委确认 · 2021级软件工程1班团支部", "停更 412 天，辅导员核实团支部已毕业，学院审核转注销。", "2026-09-29 10:10", "zombie-detail.html", True),
        ("handle", "wrench", "orange", "校级整改待复核 · 机电创客空间", "整改问题：账号无法正常访问。学生已提交第 1 轮整改材料。", "2026-09-27 21:30", "rectify-detail.html", True),
        ("handle", "alert", "orange", "数据异常待下发 · 18 条", "负责教师为空 4 · 学生负责人为空 5 · 所属组织为空 6 · 其他 3。", "2026-09-26 02:00", "anomalies.html", False),
        ("handle", "upload", "", "导入校验完成 · 2025 年度账号底库", "成功 958 条，失败 9 条，疑似重复 5 条，请确认后下发学院。", "2026-09-10 15:02", "import-result.html", False),
        ("sys", "clock", "gray", "年审节点提醒：学生填报 10 月 15 日截止", "当前全校填报完成率 68.4%，尚有 312 条记录待填报。", "2026-09-30 08:00", "annual-progress.html", False),
        ("sys", "radar", "gray", "系统风险扫描完成", "本周新增疑似僵尸号 6 个，累计 47 个，已推送至各学院。", "2026-09-29 02:00", "zombie.html", False),
        ("sys", "key", "gray", "权限变更留痕 · 王晓琳", "新增“2021级辅导员”身份授权：2021 级各班团支部账号。", "2026-09-29 16:12", "logs.html", False),
        ("sys", "download", "gray", "导出任务已完成 · 全校总表", "共 986 条记录，文件保留 30 天。", "2026-09-29 18:31", "export-records.html", False),
    ]
    cat_name = {"audit": "待审核", "handle": "待处置", "sys": "系统通知"}
    rows = "".join(
        f'<a class="msg-item{" unread" if u else ""}" data-cat="{c}" href="{h}"><span class="msg-ic {col}">{icon(ic)}</span>'
        f'<div class="grow"><div class="flex gap8"><span class="msg-t">{t}</span>{tag(cat_name[c], "muted")}</div>'
        f'<div class="sub fs13 mt4">{d}</div></div><div class="small muted nowrap">{tm}</div>{icon("chevron-right")}</a>'
        for c, ic, col, t, d, tm, h, u in items)
    counts = {k: sum(1 for x in items if x[0] == k) for k in cat_name}
    unread = sum(1 for x in items if x[7])
    tabs = seg([(f"全部 {len(items)}", "all"), (f"待审核 {counts['audit']}", "audit"), (f"待处置 {counts['handle']}", "handle"),
                (f"系统通知 {counts['sys']}", "sys")], target="#msgList")
    content = f"""
{page_hd('消息待办', f'按学校管理员身份生成的待审核、待处置事项与系统通知 · 未读 {unread} 条',
         btn('全部已读', None, 'default', 'check', toast='已将全部消息标记为已读'))}
<div class="grid g4 mb16">
  {stat('待审核', counts['audit'], '新建 · 变更 · 注销 · 年审', 'file-check', href='approvals.html')}
  {stat('待处置', counts['handle'], '僵尸号 · 整改 · 异常 · 导入', 'alert', 'orange', href='zombie.html')}
  {stat('系统通知', counts['sys'], '节点提醒 · 扫描 · 留痕', 'bell', 'gray')}
  {stat('本周已处理', 37, '较上周 +12', 'check-circle', 'green', href='logs.html')}
</div>
{card('消息列表', f'<div id="msgList">{rows}</div>', tabs, bd_cls='')}
"""
    page("messages.html", "messages", "消息待办", [("消息待办", None)], content)


# ================================================================ 账号管理
# 账号库行：名称, 平台, 平台ID, 学院, 组织, 层级, 负责教师, 学生负责人, 运行, 备案, 年审, 最近发布, 分类
ACCT_LIST = [
    ("中南大学共青团", "微信公众号", "csu_youth", "校团委", "校团委宣传部", "一级平台", "陈静", "吴思远", "正常运行", "已备案", "年审通过", "2026-09-30", "l1"),
    ("中南大学学生会", "微博", "5518230011", "校团委", "中南大学学生会", "一级平台", "陈静", "黄一鸣", "正常运行", "已备案", "待学校审核", "2026-09-29", "l1"),
    ("中南计院团委", "微信公众号", "csu_cs_tw", "计算机学院", "计算机学院团委", "二级平台", "王晓琳", "李明", "正常运行", "已备案", "待学校审核", "2026-09-28", "l2"),
    ("计算机学院学生会", "微博", "7722108845", "计算机学院", "计算机学院学生会", "二级平台", "王晓琳", "李明", "正常运行", "变更申请中", "待指导教师审核", "2026-09-27", "l2"),
    ("中南计算机青年", "微信公众号", "csu_cs_youth", "计算机学院", "学院团委新媒体中心", "二级平台", "王晓琳", "李明", "—", "备案申请中", "—", "—", "l2"),
    ("计院青年志愿者", "小红书", "csu_cs_volunteer", "计算机学院", "青年志愿者协会", "二级平台", "王晓琳", "何雨桐", "整改中", "已备案", "整改复核中", "2026-09-26", "l2"),
    ("2021级软件工程1班团支部", "微信公众号", "csu_se2101", "计算机学院", "2021级软件工程1班团支部", "三级平台", "王晓琳", "—（已毕业）", "不活跃", "已备案", "待指导教师审核", "2025-08-14", "l3 zombie"),
    ("2023级软件工程2班团支部", "QQ", "3152286640", "计算机学院", "2023级软件工程2班团支部", "三级平台", "刘洋", "陈可欣", "正常运行", "已备案", "年审通过", "2026-09-25", "l3"),
    ("计院街舞社", "抖音", "csu_cs_dance", "计算机学院", "计院街舞社", "社团平台", "王晓琳", "李四", "正常运行", "已备案", "待填报", "2026-09-28", "club"),
    ("计院ACM协会", "QQ", "2873306619", "计算机学院", "计院ACM协会", "社团平台", "王晓琳", "孙悦", "正常运行", "已备案", "待填报", "2026-09-24", "club"),
    ("计院摄影协会", "视频号", "sph_csu_cs_photo", "计算机学院", "计院摄影协会", "社团平台", "王晓琳", "李明", "不活跃", "已备案", "待填报", "2026-03-02", "club zombie"),
    ("商学院团委", "微信公众号", "csu_bs_tw", "商学院", "商学院团委", "二级平台", "杨帆", "林嘉怡", "正常运行", "已备案", "待学院审核", "2026-09-29", "l2"),
    ("湘雅医声", "抖音", "xyyisheng", "湘雅医学院", "湘雅医学院学生会", "二级平台", "郑敏", "许哲", "正常运行", "已备案", "待指导教师审核", "2026-09-30", "l2"),
    ("文学院书法协会", "抖音", "csu_wx_shufa", "文学院", "文学院书法协会", "社团平台", "—（空）", "—（空）", "不活跃", "已备案", "待填报", "2026-01-11", "club zombie"),
    ("2020级土木3班团支部", "QQ", "2209871134", "土木工程学院", "2020级土木工程3班团支部", "三级平台", "何建国", "—（已毕业）", "不活跃", "已备案", "待填报", "2025-05-20", "l3 zombie"),
    ("机电创客空间", "哔哩哔哩", "402218876", "机电工程学院", "机电学院大学生创新协会", "二级平台", "罗志强", "邓子豪", "整改中", "已备案", "待整改", "2026-04-18", "l2 zombie"),
]


def accounts_content():
    fields = [
        field("账号名称 / 平台ID", inp("支持曾用名模糊搜索")),
        field("学院", sel(["校团委"] + COLLEGES)),
        field("平台类型", sel(PLATFORM_TYPES)),
        field("平台层级", sel(LEVELS)),
        field("组织类别", sel(ORG_TYPES)),
        field("运行状态", sel(RUN_STATUS)),
        field("备案状态", sel(FILING_STATUS)),
        field("年审状态", sel(ANNUAL_STATUS)),
    ]
    rows = []
    for (n, p, pid, col, org, lv, tch, stu, run, fil, ann, last, cat) in ACCT_LIST:
        last_html = dash(last)
        if "zombie" in cat:
            last_html = f'<span class="c-danger">{last}</span>'
        tch_html = f'<span class="c-danger">{tch}</span>' if "空" in tch else tch
        stu_html = f'<span class="c-danger">{stu}</span>' if ("空" in stu or "毕业" in stu) else stu
        rows.append(dict(cells=[acct(n, p, f"ID {pid}"), f'<div class="nowrap">{col}</div><div class="small muted ellipsis" style="max-width:120px" title="{org}">{org}</div>', f'<span class="nowrap">{lv}</span>',
                                f'<span class="nowrap">{tch_html}</span>', f'<span class="nowrap">{stu_html}</span>',
                                sts(run), sts(fil), sts(ann), f'<span class="nowrap num">{last_html}</span>',
                                ops(("档案", "../common/archive-basic.html"), ("备案表", "filing-form.html"))], cat=cat))
    quick = chips([("全部", "all"), (f"一级平台 {S['level1']}", "l1"), (f"二级平台 {S['level2']}", "l2"), (f"三级平台 {S['level3']}", "l3"),
                   (f"社团平台 {S['club']}", "club"), (f"疑似僵尸号 {S['zombie']}", "zombie")], target="#acctTable")
    tbl = table(["账号", "学院 / 组织", "层级", "负责教师", "学生负责人", "运行状态", "备案状态", "年审状态", "最近发布", "操作"], rows, check=True, id_="acctTable")
    return f"""
{page_hd('全校账号库', f'全校在册 {S["total"]} 个账号，覆盖 {S["colleges"]} 个二级团组织 · 一账号一档案，支持 16 个条件组合查询',
         btn('高级筛选', 'accounts-filter.html', 'default', 'filter') + btn('导入', 'import.html', 'default', 'upload') + btn('导入记录', 'logs.html', 'default', 'history') + btn('导出台账', 'export.html', 'primary', 'download'))}
{alert('<b>一账号一档案：</b>每个平台账号只建立一份档案，名称、负责人、组织归属变化均在同一档案内留痕；<b>平台层级与是否疑似僵尸号均为筛选条件</b>，不拆分建库、不单独建表。', 'info')}
<div class="mt16"></div>
{filter_bar(fields)}
<div class="card card-bd">
  <div class="toolbar">
    {quick}
    <div class="flex gap8"><span class="sub fs13">已选 <b data-checked-count="#acctTable">0</b> 个账号</span>
      {btn('批量导出', 'export.html', 'default', 'download', 'sm')}
      {btn('批量催办', None, 'light', 'bell', 'sm', toast='已向所选账号的学生负责人及负责教师发送催办提醒')}
      {btn('高级筛选', 'accounts-filter.html', 'ghost', 'filter', 'sm')}</div>
  </div>
  {tbl}
  {pager(S['total'], 5)}
</div>"""


def accounts():
    css = ".filter{grid-template-columns:repeat(5,minmax(0,1fr))}#acctTable th,#acctTable td{padding-left:7px;padding-right:7px}"
    page("accounts.html", "accounts", "全校账号库", [("账号管理", "accounts.html"), ("全校账号库", None)], accounts_content(), css)


def accounts_filter():
    body = f"""
{alert('以下 16 个条件可任意组合；层级、运行状态与是否疑似僵尸号均作为筛选条件使用。', 'info')}
<div class="form-grid mt16">
  {field('账号名称', inp('如：中南计院团委'))}
  {field('曾用名', inp('如：计算机学院学生会'))}
  {field('平台ID', inp('如：csu_cs_tw'))}
  {field('学院', sel(['校团委'] + COLLEGES, '计算机学院'))}
  {field('团学组织', sel(['计算机学院团委', '计算机学院学生会', '计算机学院研究生会', '青年志愿者协会', '大学生科学技术协会', '计院街舞社', '计院ACM协会']))}
  {field('年级', sel(['2021级', '2022级', '2023级', '2024级', '2025级', '2026级']))}
  {field('组织类别', sel(ORG_TYPES))}
  {field('平台类型', sel(PLATFORM_TYPES))}
  {field('平台层级', sel(LEVELS, '二级平台'))}
  {field('负责教师', inp('姓名或工号', '王晓琳'))}
  {field('学生负责人姓名', inp('如：李明'))}
  {field('学生负责人学号', inp('如：8209230117'))}
  {field('运行状态', sel(RUN_STATUS, '正常运行'))}
  {field('备案状态', sel(FILING_STATUS, '已备案'))}
  {field('年审状态', sel(ANNUAL_STATUS))}
  {field('是否疑似僵尸号', radios('zb', ['不限', '是', '否'], '不限'))}
  <div class="field full"><label>最近发布时间区间</label><div class="flex gap8">{inp('', '2026-03-01', typ='date')}<span class="muted">至</span>{inp('', '2026-09-30', typ='date')}</div>
  <div class="hint">可用于排查长期未更新账号；与“停更天数”规则口径一致</div></div>
</div>
<div class="divider"></div>
<div class="small muted mb8">常用筛选方案</div>
<div class="chips">
  <button type="button" class="chip on" data-toast="已载入方案：计算机学院二级平台">计算机学院二级平台</button>
  <button type="button" class="chip" data-toast="已载入方案：已毕业团支部未注销">已毕业团支部未注销</button>
  <button type="button" class="chip" data-toast="已载入方案：负责人为空">负责人为空</button>
  <button type="button" class="chip" data-toast="已保存当前条件为筛选方案">{icon('plus')}保存为方案</button>
</div>"""
    footer = (btn('重置', None, 'default', 'refresh', toast='已重置全部筛选条件') + btn('取消', 'accounts.html', 'default')
              + go('应用筛选', 'accounts.html', 'primary', 'check', toast='已应用 6 项筛选条件，共找到 23 个账号'))
    css = ".filter{grid-template-columns:repeat(5,minmax(0,1fr))}#acctTable th,#acctTable td{padding-left:7px;padding-right:7px}"
    content = backdrop(accounts_content()) + drawer('高级筛选 · 16 项查询条件', body, footer, 'accounts.html')
    page("accounts-filter.html", "accounts", "高级筛选", [("账号管理", "accounts.html"), ("全校账号库", "accounts.html"), ("高级筛选", None)], content, css)


# 组织：名称, 类别, 上级, 年级, 指导教师, 账号数, 存续状态, 分类, 备注
ORG_LIST = [
    ("计算机学院团委", "院级学生组织", "计算机学院", "—", "周建华", 3, "存续", "alive", ""),
    ("计算机学院团委新媒体中心", "院级学生组织", "计算机学院团委", "—", "王晓琳", 1, "存续", "alive", "本年度新建 1 个账号"),
    ("计算机学院学生会", "院级学生组织", "计算机学院团委", "—", "王晓琳", 2, "存续", "alive", ""),
    ("计算机学院研究生会", "院级学生组织", "计算机学院团委", "—", "刘洋", 1, "存续", "alive", ""),
    ("计算机学院青年志愿者协会", "院级学生组织", "计算机学院团委", "—", "王晓琳", 1, "存续", "alive", "整改中 1"),
    ("计算机学院大学生科学技术协会", "院级学生组织", "计算机学院团委", "—", "王晓琳", 2, "存续", "alive", "平台 ID 变化转新建"),
    ("计院街舞社", "社团组织", "计算机学院团委", "—", "王晓琳", 1, "存续", "alive", ""),
    ("计院ACM协会", "社团组织", "计算机学院团委", "—", "王晓琳", 1, "存续", "alive", ""),
    ("计院摄影协会", "社团组织", "计算机学院团委", "—", "王晓琳", 1, "存续", "alive", "疑似僵尸号"),
    ("计院动漫社", "社团组织", "计算机学院团委", "—", "刘洋", 0, "已撤销", "revoked", "2025-12 撤销，账号已注销"),
    ("2023级软件工程2班团支部", "班级团支部", "计算机学院团委", "2023级", "刘洋", 1, "存续", "alive", ""),
    ("2021级软件工程1班团支部", "班级团支部", "计算机学院团委", "2021级", "王晓琳", 1, "已毕业", "grad", "已毕业（仍有 1 个账号未注销）"),
    ("2021级计算机科学2班团支部", "班级团支部", "计算机学院团委", "2021级", "王晓琳", 0, "已毕业", "grad", "账号已于 2025-07 注销"),
]


def org_status(v):
    return {"存续": tag("存续", "success", True), "已撤销": tag("已撤销", "muted", True), "已毕业": tag("已毕业", "warning", True)}[v]


def organizations_content():
    colleges = [("校团委（直属）", 24), ("计算机学院", 36), ("商学院", 42), ("文学院", 28), ("机电工程学院", 51), ("资源与安全工程学院", 33),
                ("湘雅医学院", 64), ("法学院", 22), ("数学与统计学院", 24), ("化学化工学院", 31), ("材料科学与工程学院", 33), ("土木工程学院", 45)]
    subs = [("学院团委", 3), ("学生会", 2), ("研究生会", 1), ("青年志愿者协会", 1), ("科协", 2), ("社团（12）", 9), ("团支部（46）", 18)]
    tree = []
    for c, n in colleges:
        if c == "计算机学院":
            tree.append(f'<button type="button" class="tree-item on" data-toast="已展开：{c}">{icon("chevron-down")}{icon("building")}{c}<span class="cnt">{n} 个账号</span></button>')
            sub_html = "".join(f'<button type="button" class="tree-item" data-toast="已定位：{c} · {s}">{icon("hierarchy")}{s}<span class="cnt">{k}</span></button>' for s, k in subs)
            tree.append(f'<div class="tree-sub">{sub_html}</div>')
        else:
            tree.append(f'<button type="button" class="tree-item" data-toast="已切换到：{c}">{icon("chevron-right")}{icon("building")}{c}<span class="cnt">{n}</span></button>')
    tree.append('<button type="button" class="tree-item" data-toast="已加载其余 23 个学院">' + icon("more") + '展开其余 23 个学院</button>')
    rows = []
    for n, typ, parent, grade, tch, cnt, stv, cat, note in ORG_LIST:
        note_html = f'<div class="small {"c-danger" if "未注销" in note else "muted"}">{note}</div>' if note else ""
        name_html = f'<div class="bold">{n}</div>{note_html}'
        cnt_html = f'<a class="link" href="accounts.html">{cnt}</a>' if cnt else '<span class="muted">0</span>'
        op = ops(("编辑", "organization-edit.html"), ("账号", "accounts.html"))
        if "未注销" in note:
            op = ops(("编辑", "organization-edit.html"), ("发起注销核实", "zombie-detail.html"))
        rows.append(dict(cells=[name_html, f'<span class="nowrap">{typ}</span>', f'<span class="nowrap">{parent}</span>', grade, person(tch), cnt_html, org_status(stv), op], cat=cat))
    tbl = table(["组织名称", "组织类别", "上级组织", "年级", "指导教师", "账号数", "存续状态", "操作"], rows, id_="orgTable")
    filt = seg([("全部 13", "all"), ("存续 10", "alive"), ("已撤销 1", "revoked"), ("已毕业 2", "grad")], target="#orgTable")
    return f"""
{page_hd('组织管理', '维护“学院 — 团学组织”树，组织撤销或团支部毕业后，其名下账号将纳入僵尸号规则核查',
         btn('导入组织', None, 'default', 'upload', toast='请下载组织导入模板后上传') + btn('新增组织', 'organization-edit.html', 'primary', 'plus'))}
<div class="grid" style="grid-template-columns:270px minmax(0,1fr);align-items:start">
  {card('学院 / 组织树', f'<label class="top-search mb12" style="width:100%">{icon("search")}<input placeholder="搜索组织名称"></label>' + "".join(tree), bd_cls='card-bd')}
  <div class="col gap16">
    <div class="grid g4">
      {stat('计算机学院组织', 58, '院级 6 · 社团 12 · 团支部 40', 'hierarchy')}
      {stat('存续', 52, '正常开展活动', 'check-circle', 'green')}
      {stat('已毕业团支部', 5, '1 个仍有账号未注销', 'flag', 'orange', href='zombie.html')}
      {stat('已撤销', 1, '名下账号均已注销', 'ban', 'gray')}
    </div>
    {alert('<b>2021级软件工程1班团支部 已毕业（仍有 1 个账号未注销）</b>：该团支部已于 2025 年 6 月毕业，名下微信公众号“2021级软件工程1班团支部”已被系统预警为疑似僵尸号，处置中。', 'warning')}
    <div class="card card-bd">
      <div class="toolbar"><div class="flex gap12"><b class="fs16">计算机学院</b><span class="muted small">组织 58 个 · 账号 36 个</span></div>{filt}</div>
      {tbl}
      {pager(58, 5)}
    </div>
  </div>
</div>"""


def organizations():
    page("organizations.html", "organizations", "组织管理", [("账号管理", "accounts.html"), ("组织管理", None)], organizations_content())


def organization_edit():
    body = f"""
<div class="form-grid">
  {field('组织名称', inp('请输入组织全称', '2021级软件工程1班团支部', req=True), req=True)}
  {field('所属学院', sel(['校团委'] + COLLEGES, '计算机学院', req=True), req=True)}
  {field('上级组织', sel(['计算机学院团委', '计算机学院学生会', '计算机学院研究生会'], '计算机学院团委', req=True), req=True)}
  {field('组织类别', sel(ORG_TYPES, '班级团支部', req=True), req=True)}
  {field('年级', sel(['2020级', '2021级', '2022级', '2023级', '2024级', '2025级', '2026级'], '2021级'), hint='班级团支部、年级组织需填写')}
  {field('指导教师', sel(['王晓琳（T20180427）', '刘洋（T20200611）', '周建华（T20090315）'], '王晓琳（T20180427）', req=True), req=True)}
  <div class="field full"><label><span class="req">*</span>存续状态</label>{radios('alive', ['存续', '已撤销', '已毕业'], '已毕业', req=True)}
  <div class="hint">变更为“已撤销 / 已毕业”后，名下未注销账号将自动命中“组织撤销或已毕业”风险规则</div></div>
  {field('毕业 / 撤销时间', inp('', '2025-06-30', typ='date'))}
  {field('组织代码', inp('', 'CS-TZB-2021-SE01', readonly=True), hint='系统自动生成，不可修改')}
  {field('备注', textarea('选填', '2021级软件工程1班已于 2025 年 6 月整体毕业。', rows=2), cls='full')}
</div>
<div class="mt16">{alert('名下账号：<b>2021级软件工程1班团支部</b>（微信公众号，未注销）。保存后该账号将进入僵尸号核实流程。', 'warning')}</div>"""
    footer = btn('取消', 'organizations.html', 'default') + submit_btn('保存', 'organizations.html', 'primary', 'check', toast='组织信息已保存，已记录操作日志')
    content = backdrop(organizations_content()) + f'<div data-form>{modal("编辑组织 · 2021级软件工程1班团支部", body, footer, "lg", "organizations.html")}</div>'
    page("organization-edit.html", "organizations", "新增 / 编辑组织", [("账号管理", "accounts.html"), ("组织管理", "organizations.html"), ("编辑组织", None)], content)


# ================================================================ 校级审核
def opinion_card(default, phrases, title="校级审核意见"):
    ph = "".join(f'<button type="button" class="chip" data-toast="已填入常用意见" onclick="this.closest(\'.card\').querySelector(\'textarea\').value=this.textContent">{p}</button>' for p in phrases)
    body = (f'{field("审核意见", textarea("请填写校级审核意见", default, req=True, maxlen=200, rows=3), req=True)}'
            f'<div class="small muted mt12 mb8">常用意见</div><div class="chips">{ph}</div>')
    return card(title, body)


def approval_detail():
    a = ACCOUNTS["new"]
    no = FLOWS["new"]["no"]
    intro = ("“中南计算机青年”是计算机学院团委新媒体中心主办的微信公众号，面向计算机学院全体团员青年及关注学院发展的校友、家长。"
             "平台以“思想引领、学业发展、科创实践、青春风采”为内容定位，设置“计院青年说”“科创前沿”“学业加油站”“青春印记”四个固定栏目，"
             "每周更新不少于 2 次。信息发布范围限于学院团学工作动态、主题团日与志愿服务活动、学科竞赛与科创成果、学业指导与就业信息等，"
             "不发布与学院团学工作无关的商业推广内容。平台严格执行“一审学生编辑、二审新媒体中心主任、三审指导教师”的三审制度，"
             "建立舆情应对、账号安全与应急处置机制，账号密码由指导教师与学生负责人共同保管，每学期更换一次。")
    left = f"""
{acct_head(a, tag('新建备案', 'primary') + st('备案申请中'), f'<div class="small muted">申请编号</div><div class="bold num">{no}</div><div class="small muted mt4">提交于 2026-09-24 10:12</div>')}
<div class="grid g2 mt16">
  {card('归属信息', kv([('所属学院', '计算机学院'), ('所属团学组织', a['org']), ('组织类别', a['org_type']), ('平台管理层级', a['level'])], 2))}
  {card('平台信息', kv([('平台类型', '<span class="flex gap8">' + pf(a['platform'], 'sm') + a['platform'] + '</span>'), ('账号名称', a['name']), ('曾用名', '无'), ('平台ID', f'<span class="num">{a["pid"]}</span>'), ('是否认证', '否'), ('粉丝数', '0'), ('开通时间', a['opened']), ('运营团队规模（单位：人）', '6'), ('主页链接', 'mp.weixin.qq.com/csu_cs_youth'), ('平台头像', '已上传'), ('二维码', '未上传（非必填）'), ('信息发布范围', '学院团学活动相关信息。', True)], 2))}
  {card('运行信息', kv([('最近一次公开内容发布时间', '2026-09-22'), ('更新频率', UPDATE_FREQ[0]), ('运行状态', '正常运行'), ('异常情况', '无'), ('备注', '无')], 2))}
  {card('责任人与审核信息', kv([('当前管理教师', '王晓琳 · ' + PEOPLE['王晓琳']['no'] + ' · 宣传工作辅导员 · 专职 · ' + PEOPLE['王晓琳']['phone']), ('具体负责人', '李明 · 8209230117 · ' + PEOPLE['李明']['phone']), ('管理员', '陈可欣（8209230221）、刘子涵（8209240133）'), ('一审负责人', '王晓琳 · ' + PEOPLE['王晓琳']['no']), ('二审负责人', '周建华 · ' + PEOPLE['周建华']['no']), ('三审负责人', '陈静 · ' + PEOPLE['陈静']['no'])], 2))}
</div>
<div class="mt16">{card('平台信息确认', mechanism_blocks())}</div>
<div class="mt16">{card('平台介绍', f'<p class="sub" style="line-height:1.9">{intro}</p><div class="small muted mt8">共 326 字 · 已按指导教师退回意见补充内容定位、栏目设置与信息发布范围</div>', tag('第 2 次提交', 'warning'))}</div>
<div class="mt16">{card('重复检查结果', alert('<b>未发现同平台同ID</b>（微信公众号 · csu_cs_youth）；<b>存在 1 个相似名称</b>：“中南计科青年”（抖音 · 计算机学院 · 2019 年已注销），<b>申请人已确认不是同一账号</b>。', 'success') + '<div class="small muted mt8">检查时间 2026-09-24 10:11 · 检查范围：全校在册与已注销账号（含曾用名）</div>')}</div>
<div class="mt16">{card('附件材料', '<div class="upload-list" style="margin:0">' + fchip('四项机制制度文件.pdf') + fchip('账号主页截图.png', 'image') + fchip('信息发布三审制度.pdf') + fchip('学院团委审批表.pdf') + '</div>')}</div>"""
    right = f"""
<div class="sticky col gap16">
  {card('审核流程', flow_tl('new', 5, '校团委终审 · 待您审核', '陈静（学校管理员） · 已停留 2 天'), tag('三级审核', 'primary'))}
  {opinion_card('准予备案。', ['准予备案，已生成备案表。', '信息完整，同意备案。', '材料不全，请补充后重新提交。'])}
</div>"""
    content = f"""<div data-form>
{page_hd('新建备案 · 校级终审', f'{no} · 学生提交 → 指导教师（退回 1 次）→ 学院团委 → 校团委终审', back_btn('approvals.html'))}
{scene('一', '第 16 步：校团委终审。审核通过后系统自动建立账号档案，并生成《新媒体公众平台备案表》。', 'filing-form.html', '下一步：生成备案表')}
<div class="split mt16"><div>{left}</div>{right}</div>
<div class="actbar"><div class="grow">{icon('info')} 审核通过后将自动建立“一账号一档案”，备案状态变为“已备案”，并通知学生与指导教师</div>
  {btn('驳回', '../common/modal-reject.html', 'danger', 'x-circle')}
  {btn('退回修改', '../common/modal-return.html', 'warning', 'undo')}
  {submit_btn('审核通过并生成备案表', 'filing-form.html', 'primary', 'check', toast='已准予备案，档案已建立')}
</div></div>"""
    page("approval-detail.html", "approvals", "新建备案 · 校级审核", [("业务审核", "approvals.html"), ("校级审核中心", "approvals.html"), ("新建备案审核", None)], content)


def approval_change():
    a = ACCOUNTS["rename"]
    no = FLOWS["rename"]["no"]
    diff = diff_table([
        ("账号名称", a["name"], a["new_name"]),
        ("曾用名", "—", a["name"]),
        ("平台类型", a["platform"], a["platform"]),
        ("平台ID", a["pid"], a["pid"]),
        ("所属组织", a["org"], a["org"]),
        ("平台层级", a["level"], a["level"]),
        ("管理教师", a["teacher"], a["teacher"]),
        ("学生负责人", a["student"], a["student"]),
    ])
    left = f"""
{acct_head(a, tag('账号名称变更', 'warning') + tag('重要变更', 'danger') + st(a['filing']), f'<div class="small muted">申请编号</div><div class="bold num">{no}</div><div class="small muted mt4">粉丝 {a["fans"]}</div>')}
<div class="mt16">{card('变更前后对比', diff + '<div class="mt12">' + alert('名称变更属于<b>重要变更</b>，须经指导教师、学院团委后报校团委审核。生效后原名称“计算机学院学生会”自动记入<b>曾用名</b>，历史发布、年审、日志均保留在同一档案下，可按曾用名检索。', 'info') + '</div>', tag('变更 2 项', 'warning'))}</div>
<div class="grid g2 mt16">
  {card('变更原因', '<p class="sub">学生会换届后统一品牌名称。经 2026 年 9 月学生会全体委员会议决议，学院学生会对外统一使用“中南计院学生会”名称，与学院其他平台命名规范保持一致。</p>')}
  {card('佐证材料', '<div class="upload-list" style="margin:0">' + fchip('学生会换届决议.pdf') + fchip('微博改名预审截图.png', 'image') + fchip('学院团委意见.pdf') + '</div><div class="small muted mt8">平台侧改名需在校级审核通过后 7 日内完成，并上传改名后主页截图</div>')}
</div>
<div class="mt16">{card('同名检查', alert('全校范围内未发现名称为“中南计院学生会”的在册或已注销账号，可以使用。', 'success'))}</div>"""
    right = f"""
<div class="sticky col gap16">
  {card('审核流程', flow_tl('rename', 3, '校团委审核 · 待您审核', '陈静（学校管理员） · 学院 2026-09-29 报送'), tag('重要变更', 'danger'))}
  {opinion_card('同意变更，原名称记入曾用名。', ['同意变更，原名称记入曾用名。', '名称不规范，请调整后重新提交。'])}
</div>"""
    content = f"""<div data-form>
{page_hd('名称变更 · 校级审核', f'{no} · 计算机学院学生会 → 中南计院学生会', back_btn('approvals.html'))}
{scene('二', '第 6 步：校级审核。审核通过后变更立即生效，可在档案“变更记录”中查看曾用名。', '../common/archive-changes.html', '下一步：查看变更记录')}
<div class="split mt16"><div>{left}</div>{right}</div>
<div class="actbar"><div class="grow">{icon('info')} 通过后账号名称更新为“中南计院学生会”，备案状态恢复为“已备案”</div>
  {btn('驳回', '../common/modal-reject.html', 'danger', 'x-circle')}
  {btn('退回修改', '../common/modal-return.html', 'warning', 'undo')}
  {submit_btn('审核通过', '../common/archive-changes.html', 'primary', 'check', toast='变更已生效，原名称记入曾用名')}
</div></div>"""
    page("approval-change.html", "approvals", "名称变更 · 校级审核", [("业务审核", "approvals.html"), ("校级审核中心", "approvals.html"), ("名称变更审核", None)], content)


def approval_cancel():
    a = dict(name="2022级市场营销2班团支部", platform="微信公众号", pid="csu_mk2202", org="商学院 · 2022级市场营销2班团支部",
             level="三级平台", opened="2022-10-12")
    tl = timeline([
        ("done", "学生提交注销申请", "王一帆（团支书） · 2026-09-23 18:22", "班级已于 2026 年 6 月毕业，申请注销团支部公众号。"),
        ("done", "指导教师审核通过", "陈立新（2022级辅导员） · 2026-09-24 10:40", "情况属实，已核对毕业名单。"),
        ("done", "学院团委审核通过", "杨帆（商学院团委） · 2026-09-27 17:05", "团支部已毕业，同意注销。"),
        ("now", "校团委审核 · 待您审核", "陈静（学校管理员）", ""),
    ])
    left = f"""
{acct_head(a, tag('账号注销', 'danger') + st('注销申请中'), '<div class="small muted">申请编号</div><div class="bold num">ZX20260923006</div><div class="small muted mt4">粉丝 214 · 最近发布 2026-06-20</div>')}
<div class="grid g2 mt16">
  {card('注销原因', kv([('注销原因', tag('团支部毕业', 'danger')), ('原因说明', '2022级市场营销2班已于 2026 年 6 月整体毕业，团支部随之撤销，无学生继续运营。', True), ('申请人', '王一帆（原团支书 · 8202220316）'), ('发起方式', '学生本人')], 2))}
  {card('佐证材料', '<div class="upload-list" style="margin:0">' + fchip('2026届毕业班级名单.pdf') + fchip('团支部撤销说明.pdf') + fchip('公众号停更公告截图.png', 'image') + '</div><div class="small muted mt8">已核验：毕业名单与学籍系统一致</div>')}
</div>
<div class="mt16">{card('账号现状', kv([('运行状态', st('不活跃')), ('年审状态', st('待填报')), ('最近发布', '2026-06-20（毕业寄语）'), ('负责教师', '陈立新'), ('学生负责人', '王一帆（已毕业）'), ('粉丝数', '214')], 3))}</div>
<div class="mt16">{card('注销后处理说明', '<div class="col gap8">' + alert('<b>不删除档案：</b>注销后账号档案、历史负责人、年审与变更记录全部永久保留，可按原名称检索。', 'info') + alert('<b>状态转为“已注销”：</b>运行状态、备案状态同步变更为“已注销”，本年度年审记为“本年度注销”，不再参与后续年审。', 'info') + alert('<b>平台侧处置：</b>学生负责人须在 15 日内于平台侧完成注销或停用，并上传平台注销截图备查。', 'warning') + '</div>')}</div>"""
    right = f"""
<div class="sticky col gap16">
  {card('审核流程', tl, tag('三级审核', 'primary'))}
  {opinion_card('同意注销，保留历史数据。', ['同意注销，保留历史数据。', '佐证材料不足，请补充。'])}
</div>"""
    content = f"""<div data-form>
{page_hd('账号注销 · 校级审核', 'ZX20260923006 · 商学院 · 2022级市场营销2班团支部', back_btn('approvals.html'))}
<div class="split"><div>{left}</div>{right}</div>
<div class="actbar"><div class="grow">{icon('info')} 同意后账号状态转为“已注销”，数据永久保留，不做物理删除</div>
  {btn('驳回', '../common/modal-reject.html', 'danger', 'x-circle')}
  {btn('退回修改', '../common/modal-return.html', 'warning', 'undo')}
  {submit_btn('同意注销', '../common/archive-cancel.html', 'danger-solid', 'ban', toast='已同意注销，账号状态转为已注销')}
</div></div>"""
    page("approval-cancel.html", "approvals", "账号注销 · 校级审核", [("业务审核", "approvals.html"), ("校级审核中心", "approvals.html"), ("注销审核", None)], content)


# ================================================================ 年度年审
ANNUAL_NODES = [("任务开始", T["start"]), ("学生填报截止", T["stu_end"]), ("教师审核截止", T["teacher_end"]),
                ("学院提交截止", T["college_end"]), ("校级审核截止", T["school_end"]), ("整改截止", T["rectify_end"]),
                ("结果发布", "2026-12-20")]
# 2026 年度年审各状态记录数（合计 986）
ANNUAL_COUNTS = [("待填报", 312, ""), ("待教师审核", 186, "orange"), ("待学院审核", 142, "orange"), ("待学校审核", 168, ""),
                 ("待整改", 23, "red"), ("年审通过", 155, "green")]


def annual_tasks():
    now_nodes = [(n, d, "done" if i == 0 else ("now" if i == 1 else "")) for i, (n, d) in enumerate(ANNUAL_NODES)]
    card26 = f"""
<div class="card task-card on">
  <div class="flex between"><div class="flex gap12"><span class="stat-ic">{icon('calendar')}</span><div><div class="fs16 bold">{T['name']}</div>
  <div class="small muted">NS2026 · 发布于 2026-09-15 09:00 · 发布人 陈静</div></div></div>{st('进行中')}</div>
  <div class="grid g4">
    <div><div class="small muted">年审账号</div><div class="fs18 bold num">{T['total']}</div></div>
    <div><div class="small muted">学生已填报</div><div class="fs18 bold num">674</div></div>
    <div><div class="small muted">年审通过</div><div class="fs18 bold num c-success">155</div></div>
    <div><div class="small muted">待整改</div><div class="fs18 bold num c-danger">23</div></div>
  </div>
  <div class="flex gap12"><span class="small muted nowrap">整体进度</span>{progress(68)}<span class="small bold num">68.4%</span></div>
  {ntl(now_nodes)}
  <div class="flex gap8 end">{btn('任务详情', 'annual-task-detail.html', 'default', 'eye', 'sm')}{btn('全校进度', 'annual-progress.html', 'light', 'chart', 'sm')}{btn('校级审核', 'annual-review.html', 'primary', 'file-check', 'sm')}</div>
</div>"""

    def past(year, total, l2, l3, club, passed, rect, cancel):
        return f"""
<div class="card task-card">
  <div class="flex between"><div class="flex gap12"><span class="stat-ic gray">{icon('archive')}</span><div><div class="fs16 bold">{year}年度团学组织新媒体平台年审</div>
  <div class="small muted">NS{year} · {year}-09-10 至 {year}-12-20</div></div></div>{st('已结束')}</div>
  <div class="grid g4">
    <div><div class="small muted">年审平台</div><div class="fs18 bold num">{total}</div></div>
    <div><div class="small muted">年审通过</div><div class="fs18 bold num c-success">{passed}</div></div>
    <div><div class="small muted">整改后通过</div><div class="fs18 bold num c-warning">{rect}</div></div>
    <div><div class="small muted">本年度注销</div><div class="fs18 bold num muted">{cancel}</div></div>
  </div>
  <div class="mini-list"><span>二级平台 {l2}</span><span>三级平台 {l3}</span><span>社团平台 {club}</span></div>
  <div class="flex gap8 end">{btn('年审结果', 'annual-task-detail.html', 'default', 'eye', 'sm')}{btn('导出年审台账', 'export.html', 'default', 'download', 'sm')}</div>
</div>"""
    history = table(["年度", "任务名称", "年审平台", "通过率", "不通过", "注销", "状态", "操作"], [
        dict(cells=["2026", T["name"], 986, '<span class="muted">进行中</span>', "—", "—", st("进行中"), ops(("详情", "annual-task-detail.html"), ("进度", "annual-progress.html"))], href="annual-task-detail.html"),
        dict(cells=["2025", "2025年度团学组织新媒体平台年审", 972, "96.3%", 11, 25, st("已结束"), ops(("详情", "annual-task-detail.html"), ("导出", "export.html"))]),
        dict(cells=["2024", "2024年度团学组织新媒体平台年审", 948, "95.1%", 14, 32, st("已结束"), ops(("详情", "annual-task-detail.html"), ("导出", "export.html"))]),
        dict(cells=["2023", "2023年度团学组织新媒体平台年审（线下）", 903, "93.8%", 19, 37, st("已结束"), ops(("归档材料", None, "2023 年度为线下年审，已归档纸质材料扫描件"),)]),
    ])
    content = f"""
{page_hd('年度年审', '每年发起一次，系统按在册账号自动生成年审记录；历史数据自动继承，当年只确认变化',
         btn('创建年审任务', 'annual-task-create.html', 'primary', 'plus'))}
{ptabs(ANNUAL_TABS, '年审任务')}
{card26}
<div class="grid g2 mt16">{past(2025, 972, 151, 662, 159, 936, 22, 25)}{past(2024, 948, 146, 649, 153, 902, 29, 32)}</div>
<div class="mt16">{card('历年年审任务', history)}</div>"""
    page("annual-tasks.html", "annual", "年度年审任务", [("业务审核", "approvals.html"), ("年度年审", None)], content)


def annual_task_create():
    date_fields = "".join(field(n, inp("", d, req=True, typ="date"), req=True) for n, d in ANNUAL_NODES)
    ev = [("账号主页截图", True), ("近 3 个月发布内容截图", True), ("信息发布审核记录", False), ("负责人变更说明", False),
          ("运营情况说明", False), ("四项机制制度文件", False)]
    ev_html = "".join(f'<button type="button" class="chip{" on" if on else ""}" data-choice>{icon("check") if on else icon("plus")}{n}{"（必传）" if on else ""}</button>' for n, on in ev)
    rules = [("长期未更新（≥ 停更阈值）", True), ("最近发布为空", True), ("账号无法访问", True), ("无学生负责人", True), ("无负责教师", True),
             ("所属组织撤销或已毕业", True), ("同平台同 ID 重复备案", True)]
    rule_html = "".join(f'<div>{cb(n, c)}</div>' for n, c in rules)
    content = f"""<div data-form>
{page_hd('创建年审任务', '演示剧本五 · 第 1 步：学校管理员配置年度、时间节点与要求并发布', back_btn('annual-tasks.html'))}
{alert('<b>继承原则：历史数据自动继承，当年只确认变化。</b>发布后系统按在册账号自动生成年审记录，自动带入 2025 年度账号信息，学生仅需确认是否仍存在、是否正常运营、负责人与名称等是否变化。', 'success')}
<div class="grid mt16" style="grid-template-columns:minmax(0,1fr) 340px;align-items:start">
<div class="col gap16">
  {card('基本信息', f'<div class="form-grid">' + field('年度', sel(['2026', '2027'], '2026', req=True), req=True) + field('任务名称', inp('', T['name'], req=True), req=True) + '</div>')}
  {card('时间节点', f'<div class="form-grid c3">{date_fields}</div><div class="divider"></div><div class="small muted mb8">时间轴预览</div>' + ntl([(n, d, '') for n, d in ANNUAL_NODES]) + '<div class="mt12">' + alert('时间节点由学校管理员按年度配置，<b>不在程序中固定</b>；发布后仍可调整，调整将通知全部相关人员并记录日志。', 'info') + '</div>', tag('7 个节点', 'primary'))}
  {card('年审要求', field('年审要求说明', textarea('', '请各学院组织本单位全部在册新媒体平台完成年审：1. 学生负责人确认账号是否仍存在、是否正常运营、能否正常访问；2. 核对负责人、管理教师、账号名称是否发生变化；3. 已停止运营的账号须同步提交注销申请；4. 指导教师须逐一核实内容安全与“三审三校”执行情况。', req=True, maxlen=500, rows=5), req=True) + '<div class="mt16"><div class="field-label mb8">佐证材料要求</div><div class="chips">' + ev_html + '</div><div class="hint mt8">点击切换是否要求提交；“必传”项未上传时学生端无法提交</div></div>')}
  {card('僵尸号筛查参数', f'<div class="flex gap24 wrap mb16"><div class="inline-inp">停更阈值 {inp("", "180", typ="number")} 天</div><div class="inline-inp">高风险阈值 {inp("", "365", typ="number")} 天</div></div><div class="grid g3">{rule_html}</div><div class="hint mt12">规则明细可在 <a class="link" href="settings-rules.html">风险规则配置</a> 中维护；命中后仅预警，不自动注销</div>')}
</div>
<div class="sticky col gap16">
  {card('年审范围', radios('scope', [f'全部在册账号（{T["total"]} 个）', '按学院选择', '按平台层级选择'], f'全部在册账号（{T["total"]} 个）') + '<div class="divider"></div>' + cb('排除已注销账号（41 个）', True) + '<div class="mt8">' + cb('包含本年度新建账号（63 个）', True) + '</div><div class="mt8">' + cb('排除备案申请中账号', False) + '</div>')}
  {card('发布预览', kv([('年审记录', f'<b class="num">{T["total"]}</b> 条'), ('涉及学院', '35 个'), ('学生负责人', '1,124 人'), ('指导教师', '312 人')], 2) + '<div class="divider"></div><div class="small muted">发布后通过站内信与 ITS 消息通知全部学生负责人、指导教师与学院管理员</div>')}
  <div class="flex gap8">{btn('保存草稿', None, 'default', 'file', toast='草稿已保存')}{submit_btn('发布任务', 'annual-task-detail.html', 'primary', 'send', toast='年审任务已发布，正在生成 986 条年审记录')}</div>
</div>
</div></div>"""
    page("annual-task-create.html", "annual", "创建年审任务", [("年度年审", "annual-tasks.html"), ("创建年审任务", None)], content)


def annual_task_detail():
    stats = "".join(stat(n, v, f"占 {v / T['total'] * 100:.1f}%", ic, c) for (n, v, c), ic in
                    zip(ANNUAL_COUNTS, ["inbox", "user", "hierarchy", "building", "wrench", "check-circle"]))
    nodes = [(n, d, "done" if i == 0 else ("now" if i == 1 else "")) for i, (n, d) in enumerate(ANNUAL_NODES)]
    rec = table(["年审编号", "账号", "学院", "层级", "继承自 2025 年度", "学生负责人", "当前状态"], [
        dict(cells=['<span class="num">NS2026-CS-0012</span>', acct("中南计院团委", "微信公众号"), "计算机学院", "二级平台", tag("年审通过", "success"), "李明", st("待学校审核")], href="annual-review-detail.html"),
        dict(cells=['<span class="num">NS2026-CS-0013</span>', acct("计算机学院学生会", "微博"), "计算机学院", "二级平台", tag("年审通过", "success"), "李明", st("待指导教师审核")]),
        dict(cells=['<span class="num">NS2026-CS-0021</span>', acct("计院街舞社", "抖音"), "计算机学院", "社团平台", tag("年审通过", "success"), "李四", st("待填报")]),
        dict(cells=['<span class="num">NS2026-CS-0027</span>', acct("计院青年志愿者", "小红书"), "计算机学院", "二级平台", tag("年审通过", "success"), "何雨桐", st("整改复核中")]),
        dict(cells=['<span class="num">NS2026-CS-0031</span>', acct("2021级软件工程1班团支部", "微信公众号"), "计算机学院", "三级平台", tag("年审通过", "success"), '<span class="c-danger">—（已毕业）</span>', st("待指导教师审核")]),
        dict(cells=['<span class="num">NS2026-BS-0004</span>', acct("商学院团委", "微信公众号"), "商学院", "二级平台", tag("年审通过", "success"), "林嘉怡", st("待学院审核")]),
        dict(cells=['<span class="num">NS2026-XY-0018</span>', acct("湘雅医声", "抖音"), "湘雅医学院", "二级平台", tag("年审通过", "success"), "许哲", st("待指导教师审核")]),
        dict(cells=['<span class="num">NS2026-JD-0009</span>', acct("机电创客空间", "哔哩哔哩"), "机电工程学院", "二级平台", tag("整改后通过", "warning"), "邓子豪", st("待整改")]),
    ])
    content = f"""
{page_hd(T['name'], 'NS2026 · 发布人 陈静 · 2026-09-15 09:00', btn('编辑时间节点', None, 'default', 'edit', toast='时间节点已进入编辑状态，调整后将通知相关人员') + btn('全校进度', 'annual-progress.html', 'primary', 'chart'))}
{alert(f'<b>已发布，系统已按在册账号自动生成 {T["total"]} 条年审记录。</b>记录已自动继承 2025 年度账号信息，并推送至 35 个学院的学生负责人与指导教师。', 'success')}
<div class="mt16">{scene('五', '第 2 步完成：年审记录已生成。下一步由学生负责人李明在移动端确认“中南计院团委”无异动并提交。', '../../app/student/annual.html', '学生端填报（演示下一步）')}</div>
<div class="grid g6 mt16">{stats}</div>
<div class="grid mt16" style="grid-template-columns:minmax(0,1fr) 360px;align-items:start">
  {card('已生成年审记录（示例）', rec + pager(T['total'], 5), btn('导出全部记录', 'export.html', 'text', 'download', 'sm'))}
  <div class="col gap16">
    {card('时间节点', timeline([('done' if s == 'done' else ('now' if s == 'now' else 'wait'), n, d + ('（进行中）' if s == 'now' else ''), '') for n, d, s in nodes]))}
    {card('任务配置', kv([('年审范围', '全部在册账号'), ('停更阈值', '180 天'), ('必传材料', '主页截图 / 近 3 月截图'), ('排除', '已注销 41 个')], 2))}
  </div>
</div>"""
    page("annual-task-detail.html", "annual", "年审任务详情", [("年度年审", "annual-tasks.html"), ("任务详情", None)], content)


ANNUAL_COLLEGES = [
    # 学院, 账号, 学生填报, 教师审核, 学院提交, 学校通过
    ("计算机学院", 36, 32, 27, 24, 21), ("商学院", 42, 42, 41, 40, 38), ("文学院", 28, 28, 28, 28, 28), ("机电工程学院", 51, 44, 38, 33, 30),
    ("湘雅医学院", 64, 58, 50, 45, 41), ("法学院", 22, 15, 12, 10, 9), ("数学与统计学院", 24, 22, 19, 17, 15), ("化学化工学院", 31, 29, 26, 24, 22),
    ("材料科学与工程学院", 33, 27, 23, 21, 20), ("土木工程学院", 45, 34, 30, 28, 26), ("交通运输工程学院", 29, 25, 21, 19, 18), ("外国语学院", 26, 24, 22, 20, 19),
]


def annual_progress():
    rows = []
    for c, n, s1, s2, s3, s4 in ANNUAL_COLLEGES:
        p = round(s4 / n * 100)
        color = "green" if p == 100 else ("orange" if p < 60 else "")
        state = tag("已完成", "success") if p == 100 else (tag("滞后", "danger") if p < 60 else tag("进行中", "primary"))

        def cell(v, _n=n):
            return f'<span class="num">{v}</span><span class="muted small"> / {_n}</span>'
        rows.append(dict(cells=[f'<b>{c}</b>', n, cell(s1), cell(s2), cell(s3), cell(s4),
                                f'<div class="flex gap8" style="min-width:150px">{progress(p, color)}<span class="num small">{p}%</span></div>', state,
                                ops(("明细", "annual-college-detail.html"), ("催办", None, f"已向{c}未完成节点的负责人发送催办提醒"))],
                         href="annual-college-detail.html"))
    tbl = table(["学院", "账号数", "学生填报", "教师审核", "学院提交", "学校通过", "完成率", "状态", "操作"], rows)
    kpis = "".join([
        stat("年审账号", T["total"], "35 个学院", "database"),
        stat("学生已填报", 674, "填报率 68.4%", "inbox", "", ),
        stat("教师已审核", 488, "审核率 49.5%", "user", "orange"),
        stat("学院已提交", 323, "提交率 32.8%", "hierarchy", "orange"),
        stat("学校已通过", 155, "通过率 15.7%", "check-circle", "green"),
        stat("滞后学院", 3, "完成率低于 60%", "alert", "red"),
    ])
    content = f"""
{page_hd('全校年审进度', f'{T["name"]} · 当前节点：学生填报（{T["stu_end"]} 截止）',
         btn('导出进度表', 'export.html', 'default', 'download') + btn('一键催办', None, 'primary', 'bell', toast='已向 32 个未完成学院的学生负责人、指导教师与学院管理员发送催办'))}
{ptabs(ANNUAL_TABS, '全校进度')}
<div class="grid g6">{kpis}</div>
<div class="grid mt16" style="grid-template-columns:minmax(0,1fr) 320px;align-items:start">
  {card('各学院节点进度', tbl + pager(35, 3), seg([('全部学院', 'a'), ('仅看滞后', 'b'), ('已完成', 'c')]))}
  <div class="col gap16">
    {card('年审状态分布', donut([(n, v) for n, v, _ in ANNUAL_COUNTS], T['total'], '年审记录'))}
    {card('节点提醒', timeline([('now', '学生填报截止', T['stu_end'] + ' · 剩余 15 天', '尚有 312 条记录待填报'), ('wait', '教师审核截止', T['teacher_end'], ''), ('wait', '学院提交截止', T['college_end'], ''), ('wait', '校级审核截止', T['school_end'], '')]))}
  </div>
</div>"""
    page("annual-progress.html", "annual", "全校年审进度", [("年度年审", "annual-tasks.html"), ("全校进度", None)], content)


def annual_college_detail():
    rows_data = [
        ("中南计院团委", "微信公众号", "二级平台", "李明", "王晓琳", "done", "done", "done", "now", "待学校审核", "无异动"),
        ("计算机学院研究生会", "微信公众号", "二级平台", "张蕾", "刘洋", "done", "done", "done", "done", "年审通过", "无异动"),
        ("2023级软件工程2班团支部", "QQ", "三级平台", "陈可欣", "刘洋", "done", "done", "done", "done", "年审通过", "无异动"),
        ("计算机学院学生会", "微博", "二级平台", "李明", "王晓琳", "done", "now", "wait", "wait", "待指导教师审核", "变更"),
        ("计院青年志愿者", "小红书", "二级平台", "何雨桐", "王晓琳", "done", "back", "now", "wait", "整改复核中", "无异动"),
        ("2021级软件工程1班团支部", "微信公众号", "三级平台", "—（已毕业）", "王晓琳", "wait", "now", "wait", "wait", "待指导教师审核", "注销"),
        ("2024级计算机科学1班团支部", "微信公众号", "三级平台", "吴迪", "刘洋", "done", "done", "now", "wait", "待学院审核", "无异动"),
        ("2022级人工智能1班团支部", "QQ", "三级平台", "彭宇", "王晓琳", "done", "now", "wait", "wait", "待指导教师审核", "无异动"),
        ("计院街舞社", "抖音", "社团平台", "李四", "王晓琳", "now", "wait", "wait", "wait", "待填报", "变更"),
        ("计院科协", "哔哩哔哩", "二级平台", "何雨桐", "王晓琳", "now", "wait", "wait", "wait", "待填报", "新建"),
        ("计院ACM协会", "QQ", "社团平台", "孙悦", "王晓琳", "now", "wait", "wait", "wait", "待填报", "变更"),
        ("计院摄影协会", "视频号", "社团平台", "李明", "王晓琳", "now", "wait", "wait", "wait", "待填报", "无异动"),
    ]
    rows = []
    for n, p, lv, stu, tch, a, b, c, d, stv, chg in rows_data:
        stu_html = f'<span class="c-danger">{stu}</span>' if "毕业" in stu else stu
        back_txt = "要求整改" if b == "back" else ""
        rows.append(dict(cells=[acct(n, p, lv), stu_html, tch, ns(a), ns(b, back_txt), ns(c), ns(d), st(chg), st(stv),
                                ops(("催办学生", None, f"已向{stu}发送年审填报催办"), ("催办教师", None, f"已向{tch}老师发送年审审核催办"))]))
    tbl = table(["账号", "学生负责人", "负责教师", "学生填报", "教师审核", "学院提交", "学校审核", "年度异动", "当前状态", "操作"], rows)
    content = f"""
{page_hd('学院年审明细 · 计算机学院', '账号 36 个 · 学院管理员 周建华 · 学院提交截止 ' + T['college_end'],
         back_btn('annual-progress.html', '返回全校进度') + btn('催办全部未完成', None, 'primary', 'bell', toast='已向计算机学院 15 个未完成账号的负责人发送催办'))}
<div class="grid g5">
  {stat('年审账号', 36, '二级 9 · 三级 18 · 社团 9', 'database')}
  {stat('学生已填报', 32, '待填报 4', 'inbox')}
  {stat('教师已审核', 27, '王晓琳 18 · 刘洋 9', 'user', 'orange')}
  {stat('学校已通过', 21, '完成率 58%', 'check-circle', 'green')}
  {stat('风险账号', 3, '疑似僵尸号 2 · 整改 1', 'alert', 'red', href='zombie.html')}
</div>
<div class="mt16">{card('账号年审节点', tbl + pager(36, 3), seg([('全部', 'a'), ('未完成', 'b'), ('已通过', 'c')]))}</div>"""
    page("annual-college-detail.html", "annual", "学院年审明细", [("年度年审", "annual-tasks.html"), ("全校进度", "annual-progress.html"), ("计算机学院", None)], content)


REVIEW_ROWS = [
    # 账号, 平台, 学院, 层级, 年度异动, 风险, 教师意见, 学院意见, 分类, 说明
    ("中南计院团委", "微信公众号", "计算机学院", "二级平台", "无异动", "无", "无异动，信息完整。", "统一提交", "batch", ""),
    ("计算机学院研究生会", "微信公众号", "计算机学院", "二级平台", "无异动", "无", "同意。", "统一提交", "batch", ""),
    ("2023级软件工程2班团支部", "QQ", "计算机学院", "三级平台", "无异动", "无", "信息无变化。", "统一提交", "batch", ""),
    ("2024级计算机科学1班团支部", "微信公众号", "计算机学院", "三级平台", "无异动", "无", "同意。", "统一提交", "batch", ""),
    ("2023级网络工程1班团支部", "QQ", "计算机学院", "三级平台", "无异动", "无", "运营正常。", "统一提交", "batch", ""),
    ("计院羽毛球协会", "抖音", "计算机学院", "社团平台", "无异动", "无", "同意。", "统一提交", "batch", ""),
    ("2024级人工智能1班团支部", "QQ", "计算机学院", "三级平台", "无异动", "无", "无异动。", "统一提交", "batch", ""),
    ("计院科技创新中心", "视频号", "计算机学院", "二级平台", "无异动", "无", "同意。", "统一提交", "batch", ""),
    ("计院青年志愿者", "小红书", "计算机学院", "二级平台", "无异动", "整改后", "要求整改（已整改通过）", "整改通过，恢复流转", "single", "整改 2 轮"),
    ("2021级软件工程1班团支部", "微信公众号", "计算机学院", "三级平台", "注销", "疑似僵尸号", "建议注销", "转注销", "single", "本年度注销"),
    ("计算机学院学生会", "微博", "计算机学院", "二级平台", "变更", "无", "名称变更已同意", "重要变更，报校团委", "single", "重要变更"),
    ("计院科协", "哔哩哔哩", "计算机学院", "二级平台", "新建", "平台 ID 变化", "转新建并注销原 ID", "同意", "single", "异常"),
]


def annual_review_content():
    rows = []
    for n, p, col, lv, chg, risk, t_op, c_op, cat, note in REVIEW_ROWS:
        risk_html = '<span class="muted">无</span>' if risk == "无" else tag(risk, "danger" if "僵尸" in risk else "warning")
        cls_tag = tag("可批量", "success") if cat == "batch" else tag("单独审核 · " + note, "warning")
        op = ops(("审核", "annual-review-detail.html")) if cat == "single" else ops(("查看", "annual-review-detail.html"), ("通过", None, f"已通过：{n}"))
        rows.append(dict(cells=[acct(n, p, f"{col} · {lv}"), st(chg), risk_html, f'<span class="small sub">{t_op}</span>',
                                f'<span class="small sub">{c_op}</span>', st("待学校审核"), cls_tag, op],
                         href="annual-review-detail.html" if cat == "single" else None, cat=cat))
    tbl = table(["账号", "年度异动", "风险", "教师意见", "学院意见", "当前状态", "审核方式", "操作"], rows, check=True, id_="revTable")
    tabs = seg([("全部 36", "all"), ("可批量通过：无异动无风险 18", "batch"), ("需单独审核：异常 · 注销 · 整改 · 重要变更 4", "single")], target="#revTable")
    return f"""
{page_hd('年审校级审核', '计算机学院已于 2026-09-29 17:00 统一提交校团委（周建华）· 当前待学校审核 36 个账号',
         sel(['计算机学院（36）', '商学院（40）', '文学院（28）', '湘雅医学院（45）'], '计算机学院（36）', ph='') )}
{ptabs(ANNUAL_TABS, '校级审核')}
{alert('<b>审核规则：</b>无异动、无风险且信息完整的账号可批量审核通过；存在异常、注销、整改、重要变更的账号原则上单独审核。', 'info')}
<div class="card card-bd mt16">
  <div class="toolbar">{tabs}
    <div class="flex gap8"><span class="sub fs13">已选 <b data-checked-count="#revTable">0</b> 个</span>
    {btn('批量通过', 'annual-batch-confirm.html', 'primary', 'check', 'sm')}</div>
  </div>
  {tbl}
  {pager(36, 3)}
</div>"""


def annual_review():
    content = annual_review_content() + '<div class="mt16">' + scene('五', '第 10 步：勾选“可批量通过”中的 18 个无异动账号（含中南计院团委），点击“批量通过”。', 'annual-batch-confirm.html', '下一步：批量通过确认') + '</div>'
    page("annual-review.html", "annual", "年审校级审核", [("年度年审", "annual-tasks.html"), ("校级审核", None)], content)


def annual_batch_confirm():
    names = ["中南计院团委", "计算机学院研究生会", "2023级软件工程2班团支部", "2024级计算机科学1班团支部", "2023级网络工程1班团支部", "计院羽毛球协会",
             "2024级人工智能1班团支部", "计院科技创新中心", "2022级软件工程1班团支部", "2022级计算机科学2班团支部", "2023级人工智能2班团支部",
             "2024级软件工程3班团支部", "2025级计算机科学1班团支部", "计院程序设计协会", "计院读书会", "计算机学院就业信息", "计院学术部", "2025级软件工程1班团支部"]
    chips_html = "".join(f"<span>{n}</span>" for n in names)
    checks = "".join(f'<div>{icon("check-circle")}{t}</div>' for t in [
        "18 个账号年度异动均为“无异动”", "均未命中僵尸号、数据异常等风险规则", "档案必填信息完整，必传佐证材料已上传",
        "指导教师审核、学院统一提交均已完成"])
    body = f"""
<div class="flex gap12 mb16"><span class="stat-ic green">{icon('check-circle')}</span><div><div class="fs16 bold">已选 18 个账号（计算机学院）</div>
<div class="small muted">年审编号 NS2026-CS · 学院提交人 周建华 · 2026-09-29 17:00</div></div></div>
<div class="ck-list">{checks}</div>
<div class="small muted mt16 mb8">批量通过范围</div>
<div class="mini-list">{chips_html}</div>
<div class="mt16">{field('审核意见', textarea('请填写审核意见', '无异动无风险，批量通过。', req=True, maxlen=200, rows=3), req=True)}</div>
<div class="mt12">{alert('批量通过后，18 个账号年审状态变为“年审通过”，并写入各账号档案的年审记录；计算机学院其余 4 个需单独审核的账号不受影响。', 'info')}</div>"""
    footer = btn('取消', 'annual-review.html', 'default') + submit_btn('确认批量通过', '../common/archive-audit.html', 'primary', 'check', toast='已批量通过 18 个账号')
    content = backdrop(annual_review_content()) + f'<div data-form>{modal("批量通过确认", body, footer, "lg", "annual-review.html")}</div>'
    page("annual-batch-confirm.html", "annual", "批量通过确认", [("年度年审", "annual-tasks.html"), ("校级审核", "annual-review.html"), ("批量通过确认", None)], content)


def annual_review_detail():
    a = ACCOUNTS["rectify"]
    confirm = kv([
        ("账号是否仍存在", tag("是", "success")), ("是否正常运营", tag("是", "success")), ("能否正常访问", tag("是", "success")),
        ("最近发布时间", "2026-09-26"), ("学生负责人是否变化", '<span class="muted">否（何雨桐）</span>'), ("管理教师是否变化", '<span class="muted">否（王晓琳）</span>'),
        ("账号名称是否变化", '<span class="muted">否</span>'), ("是否申请注销", '<span class="muted">否</span>'), ("年度异动", st("无异动")),
        ("异常情况说明", "年审中被指导教师要求整改（未建立信息发布审查机制），已于 2026-09-28 整改通过。", True),
    ], 3)
    tl = flow_tl("rectify", None)
    content = f"""<div data-form>
{page_hd('年审单账号审核', 'NS2026-CS-0027 · 整改后恢复流转，须单独审核', back_btn('annual-review.html'))}
{acct_head(a, st('整改复核中') + tag('需单独审核 · 整改后', 'warning'), '<div class="small muted">粉丝</div><div class="bold num">' + a['fans'] + '</div>')}
<div class="split mt16">
<div class="col gap16">
  {card('学生确认事项', confirm, tag('继承 2025 年度信息', 'primary'))}
  {card('佐证材料', '<div class="grid g3"><div class="shot"><img src="' + PHOTOS['screenshot'] + '" alt="账号主页截图"><span>账号主页截图</span></div><div class="shot"><img src="' + PHOTOS['students'] + '" alt="近 3 个月发布截图"><span>近 3 个月发布内容</span></div><div class="shot"><img src="' + PHOTOS['meeting'] + '" alt="审核记录"><span>信息发布审核台账</span></div></div><div class="upload-list">' + fchip('信息发布三审制度（签字盖章版）.pdf') + fchip('7-9月审核台账.xlsx') + '</div>')}
  {card('校级审核意见', field('审核意见', textarea('请填写校级年审意见', '整改到位，年审通过。', req=True, maxlen=200, rows=3), req=True))}
</div>
<div class="sticky col gap16">
  {card('年审与整改记录', timeline([('done', '学生提交年审', '何雨桐（学生用户） · 2026-09-17 20:30', '确认无异动。')]) + '<div class="mt12"></div>' + tl + '<div class="mt12"></div>' + timeline([('now', '校团委年审审核 · 待您审核', '陈静（学校管理员）', '')]), tag('整改 2 轮', 'warning'))}
  {card('整改任务', kv([('整改编号', FLOWS['rectify']['no']), ('截止时间', FLOWS['rectify']['deadline']), ('结果', st('整改通过'))], 2) + '<div class="mt8"><a class="link small" href="../common/archive-rectify.html">查看档案整改记录</a></div>')}
</div>
</div>
<div class="actbar"><div class="grow">{icon('info')} 单独审核：整改、注销、异常、重要变更账号须逐一审核</div>
  {btn('年审不通过', '../common/modal-reject.html', 'danger', 'x-circle')}
  {btn('要求整改', 'rectify-create.html', 'warning', 'wrench')}
  {btn('退回', '../common/modal-return.html', 'default', 'undo')}
  {submit_btn('年审通过', '../common/archive-audit.html', 'primary', 'check', toast='年审已通过，已写入档案年审记录')}
</div></div>"""
    page("annual-review-detail.html", "annual", "年审单账号审核", [("年度年审", "annual-tasks.html"), ("校级审核", "annual-review.html"), ("单账号审核", None)], content)


# ================================================================ 风险治理
ZOMBIE_RULES = [("长期未更新 ≥ 180 天", 31, "clock", ""), ("最近发布为空", 6, "inbox", "orange"), ("账号无法访问", 4, "ban", ""),
                ("无学生负责人", 9, "user", "orange"), ("无负责教师", 4, "users", "orange"), ("组织撤销或已毕业", 12, "flag", ""),
                ("重复备案", 2, "copy", "blue")]


def zombie():
    rules = "".join(f'<div class="hit-chip hit-v"><div class="flex between" style="width:100%"><span class="rule-ic {c}">{icon(ic)}</span><b>{v}</b></div><div class="small sub">{n}</div></div>' for n, v, ic, c in ZOMBIE_RULES)
    rows_data = [
        ("2021级软件工程1班团支部", "微信公众号", "计算机学院 · 三级平台", "412 天", "停更 ≥ 180 天 / 团支部已毕业", "高风险", "待校团委确认", "zombie-detail.html"),
        ("计院摄影协会", "视频号", "计算机学院 · 社团平台", "212 天", "停更 ≥ 180 天", "中风险", "学生核实中", None),
        ("2020级土木3班团支部", "QQ", "土木工程学院 · 三级平台", "498 天", "停更 ≥ 365 天 / 已毕业 / 无学生负责人", "高风险", "待教师核实", None),
        ("文学院书法协会", "抖音", "文学院 · 社团平台", "262 天", "无学生负责人 / 无负责教师", "中风险", "待教师核实", None),
        ("2020级材料2班团支部", "微信公众号", "材料科学与工程学院 · 三级平台", "391 天", "停更 ≥ 365 天 / 已毕业", "高风险", "待校团委确认", "zombie-detail.html"),
        ("机电创客空间", "哔哩哔哩", "机电工程学院 · 二级平台", "165 天", "账号无法访问", "中风险", "学院审核中", None),
        ("湘雅健康说", "小红书", "湘雅医学院 · 社团平台", "从未发布", "最近发布为空", "中风险", "待教师核实", None),
        ("化院科创", "微博", "化学化工学院 · 二级平台", "96 天", "重复备案（与化学化工学院团委同 ID）", "低风险", "学院审核中", None),
        ("法学院辩论队", "抖音", "法学院 · 社团平台", "402 天", "停更 ≥ 365 天", "高风险", "已处置 · 已注销", None),
        ("外国语学院日语角", "QQ", "外国语学院 · 社团平台", "236 天", "组织已撤销", "高风险", "已处置 · 已注销", None),
        ("交通学院青年", "视频号", "交通运输工程学院 · 二级平台", "188 天", "停更 ≥ 180 天", "中风险", "已处置 · 核实正常", None),
    ]
    rows = []
    for n, p, meta, days, rule, lv, node, href in rows_data:
        days_html = f'<b class="c-danger num">{days}</b>' if "天" in days and int(days.split()[0]) >= 180 else f'<b class="num">{days}</b>'
        node_kind = "success" if "已处置" in node else ("danger" if "校团委" in node else "warning")
        if href:
            op = ops(("处置", href))
        elif "已处置" in node:
            op = ops(("档案", "../common/archive-basic.html"))
        else:
            op = ops(("催办", None, f"已向{n}的核实责任人发送催办"), ("档案", "../common/archive-basic.html"))
        rows.append(dict(cells=[acct(n, p, meta), days_html, f'<span class="small sub">{rule}</span>', st(lv), tag(node, node_kind, True), op], href=href))
    tbl = table(["账号", "停更天数", "命中规则", "风险等级", "处置节点", "操作"], rows, id_="zbTable")
    content = f"""
{page_hd('僵尸号排查中心', '系统每日 02:00 按风险规则自动扫描全校在册账号 · 最近扫描 2026-09-30 02:00',
         btn('规则配置', 'settings-rules.html', 'default', 'settings') + btn('立即扫描', None, 'default', 'radar', toast='已完成全校扫描，新增疑似僵尸号 0 个') + btn('批量下发核实', None, 'primary', 'send', toast='已向 21 个待核实账号的负责教师下发核实任务'))}
{alert('<b>处置原则：</b>系统不根据算法直接注销账号。流程为：<b>系统预警 → 教师 / 学生核实 → 学院审核 → 校团委确认处置</b>（确认注销 / 转整改 / 核实正常），每一步留痕。', 'warning')}
<div class="mt16">{scene('七', '第 1 步：系统预警“2021级软件工程1班团支部”停更 412 天。下一步由辅导员王晓琳核实。', '../teacher/review-zombie.html', '辅导员核实（演示）')}</div>
<div class="grid g5 mt16">
  {stat('疑似僵尸号', 47, '占在册账号 4.8%', 'ghost', 'red')}
  {stat('待核实', 21, '教师 / 学生核实中', 'search', 'orange')}
  {stat('学院审核中', 9, '已提交核实结果', 'hierarchy', 'orange')}
  {stat('待校团委确认', 5, '学院建议注销 4 · 整改 1', 'building', '', 'zombie-detail.html')}
  {stat('已处置', 12, '注销 8 · 整改 1 · 正常 3', 'check-circle', 'green')}
</div>
<div class="mt16">{card('命中规则', f'<div class="grid" style="grid-template-columns:repeat(7,minmax(0,1fr))">{rules}</div>', btn('规则配置', 'settings-rules.html', 'text', 'settings', 'sm'))}</div>
<div class="mt16">{card('疑似僵尸号清单', tbl + pager(47, 5), seg([('全部', 'a'), ('高风险', 'h'), ('中风险', 'm'), ('低风险', 'l')]))}</div>"""
    page("zombie.html", "zombie", "僵尸号排查中心", [("风险治理", "zombie.html"), ("僵尸号排查", None)], content)


def zombie_detail():
    a = ACCOUNTS["zombie"]
    no = FLOWS["zombie"]["no"]
    trig = "".join(f'<div class="hit-chip"><span class="rule-ic {c}">{icon(ic)}</span><div><div class="bold fs13">{n}</div><div class="small muted">{d}</div></div></div>' for n, d, ic, c in [
        ("停更 ≥ 180 天", "已停更 412 天，最近发布 2025-08-14", "clock", ""),
        ("组织已毕业", "2021级软件工程1班团支部 2025-06 毕业", "flag", ""),
        ("无学生负责人", "原负责人已毕业离校", "user", "orange")])
    choices = f"""
<div class="choices g3" data-single=".zd-p">
  <div class="choice on" data-choice="#zdp1"><span class="ck"></span><div><div class="bold">确认注销</div><div class="small muted">学院建议 · 状态转为已注销</div></div></div>
  <div class="choice" data-choice="#zdp2"><span class="ck"></span><div><div class="bold">转整改</div><div class="small muted">仍需运营，下发整改任务</div></div></div>
  <div class="choice" data-choice="#zdp3"><span class="ck"></span><div><div class="bold">核实正常</div><div class="small muted">解除预警，恢复正常</div></div></div>
</div>
<div class="mt12 zd-p" id="zdp1">{alert('确认注销后：运行状态、备案状态转为“已注销”，年审记为“本年度注销”；档案与全部历史记录<b>永久保留</b>，不做删除。', 'danger')}</div>
<div class="mt12 zd-p hidden" id="zdp2">{alert('转整改：将跳转至创建整改任务，由学院指定新的学生负责人并限期恢复运营。', 'warning')}</div>
<div class="mt12 zd-p hidden" id="zdp3">{alert('核实正常：解除本次预警，180 天内同一规则不再重复预警。', 'success')}</div>"""
    left = f"""
{acct_head(a, st('疑似僵尸号') + st('高风险') + st(a['run']), f'<div class="small muted">预警编号</div><div class="bold num">{no}</div><div class="small muted mt4">粉丝 {a["fans"]}</div>')}
<div class="grid g3 mt16">
  {stat('停更天数', f'<span class="c-danger">{a["idle_days"]}</span>', '阈值 180 天', 'clock', 'red')}
  {stat('最近发布', '<span class="fs18">' + a['last_post'] + '</span>', '《毕业季 · 再见 2101》', 'calendar', 'gray')}
  {stat('负责教师', '<span class="fs18">' + a['teacher'] + '</span>', '2021级辅导员', 'user')}
</div>
<div class="mt16">{card('触发规则', f'<div class="grid g3">{trig}</div>', tag('命中 3 条', 'danger'))}</div>
<div class="mt16">{card('辅导员核实材料', kv([('核实人', '王晓琳（2021级辅导员）'), ('核实时间', '2026-09-22 15:30'), ('核实结论', tag('建议注销', 'danger')), ('核实说明', '该团支部已于 2025 年 6 月毕业，无学生继续运营。已联系原团支书确认，账号密码已交回学院团委。', True)], 3) + '<div class="upload-list">' + fchip('团支部毕业证明.pdf') + fchip('2021级软件工程1班毕业名单.xlsx') + fchip('原团支书确认说明.png', 'image') + '</div>')}</div>
<div class="mt16">{card('校团委处置决定', choices + '<div class="mt16">' + field('处置意见', textarea('请填写处置意见', '账号状态转为已注销，数据永久保留。', req=True, maxlen=200, rows=3), req=True) + '</div>')}</div>"""
    right = f"""
<div class="sticky col gap16">
  {card('处置链路', flow_tl('zombie', 3, '校团委确认 · 待您处置', '陈静（学校管理员） · 学院 2026-09-29 报送'), tag('预警 → 核实 → 审核 → 处置', 'primary'))}
  {card('账号档案', kv([('所属组织', a['org']), ('存续状态', tag('已毕业', 'warning')), ('备案状态', st(a['filing'])), ('年审状态', st(a['annual']))], 2) + '<div class="mt8"><a class="link small" href="../common/archive-basic.html">查看完整档案</a></div>')}
</div>"""
    content = f"""<div data-form>
{page_hd('僵尸号处置', f'{no} · 系统预警 → 辅导员核实 → 学院审核 → 校团委确认', back_btn('zombie.html'))}
{scene('七', '第 4 步：校团委确认注销。确认后可在档案“注销信息”中查看注销记录，数据永久保留。', '../common/archive-cancel.html', '下一步：查看注销信息')}
<div class="split mt16"><div>{left}</div>{right}</div>
<div class="actbar"><div class="grow">{icon('info')} 系统不直接注销，校团委确认后生效并记录日志</div>
  {btn('退回学院重核', '../common/modal-return.html', 'default', 'undo')}
  {go('核实正常', 'zombie.html', 'default', 'check-circle', toast='已解除预警，账号恢复正常')}
  {btn('转整改', 'rectify-create.html', 'warning', 'wrench')}
  {submit_btn('确认注销', '../common/archive-cancel.html', 'danger-solid', 'ban', toast='已确认注销，账号状态转为已注销，数据永久保留')}
</div></div>"""
    page("zombie-detail.html", "zombie", "僵尸号处置", [("风险治理", "zombie.html"), ("僵尸号排查", "zombie.html"), ("僵尸号处置", None)], content)


def anomalies():
    rows_data = [
        ("dup", "同平台ID重复", "化院科创", "微博", "化学化工学院", "平台ID 6630218871 与“化学化工学院团委”（微博）重复", "6630218871"),
        ("org", "所属组织为空", "湘雅健康说", "小红书", "湘雅医学院", "所属团学组织未填写（历史导入数据）", "—"),
        ("org", "所属组织为空", "资安青年", "视频号", "资源与安全工程学院", "原组织“资安学生科协”已合并，未重新关联", "—"),
        ("org", "所属组织为空", "物理学院之声", "微博", "物理学院", "所属团学组织未填写", "—"),
        ("teacher", "负责教师为空", "文学院书法协会", "抖音", "文学院", "原指导教师 2026-07 调离，未重新指定", "—"),
        ("teacher", "负责教师为空", "物理学院天文协会", "QQ", "物理学院", "负责教师未填写", "—"),
        ("student", "学生负责人为空", "2020级土木3班团支部", "QQ", "土木工程学院", "原负责人已毕业，未交接", "—（已毕业）"),
        ("student", "学生负责人为空", "2021级软件工程1班团支部", "微信公众号", "计算机学院", "原负责人已毕业，未交接", "—（已毕业）"),
        ("student", "学生负责人为空", "文学院书法协会", "抖音", "文学院", "学生负责人未填写", "—"),
        ("multi", "同一账号归属多个学院", "中南能源社", "微信公众号", "能源科学与工程学院 / 资源与安全工程学院", "同一平台ID在两个学院均有备案记录", "csu_energy"),
        ("missing", "必填缺失", "公管志愿服务队", "抖音", "公共管理学院", "缺少：开通时间、认证主体", "—"),
    ]
    kinds = {"dup": "danger", "org": "warning", "teacher": "warning", "student": "warning", "multi": "danger", "missing": "primary"}
    rows = [dict(cells=[tag(t, kinds[c]), acct(n, p), col, f'<span class="small sub">{d}</span>', f'<span class="num small">{raw}</span>',
                        ops(("下发学院补全", None, f"已下发{col.split(' / ')[0]}补全：{n}"), ("查看档案", "../common/archive-basic.html"))], cat=c)
            for c, t, n, p, col, d, raw in rows_data]
    tbl = table(["异常类型", "账号", "学院", "异常说明", "原始值", "操作"], rows, id_="anoTable")
    tabs = seg([("全部 18", "all"), ("同平台ID重复 1", "dup"), ("所属组织为空 6", "org"), ("负责教师为空 4", "teacher"),
                ("学生负责人为空 5", "student"), ("同一账号归属多个学院 1", "multi"), ("必填缺失 1", "missing")], target="#anoTable")
    content = f"""
{page_hd('数据异常清单', '系统每日自动校验账号档案完整性与唯一性 · 最近校验 2026-09-30 02:00',
         btn('重新校验', None, 'default', 'refresh', toast='校验完成，共发现 18 条数据异常') + btn('一键下发学院', None, 'default', 'send', toast='已将 18 条异常按学院下发补全') + btn('导出异常清单', 'export.html', 'primary', 'download'))}
<div class="grid g4 mb16">
  {stat('异常总数', 18, '涉及 11 个学院', 'alert', 'orange')}
  {stat('唯一性异常', 2, 'ID 重复 1 · 多学院归属 1', 'copy', 'red')}
  {stat('责任人缺失', 9, '教师 4 · 学生 5', 'user', 'orange')}
  {stat('本月已修复', 26, '学院补全后自动消除', 'check-circle', 'green')}
</div>
<div class="card card-bd">
  <div class="toolbar">{tabs}</div>
  {tbl}
  {pager(18, 2)}
</div>"""
    page("anomalies.html", "anomalies", "数据异常清单", [("风险治理", "zombie.html"), ("数据异常", None)], content)


def rectify():
    rows_data = [
        ("ZG20260920001", "计院青年志愿者", "小红书", "计算机学院", "未建立信息发布审查机制", "学院", "第 2 轮", "整改通过", "2026-10-20"),
        ("ZG20260915003", "机电创客空间", "哔哩哔哩", "机电工程学院", "账号无法正常访问", "校级", "第 1 轮", "整改复核中", "2026-10-15"),
        ("ZG20260918002", "文学院书法协会", "抖音", "文学院", "负责人为空", "学院", "第 1 轮", "待整改", "2026-10-18"),
        ("ZG20260921004", "湘雅医声", "抖音", "湘雅医学院", "内容审核记录缺失", "学院", "第 1 轮", "待整改", "2026-10-21"),
        ("ZG20260922006", "法学院青年", "微信公众号", "法学院", "账号安全：未绑定单位管理员", "校级", "第 1 轮", "整改复核中", "2026-10-12"),
        ("ZG20260923007", "土木青年", "微博", "土木工程学院", "发布内容未执行三审", "学院", "第 2 轮", "继续整改", "2026-10-08"),
        ("ZG20260925008", "数统青年", "QQ", "数学与统计学院", "年审佐证材料不全", "学院", "第 1 轮", "待整改", "2026-10-25"),
        ("ZG20260910001", "商学院学生会", "微信公众号", "商学院", "名称与备案不一致", "校级", "第 1 轮", "整改通过", "2026-09-30"),
        ("ZG20260912005", "外院之声", "微博", "外国语学院", "长期未更新", "学院", "第 1 轮", "整改通过", "2026-10-05"),
    ]
    rows = []
    for no, n, p, col, q, lv, rnd, stv, dl in rows_data:
        dl_html = f'<span class="c-danger">{dl}</span>' if dl <= "2026-10-08" and stv != "整改通过" else dl
        rows.append(dict(cells=[f'<span class="num bold">{no}</span>', acct(n, p, col), f'<span class="small sub">{q}</span>', tag(lv, "primary" if lv == "校级" else "muted"),
                                rnd, st(stv), dl_html, ops(("详情", "rectify-detail.html"), ("催办", None, f"已向{n}负责人发送整改催办"))], href="rectify-detail.html"))
    tbl = table(["整改编号", "账号", "整改问题", "审核层级", "轮次", "状态", "截止时间", "操作"], rows)
    content = f"""
{page_hd('整改管理', '年审、僵尸号核实与日常巡查发现的问题，统一以整改任务跟踪闭环',
         btn('导出整改台账', 'export.html', 'default', 'download') + btn('创建整改任务', 'rectify-create.html', 'primary', 'plus'))}
<div class="grid g5 mb16">
  {stat('整改中', S['rectifying'], '3 项临近截止', 'wrench', 'orange')}
  {stat('待整改', 11, '学生尚未提交', 'inbox', 'orange')}
  {stat('整改复核中', 7, '校级 2 · 学院 5', 'search')}
  {stat('继续整改', 5, '进入第 2 轮及以上', 'undo', 'red')}
  {stat('本年度已通过', 38, '平均 1.4 轮', 'check-circle', 'green')}
</div>
{card('整改任务', tbl + pager(61, 4), seg([('全部', 'a'), ('校级审核', 'b'), ('学院审核', 'c'), ('临近截止', 'd')]))}"""
    page("rectify.html", "rectify", "整改管理", [("风险治理", "zombie.html"), ("整改管理", None)], content)


def rectify_create():
    problems = ["未建立信息发布审查机制", "未执行三审三校", "账号无法正常访问", "长期未更新", "负责人为空", "名称与备案不一致", "账号安全隐患", "年审材料不全"]
    ph = "".join(f'<button type="button" class="chip{" on" if i == 0 else ""}" data-choice>{p}</button>' for i, p in enumerate(problems))
    content = f"""<div data-form>
{page_hd('创建整改任务', '校级整改任务由校团委审核；学院级由学院管理员审核', back_btn('rectify.html'))}
<div class="grid" style="grid-template-columns:minmax(0,1fr) 340px;align-items:start">
<div class="col gap16">
  {card('整改对象', '<div class="form-grid">' + field('整改账号', sel(['计院青年志愿者（小红书 · 计算机学院）', '机电创客空间（哔哩哔哩 · 机电工程学院）', '2021级软件工程1班团支部（微信公众号 · 计算机学院）', '文学院书法协会（抖音 · 文学院）'], '计院青年志愿者（小红书 · 计算机学院）', req=True), req=True) + field('整改来源', sel(['年度年审', '僵尸号核实', '日常巡查', '数据异常'], '年度年审')) + '</div>')}
  {card('整改内容', '<div class="field-label mb8">整改问题（可多选）</div><div class="chips mb16">' + ph + '</div><div class="form-grid c1">' + field('问题说明', textarea('请描述具体问题', '未建立信息发布审查机制；近 3 个月内容未执行“先审后发”。', req=True, maxlen=300, rows=3), req=True) + field('整改要求', textarea('请填写整改要求', '10 月 20 日前提交审查制度文件及近 3 个月审核记录。', req=True, maxlen=300, rows=3), req=True) + '</div>')}
  {card('附件', upload('上传整改通知、问题截图等附件', '支持 pdf / jpg / png / docx，单个不超过 20MB', ['年审问题截图.png']))}
</div>
<div class="sticky col gap16">
  {card('责任人与时限', '<div class="form-grid c1">' + field('整改责任人（学生）', sel(['何雨桐（8209230509）', '李明（8209230117）', '孙悦（8209240315）'], '何雨桐（8209230509）', req=True), req=True) + field('整改责任人（教师）', sel(['王晓琳（T20180427）', '刘洋（T20200611）'], '王晓琳（T20180427）', req=True), req=True) + field('截止时间', inp('', FLOWS['rectify']['deadline'], req=True, typ='date'), req=True) + '<div class="field"><label><span class="req">*</span>审核层级</label>' + radios('lv', ['学院审核', '校级审核'], '学院审核', req=True) + '<div class="hint">校级审核：整改材料经学院初审后报校团委复核</div></div></div>')}
  {card('通知方式', cb('站内信', True) + '<div class="mt8">' + cb('ITS 消息', True) + '</div><div class="hint mt8">截止前 3 天通过站内信与 ITS 消息提醒</div>')}
  <div class="flex gap8">{btn('取消', 'rectify.html', 'default')}{submit_btn('下发整改任务', 'rectify.html', 'primary', 'send', toast='整改任务已下发，已通知学生与指导教师')}</div>
</div>
</div></div>"""
    page("rectify-create.html", "rectify", "创建整改任务", [("风险治理", "zombie.html"), ("整改管理", "rectify.html"), ("创建整改任务", None)], content)


def rectify_detail():
    a = dict(name="机电创客空间", platform="哔哩哔哩", pid="402218876", org="机电学院大学生创新协会", level="二级平台", opened="2020-03-16")
    rounds = timeline([
        ("done", "校团委下发整改任务", "陈静（学校管理员） · 2026-09-15 10:20", "日常巡查发现账号主页无法访问（提示“账号异常”），请于 10 月 15 日前恢复访问并说明原因。"),
        ("done", "学院转发并指定责任人", "罗志强（机电学院团委） · 2026-09-15 16:40", "请邓子豪同学限期处理。"),
        ("done", "第 1 次提交整改材料", "邓子豪（学生负责人） · 2026-09-27 21:30", "已完成实名申诉并恢复账号，补发 3 条内容，附平台解封通知。"),
        ("done", "学院初审通过", "罗志强（机电学院团委） · 2026-09-28 09:15", "账号已恢复访问，报校团委复核。"),
        ("now", "校团委复核 · 待您审核", "陈静（学校管理员）", ""),
    ])
    choices = f"""
<div class="choices g3" data-single=".rd-p">
  <div class="choice on" data-choice="#rdp1"><span class="ck"></span><div><div class="bold">整改通过</div><div class="small muted">关闭任务，恢复正常运行</div></div></div>
  <div class="choice" data-choice="#rdp2"><span class="ck"></span><div><div class="bold">继续整改</div><div class="small muted">进入第 2 轮，须填写意见</div></div></div>
  <div class="choice" data-choice="#rdp3"><span class="ck"></span><div><div class="bold">转注销</div><div class="small muted">无法恢复运营，发起注销</div></div></div>
</div>
<div class="mt12 rd-p" id="rdp1">{alert('整改通过后：运行状态恢复为“正常运行”，年审状态由“待整改”恢复流转。', 'success')}</div>
<div class="mt12 rd-p hidden" id="rdp2">{alert('继续整改：须在下方填写具体意见，系统将生成第 2 轮整改并重新计时。', 'warning')}</div>
<div class="mt12 rd-p hidden" id="rdp3">{alert('转注销：将跳转至注销审核，账号数据永久保留。', 'danger')}</div>"""
    content = f"""<div data-form>
{page_hd('整改审核 · 校级', 'ZG20260915003 · 整改问题：账号无法正常访问 · 截止 2026-10-15', back_btn('rectify.html'))}
{acct_head(a, st('整改复核中') + tag('校级整改', 'primary') + tag('第 1 轮', 'muted'), '<div class="small muted">学院</div><div class="bold">机电工程学院</div>')}
<div class="split mt16">
<div class="col gap16">
  {card('整改要求', kv([('整改问题', tag('账号无法正常访问', 'danger')), ('来源', '日常巡查'), ('截止时间', '2026-10-15'), ('整改要求', '恢复账号正常访问，说明异常原因，并补充近期发布内容。', True)], 3))}
  {card('提交的整改材料', kv([('整改说明', '账号因长期未登录被平台风控冻结，已通过学院公函完成实名申诉，9 月 26 日恢复访问，并补发《创客周报》3 期。', True), ('整改结果', tag('已恢复访问', 'success')), ('提交时间', '2026-09-27 21:30'), ('提交人', '邓子豪（学生负责人）')], 3) + '<div class="grid g3 mt16"><div class="shot"><img src="' + PHOTOS['screenshot'] + '" alt="恢复后主页截图"><span>恢复后主页截图</span></div><div class="shot"><img src="' + PHOTOS['students'] + '" alt="补发内容截图"><span>补发内容截图</span></div><div class="shot"><img src="' + PHOTOS['meeting'] + '" alt="平台解封通知"><span>平台解封通知</span></div></div><div class="upload-list">' + fchip('学院申诉公函.pdf') + fchip('账号异常原因说明.docx') + '</div>')}
  {card('审核结果', choices + '<div class="mt16">' + field('审核意见', textarea('选择“继续整改”时必须填写具体意见', '', req=True, maxlen=300, rows=3), req=True) + '</div>')}
</div>
<div class="sticky col gap16">
  {card('整改轮次记录', rounds, tag('第 1 轮', 'primary'))}
  {card('关联记录', '<div class="col gap8"><a class="link" href="../common/archive-rectify.html">账号档案 · 整改记录</a><a class="link" href="zombie.html">僵尸号排查（规则：账号无法访问）</a></div>')}
</div>
</div>
<div class="actbar"><div class="grow">{icon('info')} 继续整改须填写意见；转注销将进入注销审核流程</div>
  {btn('转注销', 'approval-cancel.html', 'danger', 'ban')}
  {submit_btn('继续整改', 'rectify.html', 'warning', 'undo', toast='已判定继续整改，第 2 轮整改任务已下发')}
  {go('整改通过', 'rectify.html', 'primary', 'check', toast='整改通过，账号恢复正常运行')}
</div></div>"""
    page("rectify-detail.html", "rectify", "整改审核", [("风险治理", "zombie.html"), ("整改管理", "rectify.html"), ("整改审核", None)], content)


# ================================================================ 数据中心
IMPORT_STEPS = ["下载模板", "上传文件", "字段映射", "校验入库"]


def import_page():
    tpls = "".join(
        f'<div class="tpl"><span class="tpl-ic">XLS</span><div class="grow"><div class="bold fs13">{n}</div><div class="small muted">{d}</div></div>'
        f'{btn("下载", None, "light", "download", "sm", toast="已下载《" + n + "》")}</div>'
        for n, d in [("一级平台导入模板", "校级团学组织账号 · 18 个字段"), ("二级平台导入模板", "院级团学组织账号 · 22 个字段"),
                     ("三级平台导入模板", "班级团支部账号 · 20 个字段"), ("社团平台导入模板", "社团组织账号 · 21 个字段")])
    sys_fields = ["账号名称", "平台类型", "平台ID", "所属学院", "团学组织", "组织类别", "平台层级", "开通时间", "管理教师工号", "学生负责人学号", "更新频率", "（不导入）"]
    mapping = [("A 列 · 公众号名称", "账号名称", "中南计院团委"), ("B 列 · 平台", "平台类型", "微信公众号"), ("C 列 · 账号ID / 微信号", "平台ID", "csu_cs_tw"),
               ("D 列 · 学院", "所属学院", "计算机学院"), ("E 列 · 主办单位", "团学组织", "计算机学院团委"), ("F 列 · 类别", "组织类别", "院级学生组织"),
               ("G 列 · 级别", "平台层级", "二级平台"), ("H 列 · 开通日期", "开通时间", "2014-09-01"), ("I 列 · 指导老师工号", "管理教师工号", "T20180427"),
               ("J 列 · 负责学生学号", "学生负责人学号", "8209230117"), ("K 列 · 备注", "（不导入）", "—")]
    rows = [[f'<b>{c}</b>', f'<span class="node-arrow">{icon("arrow-right")}</span>', sel(sys_fields, f, ph=""), f'<span class="small sub">{v}</span>',
             tag("自动匹配", "success") if f != "（不导入）" else tag("忽略", "muted")] for c, f, v in mapping]
    content = f"""
{page_hd('Excel 数据导入', '从全校账号库进入。批量导入历史账号数据，导入后由各学院补充确认', btn('导入记录', 'logs.html', 'default', 'history'))}
{alert('<b>初始化说明：</b>以 <b>2025 年度账号数据</b>作为初始化底库（972 个平台），导入后下发各学院补充确认，确认后的数据作为 2026 年度年审的继承基础。', 'info')}
<div class="card card-bd mt16">{steps(IMPORT_STEPS, 2)}</div>
<div class="grid mt16" style="grid-template-columns:420px minmax(0,1fr);align-items:start">
  <div class="col gap16">
    {card('① 下载模板', f'<div class="col gap8">{tpls}</div><div class="hint mt8">模板字段与数据字典一致，平台类型、层级等请按下拉值填写</div>')}
    {card('② 上传文件', upload('点击或拖拽 Excel 文件到此处', '支持 .xlsx / .xls，单个不超过 20MB，最多 5000 行', ['2025年度团学新媒体平台底库.xlsx']) + '<div class="mt12">' + kv([('工作表', 'Sheet1 · 二级平台'), ('数据行数', '972 行'), ('表头行', '第 1 行')], 3) + '</div>')}
  </div>
  {card('③ 字段映射', table(['Excel 列', '', '系统字段', '示例值', '匹配'], rows) + '<div class="flex between mt16"><span class="small muted">已自动匹配 10 / 11 列，必填字段已全部映射</span><div class="flex gap8">' + btn('保存映射方案', None, 'default', 'file', 'sm', toast='映射方案已保存为“2025 年度底库”') + go('开始校验', 'import-result.html', 'primary', 'check', toast='校验完成：成功 958 条，失败 9 条，疑似重复 5 条') + '</div></div>', tag('智能匹配', 'primary'))}
</div>"""
    page("import.html", "accounts", "Excel 数据导入", [("全校账号库", "accounts.html"), ("数据导入", None)], content)


def import_result():
    errs = [
        (18, "平台类型不在数据字典中", "公众号（应为“微信公众号”）", "按字典值修正"),
        (57, "所属学院不存在", "计科学院", "修正为“计算机学院”"),
        (103, "平台ID为空", "—", "补充平台ID"),
        (211, "开通时间格式错误", "2019.9", "改为 yyyy-mm-dd"),
        (268, "管理教师工号不存在", "T2019041", "核对工号"),
        (344, "学生负责人学号格式错误", "820923011", "学号应为 10 位"),
        (512, "平台层级为空", "—", "补充层级"),
        (689, "组织类别不在数据字典中", "班级", "改为“班级团支部”"),
        (907, "账号名称超长", "中南大学计算机学院……（62 字）", "不超过 30 字"),
    ]
    dups = [
        (46, "中南计院团委", "微信公众号 · csu_cs_tw", "已存在同平台同 ID 账号", "跳过"),
        (132, "计院科协", "哔哩哔哩 · 386620915", "已存在同平台同 ID 账号", "跳过"),
        (377, "湘雅医声", "抖音 · xyyisheng", "已存在同平台同 ID 账号", "跳过"),
        (590, "麓山文学社", "微信公众号 · lushan_wx", "与“麓山文苑”名称相似", "学院确认"),
        (802, "机电青年说", "视频号 · sph_jd_youth", "与“机电青年”名称相似", "学院确认"),
    ]
    err_tbl = table(["行号", "错误原因", "原始值", "处理建议"], [[f'<span class="num">第 {r} 行</span>', f'<span class="c-danger">{e}</span>', f'<span class="small">{v}</span>', f'<span class="small sub">{s}</span>'] for r, e, v, s in errs])
    dup_tbl = table(["行号", "账号名称", "平台 · ID", "重复原因", "处理方式"], [[f'<span class="num">第 {r} 行</span>', n, f'<span class="small">{p}</span>', f'<span class="small sub">{e}</span>', tag(h, "muted" if h == "跳过" else "warning")] for r, n, p, e, h in dups])
    content = f"""
{page_hd('导入校验结果', '文件：2025年度团学新媒体平台底库.xlsx · 共 972 行 · 校验于 2026-09-30 16:30', back_btn('import.html'))}
<div class="card card-bd">{steps(IMPORT_STEPS, 3)}</div>
<div class="grid g4 mt16">
  {stat('校验成功', 958, '可直接入库', 'check-circle', 'green')}
  {stat('校验失败', 9, '需修正后重新上传', 'x-circle', 'red')}
  {stat('疑似重复', 5, '3 条跳过 · 2 条学院确认', 'copy', 'orange')}
  {stat('涉及学院', 35, '入库后分别下发确认', 'building')}
</div>
<div class="grid g2 mt16" style="align-items:start">
  {card('失败明细', err_tbl, btn('下载错误报告', None, 'light', 'download', 'sm', toast='已下载《导入错误报告.xlsx》（9 条）'))}
  {card('疑似重复明细', dup_tbl, tag('按“同平台同 ID”与名称相似度判断', 'muted'))}
</div>
<div class="actbar"><div class="grow">{icon('info')} 确认入库后，958 条成功数据将按学院下发，由学院管理员补充确认负责人与组织归属</div>
  {btn('重新上传', 'import.html', 'default', 'upload')}
  {go('确认入库并下发学院确认', '../college/import-confirm.html', 'primary', 'send', toast='已入库 958 条，并下发 35 个学院确认')}
</div>"""
    page("import-result.html", "accounts", "导入校验结果", [("全校账号库", "accounts.html"), ("数据导入", "import.html"), ("校验结果", None)], content)


LEDGERS = [
    ("全校总表", "全校全部在册账号及四套状态", 986, "database", ""),
    ("学院明细表", "按学院分表输出账号明细", 35, "building", ""),
    ("一级平台汇总", "校级团学组织账号", S["level1"], "layers", ""),
    ("二级平台汇总", "院级团学组织账号", S["level2"], "layers", ""),
    ("三级平台汇总", "班级团支部账号", S["level3"], "layers", ""),
    ("社团平台汇总", "社团组织账号", S["club"], "layers", ""),
    ("疑似僵尸号清单", "命中规则、停更天数与处置节点", S["zombie"], "ghost", "red"),
    ("注销清单", "本年度注销账号及原因", S["cancel"], "ban", "red"),
    ("新建清单", "本年度新建备案账号", S["new"], "file-add", "green"),
    ("年审不通过清单", "年审不通过账号及意见", 11, "x-circle", "orange"),
    ("各学院年审完成情况", "各学院各节点完成率", 35, "chart", "green"),
    ("教师负责账号清单", "教师与负责账号对应关系", 312, "user", "orange"),
    ("学生运营负责人清单", "学生负责人及联系方式（脱敏）", 1124, "users", "orange"),
]


def export():
    cards = "".join(
        f'<div class="card ledger"><div class="flex gap12"><span class="ledger-ic {c}">{icon(ic)}</span><div class="grow"><div class="bold">{n}</div>'
        f'<div class="small muted">{d}</div></div></div><div class="flex between"><span class="small muted">记录数 <b class="num fs16" style="color:var(--c-text)">{v}</b></span>'
        f'{go("导出 Excel", "export-records.html", "light", "download", toast="已创建导出任务：" + n, size="sm")}</div></div>'
        for n, d, v, ic, c in LEDGERS)
    fields = [field("学院", sel(["全部学院"] + COLLEGES, "全部学院", ph="")), field("年度", sel(["2026", "2025", "2024"], "2026", ph="")),
              field("平台类型", sel(["全部类型"] + PLATFORM_TYPES, "全部类型", ph="")), field("文件格式", sel(["Excel（.xlsx）", "CSV（.csv）"], "Excel（.xlsx）", ph="")),
              field("状态范围", sel(["含已注销", "仅在册"], "仅在册", ph="")), field("敏感字段", sel(["脱敏导出", "完整导出（需审批）"], "脱敏导出", ph="")),
              field("最近发布区间", inp("", "2026-01-01", typ="date"))]
    content = f"""
{page_hd('数据导出中心', '13 类台账按条件导出，所有导出操作均记录日志', btn('导出记录', 'export-records.html', 'default', 'history'))}
{filter_bar(fields)}
{alert('导出文件包含个人信息时默认脱敏（手机号、学号中间位隐藏）；完整导出需填写用途并经校团委负责人审批。', 'warning')}
<div class="grid g4 mt16">{cards}</div>"""
    page("export.html", "export", "数据导出中心", [("数据中心", "export.html"), ("数据导出", None)], content)


def export_records():
    rows_data = [
        ("全校总表_20260930.xlsx", "全部学院 · 2026 · 仅在册", 986, "陈静", "2026-09-30 16:35", "生成中"),
        ("疑似僵尸号清单_20260930.xlsx", "全部学院 · 2026", 47, "陈静", "2026-09-30 09:12", "已完成"),
        ("各学院年审完成情况_20260929.xlsx", "全部学院 · 2026", 35, "陈静", "2026-09-29 18:40", "已完成"),
        ("全校总表_20260929.xlsx", "全部学院 · 2026 · 仅在册", 986, "陈静", "2026-09-29 18:31", "已完成"),
        ("计算机学院明细_20260929.xlsx", "计算机学院 · 2026", 36, "周建华", "2026-09-29 11:05", "已完成"),
        ("注销清单_20260928.xlsx", "全部学院 · 2026", 41, "陈静", "2026-09-28 15:22", "已完成"),
        ("新建清单_20260926.xlsx", "全部学院 · 2026", 63, "陈静", "2026-09-26 10:02", "已完成"),
        ("学生运营负责人清单_20260925.xlsx", "全部学院 · 脱敏", 1124, "陈静", "2026-09-25 17:48", "已完成"),
        ("教师负责账号清单_20260920.xlsx", "商学院 · 2026", 28, "杨帆", "2026-09-20 09:30", "已完成"),
        ("年审不通过清单_2025.xlsx", "全部学院 · 2025", 11, "陈静", "2025-12-22 14:10", "已过期"),
    ]
    rows = []
    for f, cond, n, who, t, s in rows_data:
        s_tag = {"生成中": tag("生成中", "primary", True), "已完成": tag("已完成", "success", True), "已过期": tag("已过期", "muted", True)}[s]
        if s == "已完成":
            op = ops(("下载", None, f"开始下载：{f}"), ("日志", "logs.html"))
        elif s == "生成中":
            op = ops(("刷新", None, "文件生成中，预计 10 秒后完成"),)
        else:
            op = ops(("重新生成", None, f"已重新创建导出任务：{f}"),)
        rows.append([f'<div class="flex gap8"><span class="tpl-ic" style="width:30px;height:30px;font-size:10px">XLS</span><b class="fs13">{f}</b></div>',
                     f'<span class="small sub">{cond}</span>', f'<span class="num">{n}</span>', person(who), f'<span class="small num">{t}</span>', s_tag, op])
    content = f"""
{page_hd('导出记录', '导出文件保留 30 天，过期后可重新生成', back_btn('export.html', '返回导出中心'))}
{alert('每一次导出均记录操作人、身份、导出条件、记录数与时间，并同步写入<a class="link" href="logs.html">操作日志</a>（操作类型：数据导出），用于数据安全审计。', 'info')}
<div class="mt16">{card('导出任务', table(['文件名', '导出条件', '记录数', '操作人', '导出时间', '状态', '操作'], rows) + pager(46, 5))}</div>"""
    page("export-records.html", "export", "导出记录", [("数据中心", "export.html"), ("数据导出", "export.html"), ("导出记录", None)], content)


def filing_form():
    a = ACCOUNTS["new"]
    st_ = FLOWS["new"]["steps"]
    t_date, c_date, s_date = st_[3][0][:10], st_[4][0][:10], st_[5][0][:10]
    t_op, c_op, s_op = st_[3][3], st_[4][3], st_[5][3]
    intro = ("计算机学院团委新媒体中心主办，面向学院全体团员青年，以思想引领、学业发展、科创实践、青春风采为定位，"
             "设“计院青年说”“科创前沿”“学业加油站”“青春印记”四个栏目，每周更新不少于 2 次。")
    seal = f'<div class="seal"><span>共青团中南大学</span>{icon("star")}<span>委员会</span></div>'
    doc = f"""
<div class="doc-wrap"><div class="a4">
  <h1>中南大学团学组织新媒体公众平台备案表</h1>
  <div class="doc-no"><span>备案编号：{FLOWS['new']['no']}</span><span>填表日期：2026-09-24</span></div>
  <table class="ftable">
    <tr><td class="k">平台名称</td><td>{a['name']}</td><td class="k">平台类型</td><td>{a['platform']}</td></tr>
    <tr><td class="k">平台 ID</td><td>{a['pid']}</td><td class="k">开通时间</td><td>{a['opened']}</td></tr>
    <tr><td class="k">所属学院</td><td>计算机学院</td><td class="k">主办组织</td><td>{a['org']}</td></tr>
    <tr><td class="k">组织类别</td><td>{a['org_type']}</td><td class="k">平台层级</td><td>{a['level']}</td></tr>
    <tr><td class="k">认证主体</td><td>中南大学</td><td class="k">更新频率</td><td>每周更新（≥1次/周）</td></tr>
    <tr><td class="k">平台介绍</td><td colspan="3">{intro}</td></tr>
    <tr><td class="k">平台信息确认</td><td colspan="3">{'<br>'.join('（%s）%s 是。%s' % (m['no'], m['title'], m['body']) for m in MECHANISMS)}</td></tr>
    <tr><td class="k">第一责任人</td><td>张卫东（党委副书记）</td><td class="k">联系电话</td><td>{PEOPLE['张卫东']['phone']}</td></tr>
    <tr><td class="k">管理教师</td><td>王晓琳（宣传工作辅导员）</td><td class="k">联系电话</td><td>{PEOPLE['王晓琳']['phone']}</td></tr>
    <tr><td class="k">学生负责人</td><td>李明（{PEOPLE['李明']['no']}）</td><td class="k">联系电话</td><td>{PEOPLE['李明']['phone']}</td></tr>
    <tr><td class="k">指导教师<br>审核意见</td><td colspan="3" class="op">{t_op}<div class="sign">签字：王晓琳<br>{t_date}</div></td></tr>
    <tr><td class="k">学院团委<br>审核意见</td><td colspan="3" class="op">{c_op}<div class="sign">签字：周建华（计算机学院团委）<br>{c_date}</div></td></tr>
    <tr><td class="k">校团委<br>审核意见</td><td colspan="3" class="op">{s_op}{seal}<div class="sign">签字：陈静（校团委宣传部）<br>{s_date}</div></td></tr>
  </table>
  <div class="doc-foot">说明：1. 本表由系统根据审核通过的备案申请自动生成，内容与账号档案一致；2. 平台信息发生变化须通过系统提交变更申请；3. 本表一式两份，学院团委、校团委各存一份。</div>
</div></div>"""
    side = f"""
<div class="sticky col gap16">
  {card('备案结果', result('ok', '已准予备案', '档案已建立 · 已备案', '', '<div class="small muted mt8">生成时间 2026-09-30 10:05</div>'))}
  {card('导出与打印', '<div class="col gap8">' + btn('导出 Word', None, 'default', 'file', toast='已导出《备案表-中南计算机青年.docx》') + btn('导出 PDF', None, 'default', 'download', toast='已导出《备案表-中南计算机青年.pdf》') + btn('打印', None, 'default', 'print', toast='已发送至打印队列') + '</div>')}
  {card('后续', '<div class="col gap8">' + btn('查看账号档案', '../common/archive-basic.html', 'ghost', 'archive') + btn('学生端查看结果', '../../app/student/application-approved.html', 'primary', 'smartphone') + '</div><div class="small muted mt8">系统已通过站内信通知李明与王晓琳</div>')}
</div>"""
    content = f"""
{page_hd('备案表生成预览', f'{FLOWS["new"]["no"]} · 中南计算机青年 · 校团委终审通过后自动生成', back_btn('approvals.html', '返回待办'))}
{scene('一', '第 17 步：备案表已自动生成。下一步切换到学生端，查看“备案完成”结果。', '../../app/student/application-approved.html', '学生端查看结果')}
<div class="grid mt16" style="grid-template-columns:minmax(0,1fr) 300px;align-items:start">{doc}{side}</div>"""
    page("filing-form.html", "approvals", "备案表生成预览", [("待办", "approvals.html"), ("备案表", None)], content)


# ================================================================ 系统管理
USER_JS = """
function addUser(btn){
  var no=btn.getAttribute('data-no');
  var tb=document.querySelector('#user-table tbody');
  if(tb.querySelector('[data-no="'+no+'"]')){toast('该用户已在列表中');return;}
  var name=btn.getAttribute('data-name');
  var tr=document.createElement('tr');
  tr.innerHTML='<td><b>'+name+'</b></td><td><span class="num" data-no="'+no+'">'+no+'</span></td><td>'+btn.getAttribute('data-org')+'</td><td><span class="tag tag-primary">'+btn.getAttribute('data-job')+'</span></td><td><span class="small sub">待配置授权范围</span></td><td><span class="tag tag-success tag-dot">启用</span></td><td><a class="link" href="user-permission.html">授权</a></td>';
  tb.insertBefore(tr,tb.firstChild);
  document.getElementById('user-add').classList.add('hidden');
  toast('已添加用户：'+name);
}
"""


def users():
    rows_data = [
        ("陈静", "T19880012", "校团委宣传部", [("学校管理员", "primary")], "全校全部账号", True),
        ("周建华", "T20090315", "计算机学院团委", [("学院管理员", "primary")], "计算机学院全部账号（36）", True),
        ("王晓琳", "T20180427", "计算机学院", [("业务教师 · 宣传工作辅导员", "warning"), ("业务教师 · 2021级辅导员", "warning"), ("业务教师 · 街舞社指导教师", "warning")],
         "学院团委 / 学生会 / 新媒体中心；2021 级各班团支部；计院街舞社（共 18）", True),
        ("刘洋", "T20200611", "计算机学院", [("业务教师 · 2023级辅导员", "warning")], "2023 级各班团支部（9）", True),
        ("张卫东", "T20020108", "计算机学院党委", [("第一责任人", "muted")], "仅查看本院账号（36）", True),
        ("杨帆", "T20110206", "商学院团委", [("学院管理员", "primary"), ("业务教师 · 学生会指导", "warning")], "商学院全部账号（42）", True),
        ("李明", "8209230117", "计算机学院 2023级软件工程2班", [("学生负责人 ×3", "success")], "中南计院团委 / 计算机学院学生会 / 计院摄影协会", True),
        ("孙悦", "8209240315", "计算机学院 2024级人工智能1班", [("学生负责人", "success")], "计院ACM协会（2026-09-30 起）", True),
        ("何雨桐", "8209230509", "计算机学院 2023级网络工程1班", [("学生负责人 ×2", "success")], "计院青年志愿者 / 计院科协", True),
        ("赵磊", "8209210422", "计算机学院 2021级计算机科学2班", [("学生负责人（已毕业）", "muted")], "—（已交接，任期至 2025-06-30）", False),
    ]
    rows = []
    for n, no, unit, tags, scope, on in rows_data:
        tags_html = '<div class="flex gap4 wrap">' + "".join(tag(t, k) for t, k in tags) + "</div>"
        op = ops(("授权", "user-permission.html"), ("日志", "logs.html")) if n != "陈静" else ops(("日志", "logs.html"),)
        rows.append([person(n, PEOPLE.get(n, {}).get("job", "")), f'<span class="num" data-no="{no}">{no}</span>', unit, tags_html, f'<span class="small sub">{scope}</span>', sw(on, "账号启用"), op])
    tbl = table(["姓名", "工号 / 学号", "单位", "身份标签", "授权范围", "状态", "操作"], rows, id_="user-table")
    fields = [field("姓名 / 工号 / 学号", inp("请输入")), field("单位", sel(["校团委"] + COLLEGES)), field("身份", sel(["学校管理员", "学院管理员", "业务教师", "第一责任人", "学生负责人"])),
              field("状态", sel(["启用", "停用"]))]
    content = f"""
{page_hd('用户管理', '用户来自学校统一身份认证；同一用户可拥有多个身份，每个身份单独授权',
         btn('同步统一身份', None, 'default', 'refresh', toast='已从统一身份认证同步 3 名新增教职工') + '<button class="btn btn-primary" type="button" data-toggle="#user-add">' + icon('user-add') + '新增用户</button>')}
{alert('<b>授权原则：</b>按“组织范围 + 账号范围 + 操作权限”三维授权，<b>不得简单采用“教师 = 查看学院所有账号”</b>的方式；例如 2021 级辅导员仅可审核 2021 级各班团支部账号。', 'warning')}
<div class="mt16"></div>
{filter_bar(fields)}
{card('用户列表', tbl + pager(1486, 5), seg([('全部', 'a'), ('管理员', 'b'), ('教师', 'c'), ('学生', 'd')]))}"""
    picks = "".join(
        f'<button type="button" class="pick-item" data-cat="{esc(n)} {p["no"]}" onclick="addUser(this)" '
        f'data-name="{esc(n)}" data-no="{p["no"]}" data-org="{esc(p["org"])}" data-job="{esc(p["job"])}" '
        f'style="display:flex;justify-content:space-between;width:100%;padding:8px 10px;border:1px solid var(--c-line);border-radius:8px;margin-top:6px;background:#fff;text-align:left">'
        f'<span><b>{n}</b> <span class="small muted">{p["no"]}</span></span><span class="small muted">{p["org"]}</span></button>'
        for n, p in PEOPLE.items())
    content += (
        f'<div class="mask hidden" id="user-add"><div class="modal"><div class="modal-hd">从统一身份认证添加用户'
        f'<button class="x-btn" type="button" data-toggle="#user-add" aria-label="关闭">{icon("x")}</button></div>'
        f'<div class="modal-bd"><div class="small muted mb8">输入姓名或工号 / 学号检索，选中后加入用户列表。</div>'
        f'<label class="top-search" style="width:100%">{icon("search")}<input placeholder="输入姓名或工号 / 学号" data-search="#user-pick"></label>'
        f'<div id="user-pick" style="max-height:320px;overflow:auto;margin-top:8px">{picks}</div></div>'
        f'<div class="modal-ft"><button class="btn btn-default" type="button" data-toggle="#user-add">关闭</button></div></div></div>'
    )
    page("users.html", "users", "用户管理", [("系统管理", "users.html"), ("用户权限", None)], content, js=USER_JS)


def user_permission():
    orgs = [("计算机学院团委", False), ("计算机学院学生会", False), ("计院街舞社", False), ("2021级软件工程1班团支部", True), ("2021级软件工程2班团支部", True),
            ("2021级计算机科学1班团支部", True), ("2021级计算机科学2班团支部", True), ("2021级人工智能1班团支部", True), ("2021级网络工程1班团支部", True),
            ("2022级软件工程1班团支部", False), ("计院ACM协会", False)]
    org_html = "".join(f'<div class="perm-row{" on" if c else ""}">{cb(n, c)}</div>' for n, c in orgs)
    accts = [("2021级软件工程1班团支部", "微信公众号", "已毕业 · 待注销"), ("2021级软件工程2班团支部", "QQ", "已毕业"), ("2021级计算机科学1班团支部", "微信公众号", "已毕业"),
             ("2021级计算机科学2班团支部", "QQ", "已注销"), ("2021级人工智能1班团支部", "微信公众号", "已毕业"), ("2021级网络工程1班团支部", "QQ", "已毕业")]
    acct_html = "".join(f'<div class="perm-row on"><input type="checkbox" checked aria-label="选择" style="accent-color:var(--c-primary)">{acct(n, p, m, "sm")}</div>' for n, p, m in accts)
    perms = [("查看账号", True), ("搜索账号", True), ("审核申请", True), ("审核年审", True), ("僵尸号核实", True), ("审核整改", True), ("代办业务", True),
             ("查看负责人联系方式", True), ("导出数据", False), ("修改档案", False), ("授权他人", False), ("查看其他社团负责人信息", False)]
    perm_html = "".join(f'<div class="perm-row{" on" if c else ""}">{cb(n, c)}</div>' for n, c in perms)
    ident = seg([("宣传工作辅导员", "a"), ("2021级辅导员", "b"), ("街舞社指导教师", "c")], active="2021级辅导员")
    content = f"""
{page_hd('数据范围授权 · 王晓琳', 'T20180427 · 计算机学院 · 一人多身份，按身份分别授权', back_btn('users.html', '返回用户管理'))}
<div class="card hd-card">{avatar('王晓琳', 'lg')}<div class="grow"><div class="flex gap8 wrap"><h2>王晓琳</h2>{tag('业务教师 × 3', 'warning')}</div>
<div class="hd-meta"><span>{PEOPLE['王晓琳']['job']}</span><span>{PEOPLE['王晓琳']['phone']}</span></div></div>
<div class="hd-side"><div class="small muted mb8">当前编辑身份</div>{ident}</div></div>
<div class="mt16">{alert('<b>示例：</b>“2021级辅导员”身份可查看并审核 2021 级各班团支部账号，<b>但不能查看其他社团负责人信息</b>；“街舞社指导教师”身份仅可管理计院街舞社账号。三个身份的权限互不叠加到对方范围。', 'info')}</div>
<div class="grid g3 mt16" style="align-items:start">
  {card('① 组织范围', '<label class="top-search mb12" style="width:100%">' + icon('search') + '<input placeholder="搜索组织"></label><div class="perm-col">' + org_html + '</div>', tag('已选 6', 'primary'))}
  {card('② 账号范围', radios('ascope', ['按组织自动包含', '手动指定账号'], '按组织自动包含') + '<div class="perm-col mt12">' + acct_html + '</div>', tag('6 个账号', 'primary'))}
  {card('③ 操作权限', '<div class="perm-grid">' + perm_html + '</div><div class="hint mt12">未勾选的操作在该身份下不可见</div>', tag('8 / 12', 'primary'))}
</div>
<div class="actbar"><div class="grow">{icon('info')} 保存后立即生效，并记录操作日志（操作类型：权限变更）</div>
  {btn('取消', 'users.html', 'default')}
  {go('保存授权', 'users.html', 'primary', 'check', toast='授权已保存，已记录权限变更日志')}
</div>"""
    page("user-permission.html", "users", "数据范围授权", [("系统管理", "users.html"), ("用户权限", "users.html"), ("数据范围授权", None)], content)


FLOW_JS = """
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-flow]');if(!b)return;
  var name=b.getAttribute('data-flow');
  var title=document.getElementById('flow-title');if(title)title.textContent=name;
  var vt=document.getElementById('ver-title');if(vt)vt.textContent=name+' · 版本记录';
  var nodes=b.getAttribute('data-nodes');
  if(nodes===null)return;
  window._flowRow=b.closest('tr');
  document.querySelectorAll('#flow-edit input[type=checkbox]').forEach(function(c){c.checked=nodes.indexOf(c.value)>=0;});
});
function saveFlow(){
  var tr=window._flowRow;if(!tr){toast('请先选择要编辑的业务');return;}
  var picked=[].slice.call(document.querySelectorAll('#flow-edit input:checked')).map(function(c){return c.value;});
  if(!picked.length){toast('请至少保留一个审核节点');return;}
  var cell=tr.querySelector('[data-flow-desc]');
  if(cell)cell.textContent='已保存：'+picked.join(' → ');
  document.getElementById('flow-edit').classList.add('hidden');
  toast('审核流程已保存，将对新提交的申请生效');
}
"""


def settings_workflow():
    T_, C_, X_ = ("具体负责教师", ""), ("学院管理员", ""), ("校团委", "")
    rows_data = [
        ("新建备案", [T_, C_, X_], True, False, "校团委通过后生效，自动生成备案表"),
        ("账号名称变更", [T_, C_, X_], True, False, "重要变更，生效后记入曾用名"),
        ("所属组织变更", [T_, C_, X_], True, True, "跨学院调整须校级审核"),
        ("负责人变更", [T_], False, True, "教师审核通过即生效"),
        ("账户信息更新", [T_, C_], False, True, "学院通过后生效；平台 ID 变化转新建"),
        ("账号注销", [T_, C_, X_], True, False, "状态转已注销，数据永久保留"),
        ("年度年审", [("学生填报", "gray"), T_, ("学院统一提交", ""), X_], True, False, "无异动无风险可批量审核"),
        ("僵尸号核实", [("系统预警", "gray"), ("教师 / 学生核实", ""), C_, X_], True, False, "不自动注销，校团委确认处置"),
        ("整改反馈", [("学生提交", "gray"), T_, C_], False, True, "校级整改由校团委复核"),
    ]
    rows = []
    for n, nodes, school, bycol, d in rows_data:
        node_names = "、".join(x[0] for x in nodes)
        ops_html = (f'<div class="ops"><button class="link" type="button" data-toggle="#flow-edit" data-flow="{esc(n)}" '
                    f'data-nodes="{esc(node_names)}">编辑</button>'
                    f'<button class="link" type="button" data-toggle="#ver-modal" data-flow="{esc(n)}">版本</button></div>')
        rows.append([f'<b>{n}</b>', node_flow(nodes), sw(school, "校级节点"), sw(bycol, "按学院配置"),
                     f'<span class="small sub" data-flow-desc>{d}</span>', ops_html])
    content = f"""
{page_hd('系统配置', '审核节点、数据字典与风险规则均可配置，不在程序中写死', btn('保存配置', None, 'primary', 'check', toast='审核流程配置已保存，将对新提交的申请生效'))}
{ptabs(SETTINGS_TABS, '审核流程')}
{alert('审核链默认：<b>具体负责教师 → 学院管理员 → 校团委</b>。可按业务类型开关校级节点，并允许学院在不低于全校标准的前提下增加本院节点；配置变更不影响已在流转中的申请。', 'info')}
<div class="mt16">{card('业务审核流程（9 类）', table(['业务类型', '审核节点', '校级节点', '按学院配置', '生效说明', '操作'], rows))}</div>
<div class="grid g3 mt16">
  {card('超时提醒', '<div class="inline-inp">单节点超过 ' + inp('', '3', typ='number') + ' 个工作日未处理，提醒审核人</div><div class="inline-inp mt12">超过 ' + inp('', '7', typ='number') + ' 个工作日，抄送上级管理员</div>')}
  {card('代办规则', cb('允许教师代办负责人交接（学生毕业 / 失联）', True) + '<div class="mt8">' + cb('代办须上传说明材料', True) + '</div><div class="mt8">' + cb('代办申请须学院管理员审核', True) + '</div>')}
  {card('审核人选择', cb('学生提交时可自选一审指导教师', True) + '<div class="mt8">' + cb('仅可选择已授权该组织的教师', True) + '</div><div class="mt8">' + cb('允许学院管理员改派审核人', True) + '</div>')}
</div>"""
    flow_checks = "".join(
        f'<label class="cb" style="display:flex;margin-top:8px"><input type="checkbox" value="{esc(x)}"> {x}</label>'
        for x in ["具体负责教师", "学院管理员", "校团委", "学生填报", "学院统一提交", "系统预警", "教师 / 学生核实"])
    content += (
        f'<div class="mask hidden" id="flow-edit"><div class="modal"><div class="modal-hd">编辑审核流程 · <span id="flow-title"></span>'
        f'<button class="x-btn" type="button" data-toggle="#flow-edit" aria-label="关闭">{icon("x")}</button></div>'
        f'<div class="modal-bd"><div class="small muted mb8">勾选需要经过的节点，保存后写入本行生效说明，新提交的申请按此执行。</div>{flow_checks}</div>'
        f'<div class="modal-ft"><button class="btn btn-default" type="button" data-toggle="#flow-edit">取消</button>'
        f'<button class="btn btn-primary" type="button" onclick="saveFlow()">保存</button></div></div></div>'
        f'<div class="mask hidden" id="ver-modal"><div class="modal sm"><div class="modal-hd"><span id="ver-title">版本记录</span>'
        f'<button class="x-btn" type="button" data-toggle="#ver-modal" aria-label="关闭">{icon("x")}</button></div>'
        f'<div class="modal-bd">{table(["版本", "生效日期", "状态"], [["V1", "2025-09-01", tag("历史", "muted")], ["V2", "2026-03-01", tag("历史", "muted")], ["V3", "2026-09-01", tag("当前", "success")]])}</div>'
        f'<div class="modal-ft"><button class="btn btn-primary" type="button" data-toggle="#ver-modal">知道了</button></div></div></div>'
    )
    page("settings-workflow.html", "settings", "审核流程配置", [("系统管理", "users.html"), ("系统配置", "settings-workflow.html"), ("审核流程", None)], content, js=FLOW_JS)


DICT_JS = """
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-dname]');if(!b)return;
  document.getElementById('d-code').value=b.getAttribute('data-dcode');
  document.getElementById('d-name').value=b.getAttribute('data-dname');
  window._dictLabel=b.closest('tr').querySelector('[data-dlabel]');
});
function saveDict(){
  var name=document.getElementById('d-name').value.trim();
  if(!name){toast('请填写名称');return;}
  if(window._dictLabel)window._dictLabel.textContent=name;
  var code=document.getElementById('d-code').value;
  var btn=document.querySelector('[data-dcode="'+code+'"]');
  if(btn)btn.setAttribute('data-dname',name);
  document.getElementById('dict-edit').classList.add('hidden');
  toast('已保存字典项：'+name);
}
function moveUp(btn){
  var tr=btn.closest('tr');var prev=tr.previousElementSibling;
  if(!prev){toast('已经是第一项');return;}
  tr.parentNode.insertBefore(tr,prev);
  toast('排序已调整');
}
function addDict(id){
  var tb=document.querySelector('#'+id+' tbody');
  if(!tb){toast('请先选择字典分类');return;}
  var n=tb.querySelectorAll('tr').length+1;
  var code='X'+('0'+n).slice(-2);
  var tr=document.createElement('tr');
  tr.innerHTML='<td><span class="num muted">'+code+'</span></td><td><b data-dlabel>未命名</b></td><td><span class="num">'+n+'</span></td><td><span class="num">0</span></td><td><span class="tag tag-success tag-dot">启用</span></td><td><div class="ops"><button class="link" type="button" data-toggle="#dict-edit" data-dcode="'+code+'" data-dname="未命名">编辑</button><button class="link" type="button" onclick="moveUp(this)">上移</button></div></td>';
  tb.appendChild(tr);
  document.getElementById('d-code').value=code;
  document.getElementById('d-name').value='';
  window._dictLabel=tr.querySelector('[data-dlabel]');
  document.getElementById('dict-edit').classList.remove('hidden');
}
function addDictVisible(){
  var pane=document.querySelector('.dict-pane:not(.hidden) table');
  if(pane&&pane.id)addDict(pane.id);
}
"""


def settings_dictionary():
    groups = [
        ("平台类型", PLATFORM_TYPES),
        ("组织类别", ORG_TYPES),
        ("平台层级", LEVELS),
        ("更新频率", UPDATE_FREQ),
        ("注销原因", CANCEL_REASONS),
        ("整改问题类型", ["未建立信息发布审查机制", "内容未执行先审后发", "账号信息不完整", "长期未更新", "负责人信息缺失", "其他"]),
        ("退回原因", ["信息不全", "平台介绍不足100字", "材料不清晰", "重复备案", "其他"]),
        ("年审佐证材料", ["平台主页截图", "更新频率说明", "负责人信息", "其他"]),
    ]
    counts = dict(PLATFORM_STATS)
    fallback = {"快手": 9, "知乎": 4, "网站": 11, "APP": 2, "其他": 2}
    buttons, panes = [], []
    for i, (name, items) in enumerate(groups):
        on = " on" if i == 0 else ""
        buttons.append(f'<button type="button" class="dict-item{on}" data-choice=".dp-{i}">{icon("list")}{name}<span class="cnt">{len(items)}</span></button>')
        rows = []
        for j, item in enumerate(items):
            code = f"{i + 1:02d}{j + 1:02d}"
            used = counts.get(item, fallback.get(item, 0)) if name == "平台类型" else 0
            label = f'<div class="flex gap8">{pf(item, "sm")}<b data-dlabel>{item}</b></div>' if name == "平台类型" else f'<b data-dlabel>{item}</b>'
            ops_html = (f'<div class="ops"><button class="link" type="button" data-toggle="#dict-edit" data-dcode="{code}" data-dname="{esc(item)}">编辑</button>'
                        f'<button class="link" type="button" onclick="moveUp(this)">上移</button></div>')
            rows.append([f'<span class="num muted">{code}</span>', label, f'<span class="num">{j + 1}</span>',
                         f'<span class="num">{used}</span>', sw(True, "启用"), ops_html])
        hid = "" if i == 0 else " hidden"
        add = f'<button class="btn btn-light btn-sm" type="button" onclick="addDict(\'dict-tb-{i}\')">{icon("plus")}新增</button>'
        panes.append(f'<div class="dict-pane dp-{i}{hid}">{card(name + " · " + str(len(items)) + " 项", table(["编码", "名称", "排序", "引用账号数", "启用", "操作"], rows, id_=f"dict-tb-{i}"), btn("导出字典", None, "text", "download", "sm", toast="已导出" + name + "字典") + add)}</div>')
    left = f'<div data-single=".dict-pane">{"".join(buttons)}</div>'
    edit = (
        f'<div class="mask hidden" id="dict-edit"><div class="modal sm"><div class="modal-hd">编辑字典项'
        f'<button class="x-btn" type="button" data-toggle="#dict-edit" aria-label="关闭">{icon("x")}</button></div>'
        f'<div class="modal-bd"><div class="form-grid">{field("编码", "<input class=input id=d-code readonly>")}'
        f'{field("名称", "<input class=input id=d-name placeholder=请输入名称>", True)}</div></div>'
        f'<div class="modal-ft"><button class="btn btn-default" type="button" data-toggle="#dict-edit">取消</button>'
        f'<button class="btn btn-primary" type="button" onclick="saveDict()">保存</button></div></div></div>'
    )
    content = f"""
{page_hd('系统配置', '数据字典统一维护下拉选项，各端表单、筛选、导入模板同步引用', '<button class="btn btn-primary" type="button" onclick="addDictVisible()">' + icon('plus') + '新增字典项</button>')}
{ptabs(SETTINGS_TABS, '数据字典')}
{alert('<b>平台类型通过字典维护，不在程序中写死。</b>新增平台类型后，申请表单、筛选条件、导入模板与统计口径自动生效；已被账号引用的字典项只能停用、不能删除。', 'info')}
<div class="grid mt16" style="grid-template-columns:260px minmax(0,1fr);align-items:start">
  {card('字典分类', left)}
  <div>{''.join(panes)}</div>
</div>{edit}"""
    page("settings-dictionary.html", "settings", "数据字典", [("系统管理", "users.html"), ("系统配置", "settings-workflow.html"), ("数据字典", None)], content, js=DICT_JS)


def settings_rules():
    def rule(title, desc, ic, color, params, level, hits, on=True):
        return (f'<div class="card rule-card"><div class="rule-hd"><span class="rule-ic {color}">{icon(ic)}</span><div class="grow"><div class="bold">{title}</div>'
                f'<div class="small muted">{desc}</div></div>{sw(on, title)}</div><div class="flex gap16 wrap">{params}</div>'
                f'<div class="flex between"><span class="small muted">风险等级 {level}</span><span class="small">当前命中 <b class="num">{hits}</b> 个</span></div></div>')
    cards = "".join([
        rule("长期未更新", "按最近发布时间计算停更天数，分级预警", "clock", "",
             f'<div class="inline-inp">中风险 ≥ {inp("", "180", typ="number")} 天</div><div class="inline-inp">高风险 ≥ {inp("", "365", typ="number")} 天</div>', st("中风险") + " / " + st("高风险"), 31),
        rule("最近发布为空", "开通后从未发布内容", "inbox", "orange", f'<div class="inline-inp">开通超过 {inp("", "90", typ="number")} 天仍无发布</div>', st("中风险"), 6),
        rule("账号无法访问", "定期抓取主页，连续失败即预警", "ban", "", f'<div class="inline-inp">连续失败 {inp("", "3", typ="number")} 次</div>', st("中风险"), 4),
        rule("无学生负责人", "学生负责人为空或已毕业未交接", "user", "orange", cb("负责人毕业离校视同为空", True), st("中风险"), 9),
        rule("无负责教师", "管理教师为空或已调离", "users", "orange", cb("教师调离后 30 天未重新指定", True), st("中风险"), 4),
        rule("组织撤销或已毕业", "所属组织存续状态为已撤销 / 已毕业", "flag", "", cb("团支部毕业后自动命中", True), st("高风险"), 12),
        rule("重复备案", "同平台同 ID 存在多条在册记录", "copy", "blue", cb("同时比对曾用名与已注销账号", True), st("低风险"), 2),
    ])
    content = f"""
{page_hd('系统配置', '僵尸号与数据异常规则，命中后仅预警，不自动处置',
         btn('预览命中', None, 'default', 'eye', toast='按当前规则预览：命中 47 个账号（较现行规则无变化）') + btn('保存规则', None, 'primary', 'check', toast='风险规则已保存，将于下次扫描生效'))}
{ptabs(SETTINGS_TABS, '风险规则')}
<div class="card card-bd mb16"><div class="flex gap24 wrap">
  <div class="field" style="width:200px"><label>扫描周期</label>{sel(['每日 02:00', '每周一 02:00', '每月 1 日 02:00'], '每日 02:00', ph='')}</div>
  <div class="field" style="width:200px"><label>预警推送对象</label>{sel(['负责教师 + 学院管理员', '仅学院管理员'], '负责教师 + 学院管理员', ph='')}</div>
  <div class="field" style="width:220px"><label>重复预警间隔</label>{sel(['核实正常后 180 天内不重复', '核实正常后 90 天内不重复'], '核实正常后 180 天内不重复', ph='')}</div>
  <div class="grow">{alert('命中任一规则即列为“疑似僵尸号”；风险等级取命中规则中的最高级。', 'info')}</div>
</div></div>
<div class="grid g3">{cards}</div>"""
    page("settings-rules.html", "settings", "风险规则配置", [("系统管理", "users.html"), ("系统配置", "settings-workflow.html"), ("风险规则", None)], content)


LOG_TYPES = ["新建", "变更", "注销", "年审", "负责人交接", "整改", "权限变更", "数据导入", "数据导出", "管理员代办"]


def logs():
    rows_data = [
        ("2026-09-30 16:00", "陈静", "学校管理员", "注销", "2021级软件工程1班团支部", "校团委确认注销，状态转为已注销，数据保留", ""),
        ("2026-09-30 14:20", "陈静", "学校管理员", "年审", "中南计院团委等 18 个账号", "年审批量通过：无异动无风险", ""),
        ("2026-09-30 13:45", "周建华", "学院管理员", "负责人交接", "计院ACM协会", "审核通过，负责人由赵磊变更为孙悦", ""),
        ("2026-09-30 11:00", "陈静", "学校管理员", "变更", "中南计院学生会", "名称变更生效，原名称“计算机学院学生会”记入曾用名", ""),
        ("2026-09-30 10:05", "陈静", "学校管理员", "新建", "中南计算机青年", "准予备案，建立档案并生成备案表", ""),
        ("2026-09-30 09:20", "王晓琳", "业务教师", "负责人交接", "计院ACM协会", "发起负责人交接：赵磊 → 孙悦（原负责人已毕业）", "教师代办"),
        ("2026-09-29 18:31", "陈静", "学校管理员", "数据导出", "全校总表", "导出 986 条记录（脱敏）", ""),
        ("2026-09-29 16:12", "陈静", "学校管理员", "权限变更", "王晓琳", "新增“2021级辅导员”身份授权：2021 级各班团支部", ""),
        ("2026-09-28 09:40", "周建华", "学院管理员", "整改", "计院青年志愿者", "整改通过，年审恢复流转", ""),
        ("2026-09-26 15:30", "杨帆", "学院管理员", "管理员代办", "商学院青年", "代学生补录开通时间与认证主体", "管理员代办"),
        ("2026-09-10 15:02", "陈静", "学校管理员", "数据导入", "2025 年度账号底库", "导入 958 条，失败 9 条，疑似重复 5 条", ""),
        ("2026-09-15 09:00", "陈静", "学校管理员", "年审", "2026 年度年审任务", "发布任务，自动生成 986 条年审记录", ""),
    ]
    kind = {"新建": "primary", "变更": "warning", "注销": "danger", "年审": "success", "负责人交接": "primary", "整改": "warning",
            "权限变更": "danger", "数据导入": "muted", "数据导出": "muted", "管理员代办": "primary"}
    rows = []
    for t, who, role, typ, obj, summ, way in rows_data:
        way_html = f' {tag(way, "primary", True)}' if way else ""
        rows.append(dict(cells=[f'<span class="num small">{t}</span>', person(who), f'<span class="small sub">{role}</span>', tag(typ, kind[typ]) + way_html,
                                f'<b class="fs13">{obj}</b>', f'<span class="small sub">{summ}</span>', ops(("详情", "log-detail.html"))], href="log-detail.html"))
    fields = [field("操作类型", sel(LOG_TYPES)), field("操作人", inp("姓名 / 工号")), field("发起方式", sel(["本人办理", "教师代办", "管理员代办", "系统自动"])),
              field("操作对象", inp("账号名称 / 平台ID")), field("开始时间", inp("", "2026-09-01", typ="date")), field("结束时间", inp("", "2026-09-30", typ="date")),
              field("学院", sel(["校团委"] + COLLEGES))]
    content = f"""
{page_hd('操作日志', '全校业务操作留痕：谁、以什么身份、在何时、对哪个账号、做了什么、修改前后', btn('导出日志', 'export.html', 'default', 'download'))}
{filter_bar(fields)}
{card('日志列表', table(['时间', '操作人', '身份', '操作类型', '对象', '摘要', '操作'], rows) + pager(12860, 5), seg([('全部', 'a'), ('代办操作', 'b'), ('敏感操作', 'c')]))}"""
    page("logs.html", "logs", "操作日志", [("系统管理", "users.html"), ("操作日志", None)], content)


def log_detail():
    a = ACCOUNTS["proxy"]
    no = FLOWS["proxy"]["no"]
    diff = diff_table([
        ("学生负责人", "赵磊", a["new_student"]),
        ("学号", PEOPLE["赵磊"]["no"], PEOPLE["孙悦"]["no"]),
        ("手机", "159 7312 0846（已停用）", PEOPLE["孙悦"]["phone"]),
        ("年级班级", PEOPLE["赵磊"]["grade"], PEOPLE["孙悦"]["grade"]),
        ("任期", "2022-09-01 至 2025-06-30", "2026-09-30 起"),
        ("账号名称", a["name"], a["name"]),
        ("管理教师", a["teacher"], a["teacher"]),
    ])
    info = kv([
        ("操作人", person("王晓琳", "T20180427")), ("身份", tag("业务教师 · 宣传工作辅导员", "warning")), ("操作时间", "2026-09-30 09:20:36"),
        ("操作对象", f'{acct(a["name"], a["platform"], a["platform"] + " · " + a["pid"], "sm")}'), ("操作类型", tag("负责人交接", "primary")),
        ("发起方式", st("教师代办")), ("代办原因", "学生负责人已毕业，无法本人办理"), ("业务编号", f'<span class="num">{no}</span>'),
        ("IP 地址", '<span class="num">10.96.18.42（校内网）</span>'), ("终端", "PC · Chrome 128 / macOS"),
        ("代办说明材料", fchip("赵磊毕业离校证明.pdf") + " " + fchip("ACM协会换届决议.pdf")),
    ], 3)
    content = f"""
{page_hd('日志详情', f'{no} · 负责人交接 · 教师代办', back_btn('logs.html', '返回日志列表') + btn('查看账号操作日志', '../common/archive-logs.html', 'primary', 'log'))}
{scene('八', '第 4 步：日志已记录“发起方式：教师代办”。下一步查看该账号档案中的完整操作日志。', '../common/archive-logs.html', '下一步：档案操作日志')}
<div class="split mt16">
<div class="col gap16">
  {card('操作信息', info, st('已完成'))}
  {card('修改前后', diff, tag('变更 5 项', 'warning'))}
</div>
<div class="sticky col gap16">
  {card('审核意见', flow_tl('proxy'), tag('已生效', 'success'))}
  {card('关联', '<div class="col gap8"><a class="link" href="../common/archive-logs.html">账号档案 · 操作日志</a><a class="link" href="../common/archive-staff.html">账号档案 · 责任人员历史</a><a class="link" href="logs.html">返回日志列表</a></div>')}
</div>
</div>"""
    page("log-detail.html", "logs", "日志详情", [("系统管理", "users.html"), ("操作日志", "logs.html"), ("日志详情", None)], content)


def build():
    dashboard()
    messages()
    accounts()
    accounts_filter()
    organizations()
    organization_edit()
    approval_detail()
    approval_change()
    approval_cancel()
    annual_tasks()
    annual_task_create()
    annual_task_detail()
    annual_progress()
    annual_college_detail()
    annual_review()
    annual_batch_confirm()
    annual_review_detail()
    zombie()
    zombie_detail()
    anomalies()
    rectify()
    rectify_create()
    rectify_detail()
    import_page()
    import_result()
    export()
    export_records()
    filing_form()
    users()
    user_permission()
    settings_workflow()
    settings_dictionary()
    settings_rules()
    logs()
    log_detail()
