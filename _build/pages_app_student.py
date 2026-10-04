"""移动端 · 学生用户页面（演示身份：李明）与移动端公共页（登录、身份选择）。"""
from base import *  # noqa: F401,F403
from data import (ACCOUNTS, PEOPLE, ANNUAL_TASK as T, FLOWS, CANCEL_REASONS, UPDATE_FREQ, PLATFORM_TYPES,
                  ORG_TYPES, LEVELS, COLLEGES)

D = "app/student/"
C = "app/common/"

NEW = ACCOUNTS["new"]
REN = ACCOUNTS["rename"]
HO = ACCOUNTS["handover"]
AN = ACCOUNTS["annual"]
RE = ACCOUNTS["rectify"]
PH = ACCOUNTS["photo"]
NEW_NO = FLOWS["new"]["no"]
NEW_STEPS = FLOWS["new"]["steps"]
REN_STEPS = FLOWS["rename"]["steps"]
HO_STEPS = FLOWS["handover"]["steps"]
RC = FLOWS["rectify"]
FILING_NO = "CSU-XMT-2026-0137"
WIZ = ["归属", "平台", "运行负责人", "审核人"]

# 剧本一：第一次提交的平台介绍（68 字，被退回）与修改后重新提交的版本（326 字）
INTRO_SHORT = "中南计算机青年是计算机学院团委新媒体中心主办的微信公众号，主要发布学院团学活动通知、青年风采展示和学术科创资讯，欢迎广大师生们积极关注。"
INTRO_FULL = ("“中南计算机青年”是计算机学院团委新媒体中心主办、学院团委指导的官方微信公众号，面向学院全体团员青年及关心学院发展的校友。"
              "内容定位：以思想引领为核心，围绕青年成长、学术科创、实践志愿、校园文化四条主线，传递学院团学工作动态，展现计算机青年风采。"
              "栏目设置：开设“青年说”“科创前沿”“团学快讯”“实践足迹”“毕业季”五个固定栏目，每周更新 2 至 3 次，重大活动期间开设专题。"
              "信息发布范围：学院团学活动通知、团员教育与主题团日、科创竞赛成果、志愿服务与社会实践报道，不发布商业广告及与团学工作无关的内容。"
              "审核机制：严格执行“三审三校”制度，由学生编辑初审、新媒体中心主任复审、指导教师终审后发布，敏感内容报学院团委审定，确保内容导向正确、信息真实准确。")

CSS = """
/* ===== 学生端补充样式 ===== */
.m-card .result{padding:18px 4px 6px}.m-card .result h2{font-size:19px}.m-card .result p{font-size:13px}
.m-card .result .btn{flex:1;height:42px;border-radius:10px}
.sec{font-size:13px;color:var(--c-text-3);padding:4px 4px 8px;display:flex;align-items:center;justify-content:space-between;gap:8px}
.cell .cell-label.wrap{flex:1;min-width:0;line-height:1.45}
.cell .m-input{flex:1;min-width:0}
.m-input[readonly]{color:var(--c-text-3)}
.cell-value .tag{vertical-align:middle}
.mi{width:32px;height:32px;border-radius:10px;display:grid;place-items:center;background:var(--c-primary-light);color:var(--c-primary);flex:none}
.mi .i{width:18px;height:18px}
.mi.green{background:var(--c-success-bg);color:var(--c-success)}.mi.orange{background:var(--c-warning-bg);color:var(--c-warning)}
.mi.red{background:var(--c-danger-bg);color:var(--c-danger)}.mi.purple{background:#F0EDFB;color:#6B5BD2}.mi.gray{background:var(--c-muted-bg);color:var(--c-muted)}
.yn{display:inline-flex;background:#EEF2F6;border-radius:8px;padding:2px;gap:2px;flex:none;margin-left:auto}
.yn label{position:relative;min-width:44px;text-align:center;padding:3px 10px;border-radius:6px;font-size:13px;color:var(--c-text-2);cursor:pointer}
.yn input{position:absolute;inset:0;opacity:0;cursor:pointer;margin:0}
.yn label:has(input:checked){background:#fff;color:var(--c-primary);font-weight:600;box-shadow:var(--shadow-sm)}
.hd-card{background:#fff;border-radius:14px;padding:16px;margin-bottom:12px;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.st4{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:14px}
.st4>div{background:#F7F9FB;border-radius:8px;padding:8px 10px}
.st4 small{display:block;font-size:11px;color:var(--c-text-3);margin-bottom:4px}
.bb-grid{flex:1;display:grid;grid-template-columns:repeat(4,1fr)}
.bb-grid a{display:flex;flex-direction:column;align-items:center;gap:4px;font-size:12px;color:var(--c-text-2)}
.bb-grid a .mi{width:36px;height:36px;border-radius:11px}
.flow-hint{display:flex;flex-wrap:wrap;align-items:center;gap:2px 4px;font-size:12px;color:var(--c-text-3);margin-top:10px;padding-top:10px;border-top:1px dashed var(--c-line)}
.flow-hint .i{width:12px;height:12px}
.chk{display:flex;gap:10px;align-items:flex-start;padding:12px 0;border-bottom:1px solid #F0F2F5}
.chk:last-child{border-bottom:none}
.chk-ic{width:24px;height:24px;border-radius:50%;display:grid;place-items:center;flex:none;margin-top:1px}
.chk-ic .i{width:14px;height:14px;stroke-width:2.4}
.chk-ic.ok{background:var(--c-success-bg);color:var(--c-success)}.chk-ic.warn{background:var(--c-warning-bg);color:var(--c-warning)}
.cmp{padding:12px 0;border-bottom:1px solid #F0F2F5}.cmp:last-child{border-bottom:none}
.cmp-row{display:flex;align-items:center;gap:8px;margin-top:6px;font-size:14px;flex-wrap:wrap}
.cmp-row .i{color:var(--c-text-3);width:14px;height:14px}
.old{color:var(--c-text-3);text-decoration:line-through;text-decoration-color:rgba(223,32,39,.55)}
.new{color:var(--c-success);font-weight:600}
.cd{display:inline-flex;align-items:baseline;gap:2px;padding:3px 10px;border-radius:14px;background:rgba(255,255,255,.2);font-size:12px;white-space:nowrap}
.cd b{font-size:17px;font-weight:700;margin:0 1px}
.cd.light{background:var(--c-warning-bg);color:var(--c-warning)}
.thumb{width:72px;height:104px;border-radius:8px;object-fit:cover;border:1px solid var(--c-line);flex:none}
.person{display:flex;align-items:center;gap:10px;padding:12px 14px;border-bottom:1px solid #F0F2F5}
.person:last-child{border-bottom:none}
.x-mini{width:28px;height:28px;border-radius:8px;display:grid;place-items:center;color:var(--c-text-3);background:#F5F7FA;flex:none}
.x-mini:hover{color:var(--c-danger);background:var(--c-danger-bg)}
.add-row{display:flex;align-items:center;justify-content:center;gap:6px;width:100%;padding:12px;color:var(--c-primary);font-size:14px;border-top:1px solid #F0F2F5}
.sheet-hd{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px}
.sheet-hd b{font-size:16px}
.sheet .choices{gap:8px}.sheet .choice{padding:10px 12px}
.sheet .btn{width:100%;height:44px;border-radius:10px;font-size:16px;margin-top:14px}
.msg{display:flex;gap:12px;padding:14px;background:#fff;border-radius:12px;margin-bottom:10px;position:relative;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.msg .dot{position:absolute;top:16px;right:14px;width:8px;height:8px;border-radius:50%;background:var(--c-danger)}
.msg-bd{flex:1;min-width:0}
.msg-txt{font-size:13px;color:var(--c-text-2);margin-top:4px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.hl{border:1px solid var(--c-danger-bd);background:#FFF8F8}
.intro-box{font-size:13px;line-height:1.7;color:var(--c-text-2);background:#F7F8FA;border-radius:8px;padding:10px}
.wide-btn .btn{width:100%;height:46px;border-radius:10px;font-size:16px}
.biz{display:flex;gap:12px;align-items:flex-start}
.biz .mi{width:42px;height:42px;border-radius:12px}.biz .mi .i{width:22px;height:22px}
.lv-tip{display:grid;grid-template-columns:auto 1fr;gap:4px 10px;font-size:12px;color:var(--c-text-2);background:#F7F9FB;border-radius:8px;padding:10px 12px}
.lv-tip b{color:var(--c-text);font-weight:600}
.id-card{display:flex;align-items:center;gap:12px}
.acct-tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.mini-kv{display:flex;gap:14px;font-size:12px;color:var(--c-text-3);margin-top:10px;padding-top:10px;border-top:1px solid #F0F2F5}
.mini-kv b{color:var(--c-text);font-weight:600;margin-left:2px}
.m-search{display:flex;align-items:center;gap:8px;height:38px;padding:0 12px;border-radius:19px;background:#fff;color:var(--c-text-3);margin-bottom:12px}
.m-search input{flex:1;min-width:0;border:none;outline:none;background:none;font-size:14px}
.m-card .alert,.m-group .alert{font-size:12.5px}
.logout{display:block;text-align:center;padding:14px;color:var(--c-danger);font-size:15px}
.me-hero .avatar{border:2px solid rgba(255,255,255,.6)}
/* 登录页 */
.lg-hero{margin:-12px -16px 0;padding:22px 24px 70px;color:#fff;position:relative;display:flex;align-items:center;justify-content:space-between}
.lg-hello{font-size:34px;font-weight:900;letter-spacing:2px;line-height:1.1;font-style:italic}
.lg-name{font-size:19px;font-weight:700;margin-top:8px}
.lg-sub{font-size:12px;opacity:.85;margin-top:4px}
.lg-logo{width:78px;height:78px;border-radius:50%;flex:none;box-shadow:0 8px 20px rgba(0,40,120,.25)}
.lg-card{margin-top:-50px;position:relative;z-index:2;padding:20px 18px;border-radius:16px;box-shadow:0 8px 24px rgba(0,87,240,.08)}
.lg-card .m-group{background:#F7F8FA;border-radius:8px}.lg-card .m-group .cell{border-bottom-color:#EBEDF0}
.lg-card .wide-btn .btn{height:46px;border-radius:23px;font-size:16px}
.lg-tip{display:flex;gap:6px;align-items:flex-start;font-size:12px;color:var(--c-text-3);margin-top:12px;line-height:1.6}
.lg-tip .i{margin-top:2px;color:var(--c-success)}
"""


# ---------------------------------------------------------------- 小组件
def page(name, title, content, **kw):
    """学生端页面统一入口：统一附加本模块样式。"""
    kw.setdefault("css", CSS)
    app_page(D + name, "student", title, content, **kw)


def sec(title, extra=""):
    return f'<div class="sec"><span>{title}</span>{extra}</div>'


def group(*cells):
    return f'<div class="m-group">{"".join(cells)}</div>'


def face(name, cls=""):
    """有照片的人员用照片头像，其余用姓氏字头像，避免误用他人照片。"""
    if name in AVATARS:
        return avatar(name, cls)
    size = {"sm": 24, "lg": 56}.get(cls, 32)
    return (f'<span class="avatar {cls}" style="display:grid;place-items:center;background:#E3F1F9;color:#2A8DC7;'
            f'font-weight:600;font-size:{size // 2 - 2}px">{name[0]}</span>')


def mi(ic, color=""):
    return f'<span class="mi {color}">{icon(ic)}</span>'


def yn(label, name, val="是", opts=("是", "否")):
    """是 / 否 分段单选，用于四项机制、年审确认项等。"""
    out = []
    for o in opts:
        c = " checked" if o == val else ""
        out.append(f'<label><input type="radio" name="{name}"{c}>{o}</label>')
    return f'<div class="cell"><span class="cell-label wrap">{label}</span><span class="yn">{"".join(out)}</span></div>'


def ro(label, value):
    return (f'<div class="cell"><span class="cell-label">{label}</span>'
            f'<input class="m-input" value="{esc(value)}" readonly aria-label="{esc(label)}"></div>')


def up_cell(label, hint, files=(), req=False):
    r = '<span class="req">*</span>' if req else ""
    return (f'<div class="cell col-cell"><span class="cell-label">{r}{label}</span>'
            f'{upload("点击上传文件或拍照", hint, files)}</div>')


def countdown(days, light=False):
    return f'<span class="cd{" light" if light else ""}">剩余<b class="num">{days}</b>天</span>'


def flow_hint(nodes):
    arrow = icon("chevron-right")
    return f'<div class="flow-hint">{icon("route")}<span>流程：</span>{arrow.join(f"<span>{n}</span>" for n in nodes)}</div>'


def tl_new(kinds):
    """按剧本一时间线生成节点，kinds 与 FLOWS['new'] 的步骤一一对应。"""
    return [(k, act, f"{who} · {t}", cmt) for (t, who, act, cmt), k in zip(NEW_STEPS, kinds)]


def acct_head(a, tags_html, meta=None, extra=""):
    meta = meta or f"{a['platform']} · ID {a['pid']}"
    return (f'<div class="hd-card"><div class="flex gap12">{pf(a["platform"], "lg")}<div class="grow">'
            f'<div class="fs16 bold ellipsis">{a["name"]}</div><div class="small muted ellipsis">{meta}</div>'
            f'<div class="acct-tags">{tags_html}</div></div></div>{extra}</div>')


def mini_acct(a, right=""):
    return (f'<div class="m-card flex gap12">{pf(a["platform"])}<div class="grow"><div class="bold ellipsis">{a["name"]}</div>'
            f'<div class="small muted ellipsis">{a["platform"]} · ID {a["pid"]}</div></div>{right}</div>')


def file_btns(names):
    return "".join(f'<button type="button" class="file-chip" data-toast="正在预览：{esc(n)}">{icon("file")}{n}</button>'
                   for n in names)


def m_card_title(title, extra=""):
    return f'<div class="m-title" style="margin-top:0">{title}{extra}</div>'


# ---------------------------------------------------------------- 公共：登录 / 身份选择
def login():
    content = f"""
<div class="lg-hero">
  <div><div class="lg-hello">HELLO</div><div class="lg-name">欢迎登录团学新媒体平台</div>
  <div class="lg-sub">中南大学智慧学工 · 备案 · 年审 · 治理一体化</div></div>
  <img class="lg-logo" src="../../assets/m-center-logo.png" alt="中南大学">
</div>
<div class="m-card lg-card" data-form>
  <div class="flex between"><div><div class="bold fs16">统一身份认证登录</div><div class="small muted">使用学校统一身份认证账号登录</div></div>{icon('shield', 26, 'c-primary')}</div>
  <div class="m-group mt12">
    {m_input('学号/工号', '请输入学号或工号', '8209230117', req=True)}
    {m_input('密码', '请输入统一认证密码', 'csu2026demo', req=True, typ='password')}
  </div>
  <div class="flex between small">
    <label class="flex gap6 sub"><input type="checkbox" checked style="accent-color:var(--c-primary)">记住账号</label>
    <button type="button" class="link" data-toast="请前往学校统一身份认证平台找回密码">忘记密码？</button>
  </div>
  <div class="wide-btn mt16">{submit_btn('登录', 'identity-switch.html', toast='认证成功，请选择本次登录身份')}</div>
  <div class="lg-tip">{icon('lock', 14)}<span>本系统仅对接学校统一身份认证，<b>不收集任何第三方新媒体平台的登录账号与密码</b>。</span></div>
</div>
<div class="m-card">
  <div class="small muted mb8" style="text-align:center">其他登录方式</div>
  <div class="grid g2" style="gap:10px">
    <button type="button" class="btn btn-default" data-toast="请使用企业微信扫描二维码（演示）">{icon('qr')}企业微信扫码</button>
    <button type="button" class="btn btn-default" data-toast="验证码已发送至 151****2233（演示）">{icon('phone')}短信验证码</button>
  </div>
</div>
<div class="small muted" style="text-align:center;margin-top:6px">共青团中南大学委员会 · 宣传部</div>"""
    app_page(C + "login.html", "common", "移动端登录", content, nav_title="", blue=True, css=CSS,
             notes=["学号 / 工号 + 统一认证密码登录，两项均为必填，留空点击登录会标红提示",
                    "“忘记密码”引导至学校统一身份认证平台，本系统不存储密码",
                    "明确告知不收集第三方平台（微信、抖音等）的登录密码，账号只做登记备案",
                    "登录成功后进入身份选择，一人多身份时选择本次进入的角色"],
             flow=[("登录后选择身份", "identity-switch.html"), ("学生端首页", "../student/home.html"),
                   ("PC 端登录", "../../pc/common/login.html")])


def identity_switch():
    ids = [
        ("李明", "学生用户", "primary", "计算机学院 · 2023级软件工程2班 · 学号 8209230117",
         "发起备案、变更、交接、注销、认领申请，在线年审与整改提交；仅可见本人负责的 5 个账号", "../student/home.html", True),
        ("王晓琳", "业务教师", "warning", "计算机学院 · 宣传工作辅导员 / 2021级辅导员 / 街舞社指导教师",
         "审核本人负责范围内的申请、年审、整改与僵尸号核实，学生无法办理时可代办", "../teacher/home.html", False),
        ("周建华", "学院管理员", "success", "计算机学院团委 · 学院团委书记",
         "学院审核、年审统一提交校团委、任务分派与风险督办", "../college/home.html", False),
    ]
    cards = "".join(
        f'<a class="m-card id-card" href="{h}" style="{"box-shadow:inset 0 0 0 1.5px var(--c-primary)" if on else ""}">'
        f'{avatar(n, "lg")}<div class="grow"><div class="flex gap8"><b class="fs16">{n}</b>{tag(r, k)}</div>'
        f'<div class="small muted mt4">{o}</div><div class="small sub mt4">{d}</div></div>{icon("chevron-right", cls="arrow")}</a>'
        for n, r, k, o, d, h, on in ids)
    content = f"""
<div class="m-card flex gap12">{mi('user-switch')}<div class="grow"><div class="bold">请选择本次进入的身份</div>
<div class="small muted">统一身份认证已通过 · 演示账号绑定 3 个身份</div></div></div>
{cards}
<div class="alert alert-info">{icon('info')}<div class="grow"><b>同一账号体系、同一套数据。</b>不同身份仅授权范围不同；PC 端与移动端业务状态实时一致，移动端提交的申请可在 PC 端继续审核。</div></div>
<div class="m-group mt12">
  {cell('在 PC 端打开', '<span class="c-primary">身份选择（PC）</span>', href='../../pc/common/identity-switch.html')}
  {cell('退出登录', '', href='login.html')}
</div>"""
    app_page(C + "identity-switch.html", "common", "身份选择", content, back="login.html", css=CSS,
             notes=["一人多身份时按身份进入，各身份的数据范围与操作权限独立授权",
                    "学生身份仅能发起申请、提交材料，无最终审核权",
                    "教师 / 学院管理员进入对应的移动审核工作台",
                    "PC 与移动端共用同一数据，状态实时同步"],
             flow=[("学生：李明 首页", "../student/home.html"), ("教师：王晓琳 工作台", "../teacher/home.html"),
                   ("学院管理员：周建华 看板", "../college/home.html"), ("PC 端身份选择", "../../pc/common/identity-switch.html")])


# ---------------------------------------------------------------- 学生：首页
def home():
    me = PEOPLE["李明"]
    todos = "".join(
        f'<a class="todo-item" href="{h}"><span class="stat-ic {c}" style="width:38px;height:38px;border-radius:11px">{icon(ic, 20)}</span>'
        f'<div class="grow"><div class="bold fs13">{t}</div><div class="small muted">{m}</div></div>{tag(k, kc)}</a>'
        for t, m, ic, c, k, kc, h in [
            ("中南计院团委 · 年度年审", f"请于 {T['stu_end']} 前完成填报", "calendar", "", "待年审", "primary", "annual-fill.html"),
            ("中南计算机青年 · 新建备案", "王晓琳老师退回：请补充平台介绍", "undo", "orange", "退回修改", "danger", "application-returned.html"),
            ("计院摄影协会 · 疑似僵尸号", "停更 212 天，请核实运营情况", "ghost", "red", "待核实", "warning", "zombie-verify.html"),
        ])
    my_accts = "".join(
        f'<a class="m-card flex gap12" href="{h}" style="margin-bottom:10px">{pf(a["platform"])}<div class="grow">'
        f'<div class="bold ellipsis">{a["name"]}</div><div class="small muted">{a["platform"]} · {a["level"]}</div></div>{st(s)}</a>'
        for a, s, h in [(ACCOUNTS["annual"], "正常运行", "account-detail.html"), (ACCOUNTS["rename"], "变更申请中", "account-detail.html"),
                        (ACCOUNTS["handover"], "正常运行", "account-detail.html")])
    content = f"""
<div class="m-hero">
  <div class="flex gap12" style="position:relative;z-index:1">{avatar('李明', 'lg')}
    <div class="grow"><div class="fs18 bold">李明，下午好</div><div class="small" style="opacity:.85">{me['org']} · {me['job']}</div></div>
    <a href="messages.html" style="position:relative">{icon('bell', 22)}<span class="badge" style="position:absolute;top:-6px;right:-8px">3</span></a>
  </div>
  <div class="grid g3 mt16" style="position:relative;z-index:1;text-align:center;gap:0">
    <a href="accounts.html"><div class="fs18 bold num">5</div><div class="small" style="opacity:.8">我的账号</div></a>
    <a href="applications.html" style="border-left:1px solid rgba(255,255,255,.2);border-right:1px solid rgba(255,255,255,.2)"><div class="fs18 bold num">2</div><div class="small" style="opacity:.8">进行中申请</div></a>
    <a href="todo.html"><div class="fs18 bold num">3</div><div class="small" style="opacity:.8">待办事项</div></a>
  </div>
</div>
<div class="m-card mt12"><div class="quick">
  <a href="apply-create-basic.html"><span class="qi">{icon('file-add')}</span>新建备案</a>
  <a href="apply-change.html"><span class="qi orange">{icon('file-edit')}</span>信息变更</a>
  <a href="apply-handover.html"><span class="qi green">{icon('user-switch')}</span>负责人交接</a>
  <a href="apply-cancel.html"><span class="qi red">{icon('power')}</span>账号注销</a>
  <a href="annual.html"><span class="qi">{icon('calendar')}</span>我的年审</a>
  <a href="applications.html"><span class="qi purple">{icon('clipboard')}</span>我的申请</a>
  <a href="rectify.html"><span class="qi orange">{icon('wrench')}</span>整改任务</a>
  <a href="apply-claim.html"><span class="qi green">{icon('hand')}</span>账号认领</a>
</div></div>
<div class="alert alert-info">{icon('calendar')}<div class="grow"><b>{T['name']}</b>进行中，学生填报截止 {T['stu_end']}，请及时确认账号运行情况。</div></div>
<div class="m-title mt12">我的待办<a href="todo.html">全部{icon('chevron-right', 14)}</a></div>
<div class="m-card" style="padding:4px 14px">{todos}</div>
<div class="m-title">我负责的账号<a href="accounts.html">全部 5 个{icon('chevron-right', 14)}</a></div>
{my_accts}"""
    app_page(D + "home.html", "student", "首页", content, tab="home", nav_title="团学新媒体",
             notes=["聚合本人待办：待年审、退回修改、疑似僵尸号核实，点击直达办理页",
                    "快捷入口覆盖新建、变更、交接、注销、认领五类业务及年审、整改",
                    "顶部统计分别跳转我的账号、我的申请、我的待办"],
             flow=[("剧本一：新建备案", "apply-create-basic.html"), ("剧本五：年审填报", "annual-fill.html"),
                   ("查看退回意见", "application-returned.html")])


# ---------------------------------------------------------------- 学生：待办 / 消息 / 我的
def todo():
    items = [
        ("annual", "中南计院团委 · 2026 年度年审", "确认本年度变化并提交", "calendar", "", "待年审", "primary", "annual-fill.html", "10-15 截止"),
        ("annual", "计院街舞社 · 2026 年度年审", "历史数据已继承，待确认", "calendar", "", "待年审", "primary", "annual.html", "10-15 截止"),
        ("back", "中南计算机青年 · 新建备案", "王晓琳退回：平台介绍不足 100 字", "undo", "orange", "退回修改", "danger", "application-returned.html", "09-25 退回"),
        ("rectify", "计院青年志愿者 · 年审整改", "第 2 轮整改材料待提交", "wrench", "orange", "待整改", "danger", "rectify.html", f"{RC['deadline'][5:]} 截止"),
        ("verify", "计院摄影协会 · 疑似僵尸号", "停更 212 天，请核实运营情况", "ghost", "red", "待核实", "warning", "zombie-verify.html", "10-10 截止"),
        ("handover", "计院街舞社 · 负责人交接", "10 月起卸任，请交接给继任者", "user-switch", "green", "待交接", "primary", "apply-handover.html", "10-01 生效"),
    ]
    rows = "".join(
        f'<a class="todo-item" href="{h}" data-cat="{cat}">{mi(ic, c)}<div class="grow" style="min-width:0">'
        f'<div class="bold fs13 ellipsis">{t}</div><div class="small muted ellipsis">{m}</div></div>'
        f'<div class="col" style="align-items:flex-end;gap:4px;flex:none">{tag(k, kc)}<span class="small muted nowrap">{dl}</span></div></a>'
        for cat, t, m, ic, c, k, kc, h, dl in items)
    tabs = "".join(f'<button type="button" data-seg="{v}"{" class=on" if v == "all" else ""}>{t}</button>'
                   for t, v in [("全部", "all"), ("待年审", "annual"), ("退回修改", "back"), ("待整改", "rectify"), ("待核实", "verify")])
    content = f"""
<div class="m-tabs" data-target="#todo-list">{tabs}</div>
<div class="flex between small muted mb8" style="padding:0 2px"><span>共 {len(items)} 项待办</span><span>最早截止 2026-10-01</span></div>
<div class="m-card" style="padding:4px 14px" id="todo-list">{rows}</div>
<div class="alert alert-info">{icon('info')}<div class="grow">待办按“本人负责的账号”自动生成；学生可发起申请、提交材料，审核由指导教师、学院与校团委完成。</div></div>"""
    page("todo.html", "我的待办", content, back="home.html",
         notes=["顶部页签按类型筛选：待年审 / 退回修改 / 待整改 / 待核实，“全部”额外包含待交接事项",
                "每条待办显示业务、账号与截止时间，点击直达办理页面",
                "待办随审核流转自动增减，教师退回、学院下发整改、系统僵尸号预警都会生成待办"],
         flow=[("办理年审填报", "annual-fill.html"), ("查看退回意见（剧本一）", "application-returned.html"),
               ("提交整改（剧本六）", "rectify.html"), ("核实疑似僵尸号", "zombie-verify.html"),
               ("发起负责人交接（剧本三）", "apply-handover.html")])


def messages():
    msgs = [
        ("r", "undo", "orange", "审核退回", "2026-09-25 09:30", "王晓琳老师退回了「中南计算机青年」新建备案申请：平台介绍不足 100 字，请补充内容定位、栏目设置和信息发布范围后重新提交。", "application-returned.html", True),
        ("r", "check-circle", "green", "审核通过", "2026-09-27 11:20", "「中南计算机青年」新建备案已通过指导教师审核，已流转至学院团委审核。", "application-detail.html", True),
        ("n", "wrench", "red", "整改通知", "2026-09-24 11:30", "「计院青年志愿者」第一次整改判定为继续整改：制度文件缺少指导教师签字及学院盖章，审核记录不完整。", "rectify.html", True),
        ("n", "ghost", "red", "僵尸号预警", "2026-09-22 02:00", "「计院摄影协会」已停更 212 天（最近发布 2026-03-02），被系统标记为疑似僵尸号，请核实运营情况。", "zombie-verify.html", False),
        ("n", "calendar", "", "年审提醒", "2026-09-15 09:00", f"{T['name']}已启动，你负责的 4 个账号需在 {T['stu_end']} 前完成填报，历史数据已自动继承。", "annual.html", False),
        ("g", "bell", "purple", "系统公告", "2026-09-15 08:30", "关于开展 2026 年度团学组织新媒体平台年审工作的通知：年审遵循“历史数据自动继承、只确认本年度变化”原则。", "annual.html", False),
    ]
    rows = "".join(
        f'<a class="msg" href="{h}" data-cat="{cat}">{mi(ic, c)}<div class="msg-bd"><div class="flex between gap8" style="padding-right:{14 if u else 0}px">'
        f'<b class="fs13">{t}</b><span class="small muted nowrap">{tm[5:]}</span></div><div class="msg-txt">{x}</div></div>'
        f'{"<span class=dot></span>" if u else ""}</a>'
        for cat, ic, c, t, tm, x, h, u in msgs)
    content = f"""
{chips([('全部', 'all'), ('审核结果', 'r'), ('提醒', 'n'), ('公告', 'g')], target='#msg-list')}
<div class="mt12" id="msg-list">{rows}</div>
<div class="small muted" style="text-align:center;padding:6px 0">仅显示近 30 天消息</div>"""
    page("messages.html", "消息", content, back="home.html",
         right='<button type="button" data-toast="已将全部消息标记为已读">全部已读</button>',
         notes=["汇集审核退回、审核通过、年审提醒、整改通知、僵尸号预警与系统公告",
                "红点表示未读，点击消息直达对应业务页面",
                "右上角“全部已读”一键清除未读标记"],
         flow=[("审核退回 → 退回详情", "application-returned.html"), ("审核通过 → 申请进度", "application-detail.html"),
               ("整改通知 → 整改任务", "rectify.html"), ("年审提醒 → 我的年审", "annual.html")])


def mine():
    me = PEOPLE["李明"]

    def row(ic, color, label, value, href):
        return (f'<a class="cell" href="{href}">{mi(ic, color)}<span class="cell-label">{label}</span>'
                f'<span class="cell-value">{value}</span>{icon("chevron-right", cls="arrow")}</a>')

    content = f"""
<div class="m-hero me-hero">
  <div class="flex gap12" style="position:relative;z-index:1">{avatar('李明', 'lg')}
    <div class="grow"><div class="flex gap8"><span class="fs18 bold">李明</span><span class="tag" style="background:rgba(255,255,255,.2);border-color:transparent;color:#fff">学生用户</span></div>
    <div class="small" style="opacity:.85">学号 {me['no']} · {me['grade']}</div>
    <div class="small" style="opacity:.85">{me['org']} · {me['job']}</div></div>
  </div>
</div>
<div class="alert alert-info mt12">{icon('shield')}<div class="grow">学生身份无最终审核权，可发起申请和提交材料；仅可查看本人负责的账号。</div></div>
<div class="m-group mt12">
  {row('database', '', '我的账号', '5 个', 'accounts.html')}
  {row('clipboard', 'purple', '我的申请', '2 个进行中', 'applications.html')}
  {row('calendar', '', '我的年审', '<span class="c-primary">3 个待填报</span>', 'annual.html')}
  {row('wrench', 'orange', '整改任务', '<span class="c-danger">1 个待提交</span>', 'rectify.html')}
  {row('inbox', 'green', '我的待办', '6 项', 'todo.html')}
</div>
<div class="m-group">
  <div class="cell">{mi('bell', 'orange')}<span class="cell-label">审核结果提醒</span><button type="button" class="switch on ml-auto" aria-label="审核结果提醒"></button></div>
  <div class="cell">{mi('message', 'green')}<span class="cell-label">企业微信消息推送</span><button type="button" class="switch on ml-auto" aria-label="企业微信消息推送"></button></div>
  <div class="cell">{mi('clock', 'gray')}<span class="cell-label">截止前 3 天提醒</span><button type="button" class="switch ml-auto" aria-label="截止前提醒"></button></div>
</div>
<div class="m-group">
  {row('user-switch', '', '切换身份', '学生用户', '../common/identity-switch.html')}
  <div class="cell" data-toast="使用帮助：《学生用户操作指南》已发送至企业微信" style="cursor:pointer">{mi('help', 'gray')}<span class="cell-label">使用帮助</span><span class="cell-value"></span>{icon('chevron-right', cls='arrow')}</div>
  <div class="cell" data-toast="已是最新版本 v1.0.0" style="cursor:pointer">{mi('info', 'gray')}<span class="cell-label">关于平台</span><span class="cell-value">v1.0.0</span>{icon('chevron-right', cls='arrow')}</div>
</div>
<div class="m-group"><a class="logout" href="../common/login.html">退出登录</a></div>"""
    page("mine.html", "我的", content, tab="mine",
         notes=["个人资料来自学校统一身份认证，不可在本系统修改",
                "消息设置开关可即时切换，控制审核结果、企业微信推送与截止提醒",
                "“切换身份”进入身份选择；“退出登录”回到统一认证登录页"],
         flow=[("我的账号", "accounts.html"), ("我的申请", "applications.html"),
               ("切换身份", "../common/identity-switch.html"), ("退出登录", "../common/login.html")])


# ---------------------------------------------------------------- 学生：账号
def accounts():
    rows = [
        (AN, [st("正常运行"), st("已备案")], "account-detail.html", "annual"),
        (REN, [st("正常运行"), st("已备案")], "account-detail.html", "rename"),
        (HO, [st("正常运行"), st("已备案"), tag("待交接", "primary")], "account-detail.html", "handover"),
        (PH, [st("不活跃"), st("已备案"), st("疑似僵尸号")], "account-detail.html", "photo"),
        (NEW, [st("备案申请中")], "application-detail.html", "new"),
    ]
    cards = "".join(
        f'<a class="m-card" href="{h}" data-cat="{k}" style="display:block"><div class="flex gap12">{pf(a["platform"])}'
        f'<div class="grow" style="min-width:0"><div class="bold ellipsis">{a["name"]}</div><div class="small muted ellipsis">{a["platform"]} · {a["level"]} · {a["org_type"]}</div></div>'
        f'{icon("chevron-right", cls="arrow")}</div><div class="acct-tags">{"".join(tg)}</div>'
        f'<div class="mini-kv"><span>粉丝<b class="num">{a["fans"]}</b></span><span>指导教师<b>{a["teacher"]}</b></span><span>开通<b class="num">{a["opened"]}</b></span></div></a>'
        for a, tg, h, k in rows)
    content = f"""
<label class="m-search">{icon('search')}<input placeholder="搜索账号名称 / 平台" data-search="#acct-list"></label>
<div class="flex between small muted mb8" style="padding:0 2px"><span>我负责的账号 · 共 5 个</span><span>仅显示本人负责</span></div>
<div id="acct-list">{cards}</div>
<a class="m-card flex gap12" href="apply-claim.html" style="border:1px dashed var(--c-primary-border)">{mi('hand', 'green')}<div class="grow"><div class="bold">找不到我的账号？</div><div class="small muted">学校已导入的历史账号可在线认领</div></div>{icon('chevron-right', cls='arrow')}</a>"""
    page("accounts.html", "我的账号", content, back="mine.html",
         right='<a href="apply-claim.html">认领</a>',
         bottom=btn("认领账号", "apply-claim.html", "ghost", "hand") + btn("新建备案", "apply-create-basic.html", ic="plus"),
         notes=["仅显示李明本人负责的 5 个账号，其他账号不可见",
                "卡片展示运行状态、备案状态及风险标签（疑似僵尸号、待交接）",
                "搜索框按名称实时过滤；备案申请中的账号点击进入申请进度",
                "找不到账号时可通过“认领账号”认领学校已导入的历史数据"],
         flow=[("账号详情（剧本二起点）", "account-detail.html"), ("备案申请中 → 申请进度", "application-detail.html"),
               ("认领账号", "apply-claim.html")])


def account_detail():
    a = REN
    st4 = "".join(f'<div><small>{k}</small>{st(v)}</div>' for k, v in
                  [("运行状态", "正常运行"), ("备案状态", "已备案"), ("年审状态", "待指导教师审核"), ("年度异动", "无异动")])
    head = acct_head(a, f'{tag(a["level"], "primary")}{tag(a["org_type"], "muted")}',
                     extra=f'<div class="st4">{st4}</div>')
    copy_btn = f'<button type="button" class="btn-text btn" data-copy="{a["pid"]}">{a["pid"]}{icon("copy", 14)}</button>'
    content = f"""
{head}
{sec('基本信息')}
{group(
        cell('平台类型', a['platform']),
        cell('平台 ID', copy_btn),
        cell('粉丝数', f'<span class="num">{a["fans"]}</span>（2026-09-28 更新）'),
        cell('平台层级', a['level']),
        cell('所属组织', a['org']),
        cell('开通时间', a['opened']),
    )}
{sec('责任人员')}
{group(
        cell('指导教师', f'{a["teacher"]} · 宣传工作辅导员'),
        cell('具体负责人', '李明（本人）'),
        cell('第一责任人', '张卫东 · 党委副书记'),
    )}
{sec('运行情况')}
{group(
        cell('最近发布', '2026-09-28'),
        cell('更新频率', '每周更新（≥1次/周）'),
        cell('历史记录', '历任负责人 · 年审 · 变更', href='account-history.html'),
    )}
<div class="alert alert-info">{icon('info')}<div class="grow">账号名称、负责人、指导教师等信息变化请通过“信息变更”办理；平台 ID 变化须重新新建备案。</div></div>"""
    bottom = ('<div class="bb-grid">'
              f'<a href="apply-change.html">{mi("file-edit", "orange")}信息变更</a>'
              f'<a href="apply-handover.html">{mi("user-switch", "green")}负责人交接</a>'
              f'<a href="apply-cancel.html">{mi("power", "red")}注销</a>'
              f'<a href="annual.html">{mi("calendar")}年审</a></div>')
    page("account-detail.html", "账号详情", content, back="accounts.html", bottom=bottom,
         right='<button type="button" data-toast="已生成账号二维码名片（演示）">' + icon("qr", 20) + '</button>',
         notes=["顶部集中展示四套状态：运行 / 备案 / 年审 / 年度异动",
                "平台 ID 点击即可复制；历史记录查看历任负责人、历年年审与变更",
                "底部业务入口：信息变更（剧本二下一步）、负责人交接、注销、年审",
                "学生仅能发起申请，所有变更须经审核后才生效"],
         flow=[("剧本二下一步：信息变更", "apply-change.html"), ("负责人交接", "apply-handover.html"),
               ("账号历史", "account-history.html"), ("PC 端账号档案", "../../pc/common/archive-basic.html")])


def account_history():
    a = REN
    staff = timeline([
        ("now", "李明（现任）", "2025-06-20 至今 · 2023级软件工程2班", "学生会换届后接任新媒体负责人"),
        ("done", "周子豪", "2023-06-15 至 2025-06-20 · 2021级计算机科学1班", "毕业离任，交接给李明"),
        ("done", "罗佳怡", "2021-06-10 至 2023-06-15 · 2019级软件工程3班", ""),
        ("done", "唐嘉伟", "2016-03-12 至 2021-06-10 · 账号创建人", "历史补录，2024 年导入"),
    ])
    annual = timeline([
        ("now", "2026 年度 · 待指导教师审核", "2026-09-22 李明提交 · 王晓琳审核中", "无异动，账号正常运营"),
        ("done", "2025 年度 · 年审通过", "2025-11-18 校团委审核通过", "年度异动：变更（负责人交接）"),
        ("done", "2024 年度 · 年审通过", "2024-11-20 校团委审核通过", "年度异动：变更（指导教师由刘洋变更为王晓琳）"),
        ("done", "2023 年度 · 年审通过", "2023-11-16 校团委审核通过", "年度异动：无异动"),
    ])
    changes = timeline([
        ("done", "负责人交接：周子豪 → 李明", "2025-06-20 · 指导教师审核通过即生效", ""),
        ("done", "指导教师变更：刘洋 → 王晓琳", "2024-03-05 · 学院团委审核通过", "学院宣传工作分工调整"),
        ("done", "主页链接变更", "2022-09-01 · 学院团委审核通过", "微博主页短链更新"),
        ("done", "历史补录建档", "2024-01-10 · 学校导入 · 学院确认", "原备案纸质材料已扫描归档"),
    ])
    content = f"""
{mini_acct(a, st('正常运行'))}
<div class="seg" data-single=".hblk" style="display:flex;margin-bottom:12px">
  <button type="button" class="on grow" data-choice="#hb-staff">历任负责人</button>
  <button type="button" class="grow" data-choice="#hb-annual">历年年审</button>
  <button type="button" class="grow" data-choice="#hb-change">变更记录</button>
</div>
<div class="m-card hblk" id="hb-staff">{m_card_title('历任负责人', '<span class="small muted" style="font-weight:400">共 4 任</span>')}{staff}</div>
<div class="m-card hblk hidden" id="hb-annual">{m_card_title('历年年审', '<span class="small muted" style="font-weight:400">2023 - 2026</span>')}{annual}</div>
<div class="m-card hblk hidden" id="hb-change">{m_card_title('变更记录', '<span class="small muted" style="font-weight:400">共 4 条</span>')}{changes}</div>
<div class="alert alert-info">{icon('archive')}<div class="grow">负责人任职起止时间、历年年审与全部变更永久保留，账号注销后数据也不删除。</div></div>"""
    page("account-history.html", "账号历史", content, back="account-detail.html",
         notes=["分段切换“历任负责人 / 历年年审 / 变更记录”三类历史",
                "交接后原负责人的任职起止时间保留，形成完整责任链",
                "历年年审展示每年结果与年度异动类型"],
         flow=[("返回账号详情", "account-detail.html"), ("PC 档案 · 责任人员", "../../pc/common/archive-staff.html"),
               ("PC 档案 · 变更记录", "../../pc/common/archive-changes.html")])


# ---------------------------------------------------------------- 学生：业务申请入口
def apply():
    biz = [
        ("新建备案", "file-add", "", "新开通的新媒体账号首次登记备案，填写归属、平台、负责人并自选审核老师", ["指导教师", "学院团委", "校团委"], "apply-create-basic.html"),
        ("信息变更", "file-edit", "orange", "账号名称、负责人、指导教师、所属组织、主页链接等信息发生变化", ["指导教师", "学院团委", "重要变更报校团委"], "apply-change.html"),
        ("负责人交接", "user-switch", "green", "换届或卸任时把账号交接给继任者，原负责人任职记录保留", ["指导教师审核", "通过即生效"], "apply-handover.html"),
        ("账号注销", "power", "red", "组织撤销、社团停止运行、平台整合等，注销后数据永久保留", ["指导教师", "学院团委", "校团委"], "apply-cancel.html"),
        ("账号认领 / 历史补录", "hand", "purple", "认领学校已导入的历史账号，或补录此前未备案的账号", ["指导教师", "学院团委确认"], "apply-claim.html"),
    ]
    cards = "".join(
        f'<a class="m-card" href="{h}" style="display:block"><div class="biz">{mi(ic, c)}<div class="grow"><div class="flex between">'
        f'<b class="fs16">{t}</b>{icon("chevron-right", cls="arrow")}</div><div class="small sub mt4">{d}</div></div></div>{flow_hint(n)}</a>'
        for t, ic, c, d, n, h in biz)
    ongoing = "".join(
        f'<a class="todo-item" href="{h}">{pf(p, "sm")}<div class="grow" style="min-width:0"><div class="bold fs13 ellipsis">{t}</div>'
        f'<div class="small muted ellipsis">{m}</div></div>{st(s)}</a>'
        for t, m, p, s, h in [
            ("新建备案 · 中南计算机青年", "当前节点：学院团委审核（周建华）", "微信公众号", "审核中", "application-detail.html"),
            ("信息变更 · 计算机学院学生会", "当前节点：指导教师审核（王晓琳）", "微博", "审核中", "applications.html"),
        ])
    content = f"""
<div class="m-hero"><div style="position:relative;z-index:1"><div class="fs18 bold">请选择要办理的业务</div>
<div class="small mt4" style="opacity:.85">学生可发起申请、提交材料；审核由指导教师、学院团委与校团委逐级完成</div></div></div>
<div class="mt12">{cards}</div>
<div class="alert alert-warning">{icon('alert')}<div class="grow">平台 ID 发生变化不属于普通变更，须按“新建备案”办理，并同时注销原 ID 账号。</div></div>
<div class="m-title mt12">进行中的申请<a href="applications.html">全部{icon('chevron-right', 14)}</a></div>
<div class="m-card" style="padding:4px 14px">{ongoing}</div>"""
    page("apply.html", "业务申请", content, tab="apply",
         notes=["五类业务入口：新建备案、信息变更、负责人交接、账号注销、账号认领 / 历史补录",
                "每张卡片说明适用场景并预览审核流程，避免选错业务",
                "下方展示进行中的申请及当前节点，点击查看进度",
                "剧本一起点：点击“新建备案”进入四步填报向导"],
         flow=[("剧本一下一步：新建备案 ① 归属信息", "apply-create-basic.html"), ("信息变更（剧本二）", "apply-change.html"),
               ("负责人交接（剧本三）", "apply-handover.html"), ("我的申请", "applications.html")])


# ---------------------------------------------------------------- 学生：新建备案向导（剧本一）
def create_basic():
    org_chips = chips([("计算机学院团委新媒体中心", "a"), ("计算机学院学生会", "b"), ("计院青年志愿者协会", "c"), ("2023级软件工程2班团支部", "d")])
    content = f"""
{m_steps(WIZ, 0)}
<div data-form>
{sec('归属信息', '<span class="small">带 <span class="req">*</span> 为必填</span>')}
{group(
        ro('所属学校', '中南大学'),
        m_select('所属学院', COLLEGES, '计算机学院', req=True),
        m_input('所属团学组织', '请输入组织全称', NEW['org'], req=True),
        f'<div class="cell col-cell"><span class="small muted">本学院常用组织，点击快速填入</span>{org_chips}</div>',
        m_select('组织类别', ORG_TYPES, NEW['org_type'], req=True),
        m_select('平台层级', LEVELS, NEW['level'], req=True),
        '<div class="cell col-cell"><div class="lv-tip"><b>一级平台</b><span>学校及校级职能部门官方账号</span>'
        '<b>二级平台</b><span>学院及院级学生组织账号</span><b>三级平台</b><span>班级团支部账号</span>'
        '<b>社团平台</b><span>学生社团账号</span></div></div>',
    )}
</div>
<div class="alert alert-info">{icon('info')}<div class="grow">系统已根据你的身份预填学院与组织；所属组织须为已在册且存续的团学组织。</div></div>"""
    page("apply-create-basic.html", "新建 ① 归属信息", content, back="apply.html", nav_title="新建备案",
         right='<button type="button" data-toast="草稿已保存，可在“我的申请”中继续填写">存草稿</button>',
         bottom=back_btn("apply.html", "取消") + submit_btn("下一步", "apply-create-platform.html"),
         notes=["四步向导第 1 步：归属信息，已按李明身份预填计算机学院、新媒体中心",
                "所属团学组织支持手动输入，也可点击常用组织标签快速填入",
                "平台层级下方给出一级 / 二级 / 三级 / 社团平台的判定说明",
                "必填项留空点击“下一步”会标红提示"],
         flow=[("剧本一下一步：② 平台信息", "apply-create-platform.html"), ("返回业务申请", "apply.html")])


def create_platform():
    content = f"""
{m_steps(WIZ, 1)}
<div data-form>
{sec('平台基本信息')}
{group(
        m_select('平台类型', PLATFORM_TYPES, NEW['platform'], req=True),
        m_input('账号名称', '请输入平台上显示的名称', NEW['name'], req=True),
        m_input('曾用名', '无则不填'),
        m_input('平台 ID', '唯一标识，如微信号', NEW['pid'], req=True),
        f'<div class="cell"><span class="cell-label">头像</span><span class="ml-auto flex gap8"><span class="pf pf-wx">团</span>'
        f'<label class="upload" style="width:36px;height:36px;padding:0;display:grid;place-items:center;border-radius:9px">{icon("camera")}<input type="file" accept="image/*"></label></span></div>',
        yn('是否认证', 'auth', '否', ('已认证', '否')),
        m_input('粉丝数', '新开通账号可填 0', '0', typ='number'),
        m_input('主页链接', '请输入主页链接', 'https://mp.weixin.qq.com/csu_cs_youth', req=True),
        m_input('运营团队规模', '人数', '6 人'),
        m_input('开通时间', '', NEW['opened'], req=True),
    )}
{sec('四项机制', '<span class="small">未建立的机制须在备案后 30 日内补齐</span>')}
{group(
        yn('宣传联动机制', 'm1'), yn('信息发布审查机制', 'm2'), yn('应急处置预案', 'm3'), yn('信息安全管理制度', 'm4'),
    )}
{sec('平台介绍与发布范围')}
{group(
        m_textarea('平台介绍', '请介绍内容定位、栏目设置、信息发布范围与审核机制（不少于 100 字）', INTRO_SHORT, req=True, maxlen=800),
        m_radios('信息发布范围', 'scope', ['面向校内师生', '面向社会公众'], '面向校内师生'),
    )}
</div>"""
    page("apply-create-platform.html", "新建 ② 平台信息", content, back="apply-create-basic.html", nav_title="新建备案",
         right='<button type="button" data-toast="草稿已保存">存草稿</button>',
         bottom=back_btn("apply-create-basic.html", "上一步") + submit_btn("下一步", "apply-duplicate.html", toast="正在进行重复检查…"),
         notes=["平台类型、名称、平台 ID、主页链接、开通时间、平台介绍为必填",
                "四项机制（宣传联动 / 信息发布审查 / 应急预案 / 信息安全制度）逐项选择是否建立",
                "平台介绍限 800 字并实时计数；此处为第一次提交的简短版本（68 字），后续将被指导教师退回",
                "点击“下一步”后系统自动做重复检查（同平台同 ID、主页链接、相似名称）"],
         flow=[("剧本一下一步：重复检查结果", "apply-duplicate.html"), ("上一步：归属信息", "apply-create-basic.html")])


def duplicate():
    checks = [
        ("ok", "check", "同平台同 ID：未发现", "微信公众号 · csu_cs_youth 在全校账号库中无重复"),
        ("ok", "check", "相同主页链接：未发现", "主页链接未被其他账号登记"),
        ("warn", "alert", "高度相似名称：1 个", "“中南计算机学院”（微信公众号，已注销，相似度 82%）"),
    ]
    rows = "".join(f'<div class="chk"><span class="chk-ic {k}">{icon(ic)}</span><div class="grow"><div class="bold fs13">{t}</div>'
                   f'<div class="small muted">{d}</div></div></div>' for k, ic, t, d in checks)
    content = f"""
{m_steps(WIZ, 1)}
<div class="m-card"><div class="flex gap12">{mi('radar', 'orange')}<div class="grow"><div class="bold fs16">重复检查完成</div>
<div class="small muted">检查于 2026-09-24 10:08 · 检索全校 986 个账号</div></div>{tag('需确认', 'warning')}</div></div>
<div class="m-card" style="padding:2px 14px">{rows}</div>
{sec('相似账号详情')}
<div class="m-card"><div class="flex gap12">{pf('微信公众号')}<div class="grow"><div class="bold">中南计算机学院</div>
<div class="small muted">微信公众号 · ID csu_jsjxy · 2019-06 注销</div></div>{st('已注销')}</div>
<div class="mini-kv"><span>相似度<b class="c-warning">82%</b></span><span>原归属<b>计算机学院团委</b></span></div></div>
<div class="alert alert-danger">{icon('ban')}<div class="grow"><b>规则说明：</b>存在相同平台唯一 ID 时原则上禁止重复新建，应通过“认领”办理；名称相似仅作提示，确认不是同一账号后可继续。</div></div>"""
    page("apply-duplicate.html", "重复检查结果", content, back="apply-create-platform.html",
         bottom=back_btn("apply-create-platform.html", "返回修改") + btn("确认不是同一账号，继续", "apply-create-staff.html"),
         notes=["系统自动检查同平台同 ID、相同主页链接与高度相似名称三项",
                "本例仅发现相似名称（已注销的“中南计算机学院”），属提示级，可确认后继续",
                "若命中同平台同 ID，将禁止提交并引导走认领流程",
                "“返回修改”回到平台信息页"],
         flow=[("剧本一下一步：③ 运行与负责人", "apply-create-staff.html"), ("返回修改平台信息", "apply-create-platform.html"),
               ("PC 端：同 ID 禁止提交示例", "../../pc/common/apply-duplicate.html")])


def create_staff():
    li = PEOPLE["李明"]
    admins = [("陈可欣", "8209230221", "2023级软件工程1班 · 编辑"), ("刘子涵", "8209240133", "2024级人工智能2班 · 美编")]
    admin_rows = "".join(
        f'<div class="person staff-row">{face(n, "sm")}<div class="grow"><div class="bold fs13">{n}<span class="small muted" style="font-weight:400"> · {no}</span></div>'
        f'<div class="small muted">{d}</div></div><button type="button" class="x-mini" data-remove=".staff-row" aria-label="删除">{icon("trash", 15)}</button></div>'
        for n, no, d in admins)
    content = f"""
{m_steps(WIZ, 2)}
<div data-form>
{sec('运行信息')}
{group(
        m_input('最近发布时间', '', '2026-09-22', req=True),
        m_select('更新频率', UPDATE_FREQ, UPDATE_FREQ[0], req=True),
    )}
{sec('管理教师')}
{group(
        f'<div class="person">{avatar("王晓琳")}<div class="grow"><div class="bold fs13">王晓琳 {tag("管理教师", "warning")}</div>'
        f'<div class="small muted">计算机学院 · 宣传工作辅导员 · 139 7481 5520</div></div></div>',
    )}
{sec('具体负责人')}
{group(
        f'<div class="person">{avatar("李明")}<div class="grow"><div class="bold fs13">李明 {tag("本人", "primary")}</div>'
        f'<div class="small muted">{li["grade"]} · {li["no"]} · {li["phone"]}</div></div></div>',
    )}
{sec('管理员', '<span class="small">最多 5 人</span>')}
<div class="m-group">{admin_rows}<button type="button" class="add-row" data-toast="已打开添加管理员：输入学号即可检索（演示）">{icon('user-add')}添加管理员</button></div>
</div>"""
    page("apply-create-staff.html", "新建 ③ 运行与负责人", content, back="apply-duplicate.html", nav_title="新建备案",
         right='<button type="button" data-toast="草稿已保存">存草稿</button>',
         bottom=back_btn("apply-duplicate.html", "上一步") + submit_btn("下一步", "apply-create-reviewer.html"),
         notes=["填写最近发布时间与更新频率（7 档字典），用于后续僵尸号预警",
                "管理教师默认带出所属组织的指导教师王晓琳",
                "具体负责人为本人李明；管理员可添加、删除（点击垃圾桶移除该行）"],
         flow=[("剧本一下一步：④ 选择审核老师", "apply-create-reviewer.html"), ("上一步：重复检查", "apply-duplicate.html")])


def create_reviewer():
    teachers = [
        ("wxl", "王晓琳", "计算机学院 · 宣传工作辅导员", "推荐：该组织的管理教师", True),
        ("ly", "刘洋", "计算机学院 · 2023级辅导员", "你的年级辅导员", False),
        ("csy", "陈思远", "计算机学院团委 · 副书记", "", False),
        ("hj", "黄婧", "计算机学院 · 2022级辅导员", "", False),
    ]
    picked = "".join(f'<span class="tpick t-{k}{"" if on else " hidden"}"><b class="c-primary">{n}</b> · {d.split(" · ")[1]}</span>'
                     for k, n, d, _, on in teachers)
    items = "".join(
        f'<button type="button" class="choice{" on" if on else ""}" data-choice=".t-{k}" data-cat="{n}">{face(n)}<div class="grow" style="text-align:left">'
        f'<div class="bold fs13">{n}</div><div class="small muted">{d}</div>{f"<div class=small style=color:var(--c-success)>{r}</div>" if r else ""}</div>'
        f'<span class="ck"></span></button>'
        for k, n, d, r, on in teachers)
    overlay = f"""<div class="sheet-mask hidden" id="t-sheet"><div class="sheet">
  <div class="sheet-hd"><b>选择指导老师</b><button type="button" class="x-btn" data-toggle="#t-sheet" aria-label="关闭">{icon('x')}</button></div>
  <label class="m-search" style="background:#F5F7FA">{icon('search')}<input placeholder="搜索教师姓名" data-search="#t-list"></label>
  <div class="choices" id="t-list" data-single=".tpick">{items}</div>
  <button type="button" class="btn btn-primary" data-toggle="#t-sheet" data-toast="已选择一审指导老师">确定</button>
</div></div>"""
    preview = timeline([
        ("now", "指导老师审核 · 1 人审批", "王晓琳（可在上方更换）", ""),
        ("wait", "学院团委审核", "计算机学院团委 · 周建华", ""),
        ("wait", "校团委审核 · 2 人或签", "校团委宣传部 · 陈静 等 2 人，任一人通过即可", "终审通过后自动生成账号档案与备案表"),
    ])
    content = f"""
{m_steps(WIZ, 3)}
<div data-form>
{sec('一审指导老师')}
<div class="m-group"><div class="cell" data-toggle="#t-sheet" style="cursor:pointer"><span class="cell-label"><span class="req">*</span>指导老师</span>
<span class="cell-value">{picked}</span>{icon('chevron-right', cls='arrow')}</div></div>
{sec('审核流程预览')}
<div class="m-card">{preview}</div>
{sec('申请摘要')}
{group(
        cell('账号', f'{NEW["name"]} · {NEW["platform"]}'),
        cell('归属', '计算机学院团委新媒体中心'),
        cell('负责人', '李明 · 管理员 2 人'),
    )}
<label class="m-card flex gap8 top-align small sub" style="cursor:pointer"><input type="checkbox" checked style="accent-color:var(--c-primary);margin-top:4px">
<span>本人承诺所填信息真实准确，账号将严格执行信息发布审查制度，遵守《中南大学团学组织新媒体平台管理办法》。</span></label>
</div>"""
    page("apply-create-reviewer.html", "新建 ④ 选择审核老师", content, back="apply-create-staff.html", nav_title="新建备案",
         bottom=back_btn("apply-create-staff.html", "上一步") + submit_btn("提交申请", "apply-result.html", ic="send", toast="申请已提交"),
         overlay=overlay,
         notes=["点击“指导老师”弹出底部选择面板，可搜索、单选教师，默认推荐管理教师王晓琳",
                "流程预览：指导老师 1 人审批 → 学院团委 → 校团委 2 人或签",
                "勾选信息真实性承诺后提交，生成申请编号 " + NEW_NO],
         flow=[("剧本一下一步：提交成功", "apply-result.html"), ("上一步：运行与负责人", "apply-create-staff.html"),
               ("PC 端选择审核老师弹窗", "../../pc/common/modal-reviewer.html")])


def apply_result():
    mini = timeline([
        ("done", "学生提交新建备案申请", "李明 · 2026-09-24 10:12", ""),
        ("now", "指导教师审核", "王晓琳 · 处理中", ""),
        ("wait", "学院团委审核", "周建华", ""),
        ("wait", "校团委审核", "校团委宣传部", ""),
    ])
    actions = btn("查看进度", "application-detail.html", "ghost") + btn("返回首页", "home.html")
    info = (f'<div class="m-group mt16" style="text-align:left;background:#F7F9FB">'
            f'{cell("申请编号", f"<span class=num>{NEW_NO}</span>")}{cell("业务类型", "新建备案")}'
            f'{cell("账号", NEW["name"])}{cell("当前节点", "指导教师审核 · 王晓琳")}</div>')
    content = f"""
<div class="m-card">{result('ok', '申请已提交', '已通知指导教师王晓琳审核，审核结果将通过消息提醒你', actions, info)}</div>
<div class="m-card">{m_card_title('审核流程')}{mini}</div>
<div class="alert alert-info">{icon('info')}<div class="grow">负责人交接、信息变更等申请提交后同样进入此页，可在“我的申请”随时查看进度或撤回。</div></div>"""
    page("apply-result.html", "提交成功", content, back="home.html",
         notes=["展示申请编号 " + NEW_NO + " 与当前节点（指导教师审核 · 王晓琳）",
                "迷你时间线预览后续节点，“查看进度”进入申请详情",
                "剧本一下一步切换到 PC 端教师待办；剧本三下一步为移动端教师交接审核"],
         flow=[("剧本一下一步：PC 教师待办（演示下一角色）", "../../pc/teacher/todo.html"),
               ("剧本三下一步：APP 教师交接审核", "../teacher/review-handover.html"),
               ("查看申请进度", "application-detail.html"), ("返回首页", "home.html")])


# ---------------------------------------------------------------- 学生：变更 / 交接 / 注销 / 认领
def apply_change():
    a = REN
    fields = ["账号名称", "负责人", "指导教师", "所属组织", "联系方式", "二维码", "主页链接", "运营用途", "其他"]
    chip_html = "".join(f'<button type="button" class="chip{" on" if f == "账号名称" else ""}" data-choice="">{f}</button>' for f in fields)
    content = f"""
{mini_acct(a, st('已备案'))}
<div data-form>
{sec('选择变更项', '<span class="small">可多选</span>')}
<div class="m-card"><div class="chips">{chip_html}</div></div>
{sec('账号名称变更')}
{group(
        ro('原名称', a['name']),
        m_input('新名称', '请输入新名称', a['new_name'], req=True),
        m_textarea('变更原因', '请说明变更原因', REN_STEPS[0][3], req=True, maxlen=200),
        up_cell('证明材料', '如换届决议、名称变更说明，支持 jpg / png / pdf', ['学生会第十届换届决议.pdf']),
    )}
</div>
<div class="alert alert-warning">{icon('alert')}<div class="grow"><b>平台 ID 变化不按普通变更办理</b>，需重新新建备案并注销原账号。<a class="link" href="apply-create-basic.html">去新建</a></div></div>"""
    page("apply-change.html", "信息变更", content, back="account-detail.html",
         bottom=back_btn("account-detail.html", "取消") + submit_btn("下一步", "apply-change-confirm.html"),
         notes=["先勾选变更项（可多选），本例选择“账号名称”",
                "原名称只读，新名称“中南计院学生会”必填，变更原因必填",
                "平台 ID 变化不走普通变更，提示转新建",
                "下一步自动生成变更前后对比供确认"],
         flow=[("剧本二下一步：变更前后对比确认", "apply-change-confirm.html"), ("返回账号详情", "account-detail.html")])


def change_confirm():
    a = REN
    same = [("平台类型", a["platform"]), ("平台 ID", a["pid"]), ("负责人", "李明"), ("指导教师", a["teacher"]), ("所属组织", a["org"])]
    same_rows = "".join(f'<div class="cmp"><div class="flex between"><b class="fs13">{k}</b><span class="small muted">未变更</span></div>'
                        f'<div class="cmp-row sub">{v}</div></div>' for k, v in same)
    arrow = icon("arrow-right")
    preview = timeline([
        ("now", "指导教师审核", "王晓琳", ""),
        ("wait", "学院团委审核", "周建华 · 属重要变更，审核后报校团委", ""),
        ("wait", "校团委审核", "校团委宣传部", "通过后新名称生效，原名称记入曾用名"),
    ])
    content = f"""
{mini_acct(a, tag('重要变更', 'warning'))}
{sec('变更内容', '<span class="small">共 1 项变更</span>')}
<div class="m-card" style="padding:2px 14px">
  <div class="cmp"><div class="flex between"><b class="fs13">账号名称</b>{tag('已变更', 'warning')}</div>
  <div class="cmp-row"><span class="old">{a['name']}</span>{arrow}<span class="new">{a['new_name']}</span></div></div>
  <div class="cmp"><div class="flex between"><b class="fs13">曾用名</b>{tag('系统自动记录', 'primary')}</div>
  <div class="cmp-row"><span class="muted">无</span>{arrow}<span class="new">{a['name']}</span></div></div>
</div>
{sec('其余信息')}
<div class="m-card" style="padding:2px 14px">{same_rows}</div>
{sec('变更原因与材料')}
<div class="m-card"><div class="fs13 sub">{REN_STEPS[0][3]}</div><div class="upload-list">{file_btns(['学生会第十届换届决议.pdf'])}</div></div>
{sec('审核流程')}
<div class="m-card">{preview}</div>"""
    page("apply-change-confirm.html", "变更确认", content, back="apply-change.html",
         bottom=back_btn("apply-change.html", "返回修改") + submit_btn("确认提交", "apply-result.html", ic="send",
                                                                        toast="变更申请已提交，编号 " + FLOWS["rename"]["no"]),
         notes=["逐项展示变更前后对比：旧值删除线、新值绿色高亮，未变更字段单独列出",
                "名称变更属于重要变更：教师 → 学院 → 校团委三级审核",
                "生效后原名称自动记入曾用名，档案可追溯",
                "确认提交后生成编号 " + FLOWS["rename"]["no"]],
         flow=[("剧本二下一步：PC 教师变更审核", "../../pc/teacher/review-change.html"), ("提交成功", "apply-result.html"),
               ("返回修改", "apply-change.html")])


def apply_handover():
    a = HO
    li, ls = PEOPLE["李明"], PEOPLE["李四"]
    content = f"""
{mini_acct(a, st('正常运行'))}
<div data-form>
{sec('原负责人')}
{group(ro('姓名', '李明'), ro('学号', li['no']), ro('任期', '2024-09-10 起 至 生效日'))}
{sec('新负责人')}
{group(
        m_input('姓名', '请输入姓名', '李四', req=True),
        m_input('学号', '请输入学号', ls['no'], req=True),
        m_input('联系方式', '请输入手机号', ls['phone'], req=True, typ='tel'),
        ro('班级', ls['grade']),
        m_input('社团职务', '如宣传部部长', ls['job']),
    )}
{sec('交接信息')}
{group(
        m_input('生效时间', '', '2026-10-01', req=True),
        m_textarea('交接说明', '请说明交接原因及交接内容', HO_STEPS[0][3], req=True, maxlen=200),
    )}
</div>
<div class="m-card flex gap12 top-align">{mi('route', 'green')}<div class="grow small sub"><b class="fs13" style="color:var(--c-text)">交接流程</b><br>
学生提交 → 具体管理教师审核 → 生效。原负责人任职起止时间将保留在账号历史中，账号密码请线下当面交接。</div></div>"""
    page("apply-handover.html", "负责人交接", content, back="account-detail.html",
         bottom=back_btn("account-detail.html", "取消") + submit_btn("提交申请", "apply-result.html", ic="send",
                                                                    toast="交接申请已提交，编号 " + FLOWS["handover"]["no"]),
         notes=["剧本三起点：计院街舞社（抖音）负责人由李明交接给李四",
                "原负责人信息只读，任期自 2024-09-10 起；新负责人姓名、学号、联系方式、生效时间必填",
                "交接只需管理教师王晓琳审核，通过即生效，历史任职记录保留"],
         flow=[("剧本三下一步：提交成功", "apply-result.html"), ("教师移动端交接审核", "../teacher/review-handover.html"),
               ("PC 档案 · 责任人员历史", "../../pc/common/archive-staff.html")])


def apply_cancel():
    opts = ["计院摄影协会（视频号）", "计院街舞社（抖音）", "计算机学院学生会（微博）", "中南计院团委（微信公众号）"]
    content = f"""
<div data-form>
{sec('注销账号')}
{group(
        m_select('选择账号', opts, opts[0], req=True),
        cell('平台 ID', PH['pid']),
        cell('当前状态', st('不活跃') + ' ' + st('已备案')),
    )}
{sec('注销原因')}
{group(
        m_radios('注销原因（单选）', 'cancel', CANCEL_REASONS, None),
        m_textarea('情况说明', '请说明注销原因、账号后续处置方式等', '', req=True, maxlen=300),
        up_cell('佐证材料', '如组织撤销文件、平台注销截图等', ()),
    )}
</div>
<div class="alert alert-info">{icon('archive')}<div class="grow">审核完成后<b>账号不删除</b>，状态改为“已注销”，历史档案与年审记录永久保留。</div></div>
<div class="m-card small sub">{flow_hint(['指导教师', '学院团委', '校团委'])}</div>"""
    page("apply-cancel.html", "账号注销", content, back="account-detail.html",
         bottom=back_btn("account-detail.html", "取消") + submit_btn("提交申请", "apply-result.html", ic="send", toast="注销申请已提交"),
         notes=["从本人负责的账号中选择要注销的账号",
                "注销原因使用数据字典（团支部毕业、社团停止运行、平台整合等 9 项）",
                "情况说明为必填，留空提交会标红提示",
                "审核完成后账号不删除，状态改为已注销"],
         flow=[("提交成功", "apply-result.html"), ("教师注销审核（PC）", "../../pc/teacher/review-cancel.html"),
               ("PC 档案 · 注销信息", "../../pc/common/archive-cancel.html")])


def apply_claim():
    items = [
        ("2023级软件工程2班团支部", "QQ", "3301458862", "班级团支部", "与你所在班级匹配"),
        ("计院羽毛球协会", "抖音", "csu_cs_badminton", "社团组织", ""),
        ("计院辩论队", "微信公众号", "csu_cs_debate", "院级学生组织", ""),
        ("计院青年之声", "微博", "6630912204", "院级学生组织", ""),
    ]
    rows = "".join(
        f'<div class="m-card flex gap12" data-cat="c{i}">{pf(p)}<div class="grow" style="min-width:0"><div class="bold ellipsis">{n}</div>'
        f'<div class="small muted ellipsis">{p} · {pid}</div><div class="small muted">{o} · 2026-09-10 学校导入</div>'
        f'{f"<div class=small style=color:var(--c-success)>{m}</div>" if m else ""}</div>'
        f'<button type="button" class="btn btn-ghost btn-sm" data-toast="已加入认领清单：{n}">认领</button></div>'
        for i, (n, p, pid, o, m) in enumerate(items))
    content = f"""
<label class="m-search">{icon('search')}<input placeholder="搜索账号名称 / 平台 ID" data-search="#claim-list"></label>
<div class="alert alert-info">{icon('info')}<div class="grow">以下为学校导入、尚未认领的历史账号。认领后由指导教师确认，你将成为该账号负责人。</div></div>
<div class="flex between small muted mt12 mb8" style="padding:0 2px"><span>待认领账号 · 共 {len(items)} 个</span><span>计算机学院</span></div>
<div id="claim-list">{rows}</div>
<a class="m-card flex gap12" href="apply-create-basic.html" style="border:1px dashed var(--c-primary-border)">{mi('file-add', 'purple')}
<div class="grow"><div class="bold">历史补录</div><div class="small muted">此前开通但从未备案、也不在导入名单中的账号</div></div>{icon('chevron-right', cls='arrow')}</a>
<div class="m-group">{m_textarea('认领说明', '如：本人为该团支部现任宣传委员', '本人为 2023级软件工程2班团支部宣传委员，负责班级 QQ 号日常运营。')}</div>"""
    page("apply-claim.html", "账号认领", content, back="apply.html",
         bottom=back_btn("apply.html", "取消") + submit_btn("提交认领申请", "apply-result.html", ic="send", toast="认领申请已提交，等待指导教师确认"),
         notes=["列表为学校 Excel 导入、尚未认领的本学院历史账号，支持按名称 / ID 搜索",
                "点击“认领”加入认领清单，填写认领说明后统一提交",
                "不在导入名单中的历史账号走“历史补录”（复用新建备案表单）",
                "同平台同 ID 已存在的账号禁止重复新建，须通过认领办理"],
         flow=[("提交成功", "apply-result.html"), ("历史补录 → 新建表单", "apply-create-basic.html"),
               ("学院确认导入数据（PC）", "../../pc/college/import-confirm.html")])


# ---------------------------------------------------------------- 学生：我的申请与进度
def applications():
    apps = [
        ("ing", "新建备案", NEW_NO, NEW["name"], "微信公众号", "学院团委审核 · 周建华", "审核中", "2026-09-26 重新提交", "application-detail.html"),
        ("ing", "信息变更", FLOWS["rename"]["no"], REN["name"], "微博", "指导教师审核 · 王晓琳", "审核中", "2026-09-26 提交", "application-detail.html"),
        ("back", "新建备案", NEW_NO, NEW["name"], "微信公众号", "第 1 次提交被退回 · 王晓琳", "已退回", "2026-09-25 退回", "application-returned.html"),
        ("pass", "新建备案", NEW_NO, NEW["name"], "微信公众号", "校团委终审通过 · 已生成备案表", "已通过", "2026-09-30 完成", "application-approved.html"),
        ("pass", "负责人交接", FLOWS["handover"]["no"], HO["name"], "抖音", "指导教师审核通过，交接生效", "已通过", "2026-09-28 完成", "../../pc/common/archive-staff.html"),
        ("reject", "新建备案", "XJ20260912006", "计院学生会", "抖音", "指导教师驳回 · 与已备案账号重复", "已驳回", "2026-09-13 驳回", "application-rejected.html"),
    ]
    cards = "".join(
        f'<a class="m-card" href="{h}" data-cat="{c}" style="display:block;position:relative"><div class="flex between gap8"><span class="small muted ellipsis">{b} · <span class="num">{no}</span></span>'
        f'{"" if c == "ing" else st(s)}</div>'
        f'<div class="flex gap8 mt8">{pf(p, "sm")}<b class="ellipsis">{n}</b><span class="small muted nowrap">{p}</span></div>'
        f'<div class="small sub mt8">当前节点：{node}</div><div class="small muted">{tm}</div>'
        f'{"<img class=m-stamp src=../../assets/m-stamp-approving.png alt=审核中>" if c == "ing" else ""}</a>'
        for c, b, no, n, p, node, s, tm, h in apps)
    tabs = "".join(f'<button type="button" data-seg="{v}"{" class=on" if v == "all" else ""}>{t}</button>'
                   for t, v in [("全部", "all"), ("审核中", "ing"), ("已退回", "back"), ("已通过", "pass"), ("已驳回", "reject")])
    content = f"""
<div class="m-tabs" data-target="#app-list">{tabs}</div>
<div id="app-list">{cards}</div>
<div class="small muted" style="text-align:center;padding:4px 0 8px">“中南计算机青年”的退回 / 通过卡片演示同一申请在不同阶段的页面</div>"""
    page("applications.html", "我的申请", content, back="home.html",
         notes=["页签按状态筛选：审核中 / 已退回 / 已通过 / 已驳回",
                "每张卡片展示业务类型、编号、账号、当前节点与状态",
                "点击进入对应的进度页：审核中、退回修改、备案完成、驳回终止"],
         flow=[("审核中 → 申请进度", "application-detail.html"), ("已退回 → 查看退回意见", "application-returned.html"),
               ("已通过 → 备案完成", "application-approved.html"), ("已驳回 → 驳回原因", "application-rejected.html")])


def application_detail():
    items = tl_new(["done", "back", "done", "done"]) + [
        ("now", "学院团委审核", "周建华 · 计算机学院团委书记 · 处理中", ""),
        ("wait", "校团委审核", "校团委宣传部 · 2 人或签", ""),
    ]
    head = (f'<div class="hd-card"><div class="flex between"><span class="small muted">新建备案 · <span class="num">{NEW_NO}</span></span>{st("审核中")}</div>'
            f'<div class="flex gap12 mt12">{pf(NEW["platform"], "lg")}<div class="grow"><div class="fs16 bold">{NEW["name"]}</div>'
            f'<div class="small muted">{NEW["platform"]} · ID {NEW["pid"]}</div></div></div>'
            f'<div class="alert alert-warning mt12">{icon("clock")}<div class="grow">当前状态：<b>待学院审核</b>，已流转 1 天，预计 3 个工作日内完成</div></div></div>')
    content = f"""
{head}
{m_steps(['提交', '指导教师', '学院团委', '校团委', '完成'], 2)}
<div class="m-card">{kv([
        ('当前节点', '学院团委 · 周建华'),
        ('是否退回', '否 <span class="small muted">（历史退回 1 次）</span>'),
        ('最近审核意见', f'{NEW_STEPS[3][1]}：{NEW_STEPS[3][3]}', True),
        ('下一步操作', '无需操作，等待学院审核；如超时可点击“催办”', True),
    ], 2)}</div>
<div class="m-card">{m_card_title('审核进度', '<span class="small muted" style="font-weight:400">共 6 个节点</span>')}{timeline(items)}</div>
{sec('申请信息')}
{group(
        cell('所属组织', NEW['org']),
        cell('平台层级', NEW['level']),
        cell('平台介绍', '<span class="c-success">326 字（已补充）</span>'),
        cell('一审老师', '王晓琳'),
    )}"""
    page("application-detail.html", "申请进度", content, back="applications.html",
         bottom=btn("撤回申请", kind="default", ic="undo", toast="审核中的申请撤回后可修改再提交（演示）")
         + btn("催办", kind="primary", ic="bell", toast="已向学院团委周建华老师发送催办提醒"),
         notes=["顶部显示状态“待学院审核”，节点进度条定位到学院团委",
                "时间线完整记录：提交 → 教师退回（橙色） → 修改重提 → 教师通过 → 学院审核中",
                "按文档展示当前节点、审核意见、是否退回、下一步操作",
                "可撤回申请或向当前审核人催办"],
         flow=[("剧本一下一步：PC 教师再次审核通过", "../../pc/common/modal-approve.html"),
               ("学院审核（PC）", "../../pc/college/approval-detail.html"), ("我的申请", "applications.html")])


def application_returned():
    back_step = NEW_STEPS[1]
    items = tl_new(["done", "back"]) + [("now", "待申请人修改后重新提交", "李明 · 请于 2026-10-09 前处理", "")]
    content = f"""
<div class="hd-card" style="background:linear-gradient(180deg,#FFF1F1,#fff 70%)">
  <div class="flex gap12">{mi('undo', 'red')}<div class="grow"><div class="fs16 bold c-danger">申请已退回，请修改</div>
  <div class="small muted">{back_step[2]} · {back_step[1]} · {back_step[0]}</div></div>{st('已退回')}</div>
  <div class="tl-comment" style="background:var(--c-danger-bg);border-left-color:var(--c-danger);margin-top:12px">退回意见：{back_step[3]}</div>
</div>
{mini_acct(NEW, tag('新建备案', 'primary'))}
{sec('需修改的字段', '<span class="small c-danger">1 项</span>')}
<div class="m-card hl"><div class="flex between"><b class="fs13">平台介绍</b>{tag('需修改', 'danger')}</div>
<div class="intro-box mt8">{INTRO_SHORT}</div>
<div class="small c-danger mt8">当前 {len(INTRO_SHORT)} 字，要求不少于 100 字，需补充内容定位、栏目设置和信息发布范围</div></div>
{sec('无需修改')}
{group(cell('归属信息', '<span class="c-success">无需修改</span>'), cell('平台信息（其余字段）', '<span class="c-success">无需修改</span>'),
       cell('运行与负责人', '<span class="c-success">无需修改</span>'), cell('审核老师', '王晓琳'))}
<div class="m-card">{m_card_title('处理记录')}{timeline(items)}</div>"""
    page("application-returned.html", "申请进度 · 已退回", content, back="applications.html", nav_title="申请已退回",
         bottom=btn("撤销申请", kind="danger", toast="已撤销申请，流程终止（演示）") + btn("修改并重新提交", "application-edit.html", ic="edit"),
         notes=["顶部红色横幅展示退回人、时间与退回意见（FLOWS 剧本一第 2 步）",
                "需修改字段“平台介绍”红框高亮，并给出当前字数与要求",
                "其余字段标注“无需修改”，修改时只需关注标红项",
                "“修改并重新提交”进入修改页；“撤销申请”终止流程"],
         flow=[("剧本一下一步：修改后重新提交", "application-edit.html"), ("PC 端退回弹窗（上一步）", "../../pc/common/modal-return.html"),
               ("我的申请", "applications.html")])


def application_edit():
    back_step = NEW_STEPS[1]
    content = f"""
<div class="alert alert-danger">{icon('undo')}<div class="grow"><b>{back_step[1]}退回意见：</b>{back_step[3]}</div></div>
<div data-form class="mt12">
{sec('归属与平台（无需修改）')}
{group(
        ro('所属组织', NEW['org']),
        ro('平台类型', NEW['platform']),
        ro('账号名称', NEW['name']),
        ro('平台 ID', NEW['pid']),
    )}
{sec('需修改内容', '<span class="small c-danger">已按意见补充</span>')}
<div class="m-group hl">
  {m_textarea('平台介绍', '请介绍内容定位、栏目设置、信息发布范围与审核机制（不少于 100 字）', INTRO_FULL, req=True, maxlen=800)}
  {m_radios('信息发布范围', 'scope', ['面向校内师生', '面向社会公众'], '面向校内师生')}
  {m_textarea('修改说明', '向审核老师说明本次修改内容', NEW_STEPS[2][3], req=True, maxlen=200)}
</div>
</div>
<div class="alert alert-info">{icon('info')}<div class="grow">重新提交后回到<b>指导教师审核</b>节点，审核老师仍为王晓琳。</div></div>"""
    page("application-edit.html", "修改后重新提交", content, back="application-returned.html",
         bottom=back_btn("application-returned.html", "取消") + submit_btn("重新提交", "application-detail.html", ic="send",
                                                                           toast="已重新提交，回到指导教师审核节点"),
         notes=["顶部固定展示退回意见，便于对照修改",
                "平台介绍已补充至 " + str(len(INTRO_FULL)) + " 字，覆盖内容定位、栏目设置、发布范围、审核机制",
                "未被要求修改的字段只读，防止误改",
                "重新提交后回到指导教师审核节点"],
         flow=[("剧本一下一步：进度 · 待学院审核", "application-detail.html"), ("返回退回详情", "application-returned.html")])


def application_approved():
    items = tl_new(["done", "back", "done", "done", "done", "done"])
    info = (f'<div class="m-group mt16" style="text-align:left;background:#F7F9FB">'
            f'{cell("备案编号", f"<b class=num>{FILING_NO}</b>")}{cell("申请编号", f"<span class=num>{NEW_NO}</span>")}'
            f'{cell("账号", NEW["name"] + " · " + NEW["platform"])}{cell("备案时间", "2026-09-30 10:05")}</div>')
    actions = btn("下载备案表", kind="ghost", ic="download", toast="《新媒体公众平台备案表》已开始下载") + btn("查看账号", "account-detail.html")
    content = f"""
<div class="m-card">{result('ok', '备案完成', '校团委已审核通过，账号档案与备案表已自动生成', actions, info)}</div>
<div class="m-card">{m_card_title('完整审核记录', '<span class="small muted" style="font-weight:400">6 个节点</span>')}{timeline(items)}</div>
<div class="alert alert-success">{icon('check-circle')}<div class="grow">账号状态已更新为<b>正常运行 · 已备案</b>，将自动纳入 2027 年度年审。</div></div>"""
    page("application-approved.html", "申请进度 · 已通过", content, back="applications.html", nav_title="备案完成",
         notes=["成功态展示备案编号、申请编号与备案时间",
                "完整时间线：提交、教师退回、修改重提、教师通过、学院通过、校团委通过",
                "可下载自动生成的备案表，或查看已建立的账号"],
         flow=[("剧本一下一步：PC 账号档案已建立", "../../pc/common/archive-basic.html"),
               ("备案表预览（PC）", "../../pc/school/filing-form.html"), ("查看账号", "account-detail.html")])


def application_rejected():
    items = [
        ("done", "学生提交新建备案申请", "李明 · 2026-09-12 16:30", ""),
        ("reject", "指导教师驳回", "王晓琳 · 2026-09-13 09:10", "与已备案账号重复，请通过认领办理。该抖音号（ID csu_cs_su）已于 2024 年由学校导入。"),
        ("wait", "流程终止", "驳回后不可修改重提", ""),
    ]
    content = f"""
<div class="m-card">{result('err', '申请已驳回', '该申请不予办理，流程已终止')}</div>
<div class="m-card"><div class="flex gap12">{pf('抖音')}<div class="grow"><div class="bold">计院学生会</div>
<div class="small muted">抖音 · ID csu_cs_su · 新建备案 · XJ20260912006</div></div>{st('已驳回')}</div></div>
<div class="alert alert-danger">{icon('ban')}<div class="grow"><b>驳回原因：</b>与已备案账号重复，请通过认领办理。</div></div>
<div class="m-card mt12">{m_card_title('处理记录')}{timeline(items)}</div>
<div class="alert alert-info">{icon('info')}<div class="grow">“驳回”与“退回”不同：退回可修改后重新提交，驳回则流程终止，需按正确业务重新发起。</div></div>"""
    page("application-rejected.html", "申请进度 · 已驳回", content, back="applications.html", nav_title="申请已驳回",
         bottom=btn("重新发起", "apply.html", "default") + btn("申请认领", "apply-claim.html", ic="hand"),
         notes=["驳回示例：计院学生会（抖音）新建与已备案账号重复",
                "展示驳回原因与处理记录，流程终止不可重提",
                "引导通过“申请认领”办理，或重新发起其他业务"],
         flow=[("申请认领", "apply-claim.html"), ("重新发起", "apply.html"), ("PC 驳回弹窗", "../../pc/common/modal-reject.html")])


# ---------------------------------------------------------------- 学生：年审（剧本五）
def annual():
    rows = [
        (AN, "待填报", "确认本年度变化后提交", "annual-fill.html", ""),
        (REN, "待指导教师审核", "09-22 已提交 · 王晓琳审核中", "annual-result.html", ""),
        (HO, "待填报", "历史数据已继承，待确认", "annual-fill.html", ""),
        (PH, "待填报", "停更 212 天，请先完成核实", "zombie-verify.html", st("疑似僵尸号")),
        (RE, "待整改", "第 2 轮整改材料待提交", "rectify.html", tag("管理员", "muted")),
    ]
    cards = "".join(
        f'<a class="m-card flex gap12" href="{h}">{pf(a["platform"])}<div class="grow" style="min-width:0">'
        f'<div class="flex gap6"><b class="ellipsis">{a["name"]}</b>{x}</div><div class="small muted ellipsis">{m}</div></div>'
        f'<div class="flex gap4" style="flex:none">{st(s, False)}{icon("chevron-right", cls="arrow")}</div></a>'
        for a, s, m, h, x in rows)
    content = f"""
<div class="m-hero"><div style="position:relative;z-index:1">
  <div class="flex between"><span class="small" style="opacity:.85">年审任务 · NS{T['year']}</span>{countdown(15)}</div>
  <div class="fs16 bold mt4">{T['name']}</div>
  <div class="small mt4" style="opacity:.85">学生填报截止 {T['stu_end']} · 教师审核截止 {T['teacher_end']}</div>
  <div class="flex gap8 mt12"><div class="progress" style="background:rgba(255,255,255,.25)"><i style="width:40%;background:#fff"></i></div><span class="small bold nowrap">已提交 2 / 5</span></div>
</div></div>
<div class="alert alert-info mt12">{icon('refresh')}<div class="grow"><b>历史数据自动继承</b>，只需确认本年度变化；无变化的账号确认后即可提交。</div></div>
<div class="m-title mt12">我负责的年审账号<span class="small muted" style="font-weight:400">共 5 个</span></div>
{cards}
<div class="m-card flex gap12" style="background:#F7F9FB;box-shadow:none">{pf(NEW['platform'])}<div class="grow"><div class="bold">{NEW['name']}</div>
<div class="small muted">2026-09-20 新开通，本年度不参与年审</div></div>{st('备案申请中', False)}</div>"""
    page("annual.html", "我的年审", content, tab="annual",
         notes=["顶部任务横幅：年审名称、学生填报截止 " + T["stu_end"] + "、倒计时与本人完成进度 2 / 5",
                "列出本人负责账号的年审状态，点击进入填报、核实或整改",
                "疑似僵尸号需先完成核实；整改中的账号进入整改任务",
                "遵循“历史数据自动继承，只需确认本年度变化”原则"],
         flow=[("剧本五下一步：年审填报（中南计院团委）", "annual-fill.html"), ("疑似僵尸号核实", "zombie-verify.html"),
               ("整改任务（剧本六）", "rectify.html"), ("PC 年审任务详情（上一步）", "../../pc/school/annual-task-detail.html")])


def annual_fill():
    a = AN
    inherit = kv([("平台 / ID", f"{a['platform']} · {a['pid']}", True), ("平台层级", a["level"]), ("所属组织", a["org"]),
                  ("指导教师", a["teacher"]), ("运营负责人", a["student"]), ("粉丝数", a["fans"]), ("更新频率", "每周更新")], 2)
    content = f"""
{mini_acct(a, st('待填报'))}
<div class="m-card">{m_card_title('上年度信息', tag('继承自 2025 年度', 'primary'))}{inherit}</div>
<div data-form>
{sec('本年度确认项', '<span class="small">共 9 项</span>')}
{group(
        yn('1. 账号是否仍存在', 'q1', '是'),
        yn('2. 是否正常运营', 'q2', '是'),
        yn('3. 是否能正常访问', 'q3', '是'),
        m_input('4. 最近一次公开发布时间', '', '2026-09-17', req=True),
        m_input('5. 当前运营负责人', '请输入姓名', '李明', req=True),
        yn('6. 指导教师是否变化', 'q6', '否'),
        yn('7. 账号名称是否变化', 'q7', '否'),
        yn('8. 是否需要注销', 'q8', '否'),
        yn('9. 是否存在其他异常', 'q9', '否'),
    )}
<div class="m-group"><div class="cell"><span class="cell-label">年度异动</span><span class="cell-value">{st('无异动')}</span></div>
<div class="cell" style="padding-top:0;min-height:0"><span class="small muted">系统根据以上确认项自动判定，无需手动选择</span></div></div>
{sec('佐证材料')}
<div class="m-group"><div class="cell col-cell"><span class="cell-label"><span class="req">*</span>账号主页截图</span>
<div class="flex gap12 top-align"><img class="thumb" src="{PHOTOS['screenshot']}" alt="账号主页截图">
<div class="grow">{upload('继续上传', '需包含账号名称与最近发布时间', ())}</div></div></div></div>
</div>"""
    page("annual-fill.html", "年审填报", content, back="annual.html",
         bottom=btn("暂存", kind="default", toast="已暂存，可稍后继续填写") + submit_btn("提交年审", "annual-result.html", ic="send", toast="年审已提交"),
         notes=["上年度信息自动继承，只需逐项确认本年度变化",
                "9 项确认项：是否存在、正常运营、可访问、最近发布时间、负责人、教师 / 名称变化、是否注销、其他异常",
                "年度异动根据确认项自动计算，本例为“无异动”",
                "上传账号主页截图作为佐证，提交后进入指导教师审核"],
         flow=[("剧本五下一步：提交成功", "annual-result.html"), ("返回我的年审", "annual.html")])


def annual_result():
    items = timeline([
        ("done", "系统生成年审记录", "2026-09-15 09:00 · 继承 2025 年度信息", ""),
        ("done", "学生确认无异动并提交", "李明 · 刚刚", "账号正常运营，最近发布 2026-09-17"),
        ("now", "指导教师审核", f"王晓琳 · 截止 {T['teacher_end']}", ""),
        ("wait", "学院统一提交校团委", f"周建华 · 截止 {T['college_end']}", ""),
        ("wait", "校团委审核", f"截止 {T['school_end']}", "无异动无风险账号将批量审核"),
    ])
    info = (f'<div class="m-group mt16" style="text-align:left;background:#F7F9FB">'
            f'{cell("年审编号", "<span class=num>NS2026-CS-0012</span>")}{cell("账号", AN["name"])}'
            f'{cell("年度异动", st("无异动"))}{cell("下一节点", "指导教师审核 · 王晓琳")}</div>')
    actions = btn("返回年审", "annual.html", "ghost") + btn("返回首页", "home.html")
    content = f"""
<div class="m-card">{result('ok', '年审已提交', f'等待指导教师王晓琳审核，审核截止 {T["teacher_end"]}', actions, info)}</div>
<div class="m-card">{m_card_title('年审流程')}{items}</div>
<div class="alert alert-info">{icon('calendar')}<div class="grow">你还有 <b>3 个账号</b>待填报年审（含 1 个疑似僵尸号需核实），请在 {T['stu_end']} 前完成。</div></div>"""
    page("annual-result.html", "年审提交成功", content, back="annual.html",
         notes=["提交成功后显示下一节点：指导教师审核（王晓琳，截止 " + T["teacher_end"] + "）",
                "时间线预览学院统一提交、校团委批量审核等后续节点",
                "提醒本人其余待填报账号"],
         flow=[("剧本五下一步：APP 教师年审审核", "../teacher/review-annual.html"), ("返回我的年审", "annual.html")])


# ---------------------------------------------------------------- 学生：整改（剧本六）
def rectify():
    a = RE
    s = RC["steps"]
    history = timeline([
        ("done", s[0][2], f"{s[0][1]} · {s[0][0]}", s[0][3]),
        ("done", s[1][2], f"{s[1][1]} · {s[1][0]}", s[1][3]),
        ("done", s[2][2], f"{s[2][1]} · {s[2][0]}", s[2][3]),
        ("back", "第 1 轮结果：继续整改", f"{s[3][1]} · {s[3][0]}", s[3][3]),
        ("now", "第 2 轮：待提交整改材料", f"何雨桐 / 李明 · 截止 {RC['deadline']}", ""),
    ])
    content = f"""
<div class="m-hero"><div style="position:relative;z-index:1">
  <div class="flex between"><span class="small" style="opacity:.85">整改任务 · <span class="num">{RC['no']}</span></span>{countdown(20)}</div>
  <div class="flex gap12 mt12">{pf(a['platform'])}<div class="grow"><div class="fs16 bold">{a['name']}</div>
  <div class="small" style="opacity:.85">{a['platform']} · 第 2 轮整改 · 截止 {RC['deadline']}</div></div></div>
</div></div>
<div class="alert alert-info mt12">{icon('user')}<div class="grow">责任人：何雨桐（宣传部部长）。<b>我是该账号管理员</b>，可协助提交整改材料。</div></div>
{sec('整改内容')}
<div class="m-card">
  <div class="small muted">整改问题</div><div class="fs13 mt4">{s[0][3]}</div>
  <div class="divider" style="margin:12px 0"></div>
  <div class="small muted">整改要求</div><div class="fs13 mt4">{s[1][3]}</div>
  <div class="divider" style="margin:12px 0"></div>
  <div class="small muted">下发人</div><div class="fs13 mt4">周建华 · 计算机学院团委 · 2026-09-20</div>
  <div class="small muted mt12">附件</div><div class="upload-list">{file_btns(['整改通知书.pdf', '信息发布审查制度（模板）.docx'])}</div>
</div>
<div class="m-card">{m_card_title('整改记录', tag('第 1 轮：继续整改', 'danger'))}{history}</div>
{sec('其他整改任务')}
{group(cell('计院摄影协会 · 2025 年度', st('整改通过')), cell('中南计院团委 · 2024 年度', st('整改通过')))}"""
    page("rectify.html", "整改任务", content, back="todo.html",
         bottom=btn("联系学院", kind="default", ic="phone", toast="已复制学院团委电话 138 7310 2231") + btn("提交整改", "rectify-submit.html", ic="upload"),
         notes=["整改任务 " + RC["no"] + "：整改问题、整改要求、下发人、截止 " + RC["deadline"] + " 倒计时与附件",
                "责任人为何雨桐，李明作为账号管理员可协助提交（演示身份）",
                "整改记录显示第 1 轮被判定“继续整改”及学院意见",
                "底部“提交整改”进入第 2 轮材料提交"],
         flow=[("剧本六下一步：提交整改材料", "rectify-submit.html"), ("学院下发整改（上一步）", "../../pc/college/rectify-create.html")])


def rectify_submit():
    s = RC["steps"]
    content = f"""
{mini_acct(RE, tag('第 2 轮', 'warning'))}
<div class="alert alert-warning">{icon('alert')}<div class="grow"><b>上轮意见：</b>{s[3][3]}</div></div>
<div data-form class="mt12">
{sec('整改情况')}
{group(
        m_textarea('整改说明', '请逐条说明整改措施', '1. 已补充《信息发布三审制度》指导教师签字及学院盖章版；2. 补齐 7-9 月全部推文的三审记录台账，共 38 篇；3. 自 10 月起所有内容严格执行“先审后发”。', req=True, maxlen=500),
        m_radios('整改结果', 'rs', ['已完成整改', '部分完成'], '已完成整改'),
    )}
{sec('更新后信息')}
{group(
        yn('是否建立信息发布审查机制', 'u1', '是'),
        yn('是否执行“先审后发”', 'u2', '是'),
        m_input('审查责任人', '请输入姓名', '王晓琳（终审）'),
    )}
{sec('证明材料')}
<div class="m-group">{up_cell('上传材料', '支持 pdf / xlsx / jpg，单个不超过 10MB', ['《信息发布三审制度》签字盖章版.pdf', '7-9月审核台账.xlsx'], req=True)}</div>
</div>"""
    page("rectify-submit.html", "提交整改", content, back="rectify.html",
         bottom=back_btn("rectify.html", "取消") + submit_btn("提交整改", "rectify.html", ic="send", toast="已提交，等待学院审核"),
         notes=["顶部回显上轮“继续整改”意见，对照补充材料",
                "整改说明必填；整改结果、更新后信息（已建立信息发布审查机制）逐项确认",
                "证明材料已预置签字盖章版制度与 7-9 月审核台账",
                "提交后回到整改任务页，等待学院审核"],
         flow=[("剧本六下一步：PC 学院整改审核", "../../pc/college/rectify-detail.html"),
               ("APP 学院整改跟踪（第二次提交通过）", "../college/rectify.html"), ("返回整改任务", "rectify.html")])


# ---------------------------------------------------------------- 学生：僵尸号核实
def zombie_verify():
    a = PH
    opts = [
        ("normal", "仍在正常运营", "check-circle", "核实为正常，学院审核后解除预警", True),
        ("fix", "需要整改", "wrench", "由学院下发整改任务，限期恢复更新", False),
        ("cancel", "申请注销", "power", "转入注销流程，账号数据永久保留", False),
    ]
    choices = "".join(
        f'<button type="button" class="choice{" on" if on else ""}" data-choice=".zv-{k}"><span class="ck"></span>'
        f'<div class="grow" style="text-align:left"><div class="bold fs13">{t}</div><div class="small muted">{d}</div></div>{icon(ic, 18)}</button>'
        for k, t, ic, d, on in opts)
    content = f"""
<div class="hd-card" style="background:linear-gradient(180deg,#FFF3F3,#fff 70%)">
  <div class="flex gap12">{pf(a['platform'], 'lg')}<div class="grow"><div class="fs16 bold">{a['name']}</div>
  <div class="small muted">{a['platform']} · ID {a['pid']}</div><div class="acct-tags">{st('疑似僵尸号')}{st('不活跃')}</div></div></div>
  <div class="st4"><div><small>停更天数</small><b class="c-danger fs18 num">{a['idle_days']} 天</b></div><div><small>最近发布</small><b class="num">{a['last_post']}</b></div></div>
  <div class="small muted mt8">命中规则：停更 ≥ {T['idle_days']} 天 · 预警时间 2026-09-22 02:00</div>
</div>
<div data-form>
{sec('核实结论')}
<div class="choices" data-single=".zv-tip">{choices}</div>
<div class="zv-tip zv-normal alert alert-success mt8">{icon('check-circle')}<div class="grow">选择“正常运营”需上传近期发布截图并更新最近发布时间。</div></div>
<div class="zv-tip zv-fix alert alert-warning mt8 hidden">{icon('wrench')}<div class="grow">学院审核后将下发整改任务，整改期间账号状态为“整改中”。</div></div>
<div class="zv-tip zv-cancel alert alert-danger mt8 hidden">{icon('power')}<div class="grow">提交后将转为注销申请，由指导教师、学院、校团委逐级审核。</div></div>
{sec('核实说明')}
{group(
        m_textarea('情况说明', '请说明停更原因及后续运营计划', '寒假及毕业季暂停更新，已于 9 月恢复更新计划，9 月 27 日已发布迎新摄影作品集，后续保持每月 2 次以上更新。', req=True, maxlen=300),
        m_input('最近发布时间', '', '2026-09-27', req=True),
        up_cell('近期发布截图', '需包含发布日期', ['视频号主页截图_0927.jpg'], req=True),
    )}
</div>
<div class="m-card small sub">{flow_hint(['系统预警', '学生或教师核实', '学院审核', '正常 / 整改 / 注销'])}
<div class="mt8">系统只做预警，<b>不会直接注销</b>任何账号。</div></div>"""
    page("zombie-verify.html", "僵尸号核实", content, back="todo.html",
         bottom=back_btn("todo.html", "稍后处理") + submit_btn("提交核实", "todo.html", ic="send", toast="核实结果已提交，等待学院审核"),
         notes=["计院摄影协会（视频号）停更 212 天（最近发布 2026-03-02），被系统标记为疑似僵尸号",
                "核实结论三选一：仍在正常运营（默认）/ 需要整改 / 申请注销，切换时下方提示随之变化",
                "填写说明、更新最近发布时间并上传截图，提交后回到待办",
                "链路：系统预警 → 学生或教师核实 → 学院审核 → 正常 / 整改 / 注销，系统不会直接注销"],
         flow=[("提交后回到我的待办", "todo.html"), ("学院僵尸号核实（PC）", "../../pc/college/zombie.html"),
               ("教师核实（APP）", "../teacher/review-zombie.html")])


def build():
    login()
    identity_switch()
    home()
    todo()
    messages()
    mine()
    accounts()
    account_detail()
    account_history()
    apply()
    create_basic()
    create_platform()
    duplicate()
    create_staff()
    create_reviewer()
    apply_result()
    apply_change()
    change_confirm()
    apply_handover()
    apply_cancel()
    apply_claim()
    applications()
    application_detail()
    application_returned()
    application_edit()
    application_approved()
    application_rejected()
    annual()
    annual_fill()
    annual_result()
    rectify()
    rectify_submit()
    zombie_verify()
