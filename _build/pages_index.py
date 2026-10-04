"""index.html 原型导航页：演示入口、演示剧本、角色权限、功能清单、业务流程、审核流程、状态体系、页面目录。"""
from base import *  # noqa: F401,F403
from data import RUN_STATUS, FILING_STATUS, ANNUAL_STATUS, CHANGE_TYPES, SCHOOL_STATS as S
from manifest import GROUPS, SCENARIOS

CSS = """
body{background:#F5F7FA}
.wrap-in{max-width:1200px;margin:0 auto;padding:0 24px}
.hero{text-align:center;padding:56px 0 36px;background:radial-gradient(900px 400px at 50% -10%,#DCEBF8 0%,transparent 70%)}
.hero-logo{width:84px;height:84px;border-radius:50%;margin:0 auto 20px;display:block;box-shadow:0 14px 30px rgba(42,141,199,.35)}
.hero h1{font-size:34px;letter-spacing:1px}
.hero .lead{max-width:760px;margin:14px auto 0;color:var(--c-text-2);font-size:15px;line-height:1.9}
.hero .lead b{color:var(--c-text)}
.pills{display:flex;justify-content:center;gap:10px;margin-top:22px;flex-wrap:wrap}
.pill{display:inline-flex;align-items:center;gap:6px;height:36px;padding:0 16px;border-radius:18px;background:#fff;border:1px solid var(--c-line);font-size:13px;font-weight:500}
.pill.blue{background:var(--c-primary-light);border-color:var(--c-primary-border);color:var(--c-primary)}
.nums{display:flex;justify-content:center;gap:64px;margin-top:30px}
.nums b{display:block;font-size:40px;line-height:1.1;color:var(--c-primary);font-variant-numeric:tabular-nums}
.nums span{font-size:13px;color:var(--c-text-2)}
.tipbar{background:var(--c-primary-light);border-top:1px solid var(--c-primary-border);border-bottom:1px solid var(--c-primary-border);color:#1F5F92;font-size:13px;padding:10px 0}
.anchor{position:sticky;top:0;z-index:40;background:rgba(255,255,255,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--c-line)}
.anchor .wrap-in{display:flex;gap:4px;overflow-x:auto;height:52px;align-items:center}
.anchor a{padding:6px 14px;border-radius:8px;font-size:14px;color:var(--c-text-2);white-space:nowrap}
.anchor a:hover{background:var(--c-primary-light);color:var(--c-primary)}
.sec{padding:40px 0 8px;scroll-margin-top:52px}
.sec-hd{display:flex;align-items:center;gap:12px;margin-bottom:18px}
.sec-ic{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;background:var(--c-primary-light);color:var(--c-primary)}
.sec-hd h2{font-size:22px}
.sec-hd p{font-size:13px;color:var(--c-text-3)}
.entry{display:flex;flex-direction:column;overflow:hidden;border-radius:14px;background:#fff;border:1px solid #E3ECF5;box-shadow:var(--shadow-sm);transition:box-shadow .2s,border-color .2s}
.entry:hover{box-shadow:var(--shadow-lg);border-color:var(--c-primary-border)}
.entry-hd{display:flex;align-items:center;gap:14px;padding:18px 20px}
.entry-ic{width:50px;height:50px;border-radius:14px;display:grid;place-items:center;color:#fff;flex:none}
.entry-ic .i{width:24px;height:24px}
.entry h3{font-size:17px}
.entry-go{margin-left:auto;color:var(--c-primary);font-weight:600;font-size:14px;display:flex;align-items:center;gap:2px}
.preview{height:230px;overflow:hidden;position:relative;background:#EEF3F8;border-top:1px solid var(--c-line)}
.preview iframe{position:absolute;top:0;left:0;border:0;transform-origin:0 0;pointer-events:none}
.preview::after{content:"";position:absolute;inset:0}
.entry-links{display:flex;flex-wrap:wrap;gap:6px;padding:12px 20px 16px;border-top:1px solid var(--c-line)}
.entry-links a{font-size:12px;padding:3px 10px;border-radius:12px;background:var(--c-bg);color:var(--c-text-2)}
.entry-links a:hover{background:var(--c-primary-light);color:var(--c-primary)}
.scn{padding:20px;display:flex;flex-direction:column;gap:12px}
.scn-no{width:40px;height:40px;border-radius:12px;background:var(--c-primary);color:#fff;display:grid;place-items:center;font-weight:700;flex:none}
.scn-steps{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.scn-step{display:inline-flex;align-items:center;gap:6px;padding:4px 10px 4px 4px;border-radius:14px;background:var(--c-bg);font-size:12px;border:1px solid transparent}
.scn-step:hover{border-color:var(--c-primary-border);background:#fff;color:var(--c-primary)}
.scn-step i{font-style:normal;min-width:20px;height:20px;border-radius:10px;display:grid;place-items:center;color:#fff;font-size:11px;font-weight:600;padding:0 5px}
.scn-arrow{color:var(--c-border)}
.matrix td,.matrix th{text-align:center}
.matrix td:first-child,.matrix th:first-child{text-align:left}
.yes{color:var(--c-success);font-weight:700}.no{color:var(--c-border)}.part{color:var(--c-warning);font-weight:500;font-size:12px}
.mod{padding:18px 20px}
.mod h4{font-size:15px;display:flex;align-items:center;gap:8px;margin-bottom:8px}
.mod ul{list-style:none;display:flex;flex-wrap:wrap;gap:6px}
.mod li{font-size:12px;padding:2px 8px;border-radius:4px;background:var(--c-bg);color:var(--c-text-2)}
.life{display:flex;align-items:stretch;gap:0;overflow-x:auto;padding-bottom:4px}
.life-item{flex:1;min-width:104px;position:relative;padding:14px 12px;background:#fff;border:1px solid var(--c-line);border-radius:12px;margin-right:18px}
.life-item:last-child{margin-right:0}
.life-item::after{content:"";position:absolute;right:-15px;top:50%;width:12px;height:12px;border-top:2px solid var(--c-primary-border);border-right:2px solid var(--c-primary-border);transform:translateY(-50%) rotate(45deg)}
.life-item:last-child::after{display:none}
.life-no{font-size:12px;color:var(--c-primary);font-weight:700}
.life-item b{display:block;font-size:15px;margin:2px 0 4px}
.life-item p{font-size:12px;color:var(--c-text-3);line-height:1.6}
.lane{display:grid;grid-template-columns:120px 1fr;border-bottom:1px dashed var(--c-line)}
.lane:last-child{border-bottom:none}
.lane-hd{padding:14px 0;font-weight:600;font-size:13px;display:flex;align-items:center;gap:8px}
.lane-bd{display:flex;align-items:center;gap:8px;padding:10px 0;flex-wrap:wrap}
.node{display:inline-flex;align-items:center;gap:6px;height:30px;padding:0 12px;border-radius:15px;font-size:13px;background:#fff;border:1px solid var(--c-line)}
.node.cfg{border-style:dashed;border-color:var(--c-warning);color:#A86400;background:var(--c-warning-bg)}
.node.end{background:var(--c-success-bg);border-color:var(--c-success-bd);color:#0E8A55}
.node.start{background:var(--c-primary-light);border-color:var(--c-primary-border);color:var(--c-primary)}
.node.none{color:var(--c-text-3);background:var(--c-muted-bg);border-color:var(--c-line)}
.st-col h4{font-size:15px;margin-bottom:4px}
.st-col p{font-size:12px;color:var(--c-text-3);margin-bottom:12px}
.st-col .tags{display:flex;flex-direction:column;gap:8px;align-items:flex-start}
.dir-hd{display:flex;align-items:center;gap:12px;margin:28px 0 12px}
.dir-hd .entry-ic{width:40px;height:40px;border-radius:11px}
.dir-hd h3{font-size:18px}
.dir-hd .cnt{margin-left:auto;font-size:13px;color:var(--c-text-3)}
.pg{display:flex;align-items:center;gap:12px;padding:12px 16px;background:#fff;border:1px solid #E6EDF4;border-radius:10px;transition:border-color .15s,box-shadow .15s}
.pg:hover{border-color:var(--c-primary);box-shadow:var(--shadow-md)}
.pg-no{width:28px;height:28px;border-radius:8px;background:var(--c-bg);color:var(--c-text-3);display:grid;place-items:center;font-size:12px;font-weight:600;flex:none}
.pg b{font-size:14px;display:block}
.pg span{font-size:12px;color:var(--c-text-3)}
.pg code{margin-left:auto;font-size:11px;color:var(--c-primary);background:var(--c-primary-light);padding:2px 8px;border-radius:4px;white-space:nowrap;font-family:ui-monospace,Menlo,monospace}
.foot{padding:40px 0 60px;text-align:center;color:var(--c-text-3);font-size:12px}
"""

ROLE_COLOR = {"学生": "#2A8DC7", "教师": "#E6A23C", "学院": "#67C23A", "学校": "#006DAD", "公共": "#6B5BD2"}


def step_color(label):
    for k, c in ROLE_COLOR.items():
        if k in label:
            return c
    return "#2A8DC7"


def hero():
    total_pages = sum(len(g["pages"]) for g in GROUPS) + 1
    return f"""
<header class="hero"><div class="wrap-in">
  <img class="hero-logo" src="assets/m-center-logo.png" alt="中南大学">
  <h1>中南大学团学组织新媒体平台 · 原型页面导航</h1>
  <p class="lead">覆盖全校团学组织新媒体账号<b>全生命周期</b>的综合管理平台原型：新建备案 → 正常运行 → 人员交接 → 信息变更 → 年度年审 → 异常整改 → 账号注销 → 历史归档。<br>
  <b>PC 管理端（学校管理员 / 学院管理员 / 业务教师）+ 移动 APP（学生 / 教师 / 学院管理员）</b>，8 条演示剧本贯穿各角色，业务逻辑闭环、按钮均可点击。</p>
  <div class="pills">
    <span class="pill blue">{icon('file')}高保真交互原型</span>
    <span class="pill">{icon('layers')}每页独立 HTML · 样式内联</span>
    <span class="pill">{icon('route')}演示剧本可一路点通</span>
  </div>
  <div class="nums">
    <div><b>{total_pages}</b><span>HTML 页面</span></div>
    <div><b>2</b><span>终端形态</span></div>
    <div><b>4</b><span>系统角色</span></div>
    <div><b>8</b><span>演示剧本</span></div>
    <div><b>{S['total']}</b><span>模拟在册账号</span></div>
  </div>
</div></header>
<div class="tipbar"><div class="wrap-in flex gap8">{icon('info')}
  演示建议：先看“角色权限”与“审核流程”讲清规则，再按“演示剧本”逐步点击；PC 页面右上角“原型导航”按钮、移动端页面右侧说明栏均可一键返回本导航页；PC 页面已按中南大学智慧学工正式系统的界面风格还原。数据为模拟数据，当前日期设定为 2026-09-30（2026 年度年审进行中）。
</div></div>
<nav class="anchor"><div class="wrap-in">
  <a href="#entry">演示入口</a><a href="#scenario">演示剧本</a><a href="#role">角色权限</a><a href="#feature">功能清单</a>
  <a href="#flow">业务流程</a><a href="#audit">审核流程</a><a href="#status">状态体系</a><a href="#pages">页面目录</a>
</div></nav>"""


def sec(id_, ic, title, desc, body):
    return (f'<section class="sec" id="{id_}"><div class="wrap-in"><div class="sec-hd"><span class="sec-ic">{icon(ic, 18)}</span>'
            f'<div><h2>{title}</h2><p>{desc}</p></div></div>{body}</div></section>')


def entries():
    items = [
        ("PC 端 · 学校管理员", "校团委宣传部 陈静：全校驾驶舱、校级审核、年审发起、风险监管", "building", "#006DAD",
         "pc/school/dashboard.html", 1440, [("账号库", "pc/school/accounts.html"), ("校级审核", "pc/school/approvals.html"),
                                            ("年审任务", "pc/school/annual-tasks.html"), ("僵尸号排查", "pc/school/zombie.html"), ("系统配置", "pc/school/settings-workflow.html")]),
        ("PC 端 · 学院管理员", "计算机学院团委 周建华：学院审核、年审统筹提交、任务分派、整改", "hierarchy", "#67C23A",
         "pc/college/workbench.html", 1440, [("学院审核", "pc/college/approvals.html"), ("年审统筹", "pc/college/annual-progress.html"),
                                              ("任务分派", "pc/college/assign.html"), ("整改管理", "pc/college/rectify.html"), ("教师工作量", "pc/college/teachers.html")]),
        ("PC 端 · 业务教师", "宣传工作辅导员 王晓琳（一人多身份）：一审、年审、核实、代办", "user", "#E6A23C",
         "pc/teacher/workbench.html", 1440, [("待我审核", "pc/teacher/todo.html"), ("年审审核", "pc/teacher/review-annual.html"),
                                              ("僵尸号核实", "pc/teacher/review-zombie.html"), ("代办中心", "pc/teacher/proxy.html"), ("账号档案", "pc/common/archive-basic.html")]),
        ("移动端 · 学生用户", "新媒体中心主任 李明：发起申请、在线年审、提交整改、查看进度", "smartphone", "#2A8DC7",
         "app/student/home.html", 1100, [("业务申请", "app/student/apply.html"), ("我的年审", "app/student/annual.html"),
                                          ("我的申请", "app/student/applications.html"), ("整改任务", "app/student/rectify.html"), ("登录", "app/common/login.html")]),
        ("移动端 · 业务教师", "王晓琳：随时随地移动审核，年审无异动批量通过", "inbox", "#E6A23C",
         "app/teacher/home.html", 1100, [("待审", "app/teacher/todo.html"), ("交接审核", "app/teacher/review-handover.html"),
                                          ("年审审核", "app/teacher/review-annual.html"), ("批量审核", "app/teacher/review-batch.html")]),
        ("移动端 · 学院管理员", "周建华：移动审核、年审进度督办、整改复核", "dashboard", "#67C23A",
         "app/college/home.html", 1100, [("待学院审核", "app/college/todo.html"), ("年审进度", "app/college/annual-progress.html"),
                                          ("整改跟踪", "app/college/rectify.html"), ("提交校团委", "app/college/annual-submit.html")]),
    ]
    cards = []
    for title, desc, ic, color, href, vw, links in items:
        scale = 560 / vw
        link_html = "".join(f'<a href="{h}">{t}</a>' for t, h in links)
        cards.append(f"""<div class="entry">
  <a class="entry-hd" href="{href}"><span class="entry-ic" style="background:{color}">{icon(ic)}</span>
    <div class="grow"><h3>{title}</h3><div class="small muted">{desc}</div></div><span class="entry-go">进入{icon('chevron-right', 14)}</span></a>
  <a class="preview" href="{href}" aria-label="{title}页面预览"><iframe src="{href}" loading="lazy" tabindex="-1" title="{title}预览"
    style="width:{vw}px;height:{int(230 / scale)}px;transform:scale({scale:.4f})"></iframe></a>
  <div class="entry-links">{link_html}</div>
</div>""")
    login = (f'<div class="grid g2 mt16">'
             f'<a class="pg" href="pc/common/login.html"><span class="pg-no">{icon("lock", 14)}</span><div><b>PC 统一身份认证登录</b><span>工号 / 学号登录 → 选择身份进入各角色</span></div><code>pc/common/login.html</code></a>'
             f'<a class="pg" href="pc/common/identity-switch.html"><span class="pg-no">{icon("user-switch", 14)}</span><div><b>多身份选择</b><span>一人多身份，按组织 + 账号 + 操作授权</span></div><code>pc/common/identity-switch.html</code></a></div>')
    return f'<div class="grid g2">{"".join(cards)}</div>{login}'


def scenarios():
    cards = []
    for s in SCENARIOS:
        steps_html = []
        for i, (who, text, path) in enumerate(s["steps"], 1):
            if i > 1:
                steps_html.append(f'<span class="scn-arrow">{icon("chevron-right", 12)}</span>')
            steps_html.append(f'<a class="scn-step" href="{path}" title="{who}"><i style="background:{step_color(who)}">{i}</i>{text}</a>')
        cards.append(f"""<div class="card scn">
  <div class="flex gap12"><span class="scn-no">{s['no']}</span><div class="grow"><div class="fs16 bold flex gap8">{icon(s['ic'])}{s['title']}</div>
  <div class="small muted">{len(s['steps'])} 步 · 起点：{s['steps'][0][0]}</div></div>
  <a class="btn btn-light btn-sm" href="{s['steps'][0][2]}">从头演示{icon('arrow-right', 14)}</a></div>
  <p class="fs13 sub">{s['desc']}</p>
  <div class="scn-steps">{''.join(steps_html)}</div>
</div>""")
    legend = "".join(f'<span class="flex gap6 small"><span class="legend-dot" style="background:{c}"></span>{k}</span>' for k, c in ROLE_COLOR.items())
    return f'<div class="flex gap16 mb16 wrap"><span class="small muted">步骤颜色：</span>{legend}</div><div class="grid g2">{"".join(cards)}</div>'


def roles():
    role_tbl = table(["用户角色", "主要使用人员", "可查看数据范围", "管理范围", "审核权限", "终端"], [
        [f'<b>学校管理员</b>', "校团委宣传部负责老师及授权人员", "全校所有账号、组织、人员、年审和整改数据", "全校", "学校层面最终审核、备案、整改及注销审核", tag("PC", "primary") + " " + tag("移动", "success")],
        [f'<b>学院管理员</b>', "学院团委书记、副书记、学院指定负责教师", "本学院及所属、直属、指导组织全部数据", "本学院全部账号", "学院层面审核，统筹教师审核结果并提交学校", tag("PC", "primary") + " " + tag("移动", "success")],
        [f'<b>学院业务教师</b>', "年级辅导员、社团指导老师、宣传工作辅导员、志愿服务负责老师等", "本人被授权的组织和账号", "被授权组织或账号", "对本人负责范围内学生申请、年审、整改等进行审核", tag("PC", "primary") + " " + tag("移动", "success")],
        [f'<b>学生用户</b>', "团支书、社团负责人、学生会负责人、志愿者协会负责人、新媒体学生骨干等", "本人负责、所在组织授权或本人申请的账号", "本人负责账号", "无最终审核权，可发起申请和提交材料", tag("移动", "success")],
    ])
    Y, N = '<span class="yes">√</span>', '<span class="no">—</span>'

    def p(t):
        return f'<span class="part">{t}</span>'
    matrix = [
        ("查看全校账号", Y, N, N, N), ("查看本学院全部账号", Y, Y, N, N), ("查看本人负责账号", Y, Y, Y, Y),
        ("搜索账号", Y, Y, p("本人范围"), p("本人范围")), ("查看完整历史档案", Y, Y, p("本人账号"), p("本人账号")),
        ("新建账号申请", Y, Y, Y, Y), ("变更账号申请", Y, Y, Y, Y), ("注销账号申请", Y, Y, Y, Y),
        ("审核学生申请", Y, Y, Y, N), ("学院审核", Y, Y, N, N), ("校级审核", Y, N, N, N),
        ("发起年度年审", Y, N, N, N), ("年度年审填报", Y, Y, Y, Y), ("审核年审", Y, Y, Y, N),
        ("提交学院年度年审", Y, Y, N, N), ("查看学院年审进度", Y, Y, p("本人范围"), p("本人范围")), ("查看全校年审进度", Y, N, N, N),
        ("疑似“僵尸号”核实", Y, Y, Y, p("本人账号")), ("创建整改任务", Y, Y, N, N), ("提交整改材料", Y, Y, Y, Y),
        ("审核整改结果", Y, Y, Y, N), ("批量审核", Y, Y, Y, N), ("批量分配年审任务", Y, Y, N, N),
        ("数据批量导入", Y, Y, N, N), ("数据导出", p("全校"), p("本学院"), N, N), ("查看统计驾驶舱", p("全校"), p("本学院"), p("本人范围"), N),
        ("系统参数配置", Y, N, N, N), ("查看操作日志", p("全校"), p("本学院"), p("本人业务"), p("本人申请")), ("管理用户权限", p("全校"), p("本学院"), N, N),
    ]
    rows = [[f'<b>{r[0]}</b>'] + list(r[1:]) for r in matrix]
    half = (len(rows) + 1) // 2
    heads = ["功能", "学校管理员", "学院管理员", "学院业务教师", "学生用户"]
    mtx = (f'<div class="grid g2">{table(heads, rows[:half], cls="matrix")}{table(heads, rows[half:], cls="matrix")}</div>'
           f'<div class="flex gap20 mt12 small muted"><span><span class="yes">√</span> 具有该功能权限</span><span><span class="part">本人范围 / 本学院</span> 授权范围由学院或系统配置决定</span><span><span class="no">—</span> 原则上不具有该权限</span></div>')
    design = card("权限设计要点", f"""<div class="grid g2">
  <div>{alert('<b>一名教师可能同时承担多个身份。</b>不得简单采用“教师 = 查看学院所有账号”的方式配置权限，应实现：某用户可以管理哪些组织、哪些账号以及可以执行哪些操作。', 'warning')}
  <div class="mt12 fs13 sub">示例：王晓琳同时是 <b>宣传工作辅导员</b>、<b>2021 级辅导员</b>、<b>计院街舞社指导教师</b>，可审核 2021 级各班团支部账号与街舞社账号，但不能查看其他社团负责人信息。
  <div class="flex gap8 mt8 wrap">{btn('查看多身份选择', 'pc/common/identity-switch.html', 'light', 'user-switch', 'sm')}{btn('查看数据范围授权', 'pc/school/user-permission.html', 'light', 'key', 'sm')}</div></div></div>
  <div><div class="bold mb8">账号责任体系（与“用户角色”是不同概念）</div>
  {kv([('制度责任人', '第一责任人（学院党委分管学生工作副书记）、直接责任人（学院团委书记）'),
       ('具体管理教师', '年级辅导员、社团指导教师、宣传工作负责老师、志愿服务负责教师'),
       ('学生运营负责人', '姓名、学号、联系方式、所属组织、职务、任期起止；换届不覆盖，保留历史')], 2)}
  <div class="small muted mt8">一级平台：校团委书记为第一责任人、分管书记为直接责任人；二、三级平台：所在党委分管领导为第一责任人，二级团组织书记为直接责任人。</div></div>
</div>""")
    return (card("用户角色及数据权限", role_tbl) + '<div class="mt16"></div>' +
            card("主要功能权限矩阵（28 项功能 × 4 类角色）", mtx) + '<div class="mt16"></div>' + design)


def features():
    mods = [
        ("shield", "统一身份认证与权限", "学校统一身份认证；工号 / 学号登录；多身份切换；组织 + 账号 + 操作三维授权", ["统一认证", "多身份", "数据范围授权", "不存第三方密码"], "pc/school/user-permission.html"),
        ("database", "新媒体账号主库", "一账号一档案，层级、僵尸号均为属性与状态，通过筛选产生", ["16 条件组合查询", "账号档案 7 页签", "曾用名", "四套状态"], "pc/school/accounts.html"),
        ("file-add", "新建备案", "学生 / 教师 / 学院均可发起；重复检查；自选审核老师；三级审核", ["重复检查", "自选审核人", "退回重提", "备案表生成"], "app/student/apply.html"),
        ("file-edit", "信息变更", "重要变更报校团委，日常维护学院审核后生效；平台 ID 变化转新建", ["变更前后对比", "曾用名留痕", "ID 变化转新建"], "pc/common/apply-change.html"),
        ("user-switch", "负责人交接", "应对学生组织换届，学生提交、教师审核即生效，保留任职起止", ["原 / 新负责人", "生效时间", "历史保留"], "app/student/apply-handover.html"),
        ("power", "账号注销", "9 类注销原因；审核后只改状态为已注销，不删除数据", ["注销原因", "佐证材料", "数据永久保留"], "pc/common/apply-cancel.html"),
        ("calendar", "年度年审", "学校发起任务并配置时间节点，系统继承历史数据自动生成记录，只确认变化", ["任务配置", "学生填报", "教师 6 种操作", "学院统一提交", "校级批量审核"], "pc/school/annual-tasks.html"),
        ("ghost", "僵尸号排查中心", "按停更天数、无法访问、无负责人、组织撤销等规则自动预警，人工核实处置", ["规则可配置", "预警清单", "核实链路", "不自动注销"], "pc/school/zombie.html"),
        ("wrench", "整改闭环", "整改问题、要求、责任人、截止时间；通过 / 继续整改 / 转注销", ["多轮整改", "历史永久保留"], "pc/school/rectify.html"),
        ("route", "学院任务分派", "单个 / 批量 / 按年级 / 按组织类别分配，统计每名教师工作量", ["批量分配规则", "教师工作量"], "pc/college/assign.html"),
        ("hand", "教师代办", "学生毕业、失联、组织撤销等情形由教师代办，记录发起方式", ["代办原因", "日志标记"], "pc/teacher/proxy.html"),
        ("chart", "驾驶舱与工作台", "学校数据驾驶舱 16 项指标；学院工作台；教师工作台", ["全校底数", "年审进度", "风险预警"], "pc/school/dashboard.html"),
        ("upload", "数据导入导出", "2025 年度数据初始化导入并由学院确认；13 类台账导出；备案表自动生成", ["Excel 导入", "校验结果", "13 类台账", "Word / PDF"], "pc/school/export.html"),
        ("bell", "消息待办与日志", "按身份生成待办；新建、变更、注销、年审、交接、整改、权限、导入导出、代办全部留痕", ["待办中心", "修改前后", "审核意见"], "pc/school/logs.html"),
        ("settings", "系统配置", "审核流程节点可配置；平台类型等数据字典；风险规则阈值", ["流程配置", "数据字典", "风险规则"], "pc/school/settings-workflow.html"),
    ]
    cards = "".join(
        f'<a class="card card-hover mod" href="{h}"><h4><span class="sec-ic" style="width:28px;height:28px;border-radius:8px">{icon(ic)}</span>{t}</h4>'
        f'<p class="fs13 sub mb8">{d}</p><ul>{"".join(f"<li>{x}</li>" for x in tags)}</ul></a>'
        for ic, t, d, tags, h in mods)
    return f'<div class="grid g3">{cards}</div>'


def flows():
    life = [("01", "新建备案", "学生 / 教师发起，重复检查，三级审核后建档"), ("02", "正常运行", "账号主库统一管理，驾驶舱实时统计"),
            ("03", "人员交接", "换届时变更负责人，历史任期保留"), ("04", "信息变更", "名称、归属、教师等变更留痕"),
            ("05", "年度年审", "继承数据，只确认本年变化"), ("06", "异常整改", "僵尸号预警与整改闭环"),
            ("07", "账号注销", "只改状态，不删除数据"), ("08", "历史归档", "档案、年审、变更、日志永久可追溯")]
    life_html = "".join(f'<div class="life-item"><div class="life-no">{n}</div><b>{t}</b><p>{d}</p></div>' for n, t, d in life)

    def lanes(rows):
        out = []
        for who, color, nodes in rows:
            out.append(f'<div class="lane"><div class="lane-hd"><span class="legend-dot" style="background:{color}"></span>{who}</div><div class="lane-bd">{nodes}</div></div>')
        return "".join(out)

    def nd(t, cls="", href=None):
        if href:
            return f'<a class="node {cls}" href="{href}">{t}</a>'
        return f'<span class="node {cls}">{t}</span>'
    arrow = f'<span class="scn-arrow">{icon("arrow-right", 14)}</span>'
    annual = lanes([
        ("学校管理员", "#006DAD", nd("创建年度任务：7 个时间节点 / 要求 / 僵尸号参数", "start", "pc/school/annual-task-create.html") + arrow + nd("系统按在册账号自动生成年审记录", "", "pc/school/annual-task-detail.html")),
        ("学生用户", "#2A8DC7", nd("确认账号存在、运营、访问、发布时间、负责人、名称、是否注销、异常", "", "app/student/annual-fill.html") + arrow + nd("上传主页截图并提交", "", "app/student/annual-result.html")),
        ("业务教师", "#E6A23C", nd("通过 / 退回修改 / 修改后确认 / 标记疑似僵尸号 / 要求整改 / 建议注销", "", "pc/teacher/review-annual.html")),
        ("学院管理员", "#67C23A", nd("查看本院完成情况", "", "pc/college/annual-progress.html") + arrow + nd("全部完成后统一提交校团委", "", "pc/college/annual-submit.html")),
        ("学校管理员", "#006DAD", nd("无异动无风险批量审核；异常、注销、整改、重要变更单独审核", "", "pc/school/annual-review.html") + arrow + nd("年审通过 / 整改 / 不通过", "end", "pc/common/archive-audit.html")),
    ])
    zombie = lanes([
        ("系统", "#9096A2", nd("按规则自动预警（停更阈值后台可配）", "start", "pc/school/zombie.html")),
        ("学生或教师", "#E6A23C", nd("核实运营情况并提交说明与佐证", "", "pc/teacher/review-zombie.html")),
        ("学院管理员", "#67C23A", nd("审核核实结果：正常 / 整改 / 注销", "", "pc/college/zombie-verify-detail.html")),
        ("学校管理员", "#006DAD", nd("必要时校团委确认", "cfg", "pc/school/zombie-detail.html") + arrow + nd("处置落地，系统不自动注销", "end", "pc/common/archive-cancel.html")),
    ])
    rectify = lanes([
        ("学校 / 学院", "#67C23A", nd("创建整改任务：问题、要求、责任人、截止时间、附件", "start", "pc/college/rectify-create.html")),
        ("学生或教师", "#2A8DC7", nd("提交整改说明、结果、更新后信息、证明材料", "", "app/student/rectify-submit.html")),
        ("审核人", "#006DAD", nd("整改通过", "end", "app/college/rectify.html") + nd("继续整改（回到提交）", "cfg", "pc/college/rectify-detail.html") + nd("转注销", "", "pc/common/apply-cancel.html")),
    ])
    return (card("账号全生命周期", f'<div class="life">{life_html}</div>') + '<div class="grid g2 mt16">' +
            card("年度年审流程（泳道）", annual) + card("僵尸号排查与整改闭环", zombie + '<div class="divider"></div>' + rectify) + "</div>")


def audits():
    A = f'<span class="scn-arrow">{icon("arrow-right", 12)}</span>'

    def n(t, cls=""):
        return f'<span class="node {cls}">{t}</span>'
    rows = [
        ("新建账号备案", "学生、教师、学院管理员", [n("具体负责教师"), n("学院管理员"), n("校团委审核")], "建立正式账号档案", "app/student/apply.html"),
        ("账号名称变更", "学生、教师", [n("具体负责教师"), n("学院管理员"), n("校团委审核")], "更新账号信息并留痕", "app/student/apply-change.html"),
        ("所属组织变更", "学生、教师", [n("具体负责教师"), n("学院管理员"), n("校团委审核")], "更新归属关系", "pc/common/apply-change.html"),
        ("负责人变更", "学生、教师", [n("具体负责教师"), n("按学院配置", "cfg"), n("原则上无需", "none")], "更新当前负责人并保留历史", "app/student/apply-handover.html"),
        ("账户信息更新", "学生、教师", [n("具体负责教师"), n("按学院配置", "cfg"), n("原则上无需", "none")], "更新日常维护信息", "pc/common/apply-change.html"),
        ("账号注销", "学生、教师、学院管理员", [n("具体负责教师"), n("学院管理员"), n("校团委审核")], "账号转为已注销", "pc/common/apply-cancel.html"),
        ("年度年审", "学生或教师代办", [n("具体负责教师"), n("学院管理员"), n("校团委审核")], "通过、整改或不通过", "app/student/annual-fill.html"),
        ("“僵尸号”核实", "学生、教师", [n("具体负责教师"), n("学院管理员"), n("必要时校团委", "cfg")], "正常、整改或注销", "pc/teacher/review-zombie.html"),
        ("整改反馈", "学生、教师", [n("学院审核"), n("学院管理员"), n("按整改层级", "cfg")], "整改通过或继续整改", "app/student/rectify-submit.html"),
    ]
    body = table(["业务事项", "发起人", "审核节点（一审 → 二审 → 校级）", "最终结果", "演示"], [
        [f"<b>{b}</b>", who, f'<div class="flex gap6 wrap">{A.join(nodes)}</div>', tag(res, "success"), f'<a class="link" href="{h}">查看</a>']
        for b, who, nodes, res, h in rows])
    legend = (f'<div class="flex gap16 mt12 small muted wrap"><span class="flex gap6"><span class="node cfg" style="height:22px">虚线橙色</span>节点可在后台配置（审核流程配置）</span>'
              f'<span class="flex gap6"><span class="node none" style="height:22px">灰色</span>原则上无需该节点</span>'
              f'<a class="link" href="pc/school/settings-workflow.html">打开审核流程配置页 →</a></div>')
    branches = card("每个审核节点的分支（闭环设计）", f"""<div class="grid g4">
  <div>{tag('通过', 'success')}<div class="fs13 sub mt8">进入下一节点；最后节点通过后状态生效（建档 / 更新 / 注销）</div></div>
  <div>{tag('退回修改', 'warning')}<div class="fs13 sub mt8">发起人收到待办，按意见修改后重提，回到原节点</div></div>
  <div>{tag('驳回', 'danger')}<div class="fs13 sub mt8">不予办理，流程终止，发起人可见驳回原因</div></div>
  <div>{tag('特殊分支', 'primary')}<div class="fs13 sub mt8">年审：修改后确认 / 标记僵尸号 / 要求整改 / 建议注销；整改：继续整改 / 转注销</div></div>
</div>""")
    return card("业务审核流程表", body + legend) + '<div class="mt16"></div>' + branches


def statuses():
    cols = [
        ("运行状态", "账号实际运营情况", RUN_STATUS), ("备案状态", "备案业务所处阶段", FILING_STATUS),
        ("年度年审状态", "当年年审流转节点", ANNUAL_STATUS), ("年度异动类型", "年度工作报告分类统计口径", CHANGE_TYPES),
    ]
    html = "".join(f'<div class="card card-bd st-col"><h4>{t}</h4><p>{d}</p><div class="tags">{"".join(st(x) for x in items)}</div></div>'
                   for t, d, items in cols)
    return (alert("不得用一个“状态”字段表示账号全部业务情况，至少区分以下四种状态；“疑似僵尸号”是账号的风险状态，不是单独的数据表。", "info") +
            f'<div class="grid g4 mt16">{html}</div>')


def directory():
    out = []
    n = 0
    for g in GROUPS:
        cards = []
        for f, t, d in g["pages"]:
            n += 1
            path = f'{g["dir"]}/{f}'
            cards.append(f'<a class="pg" href="{path}"><span class="pg-no">{n}</span><div class="grow"><b>{t}</b><span>{d}</span></div><code>{f}</code></a>')
        out.append(f'<div class="dir-hd"><span class="entry-ic" style="background:{g["color"]}">{icon(g["ic"])}</span>'
                   f'<div><h3>{g["term"]} · {g["role"]}</h3><div class="small muted">{g["desc"]}</div></div>'
                   f'<span class="cnt">{len(g["pages"])} 页 · {g["dir"]}/</span></div><div class="grid g2">{"".join(cards)}</div>')
    return "".join(out)


def build():
    body = (hero() +
            sec("entry", "grid", "演示入口", "一键进入各角色工作台，卡片内为实时页面预览", entries()) +
            sec("scenario", "route", "演示剧本", "8 条业务路线贯穿学生、教师、学院、学校四类角色，按编号依次点击即可完整演示闭环", scenarios()) +
            sec("role", "users", "角色权限", "系统用户角色、数据范围与功能权限矩阵（依据《业务说明》第五章）", roles()) +
            sec("feature", "layers", "功能清单", "第一期建设范围核心功能模块，点击卡片查看对应页面", features()) +
            sec("flow", "trending", "业务流程", "账号全生命周期与年审、僵尸号、整改三条关键流程，节点可点击查看页面", flows()) +
            sec("audit", "file-check", "审核流程", "9 类业务的审核节点，具体业务是否需要校级审核支持后台配置", audits()) +
            sec("status", "tag", "状态体系", "运行、备案、年审、异动四套状态分开记录，统一配色", statuses()) +
            sec("pages", "list", "页面目录", "按“终端 · 角色”分类存放，每行两个页面入口", directory()) +
            '<footer class="foot">中南大学团学组织新媒体平台管理系统 · 高保真交互原型 · 图片素材来自 Unsplash · 模拟数据仅供演示</footer>')
    write("index.html", "原型页面导航", body, CSS)
