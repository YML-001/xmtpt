"""PC 端 · 业务教师（辅导员 / 社团指导教师）页面。

视角：王晓琳（计算机学院宣传工作辅导员，兼 2021 级辅导员、计院街舞社指导教师，体现“一人多身份”），
仅能查看本人被授权的 18 个账号；负责本人范围内学生申请、年审、整改、僵尸号核实的第一道审核，以及代办。
"""
from base import *  # noqa: F401,F403
from data import ACCOUNTS as A, FLOWS as F, PEOPLE as P, ANNUAL_TASK as T, UPDATE_FREQ

D = "pc/teacher/"
HOME = ("教师工作台", "workbench.html")

CSS = """
/* ===== 教师端：工作台问候区 ===== */
.t-hero{display:flex;align-items:center;gap:20px;padding:22px 24px;border-radius:12px;color:#fff;position:relative;overflow:hidden;
  background:linear-gradient(120deg,#2A86CF 0%,#0E5E9E 55%,#0A416F 100%);box-shadow:0 8px 24px rgba(14,94,158,.18)}
.t-hero::after{content:"";position:absolute;right:180px;top:-90px;width:260px;height:260px;border-radius:50%;background:rgba(255,255,255,.06)}
.t-hero>*{position:relative;z-index:1}
.t-hero .avatar{box-shadow:0 0 0 3px rgba(255,255,255,.35)}
.t-hero h1{font-size:22px;font-weight:700;line-height:1.3}
.t-hero .sub-line{font-size:13px;opacity:.82;margin-top:4px}
.id-tag{display:inline-flex;align-items:center;gap:6px;height:28px;padding:0 12px;border-radius:14px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.24);font-size:12px;color:#fff}
.id-tag b{font-weight:600}
a.id-tag:hover{background:rgba(255,255,255,.24)}
.t-dead{margin-left:auto;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);border-radius:12px;padding:14px 18px;min-width:250px;flex:none}
.t-dead .big{font-size:30px;font-weight:700;line-height:1.15;font-variant-numeric:tabular-nums}
.t-dead .progress{background:rgba(255,255,255,.2)}.t-dead .progress>i{background:#FFD27A}
/* ===== 待审分类磁贴 ===== */
.cat-grid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:12px}
.cat-tile{display:flex;flex-direction:column;gap:10px;padding:16px;border:1px solid var(--c-line);border-radius:10px;background:#fff;transition:border-color .15s,box-shadow .15s,transform .15s}
.cat-tile:hover{border-color:var(--c-primary-border);box-shadow:var(--shadow-lg);transform:translateY(-1px)}
.cat-tile .n{font-size:26px;font-weight:700;line-height:1;font-variant-numeric:tabular-nums}
.cat-tile .d{font-size:12px;color:var(--c-text-3);min-height:18px}
.tic{width:36px;height:36px;border-radius:10px;display:grid;place-items:center;background:var(--c-primary-light);color:var(--c-primary);flex:none}
.tic.orange{background:var(--c-warning-bg);color:var(--c-warning)}.tic.green{background:var(--c-success-bg);color:var(--c-success)}
.tic.red{background:var(--c-danger-bg);color:var(--c-danger)}.tic.purple{background:#F0EDFB;color:#6B5BD2}.tic.gray{background:var(--c-muted-bg);color:var(--c-muted)}
.u-item{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--c-line)}
.u-item:last-child{border-bottom:none}.u-item:hover .bold{color:var(--c-primary)}
.qa{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.qa a{display:flex;align-items:center;gap:10px;padding:12px;border-radius:10px;background:var(--c-bg);font-size:13px;transition:background .15s}
.qa a:hover{background:var(--c-primary-light);color:var(--c-primary)}
.m-hint{display:flex;align-items:center;gap:14px;padding:14px 16px;border-radius:10px;background:linear-gradient(120deg,#F0EDFB,#E3F1F9);border:1px solid #DCD6F5}
/* ===== 审核页通用 ===== */
.rv-head{display:flex;align-items:center;gap:16px;padding:18px 20px}
.rv-head h2{font-size:18px;font-weight:700}
.rv-meta{display:flex;flex-wrap:wrap;gap:4px 20px;font-size:13px;color:var(--c-text-3);margin-top:6px}
.rv-meta b{color:var(--c-text);font-weight:500}
.intro-box{padding:12px 14px;border-radius:8px;background:#F7F9FB;border:1px solid var(--c-line);font-size:13px;line-height:1.85;color:var(--c-text-2)}
.intro-box.warn{background:var(--c-warning-bg);border-color:var(--c-warning-bd);color:#8A5300}
.intro-box.ok{background:var(--c-success-bg);border-color:var(--c-success-bd);color:#0E6B45}
.intro-hd{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:8px}
.mech{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.mech>div{padding:12px;border:1px solid var(--c-line);border-radius:8px;display:flex;flex-direction:column;gap:8px;font-size:13px}
.mech>div.bad{border-color:var(--c-danger-bd);background:var(--c-danger-bg)}
.op-chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.op-chips button{height:26px;padding:0 10px;border-radius:13px;background:var(--c-bg);color:var(--c-text-2);font-size:12px;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.op-chips button:hover{background:var(--c-primary-light);color:var(--c-primary)}
.who{display:flex;align-items:center;gap:12px}
.who .avatar{width:44px;height:44px}
.person{flex:1;min-width:0;border:1px solid var(--c-line);border-radius:12px;padding:16px 18px;display:flex;flex-direction:column;gap:14px}
.person.old{background:#FAFBFC}
.person.new{border-color:var(--c-success-bd);background:linear-gradient(180deg,#F2FCF7,#fff 60%)}
.arrow-c{width:46px;height:46px;border-radius:50%;display:grid;place-items:center;background:var(--c-primary);color:#fff;flex:none;box-shadow:0 6px 16px rgba(42,141,199,.3)}
.shot{border-radius:10px;overflow:hidden;border:1px solid var(--c-line);position:relative;background:#0B0F14}
.shot img{width:100%;height:230px;object-fit:cover;opacity:.95}
.shot span{position:absolute;left:10px;bottom:10px;height:24px;padding:0 10px;border-radius:12px;background:rgba(0,0,0,.55);color:#fff;font-size:12px;display:inline-flex;align-items:center;gap:4px}
.rule{padding:12px 14px;border-radius:8px;border:1px solid var(--c-danger-bd);background:var(--c-danger-bg);display:flex;gap:10px}
.rule .i{color:var(--c-danger);margin-top:3px}
.rule.off{border-color:var(--c-line);background:#FAFBFC}.rule.off .i{color:var(--c-text-3)}
.choice .grow small{display:block;font-size:12px;color:var(--c-text-3);font-weight:400;margin-top:2px}
.choice b{font-size:14px}
.btn-warn-solid{background:var(--c-warning);color:#fff}.btn-warn-solid:hover{background:#D98200}
.cmp-hd,.cmp-row{display:grid;grid-template-columns:minmax(0,1fr) 40px minmax(0,1fr);align-items:stretch}
.cmp-hd>div{padding:10px 14px;font-weight:600;font-size:13px;border-radius:8px 8px 0 0}
.cmp-hd .l{background:#F2F7FC;color:var(--c-text-2)}.cmp-hd .r{background:var(--c-success-bg);color:#0E8A55}
.cmp-row{border-bottom:1px dashed var(--c-line)}.cmp-row:last-child{border-bottom:none}
.cmp-row>div{padding:14px;font-size:13px;display:flex;flex-direction:column;gap:6px}
.cmp-row .mid{align-items:center;justify-content:center;color:var(--c-text-3);padding:0}
.lbl{font-size:12px;color:var(--c-text-3)}
.case{padding:14px;border-radius:10px;background:var(--c-bg);display:flex;flex-direction:column;gap:8px;border:1px solid transparent}
.case.on{background:var(--c-primary-light);border-color:var(--c-primary-border)}
.px-banner{display:flex;align-items:center;gap:14px;padding:14px 18px;border-radius:10px;border:1px solid var(--c-primary-border);
  background:linear-gradient(120deg,#E3F1F9 0%,#F4F9FD 100%)}
.px-banner .tic{width:42px;height:42px;background:var(--c-primary);color:#fff}
.msg{display:flex;gap:14px;padding:16px 20px;border-bottom:1px solid var(--c-line);transition:background .15s}
.msg:last-child{border-bottom:none}.msg:hover{background:#F7FBFE}
.msg-t{font-weight:600;display:flex;align-items:center;gap:8px}
.msg.unread .msg-t::after{content:"";width:7px;height:7px;border-radius:50%;background:var(--c-danger)}
.side-kv{display:grid;grid-template-columns:72px minmax(0,1fr);gap:8px 12px;font-size:13px}
.side-kv dt{color:var(--c-text-3)}.side-kv dd{color:var(--c-text);word-break:break-all}
.ck-ok{color:var(--c-success);display:inline-flex;align-items:center;gap:4px;font-size:13px}
.ck-bad{color:var(--c-danger);display:inline-flex;align-items:center;gap:4px;font-size:13px;font-weight:500}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px;color:var(--c-text-2)}
/* 右侧信息栏超出视口时内部滚动，避免意见框被遮挡 */
.split>.sticky{max-height:calc(100vh - 160px);overflow-y:auto;scrollbar-width:thin;padding-bottom:2px}
.legend-item .grow{white-space:nowrap}
"""

# 常用意见：点击后填入所在卡片的意见输入框
JS = """
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-fill]');if(!b)return;
  var box=b.closest('.card');var ta=box&&box.querySelector('textarea');
  if(ta){ta.value=b.dataset.fill;ta.focus();var tip=ta.parentElement.querySelector('.count-tip');if(tip&&ta.maxLength>0)tip.textContent=ta.value.length+' / '+ta.maxLength;}
});
"""

# 一人多身份：授权来源（身份）与账号范围
SCOPES = [
    ("xc", "宣传工作辅导员", "院级组织与学院社团", 12, "users"),
    ("fdy", "2021级辅导员", "2021级各团支部（历史账号清理）", 4, "user"),
    ("jws", "计院街舞社指导教师", "计院街舞社", 2, "star"),
]
SCOPE_NAME = {k: n for k, n, _, _, _ in SCOPES}

# 待审 7 类：(分类值, 名称, 图标, 颜色, 数量, 审核页, 摘要)
CATS = [
    ("xj", "新建申请", "file-add", "", 1, "review-create.html", "中南计算机青年 · 重新提交"),
    ("bg", "变更申请", "file-edit", "orange", 1, "review-change.html", "计算机学院学生会改名"),
    ("jj", "负责人交接", "user-switch", "green", 1, "review-handover.html", "计院街舞社 李明→李四"),
    ("zx", "注销申请", "ban", "gray", 1, "review-cancel.html", "2022级人工智能2班团支部"),
    ("ns", "年审材料", "calendar", "purple", 3, "review-annual.html", "含 2 条无异动可批量"),
    ("js", "僵尸号核实", "ghost", "red", 1, "review-zombie.html", "停更 412 天 · 待核实"),
    ("zg", "整改材料", "wrench", "orange", 1, "review-rectify.html", "计院摄影协会"),
]


# ---------------------------------------------------------------- 通用小组件
def page(file, active, title, crumbs, content):
    pc_page(D + file, "teacher", active, title, [HOME] + crumbs, content, css=CSS, js=JS)


def go(text, href, kind="primary", ic=None, toast=None, size="", extra_cls=""):
    """先提示再跳转的按钮（<a> 带 data-toast 会被拦截，故用 data-href）。"""
    cls = f"btn btn-{kind}" + (f" btn-{size}" if size else "") + (f" {extra_cls}" if extra_cls else "")
    t = f' data-toast="{esc(toast)}"' if toast else ""
    return f'<button class="{cls}" type="button" data-href="{href}"{t}>{icon(ic) if ic else ""}{text}</button>'


def left_tag(days):
    kind = "danger" if days <= 1 else ("warning" if days <= 5 else "muted")
    return tag(f"剩 {days} 天", kind, True)


def head_card(platform, name, tags_html, metas, extra="", cls=""):
    meta = "".join(f"<span>{k}：<b>{v}</b></span>" for k, v in metas)
    return (f'<div class="card rv-head {cls}">{pf(platform, "lg")}<div class="grow"><div class="flex gap8 wrap"><h2>{name}</h2>{tags_html}</div>'
            f'<div class="rv-meta">{meta}</div></div>{extra}</div>')


def who_card(name, sub, rows, title="申请人信息", extra="", cls=""):
    items = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows)
    body = (f'<div class="who">{avatar(name)}<div class="grow"><div class="fs16 bold">{name}</div><div class="small muted">{sub}</div></div>{extra}</div>'
            f'<div class="divider" style="margin:14px 0"></div><dl class="side-kv">{items}</dl>')
    return card(title, body, cls=cls)


def flow_done(key, n, states=None):
    """取 FLOWS[key] 前 n 步作为已发生节点；states 可把某步标记为 back / reject。"""
    out = []
    for i, (tm, who, title, cm) in enumerate(F[key]["steps"][:n]):
        out.append(((states or {}).get(i, "done"), title, f"{who} · {tm}", cm))
    return out


def flow_card(items, cls="", extra=""):
    return card("审核流程", timeline(items), extra, cls=cls)


def opinion_card(quick, val="", ph="请填写审核意见，退回或驳回时必填", cls="", title="审核意见"):
    chips_html = "".join(f'<button type="button" data-fill="{esc(q)}" data-toast="已填入常用意见">{q}</button>' for q in quick)
    body = (f'{textarea(ph, val, maxlen=300, rows=4)}<div class="small muted mt8">常用意见</div>'
            f'<div class="op-chips">{chips_html}</div>')
    return card(title, body, cls=cls)


def review_layout(left, right, bar):
    return (f'<div class="split"><div class="col gap16">{"".join(left)}</div>'
            f'<div class="sticky col gap16">{"".join(right)}</div></div>{bar}')


def actbar(note, buttons, cls=""):
    return f'<div class="actbar {cls}"><div class="grow flex gap6">{icon("info")}{note}</div>{buttons}</div>'


def files(*names):
    return '<div class="upload-list" style="margin-top:0">' + "".join(
        f'<button class="file-chip" type="button" data-toast="正在预览：{esc(n)}">{icon("file")}{n}</button>' for n in names) + "</div>"


# ---------------------------------------------------------------- 工作台
def workbench():
    ids = "".join(f'<span class="id-tag">{icon(ic, 14)}<b>{n}</b>· {s} · {c} 个账号</span>' for _, n, s, c, ic in SCOPES)
    hero = f"""
<div class="t-hero">
  {avatar('王晓琳', 'lg')}
  <div class="grow">
    <h1>王晓琳老师，下午好</h1>
    <div class="sub-line">计算机学院 · 工号 {P['王晓琳']['no']} · 您当前有 9 项待审核事项，其中 4 项将在 3 天内到期</div>
    <div class="flex gap8 wrap mt12">{ids}<a class="id-tag" href="../common/identity-switch.html">{icon('swap', 14)}切换身份</a></div>
  </div>
  <div class="t-dead">
    <div class="small" style="opacity:.8">{T['year']} 年度年审 · 教师审核截止 {T['teacher_end']}</div>
    <div class="flex gap8 mt4" style="align-items:baseline"><span class="big">25</span><span class="small">天后截止</span></div>
    <div class="flex gap8 mt8">{progress(58)}<span class="small num">7 / 12</span></div>
    <div class="small mt4" style="opacity:.75">学生已提交 12 个，您已审核 7 个</div>
  </div>
</div>"""
    stats = "".join([
        stat("负责账号总数", "18", "3 个身份授权范围", "database", href="accounts.html"),
        stat("待审核数", "9", "4 项 3 天内到期", "inbox", "orange", href="todo.html"),
        stat("已完成数", "27", "本年度 · 通过 21 项", "check-circle", "green", href="done.html"),
        stat("疑似僵尸号数", "2", "1 项待本人核实", "ghost", "red", href="review-zombie.html"),
        stat("待整改数", "1", "计院摄影协会 · 材料待审", "wrench", "orange", href="review-rectify.html"),
    ])
    tiles = "".join(
        f'<a class="cat-tile" href="{h}"><div class="flex between"><span class="tic {c}">{icon(ic)}</span>{icon("chevron-right")}</div>'
        f'<div><div class="small sub">{n}</div><div class="n mt4">{cnt}</div></div><div class="d ellipsis">{d}</div></a>'
        for _, n, ic, c, cnt, h, d in CATS)
    urgent = [
        ("新建备案 · 中南计算机青年", "李明 · 2026-09-26 20:05 重新提交 · 已补充平台介绍", "file-add", "", 1, "review-create.html"),
        ("负责人交接 · 计院街舞社（李明 → 李四）", "拟 2026-10-01 生效，需在生效前完成审核", "user-switch", "green", 1, "review-handover.html"),
        ("名称变更 · 计算机学院学生会 → 中南计院学生会", "重要变更 · 教师通过后报学院、校团委", "file-edit", "orange", 2, "review-change.html"),
        ("僵尸号核实 · 2021级软件工程1班团支部", "系统预警：停更 412 天 · 团支部已毕业", "ghost", "red", 3, "review-zombie.html"),
    ]
    urgent_html = "".join(
        f'<a class="u-item" href="{h}"><span class="tic {c}">{icon(ic)}</span><div class="grow"><div class="bold fs13">{t}</div>'
        f'<div class="small muted">{m}</div></div>{left_tag(d)}{icon("chevron-right")}</a>' for t, m, ic, c, d, h in urgent)
    annual_body = (steps(["任务发布 09-15", "学生填报 10-15", "教师审核 10-25", "学院审核 11-05", "学校审核 11-20"], 1)
                   + '<div class="mt16">' + alert(f'<b>教师审核截止 {T["teacher_end"]}</b>：本人负责 18 个账号中学生已提交 12 个，已审核 7 个，'
                                                  '待审 3 个，退回 / 整改 2 个，学生未提交 6 个。', "warning", "clock") + '</div>'
                   + f'<div class="flex gap8 mt12">{btn("审核年审材料", "review-annual.html", "primary", "calendar", "sm")}'
                     f'{btn("催未提交学生", None, "default", "bell", "sm", toast="已向 6 个未提交账号的学生负责人发送填报提醒")}</div>')
    quick = "".join(f'<a href="{h}"><span class="tic {c}">{icon(ic)}</span><div><div class="bold">{t}</div><div class="small muted">{d}</div></div></a>'
                    for t, d, ic, c, h in [
                        ("发起新建", "为本人范围组织新建备案", "file-add", "", "../common/apply-create-basic.html"),
                        ("教师代办", "学生毕业 / 失联时代办", "hand", "orange", "proxy.html"),
                        ("我负责的账号", "18 个账号 · 3 个身份", "database", "green", "accounts.html"),
                        ("已审核记录", "本年度 27 项", "file-check", "purple", "done.html"),
                    ])
    mobile = (f'<div class="m-hint"><span class="tic purple">{icon("smartphone")}</span><div class="grow"><div class="bold fs13">移动端同样支持审核</div>'
              f'<div class="small muted">新建、变更、交接、年审、僵尸号核实均可在手机上完成</div></div>'
              f'{btn("打开移动端", "../../app/teacher/home.html", "light", size="sm")}</div>')
    recent = timeline([
        ("done", "审核通过 · 中南计算机青年（新建）", "2026-09-27 11:20", F["new"]["steps"][3][3]),
        ("back", "退回修改 · 中南计算机青年（新建）", "2026-09-25 09:30", F["new"]["steps"][1][3]),
        ("done", "年审通过 · 2023级软件工程2班团支部", "2026-09-24 15:02", "无异动，信息完整。"),
        ("done", "交接生效 · 计院羽毛球协会", "2026-09-21 10:18", "同意交接，原负责人任期记入历史。"),
    ])
    content = f"""
{hero}
<div class="grid g5 mt16">{stats}</div>
{card('待我审核', f'<div class="cat-grid">{tiles}</div>', btn('全部待审', 'todo.html', 'text', size='sm'), cls='mt16')}
<div class="grid mt16" style="grid-template-columns:3fr 2fr">
  {card('临近截止', urgent_html, btn('去处理', 'todo.html', 'text', size='sm'))}
  {card('快捷操作', f'<div class="qa">{quick}</div><div class="mt12">{mobile}</div>')}
</div>
<div class="grid mt16" style="grid-template-columns:3fr 2fr">
  {card(f"{T['year']} 年度年审进度", annual_body)}
  {card('负责账号运行概况', donut([('正常运行', 11), ('申请注销', 3), ('不活跃', 2), ('整改中', 1), ('备案申请中', 1)], 18, '负责账号'), btn('查看账号', 'accounts.html', 'text', size='sm'))}
</div>
{card('最近审核动态', recent, btn('已审核记录', 'done.html', 'text', size='sm'), cls='mt16')}"""
    page("workbench.html", "workbench", "教师工作台", [("工作台", None)], content)


# ---------------------------------------------------------------- 审核页：新建备案（剧本一）
INTRO_V1 = "中南计算机青年是计算机学院团委新媒体中心运营的官方公众号，主要发布本学院团学活动通知、青年榜样故事和学术科创资讯，欢迎广大同学积极关注。"
INTRO_V2 = ("“中南计算机青年”是中南大学计算机学院团委指导、学院团委新媒体中心具体运营的官方微信公众号，定位为学院共青团思想引领和青年服务的主阵地。"
            "平台围绕“思想引领、学风建设、科创实践、青春风采”四条主线开展内容建设，设置四个固定栏目："
            "“青年学习社”推送习近平新时代中国特色社会主义思想学习、主题团日与团课内容；"
            "“科创前沿”介绍学院竞赛获奖、科研团队与学术讲座；"
            "“榜样力量”讲述优秀学生、志愿者和毕业生故事；"
            "“院团通知”发布团学工作通知、活动报名与评优公示。"
            "信息发布范围限于计算机学院团学工作相关内容，不发布任何商业广告及与学院无关的转载信息。"
            "平台严格执行“先审后发”三级审核，由学生编辑初审、新媒体中心主任复审、指导教师终审后发布，计划每周更新不少于两次推送。")
MECHS = ["团学组织宣传联动工作机制", "信息发布审查机制", "应急预案处理机制", "信息安全管理制度"]


def mech_grid(bad=()):
    out = []
    for m in MECHS:
        if m in bad:
            out.append(f'<div class="bad"><span class="bold">{m}</span>{tag("未建立", "danger", True)}</div>')
        else:
            out.append(f'<div><span class="bold">{m}</span>{tag("已建立", "success", True)}</div>')
    return f'<div class="mech">{"".join(out)}</div>'


def review_create():
    a = A["new"]
    ver = ('<div class="seg" data-single=".v-ver"><button type="button" class="on" data-choice=".v-first">首次提交 · 09-24</button>'
           '<button type="button" data-choice=".v-resub">重新提交 · 09-26</button></div>')
    demo = (f'<div class="alert alert-info" style="align-items:center">{icon("info")}<div class="grow"><b>演示说明：</b>'
            f'首次审核选择退回；学生重提后再次进入本页选择通过。切换右侧页签查看两次提交的差异。</div>{ver}</div>')
    head = head_card(a["platform"], a["name"],
                     tag("新建备案") + st(a["filing"]) + '<span class="v-ver v-first">' + tag("第 1 次提交", "muted") + '</span>'
                     + '<span class="v-ver v-resub hidden">' + tag("第 2 次提交 · 已按意见修改", "success") + '</span>',
                     [("申请编号", F["new"]["no"]), ("平台 ID", a["pid"]), ("平台层级", a["level"]), ("申请人", a["student"])],
                     left_tag(1))
    dup = alert('<b>重复检查通过：</b>未发现同平台同 ID（csu_cs_youth）账号；名称与已备案账号“中南计院团委”相似度 58%，'
                '申请人已确认二者为不同账号。 <a class="link" href="../common/apply-similar.html">查看比对详情</a>', "success", "shield")
    belong = card("归属信息", kv([("所属学校", "中南大学"), ("所属学院", "计算机学院"), ("所属团学组织", a["org"]),
                              ("组织类别", a["org_type"]), ("平台层级", a["level"]), ("上级团组织", "计算机学院团委")]))
    intro_v1 = (f'<div class="v-ver v-first"><div class="intro-hd"><span class="field-label">平台介绍</span>'
                f'{tag(icon("alert", 12) + str(len(INTRO_V1)) + " 字，少于 100 字要求", "warning")}</div>'
                f'<div class="intro-box warn">{INTRO_V1}</div>'
                f'<div class="small c-warning mt8">缺少内容定位、栏目设置和信息发布范围说明，不满足“平台介绍不少于 100 字”的填报要求。</div></div>')
    intro_v2 = (f'<div class="v-ver v-resub hidden"><div class="intro-hd"><span class="field-label">平台介绍</span>'
                f'<div class="flex gap6">{tag(str(len(INTRO_V2)) + " 字 · 符合要求", "success")}{tag("已修改", "warning")}</div></div>'
                f'<div class="intro-box ok">{INTRO_V2}</div></div>')
    scope = ('<div class="mt16"><div class="field-label mb8">信息发布范围</div>'
             '<div class="v-ver v-first intro-box">学院团学活动相关信息。</div>'
             '<div class="v-ver v-resub hidden intro-box ok">限于计算机学院团学工作相关内容：思想引领、团学活动、学术科创、评优公示；不发布商业广告及无关转载。</div></div>')
    platform = card("平台信息", kv([
        ("平台类型", f'<span class="flex gap6">{pf(a["platform"], "sm")}{a["platform"]}</span>'), ("账号名称", a["name"]), ("曾用名", "—"),
        ("平台 ID", f'{a["pid"]} <button class="link small" type="button" data-copy="{a["pid"]}">复制</button>'),
        ("是否认证", "是（中南大学计算机学院）"), ("粉丝数", "1,056"), ("开通时间", a["opened"]), ("运营团队规模", "8 人"),
        ("主页链接", '<span class="link">mp.weixin.qq.com/csu_cs_youth</span>'),
    ]) + f'<div class="divider"></div>{intro_v1}{intro_v2}{scope}'
       + f'<div class="mt16"><div class="field-label mb8">四项机制</div>{mech_grid()}</div>')
    run = card("运行信息", kv([("更新频率", UPDATE_FREQ[0]), ("主要栏目", "青年学习社 / 科创前沿 / 榜样力量 / 院团通知"),
                            ("内容来源", "原创为主，转载须注明来源"), ("二维码", "已上传"), ("备注", "—", True)]))
    staff = card("责任人员", kv([("第一责任人", "张卫东（学院党委副书记）"), ("管理教师", "王晓琳（宣传工作辅导员）"),
                              ("学生负责人", f'李明（{P["李明"]["no"]} · {P["李明"]["phone"]}）'),
                              ("学生管理员", "陈子墨、刘佳怡"), ("负责人职务", "新媒体中心主任"), ("所在班级", P["李明"]["grade"])]))
    audit = card("审核信息", kv([("一审教师", "王晓琳（学生自选）"), ("审核流程", "指导教师 → 学院团委 → 校团委"), ("审核时限", "每个节点 5 个工作日")])
                 + '<div class="mt16"><div class="field-label mb8">附件材料</div>'
                 + files("新媒体平台备案承诺书.pdf", "四项机制制度汇编.pdf", "账号主页截图.png") + "</div>")
    who = who_card("李明", f'{P["李明"]["grade"]} · 新媒体中心主任',
                   [("学号", P["李明"]["no"]), ("手机", P["李明"]["phone"]), ("所在组织", a["org"]), ("历史申请", "3 次 · 均已办结")],
                   extra=btn("提醒", None, "light", "bell", "sm", toast="已向李明发送站内提醒"))
    wait_tail = [("wait", "学院团委审核", "周建华 · 待流转", ""), ("wait", "校团委审核", "陈静 · 待流转", "")]
    tl1 = flow_done("new", 1) + [("now", "指导教师审核 " + tag("当前", "primary"), "王晓琳 · 剩 1 天", "")] + wait_tail
    tl2 = flow_done("new", 3, {1: "back"}) + [("now", "指导教师再次审核 " + tag("当前", "primary"), "王晓琳 · 剩 1 天", "")] + wait_tail
    s = F["new"]["steps"]
    quick = [s[1][3], s[3][3], "与已备案账号重复开设，不予备案。"]
    bar1 = actbar("首次提交：平台介绍不足 100 字，建议退回修改",
                  btn("驳回", "../common/modal-reject.html", "danger", "x-circle") + btn("审核通过", "../common/modal-approve.html", "ghost", "check")
                  + btn("退回修改", "../common/modal-return.html", "primary", "undo"), "v-ver v-first")
    bar2 = actbar("重新提交：平台介绍已补充至 326 字，信息完整",
                  btn("驳回", "../common/modal-reject.html", "danger", "x-circle") + btn("退回修改", "../common/modal-return.html", "default", "undo")
                  + btn("审核通过", "../common/modal-approve.html", "primary", "check"), "v-ver v-resub hidden")
    content = demo + '<div class="mt16"></div>' + review_layout(
        [head, dup, belong, platform, run, staff, audit],
        [who, flow_card(tl1, "v-ver v-first"), flow_card(tl2, "v-ver v-resub hidden"),
         opinion_card(quick, s[1][3], cls="v-ver v-first"), opinion_card(quick, s[3][3], cls="v-ver v-resub hidden")],
        bar1 + bar2)
    page("review-create.html", "todo", "新建备案审核", [("待我审核", "todo.html"), ("新建备案审核", None)], content)


# ---------------------------------------------------------------- 审核页：信息变更（剧本二）
def review_change():
    a = A["rename"]
    head = head_card(a["platform"], a["name"], tag("信息变更", "warning") + tag("重要变更", "danger") + st(a["filing"]),
                     [("申请编号", F["rename"]["no"]), ("平台 ID", a["pid"]), ("粉丝数", a["fans"]), ("开通时间", a["opened"])], left_tag(2))
    rule = alert("<b>账号名称变更属重要变更：教师→学院→校团委。</b>教师审核通过后流转学院团委审核，再报校团委审核；变更生效后原名称自动记入“曾用名”。", "warning")
    diff = card("变更前后对比", diff_table([
        ("账号名称", a["name"], a["new_name"]), ("平台类型", a["platform"], a["platform"]), ("平台 ID", a["pid"], a["pid"]),
        ("所属团学组织", a["org"], a["org"]), ("平台层级", a["level"], a["level"]), ("学生负责人", "李明", "李明"), ("管理教师", "王晓琳", "王晓琳"),
    ]), tag("变更 1 项", "warning"))
    reason = card("变更原因与材料", kv([("变更原因", F["rename"]["steps"][0][3], True),
                                   ("详细说明", "2026 年 9 月学生会完成换届，经学生会主席团会议决议，学院各新媒体平台统一使用“中南计院”品牌前缀，"
                                            "微博名称同步调整为“中南计院学生会”，账号主体、运营团队与内容定位不变。", True)], 2)
                   + '<div class="mt16"><div class="field-label mb8">佐证材料</div>'
                   + files("学生会换届决议.pdf", "新名称审批表.pdf", "微博改名预览截图.png") + "</div>")
    check = card("系统校验", '<div class="col gap8">'
                 + "".join(f'<div class="flex gap8">{icon("check-circle", cls="c-success")}<span class="grow">{t}</span>{tag(r, "success")}</div>' for t, r in [
                     ("新名称与全校在册账号重名检查", "无重名"), ("新名称敏感词检查", "通过"), ("平台 ID 未变化，按普通变更办理", "符合"),
                     ("新名称包含组织规范简称", "符合")]) + "</div>")
    who = who_card("李明", f'{P["李明"]["grade"]} · 学生会账号负责人',
                   [("学号", P["李明"]["no"]), ("手机", P["李明"]["phone"]), ("所在组织", a["org"]), ("提交时间", F["rename"]["steps"][0][0])])
    tl = flow_done("rename", 1) + [("now", "指导教师审核 " + tag("当前", "primary"), "王晓琳 · 剩 2 天", ""),
                                   ("wait", "学院团委审核", "周建华 · 待流转", ""), ("wait", "校团委审核", "陈静 · 重要变更终审", "")]
    quick = [F["rename"]["steps"][1][3], "新名称不符合命名规范，请修改后重新提交。", "变更材料不完整，请补充换届决议。"]
    bar = actbar("通过后流转至学院审核，生效后原名称记入曾用名",
                 btn("驳回", "../common/modal-reject.html", "danger", "x-circle") + btn("退回修改", "../common/modal-return.html", "default", "undo")
                 + go("审核通过", "../college/approval-change.html", "primary", "check", "已通过，流转至学院审核"))
    content = review_layout([head, rule, diff, reason, check], [who, flow_card(tl), opinion_card(quick, F["rename"]["steps"][1][3])], bar)
    page("review-change.html", "todo", "信息变更审核", [("待我审核", "todo.html"), ("信息变更审核", None)], content)


# ---------------------------------------------------------------- 审核页：负责人交接（剧本三）
def person_card(cls, label, name, sub, rows, badge):
    return (f'<div class="person {cls}"><div class="flex between"><span class="small muted bold">{label}</span>{badge}</div>'
            f'<div class="who">{avatar(name)}<div><div class="fs16 bold">{name}</div><div class="small muted">{sub}</div></div></div>'
            f'{kv(rows, 2)}</div>')


def review_handover():
    a = A["handover"]
    head = head_card(a["platform"], a["name"], tag("负责人交接", "success") + st(a["run"]),
                     [("申请编号", F["handover"]["no"]), ("平台 ID", a["pid"]), ("粉丝数", a["fans"]), ("生效时间", "2026-10-01")], left_tag(1))
    old = person_card("old", "原负责人", "李明", "2023级软件工程2班 · 街舞社原宣传负责人",
                      [("学号", "8209230117"), ("手机", P["李明"]["phone"]), ("任期", "2024-09-10 ~ 2026-09-30", True)], tag("卸任", "muted"))
    new = person_card("new", "新负责人", "李四", f'{P["李四"]["grade"]} · {P["李四"]["job"]}',
                      [("学号", "8209240208"), ("手机", "188 7310 4521"), ("任期", "2026-10-01 起", True)], tag("接任", "success"))
    pair = card("交接双方", f'<div class="flex gap16" style="align-items:center">{old}<span class="arrow-c">{icon("arrow-right", 22)}</span>{new}</div>'
                + '<div class="mt16">' + alert("<b>交接规则：</b>学生提交→具体管理教师审核→生效；原负责人任职起止时间保留，在账号档案“责任人员”中可查询历任记录。") + "</div>")
    items = card("交接事项确认", '<div class="grid g2">' + "".join(
        f'<div class="flex gap8">{icon("check-circle", cls="c-success")}<span class="grow">{t}</span><span class="small muted">{d}</span></div>' for t, d in [
            ("账号登录密码已更换", "李四确认"), ("绑定手机号已变更为新负责人", "平台后台截图"),
            ("运营资料与素材库已移交", "交接清单"), ("新负责人已签署信息安全承诺书", "已上传")]) + "</div>"
        + '<div class="mt16"><div class="field-label mb8">佐证材料</div>' + files("街舞社换届名单.pdf", "交接清单（双方签字）.pdf", "信息安全承诺书-李四.pdf") + "</div>")
    reason = card("交接说明", kv([("交接原因", F["handover"]["steps"][0][3], True), ("生效时间", "2026-10-01 00:00"), ("交接后学生负责人", "李四")], 2))
    who = who_card("李明", "原负责人 · 发起人", [("学号", "8209230117"), ("手机", P["李明"]["phone"]), ("提交时间", F["handover"]["steps"][0][0])])
    tl = flow_done("handover", 1) + [("now", "指导教师审核 " + tag("当前", "primary"), "王晓琳 · 审核通过即生效", ""),
                                     ("wait", "交接生效", "2026-10-01 · 自动更新责任人员", "")]
    bar = actbar("交接由具体管理教师审核，通过后即按生效时间生效",
                 btn("驳回", "../common/modal-reject.html", "danger", "x-circle") + btn("退回修改", "../common/modal-return.html", "default", "undo")
                 + go("通过并生效", "../common/archive-staff.html", "primary", "check", "审核通过，交接将于 2026-10-01 生效，责任人员历史已更新"))
    content = review_layout([head, pair, reason, items],
                            [who, flow_card(tl), opinion_card([F["handover"]["steps"][1][3], "新负责人信息不完整，请补充联系方式。"], F["handover"]["steps"][1][3])], bar)
    page("review-handover.html", "todo", "负责人交接审核", [("待我审核", "todo.html"), ("负责人交接审核", None)], content)


# ---------------------------------------------------------------- 审核页：注销申请
def review_cancel():
    head = head_card("抖音", "2022级人工智能2班团支部", tag("注销申请", "danger") + st("申请注销"),
                     [("申请编号", "ZX20260928004"), ("平台 ID", "csu_ai2202"), ("平台层级", "三级平台"), ("粉丝数", "412")], left_tag(4))
    reason = card("注销原因", kv([("注销原因", tag("重复账号", "danger")), ("最近发布", "2026-05-18"), ("开通时间", "2022-10-11"),
                               ("注销说明", "本团支部先后开设两个抖音账号，2024 年起统一使用“AI2202团支部”（ID csu_ai2202_new，已备案）运营，"
                                        "本账号已停止发布并在简介中公告迁移，现申请注销。", True)]))
    cmp_rows = kv([("本账号", "csu_ai2202 · 粉丝 412 · 停更 135 天"), ("保留账号", "csu_ai2202_new · 粉丝 1,208 · 正常运行"),
                   ("所属组织", "同为 2022级人工智能2班团支部"), ("系统比对", tag("同组织同平台重复", "warning"))], 2)
    evidence = card("佐证核验", cmp_rows + '<div class="divider"></div><div class="col gap8">' + "".join(
        f'<div class="flex gap8">{icon("check-circle", cls="c-success")}<span class="grow">{t}</span>{tag("已核验", "success")}</div>'
        for t in ["同一主体重复开设，保留账号已正常备案", "本账号已发布停更迁移公告", "本账号无未完成的年审、整改事项", "团支部大会决议同意注销"])
        + '</div><div class="mt16"><div class="field-label mb8">佐证材料</div>'
        + files("团支部大会决议.pdf", "两账号主页截图对比.png", "停更迁移公告截图.png") + "</div>")
    keep = alert("<b>注销后不删除：</b>账号状态转为“已注销”，档案、历任责任人、年审记录与操作日志永久保留，可在账号档案“注销信息”中查询。", "warning")
    who = who_card("陈思远", "2022级人工智能2班 · 团支部书记", [("学号", "8209220611"), ("手机", "159 7318 0426"), ("提交时间", "2026-09-28 16:22")])
    tl = [("done", "学生提交注销申请", "陈思远 · 2026-09-28 16:22", "重复账号，统一保留 csu_ai2202_new。"),
          ("now", "指导教师审核 " + tag("当前", "primary"), "王晓琳 · 剩 4 天", ""),
          ("wait", "学院团委审核", "周建华 · 待流转", ""), ("wait", "校团委确认注销", "陈静 · 待流转", "")]
    bar = actbar("通过后流转学院审核，校团委确认后账号转为已注销",
                 btn("驳回", "../common/modal-reject.html", "danger", "x-circle") + btn("退回修改", "../common/modal-return.html", "default", "undo")
                 + btn("审核通过", "../common/review-done.html", "primary", "check"))
    content = review_layout([head, keep, reason, evidence],
                            [who, flow_card(tl), opinion_card(["属同一主体重复开设，同意注销，数据保留。", "佐证材料不足，请补充团支部决议。"], "属同一主体重复开设，同意注销，数据保留。")], bar)
    page("review-cancel.html", "todo", "注销申请审核", [("待我审核", "todo.html"), ("注销申请审核", None)], content)


# ---------------------------------------------------------------- 审核页：年审材料（剧本六第 1 步）
def confirm_table(items):
    rows = []
    for q, ans, sys_, ok in items:
        mark = f'<span class="ck-ok">{icon("check-circle", 14)}一致</span>' if ok else f'<span class="ck-bad">{icon("alert-circle", 14)}需关注</span>'
        rows.append([q, f'<b>{ans}</b>', f'<span class="sub">{sys_}</span>', mark])
    return table(["学生确认事项", "学生填报", "系统比对 / 教师核查", "结论"], rows)


def yoy_table(items):
    rows = []
    for f, y1, y2, note in items:
        rows.append([f'<b>{f}</b>', y1, y2, note])
    return table(["项目", "2025 年度", "2026 年度", "变化"], rows)


def annual_record(key, cls, hidden, who_name, submit_tm, confirms, yoy, issue, tl, op_val, bar_note, primary):
    """生成一条年审记录的左侧内容、右侧信息与操作栏，均带 v-rec 类以便页内切换。"""
    a = A[key]
    c = f"v-rec {cls}" + (" hidden" if hidden else "")
    no = "NS2026-CS-0027" if key == "rectify" else F["annual"]["no"]
    head = head_card(a["platform"], a["name"], tag("年审材料") + st(a["change"]) + st("待指导教师审核"),
                     [("年审编号", no), ("平台 ID", a["pid"]), ("粉丝数", a["fans"]), ("提交时间", submit_tm)], left_tag(25), cls=c)
    shot = (f'<div class="grid" style="grid-template-columns:260px minmax(0,1fr);align-items:start">'
            f'<div class="shot"><img src="{PHOTOS["screenshot"]}" alt="账号主页截图"><span>{icon("image", 12)}学生上传 · 主页截图</span></div>'
            + kv([("主页链接", f'<span class="link">{a["platform"]} · {a["pid"]}</span>', True), ("截图时间", submit_tm),
                  ("近 30 天发布", "9 条" if key == "rectify" else "21 条"), ("能否正常访问", tag("可访问", "success")),
                  ("认证状态", "已认证"), ("运营团队", "6 人" if key == "rectify" else "12 人")], 2) + "</div>")
    left = [head, f'<div class="{c}">{issue}</div>',
            card("学生确认信息", confirm_table(confirms), f'<span class="small muted">填报人：{who_name}</span>', cls=c),
            card("账号主页截图", shot, cls=c),
            card("同比对照（历史数据自动继承，当年只确认变化）", yoy_table(yoy), cls=c)]
    p = P[who_name]
    right = [who_card(who_name, f'{p["grade"]} · {p["job"]}', [("学号", p["no"]), ("手机", p["phone"]), ("所在组织", a["org"])], cls=c),
             flow_card(tl, c),
             opinion_card(["无异动，信息完整。", F["rectify"]["steps"][0][3], "最近发布时间填写有误，请按平台主页如实填写。"], op_val, cls=c)]
    return left, right, actbar(bar_note, annual_buttons(primary), c)


def annual_buttons(primary):
    """教师年审 6 项操作；primary 为本记录建议操作。"""
    fix_kind = "warn-solid" if primary == "fix" else "warning"
    pass_kind = "primary" if primary == "pass" else "ghost"
    return (go("建议注销", "../common/apply-cancel.html", "danger", "ban", "已提出注销建议，请填写注销申请")
            + go("标记疑似僵尸号", "review-zombie.html", "default", "ghost", "已标记为疑似僵尸号，进入核实流程")
            + btn("修改后确认", "review-annual-edit.html", "default", "edit")
            + btn("退回修改", "../common/modal-return.html", "default", "undo")
            + go("要求整改", "../college/rectify-create.html", fix_kind, "wrench", "已要求整改，学院将下发整改任务")
            + btn("审核通过", "../common/review-done.html", pass_kind, "check"))


def review_annual():
    vol = A["rectify"]
    rec_seg = ('<div class="seg" data-single=".v-rec"><button type="button" class="on" data-choice=".r-vol">计院青年志愿者（小红书）· 发现问题</button>'
               '<button type="button" data-choice=".r-tw">中南计院团委（无异动）</button></div>')
    top = (f'<div class="toolbar"><div class="flex gap12">{rec_seg}<span class="small muted">本人待审年审材料 3 条 · 教师审核截止 {T["teacher_end"]}</span></div>'
           f'{btn("返回待审列表", "todo.html", "default", "arrow-left", "sm")}</div>')
    vol_confirms = [
        ("账号是否仍存在", "是", "平台主页可检索", True), ("是否正常运营", "是", "近 30 天发布 9 条", True),
        ("是否能正常访问", "是", "主页可正常访问", True), ("最近一次公开发布时间", "2026-09-25", "与主页抓取一致", True),
        ("当前运营负责人", "何雨桐（8209230509）", "与档案一致", True), ("指导教师是否变化", "否", "王晓琳", True),
        ("账号名称是否变化", "否", "计院青年志愿者", True), ("是否需要注销", "否", "—", True),
        ("是否存在其他异常", "否", "档案中“信息发布审查机制”为“否”；抽查近 3 个月 12 条笔记，9 条无审核记录", False),
    ]
    vol_yoy = [
        ("粉丝数", "3,862", vol["fans"], '<span class="up">+32.5%</span>'), ("年度发布量", "86 条", "112 条", '<span class="up">+26 条</span>'),
        ("更新频率", "每周更新", "每周更新", '<span class="muted">未变化</span>'), ("学生负责人", "何雨桐", "何雨桐", '<span class="muted">未变化</span>'),
        ("指导教师", "王晓琳", "王晓琳", '<span class="muted">未变化</span>'),
        ("信息发布审查机制", tag("未建立", "danger"), tag("未建立", "danger"), '<span class="c-danger bold">连续两年未建立</span>'),
        ("年审结果", "年审通过（附条件补建制度）", "审核中", '<span class="muted">—</span>'),
    ]
    vol_issue = alert(f'<b>发现问题 1 项：</b>{F["rectify"]["steps"][0][3]}建议选择“要求整改”，由学院下发整改任务（截止 {F["rectify"]["deadline"]}）。'
                      + f'<div class="mt8">{mech_grid(("信息发布审查机制",))}</div>', "danger")
    vol_tl = [("done", "年审任务发布，自动生成年审记录", "系统 · 2026-09-15 09:00", "继承 2025 年度账号信息"),
              ("done", "学生确认并提交", "何雨桐 · 2026-09-18 20:02", "账号正常运营，最近发布 2026-09-25"),
              ("now", "指导教师审核 " + tag("当前", "primary"), "王晓琳 · 截止 " + T["teacher_end"], ""),
              ("wait", "学院统筹 / 下发整改", "周建华 · 待流转", ""), ("wait", "校团委审核", "陈静 · 待流转", "")]
    l1, r1, b1 = annual_record("rectify", "r-vol", False, "何雨桐", "2026-09-18 20:02", vol_confirms, vol_yoy, vol_issue, vol_tl,
                               F["rectify"]["steps"][0][3], "发现问题 1 项 · 建议要求整改，由学院下发整改任务", "fix")

    tw = A["annual"]
    fs = F["annual"]["steps"]
    tw_confirms = [
        ("账号是否仍存在", "是", "平台主页可检索", True), ("是否正常运营", "是", "近 30 天发布 21 条", True),
        ("是否能正常访问", "是", "主页可正常访问", True), ("最近一次公开发布时间", "2026-09-17", "与主页抓取一致", True),
        ("当前运营负责人", "李明（8209230117）", "与档案一致", True), ("指导教师是否变化", "否", "王晓琳", True),
        ("账号名称是否变化", "否", tw["name"], True), ("是否需要注销", "否", "—", True), ("是否存在其他异常", "否", "未命中风险规则", True),
    ]
    tw_yoy = [
        ("粉丝数", "31,204", tw["fans"], '<span class="up">+17.0%</span>'), ("年度发布量", "214 条", "238 条", '<span class="up">+24 条</span>'),
        ("更新频率", "每周更新", "每周更新", '<span class="muted">未变化</span>'), ("学生负责人", "李明", "李明", '<span class="muted">未变化</span>'),
        ("指导教师", "王晓琳", "王晓琳", '<span class="muted">未变化</span>'), ("四项机制", "均已建立", "均已建立", '<span class="muted">未变化</span>'),
        ("年审结果", "年审通过", "审核中", '<span class="muted">—</span>'),
    ]
    tw_issue = alert("<b>系统校验通过：</b>本年度无异动、未命中风险规则、信息完整，可直接审核通过，也可在“待我审核”中批量通过。", "success")
    tw_tl = flow_done("annual", 2) + [("now", "指导教师审核 " + tag("当前", "primary"), "王晓琳 · 截止 " + T["teacher_end"], ""),
                                      ("wait", "学院统一提交校团委", "周建华 · 待流转", ""), ("wait", "校团委批量审核", "陈静 · 待流转", "")]
    l2, r2, b2 = annual_record("annual", "r-tw", True, "李明", fs[1][0], tw_confirms, tw_yoy, tw_issue, tw_tl, fs[2][3],
                               "无异动、无风险 · 建议审核通过", "pass")

    content = top + review_layout(l1 + l2, r1 + r2, b1 + b2)
    page("review-annual.html", "todo", "年审材料审核", [("待我审核", "todo.html"), ("年审材料审核", None)], content)


# ---------------------------------------------------------------- 年审 · 修改后确认
def review_annual_edit():
    a = A["annual"]
    rows = [
        ("最近发布时间", "2026-09-17", inp(val="2026-09-28", typ="date", req=True), "平台主页抓取：2026-09-28 发布《迎新季 · 计算机学院团学组织纳新》"),
        ("当前负责人", "李明（8209230117）", sel(["李明（8209230117）", "陈子墨（8209230342）", "刘佳怡（8209230518）"], "李明（8209230117）", req=True), "与学生组织任职名单一致"),
        ("粉丝数", "36,000", inp(val="36,512", req=True), "公众号后台 2026-09-30 数据截图"),
        ("更新频率", "每月更新（1-3次/月）", sel(UPDATE_FREQ, UPDATE_FREQ[0], req=True), "近 3 个月月均发布 19 条"),
    ]
    tbl = table(["字段", "学生填报", "教师修正为", "核对依据"],
                [[f'<b class="nowrap">{f}</b>', f'<span class="sub">{o}</span>', f'<div class="field" style="min-width:220px">{c}</div>', f'<span class="small muted">{b}</span>']
                 for f, o, c, b in rows])
    diff = diff_table([("最近发布时间", "2026-09-17", "2026-09-28"), ("当前负责人", "李明（8209230117）", "李明（8209230117）"),
                       ("粉丝数", "36,000", "36,512"), ("更新频率", "每月更新（1-3次/月）", UPDATE_FREQ[0])])
    note = field("修改说明", textarea("请说明修改原因，将同步通知学生并写入操作日志",
                                     "学生填报的粉丝数为估算值，最近发布时间未更新至提交日，更新频率选择有误，已按平台后台数据修正。", req=True, maxlen=200),
                 req=True, hint="修改说明为必填项，修改前后值将完整记录")
    head = head_card(a["platform"], a["name"], tag("年审 · 修改后确认") + st(a["change"]),
                     [("年审编号", F["annual"]["no"]), ("平台 ID", a["pid"]), ("填报人", "李明"), ("提交时间", F["annual"]["steps"][1][0])])
    left = [head,
            alert("<b>修改后确认：</b>教师可直接修正学生填报中的事实性信息后确认通过，无需退回；系统记录修改前后值并通知学生。"
                  "涉及账号名称、平台 ID 变化的，应退回学生按变更流程办理。"),
            card("修正填报信息", tbl),
            card("修改预览", diff, tag("修改 3 项", "warning")),
            card("修改说明", note)]
    right = [who_card("李明", f'{P["李明"]["grade"]} · 新媒体中心主任', [("学号", P["李明"]["no"]), ("手机", P["李明"]["phone"]), ("所在组织", a["org"])], title="填报人"),
             card("确认后将会", '<div class="col gap8 fs13">' + "".join(
                 f'<div class="flex gap8 top-align">{icon("check-circle", 14, "c-success")}<span class="grow">{t}</span></div>' for t in [
                     "更新年审记录与账号档案对应字段", "向学生李明发送修改通知", "操作日志记录：修改人 王晓琳 · 修改字段 3 项 · 修改前后值",
                     "年审记录流转至学院统筹"]) + "</div>")]
    bar = actbar("请核对修改预览后确认",
                 btn("取消", "review-annual.html", "default", "arrow-left")
                 + submit_btn("确认并通过", "../common/review-done.html", "primary", "check", "已修正并审核通过，已通知学生"))
    content = '<div data-form>' + review_layout(left, right, bar) + "</div>"
    page("review-annual-edit.html", "todo", "年审 · 修改后确认",
         [("待我审核", "todo.html"), ("年审材料审核", "review-annual.html"), ("修改后确认", None)], content)


# ---------------------------------------------------------------- 僵尸号核实（剧本七第 2 步）
def review_zombie():
    a = A["zombie"]
    zs = F["zombie"]["steps"]
    head = head_card(a["platform"], a["name"], st("疑似僵尸号") + st("高风险") + st(a["run"]),
                     [("核实编号", F["zombie"]["no"]), ("平台 ID", a["pid"]), ("最近发布", a["last_post"]), ("停更", f'{a["idle_days"]} 天')], left_tag(3))
    rules = card("命中预警规则", '<div class="grid g3">' + "".join(
        f'<div class="rule">{icon("alert-circle")}<div class="grow"><div class="flex between gap8"><span class="bold">{t}</span>{src}</div>'
        f'<div class="small sub">{d}</div></div></div>' for t, d, src in [
            ("停更 ≥ 180 天", f'最近发布 {a["last_post"]}，已停更 {a["idle_days"]} 天', tag("系统预警", "danger")),
            ("所属团支部已毕业", "2021级软件工程1班已于 2025 年 6 月毕业", tag("系统预警", "danger")),
            ("无明确学生负责人", "原负责人已毕业离校，账号无人接管", tag("核实补充", "warning"))]) + "</div>"
        + '<div class="grid g4 mt16">' + "".join(
            f'<div class="card" style="padding:12px 14px;box-shadow:none"><div class="small muted">{k}</div><div class="fs18 bold num mt4">{v}</div></div>'
            for k, v in [("近 12 个月发布", "0 条"), ("粉丝数", a["fans"]), ("团支部状态", "已毕业"), ("开通时间", a["opened"])]) + "</div>",
        '<span class="small muted">系统于 ' + zs[0][0] + " 自动预警</span>")
    choice_items = [
        ("仍在正常运营", "有学生持续运营，解除预警", "check-circle", False),
        ("需整改", "账号保留，限期恢复运营或补全负责人", "wrench", False),
        ("建议注销", "组织已撤销 / 已毕业，无人运营", "ban", True),
    ]
    choices = '<div class="choices g3" data-single="">' + "".join(
        f'<div class="choice{" on" if on else ""}" data-choice=""><span class="ck"></span>{icon(ic, 20)}<div class="grow"><b>{t}</b><small>{d}</small></div></div>'
        for t, d, ic, on in choice_items) + "</div>"
    verify = card("核实结论", choices
                  + '<div class="mt16">' + field("核实说明", textarea("请填写核实情况", zs[1][3], req=True, maxlen=300), req=True) + "</div>"
                  + '<div class="mt16">' + field("核实佐证", upload(files=("2021级毕业生名单.pdf",))) + "</div>")
    safe = alert("<b>系统不会直接注销账号：</b>核实结论提交后流转学院审核、校团委确认；确认注销后账号状态转为“已注销”，数据永久保留。", "warning", "shield")
    who = who_card("王晓琳", "2021级辅导员 · 本次核实人", [("授权来源", "2021级辅导员"), ("原负责人", "张可欣（已毕业）"),
                                                   ("所属组织", a["org"]), ("组织状态", tag("已毕业", "muted"))], title="核实信息")
    tl = [("done", zs[0][2], f"系统 · {zs[0][0]}", zs[0][3]),
          ("now", "辅导员核实 " + tag("当前", "primary"), "王晓琳 · 剩 3 天", ""),
          ("wait", "学院审核", "周建华 · 待流转", ""), ("wait", "校团委确认", "陈静 · 待流转", "")]
    bar = actbar("核实结论将流转学院审核",
                 btn("暂存", None, "default", "file", toast="已暂存核实结果") + btn("通知原负责人核实", None, "default", "bell", toast="已向原负责人发送核实提醒（已毕业，可能无法联系）")
                 + submit_btn("提交核实结果", "../college/zombie-verify-detail.html", "primary", "send", "已提交，流转至学院审核"))
    content = '<div data-form>' + review_layout([head, rules, safe, verify], [who, flow_card(tl)], bar) + "</div>"
    page("review-zombie.html", "todo", "僵尸号核实", [("待我审核", "todo.html"), ("僵尸号核实", None)], content)


# ---------------------------------------------------------------- 整改材料审核
def review_rectify():
    a = A["photo"]
    head = head_card(a["platform"], a["name"], tag("整改材料", "warning") + st("整改复核中") + st(a["run"]),
                     [("整改编号", "ZG20260910003"), ("平台 ID", a["pid"]), ("截止时间", "2026-10-20"), ("提交次数", "第 1 次")], left_tag(5))
    items = [
        ("账号停更 212 天，命中“停更 ≥ 180 天”预警", "恢复更新，10 月起每月发布不少于 2 条，并提交 10-12 月内容计划",
         "9 月 26 日、28 日已发布 2 条作品；已制定第四季度内容计划（12 期）", ("近期作品截图.png", "第四季度内容计划.xlsx")),
        ("学生管理员信息缺失", "补全学生负责人及至少 1 名学生管理员信息",
         "新增学生管理员周子涵（8209240733），负责人仍为李明", ("协会换届名单.pdf",)),
        ("未提交信息发布审查机制", "提交经指导教师签字的作品发布审核办法",
         "已制定《摄影协会作品发布审核办法》，实行“社员初审 + 负责人复审 + 指导教师终审”", ("作品发布审核办法（签字版）.pdf",)),
    ]
    rows = "".join(
        f'<div class="cmp-row"><div><span class="lbl">问题 {i + 1}</span><b>{q}</b><span class="lbl mt4">整改要求</span><span class="sub">{r}</span></div>'
        f'<div class="mid">{icon("arrow-right")}</div>'
        f'<div><div class="flex between"><span class="lbl">整改说明 / 结果</span><span class="ck-ok">{icon("check-circle", 14)}已满足</span></div>'
        f'<span>{d}</span><span class="lbl mt4">证明材料</span>{files(*fs)}</div></div>'
        for i, (q, r, d, fs) in enumerate(items))
    compare = card("整改要求与整改结果对照",
                   '<div class="cmp-hd"><div class="l">整改要求（学院下发 · 周建华 · 2026-09-10）</div><div></div>'
                   '<div class="r">整改说明 / 结果 / 证明材料（李明 · 2026-09-26）</div></div>' + rows)
    choice_items = [
        (".rc-pass", "整改通过", "问题均已整改到位，恢复正常状态", "check-circle", True),
        (".rc-more", "继续整改", "仍有问题未整改到位，退回学生再次提交", "refresh", False),
        (".rc-cancel", "转注销", "无法整改或组织已不存在，转入注销流程", "ban", False),
    ]
    choices = '<div class="choices g3" data-single=".rc-act">' + "".join(
        f'<div class="choice{" on" if on else ""}" data-choice="{sel_}"><span class="ck"></span>{icon(ic, 20)}<div class="grow"><b>{t}</b><small>{d}</small></div></div>'
        for sel_, t, d, ic, on in choice_items) + "</div>"
    decide = card("审核结论", choices)
    who = who_card("李明", f'{P["李明"]["grade"]} · 摄影协会负责人', [("学号", P["李明"]["no"]), ("手机", P["李明"]["phone"]), ("提交时间", "2026-09-26 18:30")], title="整改提交人")
    tl = [("done", "系统预警：停更 212 天", "系统 · 2026-09-01 02:00", "最近发布 2026-03-02"),
          ("done", "学院下发整改任务", "周建华 · 2026-09-10 10:00", "10 月 20 日前恢复更新并补全负责人信息。"),
          ("done", "学生提交整改材料", "李明 · 2026-09-26 18:30", "已恢复更新，补全管理员并制定审核办法。"),
          ("now", "指导教师审核 " + tag("当前", "primary"), "王晓琳 · 剩 5 天", ""), ("wait", "学院复核", "周建华 · 待流转", "")]
    bar = actbar("请选择审核结论后提交",
                 f'<a class="btn btn-primary rc-act rc-pass" href="../common/review-done.html">{icon("check")}确认整改通过</a>'
                 + go("确认继续整改", "todo.html", "warn-solid", "refresh", "已判定继续整改，已通知学生重新提交", extra_cls="rc-act rc-more hidden")
                 + go("确认转注销", "../common/apply-cancel.html", "danger-solid", "ban", "已转入注销流程，请填写注销申请", extra_cls="rc-act rc-cancel hidden"))
    content = review_layout([head, compare, decide],
                            [who, flow_card(tl), opinion_card(["整改到位，同意整改通过。", "制度文件缺少签字，请补充后重新提交。", "组织已停止活动，建议转注销。"], "整改到位，同意整改通过。")], bar)
    page("review-rectify.html", "todo", "整改材料审核", [("待我审核", "todo.html"), ("整改材料审核", None)], content)


# ---------------------------------------------------------------- 我负责的账号（剧本四第 1 步）
MY_ACCOUNTS = [
    # (名称, 平台, 平台ID, 身份, 层级, 学生负责人, 运行状态, 年审状态, 最近发布, 剧本标记)
    ("中南计院团委", "微信公众号", "csu_cs_tw", "xc", "二级平台", "李明", "正常运行", "待学校审核", "2026-09-28", ""),
    ("计院科协", "哔哩哔哩", "386620915", "xc", "二级平台", "何雨桐", "正常运行", "待填报", "2026-09-21", "idchange"),
    ("计算机学院学生会", "微博", "7722108845", "xc", "二级平台", "李明", "正常运行", "待指导教师审核", "2026-09-26", ""),
    ("计院青年志愿者", "小红书", "csu_cs_volunteer", "xc", "二级平台", "何雨桐", "整改中", "整改复核中", "2026-09-25", ""),
    ("中南计算机青年", "微信公众号", "csu_cs_youth", "xc", "二级平台", "李明", "备案申请中", "未开始", "2026-09-26", ""),
    ("计算机学院研究生会", "微信公众号", "csu_cs_gsu", "xc", "二级平台", "陈子墨", "正常运行", "待指导教师审核", "2026-09-24", ""),
    ("计院ACM协会", "QQ", "2873306619", "xc", "社团平台", "赵磊（已毕业）", "正常运行", "待填报", "2026-09-12", ""),
    ("计院摄影协会", "视频号", "sph_csu_cs_photo", "xc", "社团平台", "李明", "不活跃", "待填报", "2026-03-02", ""),
    ("2022级人工智能2班团支部", "抖音", "csu_ai2202", "xc", "三级平台", "陈思远", "申请注销", "待填报", "2026-05-18", ""),
    ("2021级软件工程1班团支部", "微信公众号", "csu_se2101", "fdy", "三级平台", "—（已毕业）", "不活跃", "待指导教师审核", "2025-08-14", ""),
    ("2021级网络工程1班团支部", "微信公众号", "csu_ne2101", "fdy", "三级平台", "—（已毕业）", "申请注销", "本年度注销", "2025-06-27", ""),
    ("2021级计算机科学2班团支部", "QQ", "3310862754", "fdy", "三级平台", "—（已毕业）", "申请注销", "本年度注销", "2025-06-18", ""),
    ("计院街舞社", "抖音", "csu_cs_dance", "jws", "社团平台", "李明 → 李四（交接中）", "正常运行", "待填报", "2026-09-27", ""),
    ("计院街舞社", "微信公众号", "csu_cs_dance_wx", "jws", "社团平台", "李四", "正常运行", "年审通过", "2026-09-19", ""),
]


def accounts():
    rows = []
    for name, plat, pid, sc, lv, stu, run, ann, last, flag in MY_ACCOUNTS:
        if flag == "idchange":
            change = (f'<a class="btn btn-primary btn-sm" href="../common/apply-change.html">{icon("file-edit")}变更</a>')
            name_cell = acct(name + " " + tag("平台 ID 已变化", "warning"), plat, f"{plat} · ID {pid}")
        else:
            change = '<a class="link" href="../common/apply-change.html">变更</a>'
            name_cell = acct(name, plat, f"{plat} · ID {pid}")
        more = (f'<a class="link" href="../common/apply-handover.html">交接</a><a class="link" href="../common/apply-cancel.html">注销</a>')
        op = f'<div class="ops" style="align-items:center"><a class="link" href="../common/archive-basic.html">档案</a>{change}{more}</div>'
        idle = ' <span class="small c-danger">停更</span>' if last < "2026-04-01" else ""
        rows.append(dict(cells=[name_cell, tag(SCOPE_NAME[sc], "primary"), f'<span class="nowrap">{lv}</span>', stu, f'<div class="flex gap4 wrap">{st(run)}{st(ann)}</div>',
                                f'<span class="num">{last}</span>{idle}', op], cat=sc))
    chip_items = [("全部 18", "all")] + [(f"{n} {c}", k) for k, n, _, c, _ in SCOPES]
    scope_cards = "".join(
        f'<div class="card" style="padding:16px 18px"><div class="flex gap12"><span class="tic">{icon(ic)}</span><div class="grow">'
        f'<div class="bold">{n}</div><div class="small muted">{s}</div></div><span class="fs18 bold num">{c}</span></div></div>'
        for _, n, s, c, ic in SCOPES)
    filters = filter_bar([
        field("账号名称 / 平台 ID", inp("请输入关键词")),
        field("平台类型", sel(["微信公众号", "微博", "抖音", "哔哩哔哩", "小红书", "视频号", "QQ"])),
        field("运行状态", sel(["正常运行", "不活跃", "整改中", "申请注销", "备案申请中"])),
    ])
    tip = alert("<b>剧本四：</b>“计院科协”（哔哩哔哩）已更换新平台 ID（386620915 → 1928840012），点击该行“变更”发起信息变更，系统将识别 ID 变化并转为新建办理。")
    content = f"""
{page_hd('我负责的账号', '仅显示本人被授权范围内的账号；一人多身份时按授权来源分别统计',
         btn('教师代办', 'proxy.html', 'default', 'hand') + btn('发起新建', '../common/apply-create-basic.html', 'primary', 'plus'))}
<div class="grid g3 mb16">{scope_cards}</div>
{filters}
{tip}
{card('', f'<div class="toolbar">{chips(chip_items, target="#acctTbl")}{btn("导出清单", None, "default", "download", "sm", toast="已导出本人负责账号清单")}</div>'
      + table(['账号', '授权来源（身份）', '层级', '学生负责人', '运行 / 年审', '最近发布', '操作'], rows, id_='acctTbl') + pager(18, 2), cls='mt16')}"""
    page("accounts.html", "accounts", "我负责的账号", [("账号管理", "accounts.html"), ("我负责的账号", None)], content)


# ---------------------------------------------------------------- 代办中心（剧本八第 1 步）
def proxy():
    cases = [
        ("user", "学生负责人已毕业", "负责人离校，无法登录办理"), ("phone", "学生负责人联系不上", "多次联系无回应超过 30 天"),
        ("ban", "学生组织已撤销", "组织解散或合并，账号无人管理"), ("archive", "学院集中清理历史账号", "批量处置历史遗留账号"),
        ("more", "其他情形", "其他无法由学生正常办理的情形"),
    ]
    case_html = '<div class="grid g5">' + "".join(
        f'<div class="case"><span class="tic">{icon(ic)}</span><div class="bold fs13">{t}</div><div class="small muted">{d}</div></div>' for ic, t, d in cases) + "</div>"
    intro = card("代办机制", '<div class="small sub mb12">学生端开放后，教师仍保留代办权限。代办申请与学生申请走同一套审核流程，'
                 '系统在申请记录与操作日志中标记“发起方式：教师代办”。</div>' + case_html)
    need = [
        dict(cells=[acct("计院ACM协会", "QQ", "QQ · 2873306619"), "负责人赵磊已毕业", tag("学生负责人已毕业", "warning"), "负责人交接",
                    f'<a class="btn btn-primary btn-sm" href="proxy-apply.html">{icon("hand")}发起代办</a>'], href="proxy-apply.html"),
        dict(cells=[acct("2021级软件工程1班团支部", "微信公众号", "微信公众号 · csu_se2101"), "团支部已毕业，停更 412 天", tag("学生组织已撤销", "warning"), "账号注销",
                    '<a class="link" href="../common/apply-cancel.html">代办注销</a>'], href="../common/apply-cancel.html"),
        dict(cells=[acct("计院辩论队", "微博", "微博 · 6628301174"), "负责人失联 42 天", tag("学生负责人联系不上", "warning"), "负责人交接",
                    '<a class="link" href="../common/apply-handover.html">代办交接</a>'], href="../common/apply-handover.html"),
        dict(cells=[acct("2021级网络工程1班团支部", "微信公众号", "微信公众号 · csu_ne2101"), "年审无人填报", tag("学院集中清理历史账号", "primary"), "年审代填",
                    '<a class="link" href="review-annual-edit.html">代填年审</a>'], href="review-annual-edit.html"),
    ]
    types = [
        (".px-new", "代办新建", "file-add", "为本人范围组织补录新账号"), (".px-chg", "代办变更", "file-edit", "名称、简介、组织归属等"),
        (".px-hd", "代办负责人交接", "user-switch", "负责人毕业 / 失联时指定新负责人"), (".px-cc", "代办注销", "ban", "组织撤销 / 毕业后注销"),
        (".px-an", "代办年审", "calendar", "无人填报时由教师代填"),
    ]
    type_html = '<div class="choices g5" data-single=".px-go">' + "".join(
        f'<div class="choice{" on" if s == ".px-hd" else ""}" data-choice="{s}"><span class="ck"></span>{icon(ic, 20)}<div class="grow"><b>{t}</b><small>{d}</small></div></div>'
        for s, t, ic, d in types) + "</div>"
    go_btns = "".join(
        f'<a class="btn btn-primary px-go {c}{"" if c == "px-hd" else " hidden"}" href="{h}">{icon("arrow-right")}{t}</a>' for c, t, h in [
            ("px-new", "发起代办新建", "../common/apply-create-basic.html"), ("px-chg", "发起代办变更", "../common/apply-change.html"),
            ("px-hd", "发起代办负责人交接", "proxy-apply.html"), ("px-cc", "发起代办注销", "../common/apply-cancel.html"),
            ("px-an", "发起代办年审", "review-annual-edit.html")])
    biz = card("选择代办业务", type_html + f'<div class="flex between mt16"><span class="small muted">{icon("info", 14)} 代办申请提交后由学院管理员审核（审核节点可由学院配置）</span>{go_btns}</div>',
               cls="mt16")
    hist = [
        ("ZX20260615002", "2020级计算机科学3班团支部", "微信公众号", "账号注销", "学生组织已撤销", "2026-06-15 10:20", "已通过"),
        ("JJ20260310001", "计院摄影协会", "视频号", "负责人交接", "学生负责人联系不上", "2026-03-10 14:05", "已通过"),
        ("NS2025-CS-0041", "计院动漫社", "哔哩哔哩", "年审代填", "学院集中清理历史账号", "2025-11-20 16:40", "已通过"),
        ("BG20251108003", "计院青年志愿者", "小红书", "信息变更", "学生负责人已毕业", "2025-11-08 09:12", "已退回"),
    ]
    hist_rows = [dict(cells=[f'<span class="mono">{no}</span>', acct(n, p, p, "sm"), b, r, st("教师代办"), t, st(s),
                             ops(("日志", "../common/archive-logs.html"))], href="../common/archive-logs.html") for no, n, p, b, r, t, s in hist]
    content = f"""
{page_hd('代办中心', '学生负责人毕业、失联或组织撤销时，由教师代为发起业务办理', btn('代办记录导出', None, 'default', 'download', toast='已导出本人代办记录'))}
{intro}
{card('需要代办的账号', table(['账号', '情况', '适用情形', '建议业务', '操作'], need), tag('系统识别 4 个', 'warning'), cls='mt16')}
{biz}
{card('代办记录', table(['申请编号', '账号', '代办业务', '代办原因', '发起方式', '发起时间', '状态', '操作'], hist_rows), cls='mt16')}"""
    page("proxy.html", "proxy", "代办中心", [("账号管理", "accounts.html"), ("代办中心", None)], content)


# ---------------------------------------------------------------- 代办申请（剧本八第 2 步）
def proxy_apply():
    a = A["proxy"]
    zl, sy = P["赵磊"], P["孙悦"]
    banner = (f'<div class="px-banner"><span class="tic">{icon("hand", 22)}</span><div class="grow"><div class="fs16 bold">发起方式：教师代办</div>'
              f'<div class="small sub">代办人 王晓琳（{P["王晓琳"]["no"]} · 宣传工作辅导员）· 代办申请与学生申请走同一审核流程，全程留痕</div></div>{st("教师代办")}</div>')
    old = (f'<div class="person old"><div class="flex between"><span class="small muted bold">原负责人</span>{tag("已毕业", "muted")}</div>'
           f'<div class="who">{avatar("赵磊")}<div><div class="fs16 bold">赵磊</div><div class="small muted">{zl["grade"]} · {zl["job"]}</div></div></div>'
           + kv([("学号", zl["no"]), ("任期", "2023-09 ~ 2025-06"), ("状态", "已于 2025 年 6 月毕业离校", True)], 2) + "</div>")
    new = ('<div class="person new"><div class="flex between"><span class="small muted bold">新负责人</span>' + tag("接任", "success") + "</div>"
           '<div class="form-grid">'
           + field("姓名", inp("请输入姓名", "孙悦", req=True), req=True) + field("学号", inp("请输入学号", sy["no"], req=True), req=True)
           + field("手机号", inp("请输入手机号", sy["phone"], req=True), req=True) + field("班级 / 职务", inp("", f'{sy["grade"]} · {sy["job"]}'))
           + "</div></div>")
    form = card("代办信息", f"""
<div class="form-section">代办对象</div>
<div class="form-grid">
  {field('代办账号', inp('', f"{a['name']}（{a['platform']} · {a['pid']}）", readonly=True), req=True, hint='所属组织：计院ACM协会 · 社团平台')}
  {field('代办业务', sel(['负责人交接', '信息变更', '账号注销', '年审代填'], '负责人交接', req=True), req=True)}
  <div class="full">{field('代办原因', radios('px-reason', ['学生负责人已毕业', '学生负责人联系不上', '学生组织已撤销', '学院集中清理历史账号', '其他'], '学生负责人已毕业', req=True), req=True)}</div>
  <div class="full">{field('情况说明', textarea('请说明需要代办的原因', F['proxy']['steps'][0][3], req=True, maxlen=300), req=True)}</div>
</div>
<div class="divider"></div>
<div class="form-section">交接信息</div>
<div class="flex gap16" style="align-items:center">{old}<span class="arrow-c">{icon('arrow-right', 22)}</span>{new}</div>
<div class="form-grid mt16">
  {field('生效时间', sel(['审核通过后立即生效', '指定日期生效'], '审核通过后立即生效', req=True), req=True)}
  {field('交接后原负责人记录', inp('', '保留任期 2023-09 ~ 2025-06，记入历任负责人', readonly=True))}
  <div class="full">{field('佐证材料', upload(files=('赵磊学籍状态截图（已毕业）.png', 'ACM协会换届决议.pdf')), hint='建议上传毕业证明或学籍状态截图、组织换届决议')}</div>
</div>""")
    preview = card("流程预览", steps(["教师代办", "学院审核", "生效"], 0)
                   + '<div class="mt16">' + timeline([("now", "教师代办提交", "王晓琳 · 提交后进入学院审核", ""),
                                                      ("wait", "学院管理员审核（学院配置）", "周建华 · 计算机学院团委", ""),
                                                      ("wait", "交接生效", "孙悦成为学生负责人", "")]) + "</div>")
    log = card("留痕说明", alert("系统将在操作日志记录发起方式：教师代办", "info", "log")
               + '<div class="mt12">' + kv([("发起人", "王晓琳"), ("发起身份", "宣传工作辅导员"), ("发起方式", st("教师代办")), ("通知对象", "孙悦、周建华")], 2) + "</div>")
    bar = actbar("请确认代办原因与新负责人信息",
                 btn("取消", "proxy.html", "default", "arrow-left") + btn("保存草稿", None, "default", "file", toast="已保存为草稿，可在代办中心继续编辑")
                 + submit_btn("提交代办", "../common/apply-success.html", "primary", "send", "代办申请已提交，等待学院管理员审核"))
    content = '<div data-form>' + banner + '<div class="mt16"></div>' + review_layout([form], [preview, log], bar) + "</div>"
    page("proxy-apply.html", "proxy", "代办申请", [("代办中心", "proxy.html"), ("代办申请", None)], content)


# ---------------------------------------------------------------- 消息提醒
def messages():
    msgs = [
        ("todo", True, "file-add", "", "李明重新提交了新建备案申请“中南计算机青年”", "已补充平台介绍（326 字）及信息发布范围，请再次审核。", "今天 09:12", "review-create.html"),
        ("todo", True, "user-switch", "green", "计院街舞社负责人交接待您审核", "李明 → 李四，拟 2026-10-01 生效，审核通过即生效。", "昨天 19:41", "review-handover.html"),
        ("todo", True, "file-edit", "orange", "计算机学院学生会名称变更待您审核", "拟改名为“中南计院学生会”，属重要变更。", "09-26 14:31", "review-change.html"),
        ("todo", False, "ghost", "red", "系统推送 1 个疑似僵尸号待您核实", "2021级软件工程1班团支部停更 412 天，命中 3 条规则。", "09-22 08:00", "review-zombie.html"),
        ("todo", False, "wrench", "orange", "计院摄影协会提交了整改材料", "整改编号 ZG20260910003，请审核整改结果。", "09-26 18:31", "review-rectify.html"),
        ("deadline", True, "clock", "red", "新建申请 XJ20260924001 将于 1 天后超时", "超时未审核将通知学院管理员。", "今天 08:00", "review-create.html"),
        ("deadline", False, "calendar", "orange", f"{T['year']} 年度年审：教师审核截止 {T['teacher_end']}", "您负责的账号中还有 3 条年审材料待审核。", "09-28 09:00", "review-annual.html"),
        ("deadline", False, "bell", "orange", f"学生填报截止 {T['stu_end']}，6 个账号尚未提交", "可在“我负责的账号”中查看并提醒学生。", "09-27 09:00", "accounts.html"),
        ("system", False, "key", "", "学院管理员周建华将“计院ACM协会”分配给您负责", "授权来源：宣传工作辅导员。原负责人已毕业，建议发起代办交接。", "09-25 11:06", "proxy.html"),
        ("system", False, "user-switch", "purple", "您的身份授权已更新", "新增身份“计院街舞社指导教师”，可在右上角切换身份。", "09-12 10:20", "../common/identity-switch.html"),
        ("system", False, "smartphone", "purple", "教师移动端审核已上线", "新建、变更、交接、年审、僵尸号核实均可在手机上完成。", "09-10 15:00", "../../app/teacher/home.html"),
    ]
    items = "".join(
        f'<a class="msg{" unread" if unread else ""}" href="{h}" data-cat="{cat}"><span class="tic {c}">{icon(ic)}</span>'
        f'<div class="grow"><div class="msg-t">{t}</div><div class="small sub mt4">{d}</div></div>'
        f'<div class="col" style="align-items:flex-end;gap:6px"><span class="small muted nowrap">{tm}</span>{icon("chevron-right")}</div></a>'
        for cat, unread, ic, c, t, d, tm, h in msgs)
    sg = seg([("全部 11", "all"), ("审核待办 5", "todo"), ("截止提醒 3", "deadline"), ("系统通知 3", "system")], target="#msgList")
    extra = (btn("全部已读", None, "default", "check", "sm", toast="已将全部消息标记为已读")
             + btn("提醒设置", None, "text", "settings", "sm", toast="已开启微信、短信双通道提醒"))
    content = f"""
{page_hd('消息提醒', '审核待办、截止提醒与系统通知，点击消息直达办理页面', btn('去审核', 'todo.html', 'primary', 'inbox'))}
{card('', f'<div class="toolbar" style="padding:14px 20px 0">{sg}<div class="flex gap8">{extra}</div></div><div id="msgList">{items}</div>', bd_cls='')}"""
    page("messages.html", "messages", "消息提醒", [("消息提醒", None)], content)


def build():
    workbench()
    review_create()
    review_change()
    review_handover()
    review_cancel()
    review_annual()
    review_annual_edit()
    review_zombie()
    review_rectify()
    accounts()
    proxy()
    proxy_apply()
    messages()
