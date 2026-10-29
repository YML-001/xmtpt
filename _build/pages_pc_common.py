"""PC 端 · 公共页面：登录、身份切换、账号档案、业务申请、审核弹窗与结果页。

默认演示视角为业务教师王晓琳；账号档案各页签分别呈现不同剧本账号，便于从剧本终点直接查看。
"""
import random

from base import *  # noqa: F401,F403
from data import (ACCOUNTS, PEOPLE, FLOWS, COLLEGES, CANCEL_REASONS, UPDATE_FREQ, PLATFORM_TYPES, ORG_TYPES,
                  RUN_STATUS, SCHOOL_STATS as S, MECHANISMS, LEVELS, LEVEL_TEXT, LEVEL_NOTE, ORG_HINT, ORG_PROMPTS,
                  PLATFORM_TYPE_HINT, ACCOUNT_NAME_HINT, FORMER_NAME_HINT, PID_HINT, FANS_HINT, INTRO_HINT, QR_HINT,
                  TEAM_LABEL, PUBLISH_TIME_LABEL, STUDENTS)

D = "pc/common/"
ACC_LIST = "../teacher/accounts.html"
REVIEW = "../teacher/review-create.html"

# ---------------------------------------------------------------- 本模块专用样式
CSS = """
/* 档案头部 */
.ah-card{overflow:hidden}
.ah{display:flex;gap:18px;align-items:flex-start;padding:20px 22px}
.ah .pf.lg{width:64px;height:64px;font-size:26px;border-radius:16px}
.ah-name{font-size:21px;font-weight:700;display:flex;align-items:center;gap:10px;flex-wrap:wrap;line-height:1.3}
.ah-meta{display:flex;flex-wrap:wrap;gap:6px 20px;font-size:13px;color:var(--c-text-2);margin-top:8px}
.ah-meta span{display:inline-flex;align-items:center;gap:5px}.ah-meta .i{width:14px;height:14px;color:var(--c-text-3)}
.ah-st{display:grid;grid-template-columns:repeat(4,minmax(0,140px));gap:10px;margin-top:14px}
.ah-st>div{background:var(--c-bg);border-radius:8px;padding:8px 12px}
.ah-st small{display:block;font-size:12px;color:var(--c-text-3);margin-bottom:4px}
.ah-ops{display:flex;flex-wrap:wrap;gap:8px;justify-content:flex-end;max-width:440px;margin-left:auto}
.ah-tabs{display:flex;align-items:center;gap:16px;padding:0 22px;border-top:1px solid var(--c-line)}
.ah-tabs .ptabs{margin:0;border-bottom:none;flex:1}
.ah-tabs .tip{font-size:12px;color:var(--c-text-3);white-space:nowrap}
/* 二维码 */
.qr{display:inline-block;padding:8px;background:#fff;border:1px solid var(--c-line);border-radius:8px}
.qr svg{display:block}
/* 四项机制 */
.mech-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.mech-box{border:1px solid var(--c-line);border-radius:8px;padding:12px 14px;background:#FBFCFD}
.mech-box .flex{justify-content:space-between}
.mech{display:grid;grid-template-columns:minmax(0,1fr) 160px;gap:18px;align-items:flex-start;padding:14px 0;border-bottom:1px dashed var(--c-line)}
.mech:last-child{border-bottom:none;padding-bottom:0}.mech:first-child{padding-top:0}
.mech-t{font-weight:600;font-size:14px;display:flex;align-items:flex-start;gap:8px;line-height:1.5}
.mech-t .no{width:20px;height:20px;border-radius:6px;background:var(--c-primary-light);color:var(--c-primary);display:grid;place-items:center;font-size:12px;flex:none;margin-top:1px}
.mech-h{font-size:12px;color:var(--c-text-2);margin-top:6px;line-height:1.75}
.picker{margin-top:12px;border:1px solid var(--c-line);border-radius:8px;padding:12px;background:#FBFCFD}
.pick-list{display:grid;gap:6px;max-height:240px;overflow:auto;margin-top:8px}
.pick-item{display:flex;align-items:center;justify-content:space-between;gap:8px;width:100%;padding:8px 10px;border:1px solid var(--c-line);border-radius:8px;background:#fff;text-align:left}
.pick-item:hover{border-color:var(--c-primary-border)}
/* 人员卡 */
.person{display:flex;gap:12px;align-items:center;padding:14px 16px;border:1px solid var(--c-line);border-radius:10px;background:#fff}
.person .nm{font-weight:600}.person .sub{font-size:12px;color:var(--c-text-3)}
.person.on{border-color:var(--c-primary);background:#F3F9FD}
.role-ic{width:40px;height:40px;border-radius:12px;display:grid;place-items:center;background:var(--c-primary-light);color:var(--c-primary);flex:none}
.role-ic.green{background:var(--c-success-bg);color:var(--c-success)}.role-ic.orange{background:var(--c-warning-bg);color:var(--c-warning)}
.role-ic.red{background:var(--c-danger-bg);color:var(--c-danger)}.role-ic.gray{background:var(--c-muted-bg);color:var(--c-muted)}
/* 列表行 */
.li{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--c-line)}
.li:last-child{border-bottom:none;padding-bottom:0}.li:first-child{padding-top:0}
a.li:hover .li-t{color:var(--c-primary)}
.li-t{font-weight:600;font-size:14px}.li-m{font-size:12px;color:var(--c-text-3)}
.mini-stat{background:var(--c-bg);border-radius:10px;padding:12px 16px}
.mini-stat b{display:block;font-size:22px;line-height:1.3;font-variant-numeric:tabular-nums}
.mini-stat span{font-size:12px;color:var(--c-text-3)}
.txt{font-size:14px;line-height:1.9;color:var(--c-text)}
.check-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.ck-item{display:flex;align-items:center;gap:8px;padding:10px 12px;border:1px solid var(--c-line);border-radius:8px;cursor:pointer;font-size:14px;background:#fff}
.ck-item:hover{border-color:var(--c-primary-border)}
.ck-item input{accent-color:var(--c-primary);width:15px;height:15px}
.ck-item:has(input:checked){border-color:var(--c-primary);background:#F3F9FD;color:var(--c-primary);font-weight:500}
.cg-row{display:grid;grid-template-columns:130px minmax(0,1fr) 28px minmax(0,1fr);gap:12px;align-items:center;padding:12px 0;border-bottom:1px dashed var(--c-line)}
.cg-row:last-child{border-bottom:none}
.cg-row .lb{font-weight:600;font-size:14px}
.cg-row .ar{color:var(--c-text-3);display:grid;place-items:center}
.cg-hd{display:grid;grid-template-columns:130px minmax(0,1fr) 28px minmax(0,1fr);gap:12px;font-size:12px;color:var(--c-text-3);padding-bottom:8px;border-bottom:1px solid var(--c-line)}
.wiz-hd{padding:18px 24px}
.side-steps .li-t{font-size:13px}
.hl-box{border-radius:12px;padding:18px 20px;background:linear-gradient(135deg,#F3F9FD,#FFFFFF);border:1px solid var(--c-primary-border)}
.id-cmp{display:grid;grid-template-columns:1fr 56px 1fr;align-items:center;gap:12px}
.id-cmp .box{border:1px solid var(--c-line);border-radius:10px;padding:14px 16px;background:#fff}
.id-cmp .box b{font-size:20px;font-variant-numeric:tabular-nums;letter-spacing:.5px}
.id-cmp .mid{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;background:var(--c-warning-bg);color:var(--c-warning);margin:0 auto}
.task{border:1px solid var(--c-line);border-radius:12px;padding:18px 20px;background:#fff;display:flex;flex-direction:column;gap:12px}
.task-no{width:30px;height:30px;border-radius:9px;display:grid;place-items:center;font-weight:700;color:#fff;background:var(--c-primary);flex:none}
.task-no.red{background:var(--c-danger)}
.task ul{list-style:none;display:grid;gap:6px;font-size:13px;color:var(--c-text-2)}
.task li{display:flex;gap:8px}.task li .i{color:var(--c-success);margin-top:3px}
.sim{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr) 110px;gap:16px;align-items:center;padding:14px 0;border-bottom:1px solid var(--c-line)}
.sim:last-child{border-bottom:none}
.ho{display:grid;grid-template-columns:1fr 64px 1fr;gap:12px;align-items:stretch}
.ho .side-box{border:1px solid var(--c-line);border-radius:12px;padding:16px 18px}
.ho .side-box.new{border-color:var(--c-primary-border);background:#F7FBFE}
.ho .mid{display:grid;place-items:center;color:var(--c-primary)}
.ho .mid span{width:44px;height:44px;border-radius:50%;background:var(--c-primary-light);display:grid;place-items:center}
.flow-h{display:flex;align-items:center;gap:10px}
.flow-h .nd{flex:1;border:1px solid var(--c-line);border-radius:10px;padding:10px 12px;background:#fff;min-width:0}
.flow-h .nd.on{border-color:var(--c-primary);background:#F3F9FD}
.flow-h .nd b{display:block;font-size:13px}.flow-h .nd span{font-size:12px;color:var(--c-text-3)}
.flow-h>.i{color:var(--c-border);flex:none}
.sub-item{display:grid;grid-template-columns:44px minmax(0,1fr) auto;gap:14px;align-items:center;padding:16px 18px;border:1px solid var(--c-line);border-radius:12px;background:#fff;text-align:left}
.sub-item+.sub-item{margin-top:10px}
.no-code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-weight:600;color:var(--c-primary);letter-spacing:.3px}
.round{border:1px solid var(--c-line);border-radius:12px;padding:16px 18px;background:#fff}
.round.back{border-color:var(--c-warning-bd);background:#FFFBF3}
.round.ok{border-color:var(--c-success-bd);background:#F6FEFA}
.role-card{display:flex;flex-direction:column;gap:14px;padding:22px}
.role-card .top{display:flex;gap:14px;align-items:center}
.role-card ul{list-style:none;display:grid;gap:8px;font-size:13px;color:var(--c-text-2)}
.role-card li{display:flex;gap:8px;align-items:flex-start}.role-card li .i{color:var(--c-primary);margin-top:3px}
.role-card.cur{border-color:var(--c-primary);box-shadow:0 0 0 1px var(--c-primary),var(--shadow-lg)}
.scope{display:flex;gap:6px;flex-wrap:wrap}
.diff-side .table{table-layout:fixed}.diff-side td{word-break:break-all;font-size:12px}.diff-side td:first-child{font-size:13px}
.dim{display:flex;gap:12px;align-items:flex-start;padding:14px 16px;border-radius:10px;background:var(--c-bg)}
/* 新建备案弹窗叠在账号列表上时，补齐列表里用到的图标块，并让表单贴合大弹窗 */
.tic{width:36px;height:36px;border-radius:10px;display:grid;place-items:center;background:var(--c-primary-light);color:var(--c-primary);flex:none}
.zx-main:has(.content>.backdrop>.page-hd:first-child) .zx-tabs{border-radius:8px 8px 0 0;margin-bottom:0;border-bottom:1px solid var(--c-bg)}
.content>.backdrop>.page-hd:first-child{border-radius:0 0 8px 8px}
.wf-dialog .page-hd{padding:0 0 12px;margin-bottom:14px;background:transparent;border-radius:0;border-bottom:1px dashed #E4E7ED}
.wf-dialog .page-hd h1{font-size:16px}
.wf-dialog .wiz-hd{padding:14px 18px}
.wf-dialog>.actbar{margin:0;border-radius:0;box-shadow:0 -4px 16px rgba(42,141,199,.12)}
.wf-dialog .split{grid-template-columns:minmax(0,1fr) 320px}
"""

LOGIN_CSS = """
/* 统一身份认证（对齐正式系统 CAS 登录页） */
.cas{position:relative;min-height:calc(100vh / var(--z,1));background:#fff url(../../assets/login-top.webp) top center/100% auto no-repeat;overflow:hidden;display:flex;flex-direction:column;align-items:center}
.cas::after{content:"";position:absolute;left:0;right:0;bottom:0;height:525px;background:url(../../assets/login-campus.webp) center bottom/100% auto no-repeat;z-index:0;pointer-events:none}
.cas-logo{position:relative;z-index:1;margin-top:28px;width:540px;height:140px;background:url(../../assets/pc-logo-title.webp) 0 0/540px 140px no-repeat;border-radius:12px;box-shadow:0 8px 24px rgba(42,141,199,.18)}
.cas-box{position:relative;z-index:1;width:440px;margin-top:40px;background:rgba(255,255,255,.9);border-radius:12px;padding:26px 30px 22px;box-shadow:0 10px 30px rgba(76,94,114,.10)}
.cas-hd{display:flex;align-items:center;justify-content:space-between}
.cas-hd h2{font-size:26px;font-weight:700;color:#4C5E72;letter-spacing:1px}
.cas-lang{display:flex;border-radius:4px;overflow:hidden;font-size:12px}
.cas-lang button{padding:3px 9px;background:#F2F3F5;color:#A8ABB2}.cas-lang button.on{background:#0F4C99;color:#fff}
.seg.cas-tabs{display:flex;gap:32px;background:none;border-radius:0;padding:0;margin-top:16px;border-bottom:1px solid #E4E7ED}
.seg.cas-tabs button{padding:8px 0;border-radius:0;color:#333;font-size:15px;font-weight:600;position:relative}
.seg.cas-tabs button:hover{background:none;color:var(--c-primary)}
.seg.cas-tabs button.on{background:none;color:var(--c-primary)}
.seg.cas-tabs button.on::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:var(--c-primary)}
.cas-in{display:flex;flex-direction:row;align-items:center;gap:12px;height:46px;background:#F9F9F9;border-radius:10px;padding:0 14px;margin-top:16px}
.cas-in .i{width:20px;height:20px;color:#333;flex:none}
.cas-in input{flex:1;min-width:0;border:none;outline:none;background:none;font-size:15px}
.cas-in input::placeholder{color:#A8ABB2}
.cas-in.invalid{background:#FEF0F0;box-shadow:0 0 0 1px var(--c-danger) inset}
.cas-in .sms{color:var(--c-primary);font-size:14px;white-space:nowrap}
.cas-row{display:flex;align-items:center;justify-content:space-between;margin-top:14px;font-size:14px;color:#333}
.cas-row .links{display:flex;gap:10px;align-items:center}.cas-row .links i{width:1px;height:12px;background:#DCDFE6}
.cas-row .link{font-weight:600}
.cas-btn{width:100%;height:46px;border-radius:12px;font-size:16px;margin-top:18px}
.cas-qr{text-align:center;padding:18px 0 6px}
.cas-note{display:flex;gap:8px;align-items:flex-start;font-size:12px;color:#909399;margin-top:14px;line-height:1.7}
.cas-note .i{width:14px;height:14px;margin-top:3px;color:var(--c-primary)}
.cas-foot{position:relative;z-index:1;margin-top:18px;text-align:center;font-size:12px;color:#606266;line-height:1.8}
.cas-proto{position:relative;z-index:1;display:flex;gap:12px;margin-top:10px}
.cas-proto a{height:30px;padding:0 14px;border-radius:15px;background:rgba(255,255,255,.85);border:1px solid #BFDDEE;color:var(--c-primary);font-size:13px;display:flex;align-items:center;gap:6px}
"""

# 建议填入：点击提示词写入对应输入框
FILL_JS = """
document.addEventListener('click',function(e){var b=e.target.closest('[data-fill]');if(!b)return;
var el=document.querySelector(b.dataset.fillTarget);if(el){el.value=b.dataset.fill;el.dispatchEvent(new Event('input',{bubbles:true}));}});
"""

# 承诺勾选校验：未勾选时拦截提交
PROMISE_JS = """
document.addEventListener('click',function(e){var b=e.target.closest('[data-submit]');var c=document.getElementById('promise');
if(b&&c&&!c.checked){e.preventDefault();e.stopImmediatePropagation();c.closest('.promise').classList.add('invalid');toast('请先阅读并勾选信息真实性承诺');}},true);
document.addEventListener('change',function(e){if(e.target.id==='promise'&&e.target.checked){e.target.closest('.promise').classList.remove('invalid');}});
"""

# 变更申请：勾选字段显示对应行，输入新值实时刷新对比表
DIFF_JS = """
document.addEventListener('change',function(e){var el=e.target;if(!el.dataset.field)return;
['fr-','dr-'].forEach(function(p){var x=document.getElementById(p+el.dataset.field);if(x)x.classList.toggle('hidden',!el.checked);});
var n=document.querySelectorAll('[data-field]:checked').length;var c=document.getElementById('field-count');if(c)c.textContent=n;});
document.addEventListener('input',function(e){var el=e.target;if(!el.dataset.diff)return;var row=document.getElementById('dr-'+el.dataset.diff);if(!row)return;
var oldTd=row.querySelector('.dv-old'),newTd=row.querySelector('.dv-new'),mk=row.querySelector('.dv-mk');var v=el.value.trim();var ch=v&&v!==oldTd.textContent.trim();
newTd.textContent=v||'—';row.classList.toggle('changed',!!ch);oldTd.classList.toggle('old',!!ch);newTd.classList.toggle('new',!!ch);
mk.innerHTML=ch?'<span class="tag tag-warning">已变更</span>':'<span class="muted small">未变更</span>';});
"""


# ---------------------------------------------------------------- 通用小部件
def qr(size=112, seed=7):
    """生成确定性的示意二维码（SVG）。"""
    n = 25
    r = random.Random(seed)
    cells = []
    for y in range(n):
        for x in range(n):
            fx = x if x < 8 else x - (n - 8)
            fy = y if y < 8 else y - (n - 8)
            in_zone = (x < 8 or x >= n - 8) and (y < 8 or y >= n - 8) and not (x >= n - 8 and y >= n - 8)
            if in_zone:
                if fx > 6 or fy > 6 or fx < 0 or fy < 0:
                    on = False
                else:
                    on = fx in (0, 6) or fy in (0, 6) or (2 <= fx <= 4 and 2 <= fy <= 4)
            else:
                on = r.random() < 0.48
            if on:
                cells.append(f"M{x} {y}h1v1h-1z")
    return (f'<span class="qr"><svg width="{size}" height="{size}" viewBox="0 0 {n} {n}" shape-rendering="crispEdges">'
            f'<path fill="#1F2A37" d="{"".join(cells)}"/></svg></span>')


def copy_btn(val):
    return f'<button class="btn btn-text btn-sm" type="button" data-copy="{esc(val)}">{icon("copy", 14)}复制</button>'


def flow_items(key, upto=None):
    items = []
    for t, who, title, cm in FLOWS[key]["steps"][:upto]:
        state = "back" if ("退回" in title or "继续整改" in title) else "done"
        items.append((state, title, f"{who} · {t}", cm))
    return items


def mini(label, value, color=""):
    c = f' class="c-{color}"' if color else ""
    return f'<div class="mini-stat"><b{c}>{value}</b><span>{label}</span></div>'


def ini(name, cls="sm"):
    """无照片人员使用姓氏头像。"""
    return (f'<span class="avatar {cls}" style="display:grid;place-items:center;font-size:11px;font-weight:600;'
            f'color:var(--c-primary);background:var(--c-primary-light)">{name[0]}</span>')


def person(name, sub, right="", on=False):
    return (f'<div class="person{" on" if on else ""}">{avatar(name)}<div class="grow"><div class="nm">{name}</div>'
            f'<div class="sub">{sub}</div></div>{right}</div>')


def li(title, meta, left="", right="", href=None):
    inner = f'{left}<div class="grow"><div class="li-t">{title}</div><div class="li-m">{meta}</div></div>{right}'
    if href:
        return f'<a class="li" href="{href}">{inner}</a>'
    return f'<div class="li">{inner}</div>'


def role_ic(name, color=""):
    return f'<span class="role-ic {color}">{icon(name, 20)}</span>'


def check_item(text, checked=False, attrs=""):
    c = " checked" if checked else ""
    return f'<label class="ck-item"><input type="checkbox"{c} {attrs}>{text}</label>'


def actbar(left, right):
    return f'<div class="actbar"><div class="grow">{left}</div>{right}</div>'


# ---------------------------------------------------------------- 账号档案
ARCH_TABS = [("基本信息", "archive-basic.html"), ("责任人员", "archive-staff.html"), ("年审记录", "archive-audit.html"),
             ("变更记录", "archive-changes.html"), ("整改记录", "archive-rectify.html"), ("注销信息", "archive-cancel.html"),
             ("操作日志", "archive-logs.html")]


def arch_header(a, name, statuses, tab, dossier, cancelled=False):
    run, filing, annual, change = statuses
    st_html = "".join(f'<div><small>{k}</small>{st(v)}</div>'
                      for k, v in [("运行状态", run), ("备案状态", filing), ("年审状态", annual), ("年度异动", change)])
    meta = "".join(f'<span>{icon(ic)}{v}</span>' for ic, v in [
        ("tag", f'平台ID：{a["pid"]}'), ("building", f'{a["org"]}'), ("user", f'管理教师：{a["teacher"]}'),
        ("calendar", f'开通时间：{a["opened"]}'), ("archive", f'档案编号：{dossier}')])
    if cancelled:
        ops_html = (btn("发起变更", None, "default", "file-edit", "sm", toast="账号已注销，不可发起变更")
                    + btn("负责人交接", None, "default", "user-switch", "sm", toast="账号已注销，不可办理交接")
                    + btn("导出备案表", "../school/filing-form.html", "ghost", "download", "sm"))
    else:
        ops_html = (btn("发起变更", "apply-change.html", "primary", "file-edit", "sm")
                    + btn("负责人交接", "apply-handover.html", "default", "user-switch", "sm")
                    + btn("注销", "apply-cancel.html", "danger", "power", "sm")
                    + btn("导出备案表", "../school/filing-form.html", "ghost", "download", "sm"))
    return f"""<div class="card ah-card">
  <div class="ah">{pf(a['platform'], 'lg')}
    <div class="grow">
      <div class="ah-name">{name}{tag(a['platform'], 'muted')}{tag(a['level'], 'primary')}{tag(a['org_type'], 'muted')}</div>
      <div class="ah-meta">{meta}</div>
      <div class="ah-st">{st_html}</div>
    </div>
    <div class="ah-ops">{ops_html}</div>
  </div>
  <div class="ah-tabs">{ptabs(ARCH_TABS, tab)}<span class="tip">各页签分别展示对应剧本账号的档案</span></div>
</div>"""


def arch_page(file, tab, name, header, body):
    content = header + f'<div class="mt16">{body}</div>'
    pc_common_page(D + file, f"账号档案 · {tab}", [("我负责的账号", ACC_LIST), ("账号档案", None), (f"{name} · {tab}", None)],
                   content, css=CSS, back=ACC_LIST)


def archive_basic():
    a = ACCOUNTS["new"]
    t = PEOPLE["王晓琳"]
    home_url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=csu_cs_youth"
    intro = ("“中南计算机青年”是计算机学院团委新媒体中心主办的官方微信公众号，面向学院 4600 余名本科生和研究生，"
             "围绕“思想引领、学业发展、科创实践、青春风采”四条主线开展内容建设。平台设置“计院青年说”“竞赛直通车”"
             "“实验室开放日”“学长学姐来了”“团学快讯”五个固定栏目，及时发布学院团学活动、主题团日、学科竞赛与"
             "科创成果、志愿服务及就业实习信息。平台严格执行“先审后发”三审制度，所有推文经学生编辑初审、新媒体中心"
             "主任复审、指导教师终审后发布，坚持正确政治方向和舆论导向，讲好计院青年成长故事。")
    mech = mechanism_blocks()
    belong = kv([("所属学院", "计算机学院"), ("所属团学组织", a["org"]), ("组织类别", a["org_type"]),
                 ("平台管理层级", f'{a["level"]} <span class="small muted">（二级团组织直属学生组织开设）</span>')], 4)
    platform = kv([
        ("平台类型", f'<span class="flex gap6">{pf(a["platform"], "sm")}{a["platform"]}</span>'),
        ("账号名称", f'<b>{a["name"]}</b>'), ("曾用名", '<span class="muted">无</span>'),
        ("平台ID", f'<span class="flex gap4"><span class="num">{a["pid"]}</span>{copy_btn(a["pid"])}</span>'),
        ("平台头像", f'<span class="flex gap8">{pf(a["platform"])}<span class="small muted">已上传 · 2026-09-24</span></span>'),
        ("是否认证", f'{tag("是", "success")} <span class="small muted">微信认证 · 2026-09-22</span>'),
        ("粉丝数", '<span class="num">218</span> <span class="small muted">（2026-09-30 统计）</span>'),
        (TEAM_LABEL, "12"), ("开通时间", a["opened"]),
        ("主页链接", f'<span class="flex gap4"><a class="link ellipsis" style="max-width:420px" href="https://mp.weixin.qq.com/">{home_url}</a>{copy_btn(home_url)}</span>', True),
    ], 3)
    run = kv([
        (PUBLISH_TIME_LABEL, "2026-09-29 20:30 <span class='small muted'>《计院新生入学教育周圆满收官》</span>"),
        ("更新频率", UPDATE_FREQ[0]), ("运行状态", st("正常运行")), ("异常情况", "无"),
        ("管理教师", f'王晓琳 <span class="small muted">{t["no"]} · 宣传工作辅导员 · 专职 · {t["phone"]}</span>'),
        ("学生具体负责人", f'李明 <span class="small muted">{PEOPLE["李明"]["no"]} · {PEOPLE["李明"]["phone"]}</span>'),
        ("管理员", '陈思远、周可欣 <span class="small muted">共 2 人</span>'),
    ], 3)
    left = (card("归属信息", belong)
            + card("平台信息", platform + '<div class="divider"></div><div class="field-label mb8">平台信息确认</div>'
                   + mech + '<div class="divider"></div>'
                   + kv([("平台介绍", f'<div class="txt">{intro}</div>', True),
                         ("信息发布范围", "学院团学活动与主题团日、青年思想引领、学科竞赛与科创成果、志愿服务、学院通知公告及就业实习信息", True),
                         ("备注", "由学生李明于 2026-09-24 发起新建备案，经指导教师、学院团委、校团委三级审核通过。", True)], 3),
                   cls="mt16")
            + card("运行信息", run, cls="mt16"))
    filing = kv([("备案申请编号", f'<span class="no-code">{FLOWS["new"]["no"]}</span>'), ("备案时间", "2026-09-30 10:05"),
                 ("终审人", "陈静 · 校团委宣传部"), ("备案表", '<a class="link" href="../school/filing-form.html">《新媒体公众平台备案表》</a>')], 2)
    right = (card("备案信息", alert("账号档案已于 2026-09-30 建立，纳入全校统一账号主库。", "success") + '<div class="mt12"></div>' + filing)
             + card("平台二维码", f'<div class="flex gap16">{qr(104, 11)}<div class="small muted">扫码关注<br><b class="fs13" style="color:var(--c-text)">{a["name"]}</b><br>上传于 2026-09-24<div class="mt8">{btn("下载二维码", None, "default", "download", "sm", toast="已下载二维码图片")}</div></div></div>', cls="mt16")
             + card("备案审核记录", timeline(flow_items("new")), cls="mt16"))
    body = f'<div class="split" style="grid-template-columns:minmax(0,1fr) 380px"><div>{left}</div><div>{right}</div></div>'
    hd = arch_header(a, a["name"], ("正常运行", "已备案", "未开始", "新建"), "基本信息", "DA-CS-2026-0158")
    arch_page("archive-basic.html", "基本信息", a["name"], hd, body)


def archive_staff():
    a = ACCOUNTS["handover"]
    zw, zj, wx, l4, lm = PEOPLE["张卫东"], PEOPLE["周建华"], PEOPLE["王晓琳"], PEOPLE["李四"], PEOPLE["李明"]
    sys_resp = (person("张卫东", f'第一责任人 · 计算机学院党委 · {zw["job"]}', f'<div class="small muted" style="text-align:right">{zw["phone"]}<br>2022-07-01 起</div>')
                + '<div class="mt12"></div>'
                + person("周建华", f'直接责任人 · 计算机学院团委 · {zj["job"]}', f'<div class="small muted" style="text-align:right">{zj["phone"]}<br>2021-09-01 起</div>'))
    teachers = table(["姓名", "工号", "类型", "是否专职", "联系方式", "任职时间", "状态"], [
        [f'<span class="flex gap8">{avatar("王晓琳", "sm")}<b>王晓琳</b></span>', wx["no"], "社团指导教师", "是", wx["phone"], "2023-09-01 至今", st("启用")],
        [f'<span class="flex gap8">{avatar("刘洋", "sm")}刘洋</span>', PEOPLE["刘洋"]["no"], "社团指导教师", "是", PEOPLE["刘洋"]["phone"], "2020-09-01 ~ 2023-08-31", tag("已卸任", "muted")],
        [f'<span class="flex gap8">{ini("邓志强")}邓志强</span>', "T20120906", "社团指导教师", "否（兼职）", "136 0731 5528", "2019-10-08 ~ 2020-08-31", tag("已卸任", "muted")],
    ])
    history = [
        ("李四", l4["no"], l4["grade"], "宣传部部长", l4["phone"], "2026-10-01", "至今", "JJ20260927002", True),
        ("李明", lm["no"], lm["grade"], "宣传部部长", lm["phone"], "2024-09-10", "2026-09-30", "JJ20240908011", False),
        ("陈雨萱", "8209210633", "2021级网络工程2班", "宣传部部长", "—", "2022-09-05", "2024-09-09", "历史补录", False),
        ("黄子轩", "8209200217", "2020级计算机科学3班", "社长兼宣传负责人", "—", "2020-09-12", "2022-09-04", "历史补录", False),
        ("刘梦琪", "8209190105", "2019级软件工程1班", "创始社长", "—", "2019-10-08", "2020-09-11", "历史补录", False),
    ]
    h_rows = []
    for nm, no, grade, job, ph, s, e, src, cur in history:
        status = tag("2026-10-01 生效", "primary") if cur else tag("已卸任", "muted")
        if nm in ("李四", "李明"):
            name_html = f'<span class="flex gap8 nowrap">{avatar(nm, "sm")}<b>{nm}</b></span>'
        else:
            name_html = f'<span class="flex gap8 nowrap">{ini(nm)}{nm}</span>'
        src_html = f'<span class="no-code">{src}</span>' if src.startswith("JJ") else f'<span class="muted">{src}</span>'
        h_rows.append([name_html, no, grade, job, f'<span class="nowrap">{ph}</span>',
                       f'<span class="num nowrap">{s} ~ {e}</span>', src_html, status])
    h_tbl = table(["姓名", "学号", "年级班级", "学生职务", "联系方式", "任期起止", "来源 / 交接单号", "状态"], h_rows)
    admins = table(["管理员", "学号", "负责内容", "授权时间"], [
        ["<b>吴嘉怡</b>", "8209240417", "短视频剪辑与发布", "2025-09-20"],
        ["<b>张博文</b>", "8209250126", "评论区管理与数据统计", "2026-09-15"],
    ])
    cur = (f'<div class="ho"><div class="side-box"><div class="small muted mb8">原负责人（已卸任）</div>'
           + person("李明", f'{lm["no"]} · {lm["grade"]}')
           + '<div class="small muted mt8">任期 2024-09-10 ~ 2026-09-30，任职记录永久保留</div></div>'
           + f'<div class="mid"><span>{icon("arrow-right", 20)}</span></div>'
           + '<div class="side-box new"><div class="small muted mb8">现任负责人</div>'
           + person("李四", f'{l4["no"]} · {l4["grade"]}', tag("现任", "success"))
           + f'<div class="small muted mt8">{l4["job"]} · {l4["phone"]} · 2026-10-01 起</div></div></div>')
    left = (card("学生运营负责人 · 本次交接", cur + '<div class="mt16">' + alert("人员换届不覆盖原负责人：新负责人生效后，原负责人记录转入历任名单，任职起止时间保留可追溯。", "info") + "</div>",
                 btn("查看交接申请", "apply-handover.html", "text", size="sm"))
            + card("交接审核记录", f'<div class="small muted mb12">交接单号 <span class="no-code">{FLOWS["handover"]["no"]}</span></div>' + timeline(flow_items("handover")), cls="mt16"))
    right = (card("制度责任人", sys_resp)
             + card("账号管理员", admins, cls="mt16"))
    body = (f'<div class="split" style="grid-template-columns:minmax(0,1fr) 440px"><div>{left}</div><div>{right}</div></div>'
            + card("历任学生负责人", h_tbl, f'<span class="small muted">共 {len(history)} 任 · 历史记录不可覆盖</span>', cls="mt16")
            + card("具体管理教师", teachers, cls="mt16"))
    hd = arch_header(a, a["name"], ("正常运行", "已备案", "待填报", "变更"), "责任人员", "DA-CS-2019-0042")
    arch_page("archive-staff.html", "责任人员", a["name"], hd, body)


def archive_audit():
    a = ACCOUNTS["annual"]
    stats = "".join([mini("累计年审", "6 次"), mini("年审通过", "6 次", "success"), mini("涉及整改", "1 次", "warning"), mini("最近通过", "2026-09-30", "primary")])
    rows = [
        ("2026", FLOWS["annual"]["no"], st("无异动"), "2026-09-18", "2026-09-20", "2026-09-29", "2026-09-30", tag("批量通过", "primary"), st("年审通过")),
        ("2025", "NS2025-CS-0011", st("变更"), "2025-10-09", "2025-10-15", "2025-10-28", "2025-11-18", tag("线下年审 · 初始化导入", "muted"), st("年审通过")),
        ("2024", "NS2024-CS-0010", st("无异动"), "2024-10-12", "2024-10-16", "2024-10-30", "2024-11-21", tag("历史补录", "muted"), st("年审通过")),
        ("2023", "NS2023-CS-0013", st("变更"), "2023-10-08", "2023-10-19", "2023-11-06", "2023-12-01", tag("历史补录 · 整改后通过", "warning"), st("年审通过")),
        ("2022", "NS2022-CS-0009", st("无异动"), "2022-10-15", "2022-10-20", "2022-11-02", "2022-11-25", tag("历史补录", "muted"), st("年审通过")),
        ("2021", "NS2021-CS-0012", st("无异动"), "2021-10-11", "2021-10-18", "2021-11-01", "2021-11-19", tag("历史补录", "muted"), st("年审通过")),
    ]
    tbl = table(["年度", "年审编号", "年度异动", "学生填报", "教师审核", "学院审核", "学校审核", "审核方式", "年审结果"],
                [[f"<b>{r[0]}</b>"] + [f'<span class="no-code">{r[1]}</span>'] + list(r[2:]) for r in rows])
    snap = kv([("年审填报人", "李明 · 新媒体中心主任"), ("年度异动", st("无异动")), ("粉丝数", '<span class="num">36,512</span> <span class="small up">较上年 +4,218</span>'),
               ("最近发布", "2026-09-17"), ("年度发布量", "186 篇"), ("更新频率", UPDATE_FREQ[0]),
               ("四项机制", "均已建立"), ("负责人 / 教师", "李明 / 王晓琳"), ("风险标记", '<span class="c-success">无风险</span>')], 3)
    opinions = "".join(li(title, f"{who} · {t}", role_ic("check-circle", "green"), f'<span class="small sub" style="max-width:260px">{cm}</span>')
                       for t, who, title, cm in FLOWS["annual"]["steps"][1:])
    body = (f'<div class="grid g4">{stats}</div>'
            + f'<div class="split mt16" style="grid-template-columns:minmax(0,1fr) 400px"><div>'
            + card("2026 年度年审 · 已通过", alert("2026-09-30 14:20 校团委宣传部陈静在“年审校级审核”中对无异动无风险账号批量通过，本账号在批次内。", "success")
                   + '<div class="mt16"></div>' + snap, tag("批次：计算机学院无异动 18 个账号", "primary"))
            + card("历年年审记录", tbl, btn("导出年审台账", None, "default", "download", "sm", toast="已导出《中南计院团委历年年审记录》"), cls="mt16")
            + '</div><div>'
            + card("本年度审核流转", timeline(flow_items("annual")))
            + card("各级审核意见", opinions, cls="mt16")
            + "</div></div>")
    hd = arch_header(a, a["name"], ("正常运行", "已备案", "年审通过", "无异动"), "年审记录", "DA-CS-2014-0001")
    arch_page("archive-audit.html", "年审记录", a["name"], hd, body)


def archive_changes():
    a = ACCOUNTS["rename"]
    names = (li("中南计院学生会", "2026-09-30 起使用 · 当前名称", role_ic("check-circle", "green"), tag("当前", "success"))
             + li("计算机学院学生会", "2019-07-01 ~ 2026-09-30 · 学院成立后统一更名", role_ic("history", "gray"), tag("曾用名", "muted"))
             + li("中南信息学院学生会", "2016-03-12 ~ 2019-06-30 · 原信息科学与工程学院时期", role_ic("history", "gray"), tag("曾用名", "muted")))
    diff = diff_table([("账号名称", "计算机学院学生会", "中南计院学生会"), ("曾用名", "中南信息学院学生会", "中南信息学院学生会；计算机学院学生会"),
                       ("平台类型", "微博", "微博"), ("平台ID", a["pid"], a["pid"]), ("所属组织", a["org"], a["org"]), ("负责人", "李明", "李明")])
    rows = [
        ("2026-09-30", "账号名称", "计算机学院学生会", "中南计院学生会", "BG20260926003", tag("重要变更", "warning"), "陈静（校团委）", "name"),
        ("2025-09-20", "学生负责人", "张涵", "李明", "JJ20250918004", tag("交接", "primary"), "王晓琳", "staff"),
        ("2024-09-12", "学生负责人", "罗一鸣", "张涵", "历史补录", tag("交接", "primary"), "刘洋", "staff"),
        ("2024-03-05", "指导教师", "刘洋", "王晓琳", "历史补录", tag("日常维护", "muted"), "周建华（学院）", "teacher"),
        ("2023-06-18", "主页链接", "weibo.com/csuxxxy", "weibo.com/u/7722108845", "历史补录", tag("日常维护", "muted"), "周建华（学院）", "other"),
        ("2022-11-02", "二维码", "旧版二维码", "新版二维码", "历史补录", tag("日常维护", "muted"), "周建华（学院）", "other"),
        ("2019-07-01", "账号名称", "中南信息学院学生会", "计算机学院学生会", "历史补录", tag("重要变更", "warning"), "校团委", "name"),
        ("2019-07-01", "所属组织", "信息科学与工程学院学生会", "计算机学院学生会", "历史补录", tag("重要变更", "warning"), "校团委", "org"),
    ]
    tbl = table(["生效日期", "变更字段", "变更前", "变更后", "申请编号", "变更类型", "终审人"],
                [dict(cells=[f'<span class="num nowrap">{r[0]}</span>', f'<b class="nowrap">{r[1]}</b>', f'<span class="muted">{r[2]}</span>', f'<span class="c-success">{r[3]}</span>',
                             f'<span class="no-code">{r[4]}</span>' if r[4].startswith(("BG", "JJ")) else f'<span class="muted">{r[4]}</span>', r[5],
                             f'<span class="nowrap">{r[6]}</span>'], cat=r[7]) for r in rows], id_="chg-tbl")
    filt = chips([("全部", "all"), ("账号名称", "name"), ("负责人", "staff"), ("指导教师", "teacher"), ("组织归属", "org"), ("其他", "other")], target="#chg-tbl")
    body = (f'<div class="split" style="grid-template-columns:minmax(0,1fr) 380px"><div>'
            + card("最近一次变更 · 账号名称", f'<div class="flex gap12 mb12"><span class="no-code">{FLOWS["rename"]["no"]}</span>{tag("重要变更 · 报校团委", "warning")}<span class="small muted">2026-09-30 11:00 生效</span></div>' + diff,
                   btn("查看校级审核", "../school/approval-change.html", "text", size="sm"))
            + card("本次变更审核流转", timeline(flow_items("rename")), cls="mt16")
            + '</div><div>'
            + card("曾用名", names + '<div class="mt12">' + alert("名称变更生效后，原名称自动记入曾用名，可在全校账号库中按曾用名检索。", "info") + "</div>")
            + "</div></div>"
            + card("全部变更记录", f'<div class="mb12">{filt}</div>' + tbl, f'<span class="small muted">共 {len(rows)} 条</span>', cls="mt16"))
    hd = arch_header(a, a["new_name"], ("正常运行", "已备案", a["annual"], "变更"), "变更记录", "DA-CS-2016-0007")
    arch_page("archive-changes.html", "变更记录", a["new_name"], hd, body)


def archive_rectify():
    a = ACCOUNTS["rectify"]
    f = FLOWS["rectify"]
    s = f["steps"]
    task = kv([("整改编号", f'<span class="no-code">{f["no"]}</span>'), ("整改来源", "2026 年度年审 · 指导教师要求整改"),
               ("下发人", "周建华 · 学院团委"), ("整改责任人", f'何雨桐 · {PEOPLE["何雨桐"]["phone"]}'),
               ("下发时间", "2026-09-20"), ("截止时间", f'<span class="c-warning bold">{f["deadline"]}</span>'),
               ("整改问题", s[0][3], True), ("整改要求", s[1][3], True)], 2)
    r1 = (f'<div class="round back"><div class="flex between"><div class="bold">第一次提交</div>{st("继续整改")}</div>'
          f'<div class="small muted mt4">何雨桐 · {s[2][0]}</div><div class="txt mt8">{s[2][3]}</div>'
          f'<div class="upload-list"><span class="file-chip">{icon("file")}信息发布三审制度.pdf</span></div>'
          f'<div class="tl-comment" style="background:var(--c-warning-bg);border-left-color:var(--c-warning)"><b>周建华 · {s[3][0]}：</b>{s[3][3]}</div></div>')
    r2 = (f'<div class="round ok"><div class="flex between"><div class="bold">第二次提交</div>{st("整改通过")}</div>'
          f'<div class="small muted mt4">何雨桐 · {s[4][0]}</div><div class="txt mt8">{s[4][3]}</div>'
          f'<div class="upload-list"><span class="file-chip">{icon("file")}信息发布三审制度（签字盖章版）.pdf</span>'
          f'<span class="file-chip">{icon("file")}2026年7-9月内容审核台账.xlsx</span><span class="file-chip">{icon("image")}审核记录截图.png</span></div>'
          f'<div class="tl-comment" style="background:var(--c-success-bg);border-left-color:var(--c-success)"><b>周建华 · {s[5][0]}：</b>{s[5][3]}</div></div>')
    hist_rows = [
        (f'<span class="no-code">{f["no"]}</span>', "2026 年审", "未建立信息发布审查机制", "2026-09-20", "2026-09-28", "2 次"),
        ('<span class="muted">ZG20241105003</span>', "2024 年审", "账号管理员信息为空", "2024-11-05", "2024-11-12", "1 次"),
        ('<span class="muted">ZG20230518001</span>', "专项检查", "二维码与主页链接失效", "2023-05-18", "2023-05-25", "1 次"),
    ]
    hist = table(["整改编号", "来源", "整改问题", "下发 / 完成", "轮次", "结果"],
                 [[no, f'<span class="nowrap">{src}</span>', prob, f'<span class="num nowrap">{s1} ~ {s2}</span>', n, st("整改通过")]
                  for no, src, prob, s1, s2, n in hist_rows])
    stats = "".join([mini("累计整改", "3 次"), mini("本次提交轮次", "2 轮", "warning"), mini("本次用时", "8 天", "primary"), mini("当前结果", "整改通过", "success")])
    body = (f'<div class="grid g4">{stats}</div>'
            + '<div class="split mt16" style="grid-template-columns:minmax(0,1fr) 400px"><div>'
            + card("本次整改任务", task, btn("查看学院整改审核", "../college/rectify-detail.html", "text", size="sm"))
            + card("整改提交与审核（两轮）", f'<div class="grid g2">{r1}{r2}</div>', cls="mt16")
            + card("历次整改记录", hist, cls="mt16")
            + '</div><div>'
            + card("整改全流程", timeline(flow_items("rectify")))
            + card("整改后状态", alert("整改通过后，账号运行状态恢复为“正常运行”，2026 年度年审恢复流转至学院审核。", "success"), cls="mt16")
            + "</div></div>")
    hd = arch_header(a, a["name"], ("正常运行", "已备案", "待学院审核", "无异动"), "整改记录", "DA-CS-2021-0093")
    arch_page("archive-rectify.html", "整改记录", a["name"], hd, body)


def archive_cancel():
    a = ACCOUNTS["zombie"]
    info = kv([("注销编号", f'<span class="no-code">{FLOWS["zombie"]["no"]}</span>'), ("注销时间", "2026-09-30 16:00"),
               ("注销原因", tag("团支部毕业", "danger")), ("发起方式", "系统预警 → 辅导员核实"),
               ("最后发布时间", f'{a["last_post"]}'), ("停更天数", f'<span class="c-danger bold">{a["idle_days"]} 天</span>'),
               ("核实人", "王晓琳 · 2021级辅导员"), ("学院审核", "周建华 · 学院团委书记"), ("校团委确认", "陈静 · 校团委宣传部"),
               ("注销说明", "该团支部已于 2025 年 6 月整体毕业离校，无学生继续运营；账号已在微信后台停止更新，由辅导员代为保管管理员权限。", True)], 3)
    retained = "".join(
        f'<a class="card card-hover" href="{h}" style="padding:14px 16px"><div class="flex gap12">{role_ic(ic, c)}'
        f'<div class="grow"><div class="bold fs13">{t}</div><div class="small muted">{m}</div></div>{icon("chevron-right")}</div></a>'
        for t, m, ic, c, h in [("基本信息快照", "注销时点全部字段", "file", "", "archive-basic.html"),
                               ("历任负责人", "3 任团支书记录", "users", "green", "archive-staff.html"),
                               ("年审记录", "2021-2025 共 5 条", "calendar", "orange", "archive-audit.html"),
                               ("操作日志", "全部业务留痕 27 条", "log", "gray", "archive-logs.html")])
    body = (alert("本账号已注销，档案转为只读。系统不删除注销账号，全部历史信息、审核记录与佐证材料永久保留，可随时查询与导出。", "warning", "lock")
            + '<div class="split mt16" style="grid-template-columns:minmax(0,1fr) 400px"><div>'
            + card("注销信息", info, st("已注销"))
            + card("佐证材料", upload_list(["2021级软件工程1班毕业团员名单.pdf", "公众号后台停更截图.png", "辅导员核实说明.docx"]), cls="mt16")
            + card("保留的历史数据", f'<div class="grid g2">{retained}</div>', cls="mt16")
            + '</div><div>'
            + card("注销审批链路", timeline(flow_items("zombie")), btn("校级处置记录", "../school/zombie-detail.html", "text", size="sm"))
            + "</div></div>")
    hd = arch_header(a, a["name"], ("已注销", "已注销", "本年度注销", "注销"), "注销信息", "DA-CS-2021-0311", cancelled=True)
    arch_page("archive-cancel.html", "注销信息", a["name"], hd, body)


def upload_list(files):
    return '<div class="upload-list" style="margin-top:0">' + "".join(f'<span class="file-chip">{icon("file")}{x}</span>' for x in files) + "</div>"


def archive_logs():
    a = ACCOUNTS["proxy"]
    proxy = tag("教师代办", "primary", True)
    me = '<span class="muted">本人办理</span>'
    sysm = '<span class="muted">系统自动</span>'
    rows = [
        ("2026-09-30 13:45", "周建华", "学院管理员", "审核通过", "负责人交接生效：赵磊 → 孙悦（JJ20260930006）", me, "10.96.12.37", "review"),
        ("2026-09-30 09:20", "王晓琳", "业务教师 · 宣传工作辅导员", "发起负责人交接", "原负责人赵磊已于 2025 年 6 月毕业，无法本人办理，由教师代为发起", proxy, "10.96.8.114", "apply"),
        ("2026-09-30 09:12", "王晓琳", "业务教师 · 宣传工作辅导员", "查看档案", "查看账号档案 · 责任人员", me, "10.96.8.114", "view"),
        ("2026-09-15 09:00", "系统", "—", "生成年审记录", "2026 年度年审任务发布，自动生成年审记录 NS2026-CS-0027", sysm, "—", "sys"),
        ("2026-07-01 02:00", "系统", "—", "负责人预警", "学生负责人赵磊（2021级）已毕业离校，负责人信息待更新", sysm, "—", "sys"),
        ("2026-06-11 10:26", "王晓琳", "业务教师 · 宣传工作辅导员", "审核通过", "信息变更：更新二维码（BG20260610004）", me, "10.96.8.114", "review"),
        ("2026-06-10 21:03", "赵磊", "学生用户", "发起信息变更", "更新 QQ 群二维码与主页链接", me, "APP", "apply"),
        ("2026-04-18 15:40", "王晓琳", "业务教师 · 宣传工作辅导员", "导出备案表", "导出《新媒体公众平台备案表》PDF", me, "10.96.8.114", "view"),
        ("2026-03-02 11:15", "周建华", "学院管理员", "确认导入数据", "补充确认组织类别、管理教师，确认建档", me, "10.96.12.37", "review"),
        ("2026-01-10 09:30", "陈静", "学校管理员", "历史数据导入", "以 2025 年度底库初始化建档（导入批次 IMP20260110）", sysm, "10.96.1.8", "sys"),
    ]
    tbl = table(["操作时间", "操作人", "身份", "操作类型", "操作内容", "发起方式", "终端 / IP", "操作"],
                [dict(cells=[f'<span class="num nowrap">{r[0]}</span>', f"<b>{r[1]}</b>", f'<span class="small sub">{r[2]}</span>', r[3], r[4], r[5],
                             f'<span class="small muted">{r[6]}</span>', ops(("详情", "../school/log-detail.html"))],
                      href="../school/log-detail.html", cat=r[7], cls="sel" if r[5] == proxy else "") for r in rows], id_="log-tbl")
    filt = seg([("全部", "all"), ("业务申请", "apply"), ("审核", "review"), ("系统", "sys"), ("查看 / 导出", "view")], target="#log-tbl")
    hl = (f'<div class="hl-box"><div class="flex gap12">{role_ic("hand")}<div class="grow"><div class="bold">教师代办留痕 · 负责人交接</div>'
          f'<div class="small sub mt4">王晓琳于 2026-09-30 09:20 代办交接，日志记录“发起方式：教师代办”，并留存代办原因；学院管理员周建华 13:45 审核通过后生效。</div></div>'
          f'{btn("查看日志详情", "../school/log-detail.html", "primary", "eye", "sm")}</div></div>')
    body = (hl
            + card("操作日志", f'<div class="toolbar"><div>{filt}</div><label class="top-search" style="width:260px">{icon("search")}<input placeholder="搜索操作人 / 操作内容" data-search="#log-tbl"></label></div>' + tbl + pager(27, 3),
                   btn("导出日志", None, "default", "download", "sm", toast="已导出计院ACM协会操作日志"), cls="mt16"))
    hd = arch_header(a, a["name"], ("正常运行", "已备案", "待填报", "变更"), "操作日志", "DA-CS-2018-0027")
    arch_page("archive-logs.html", "操作日志", a["name"], hd, body)


# ---------------------------------------------------------------- 新建备案向导（从「我负责的账号」打开放弹窗，不占侧栏）
WIZ = ["归属信息", "平台信息", "运行与责任人", "审核人与流程"]
IDC = ACCOUNTS["idchange"]


def accounts_backdrop():
    """弹窗背后的教师账号列表。代办按钮改成从 pc/common 能点到的地址，避免校验断链。"""
    from pages_teacher import accounts_content
    return f'<div class="backdrop">{accounts_content("../teacher/proxy.html")}</div>'


def apply_dialog(title, body, close=None):
    """居中大弹窗。关闭固定回到「我负责的账号」。"""
    href = close or ACC_LIST
    return (
        f'<div class="mask wf-mask"><div class="wf-dialog" role="dialog" aria-modal="true" aria-label="{esc(title)}">'
        f'<div class="wf-hd"><b>{title}</b><a class="x-btn" href="{href}" aria-label="关闭">{icon("x")}</a></div>'
        f'<div class="wf-bd">{body}</div></div></div>'
    )


def filing_page(file, title, inner, js="", shell_back=None, dialog_title=None):
    """保留原 html 路径，打开时是账号列表上的弹窗，侧栏高亮「我负责的账号」。"""
    shell_back = shell_back or ACC_LIST
    content = accounts_backdrop() + apply_dialog(dialog_title or title, inner)
    pc_common_page(D + file, title, [("我负责的账号", None)], content, css=CSS, js=js, back=shell_back, active="accounts")


def wiz_side(idx):
    done = [("归属信息", "apply-create-basic.html"), ("平台信息", "apply-create-platform.html"),
            ("运行与责任人", "apply-create-staff.html"), ("审核人与流程", "apply-create-reviewer.html")]
    prog = []
    for i, (n, h) in enumerate(done):
        state = "done" if i < idx else ("now" if i == idx else "")
        no = icon("check", 14) if i < idx else str(i + 1)
        dot = f'<span class="step {state}" style="flex:none"><span class="step-no">{no}</span></span>'
        meta = "已填写" if i < idx else ("正在填写" if i == idx else "待填写")
        prog.append(li(n, meta, dot, "", h if i != idx else None))
    prog = "".join(prog)
    linked = (li("① 新 ID 新建备案", f'计院科协 · 新 ID {IDC["new_pid"]} · 当前填写', role_ic("file-add"), tag("填写中", "primary"))
              + li("② 原 ID 注销申请", f'计院科协 · 原 ID {IDC["pid"]} · 同步提交', role_ic("power", "red"), icon("chevron-right"), "apply-cancel.html"))
    tips = ('<ul class="small sub" style="list-style:none;display:grid;gap:8px">'
            + "".join(f'<li class="flex top-align gap8">{icon("check-circle", 14, "c-success")}<span>{x}</span></li>' for x in [
                "带 <span class='req'>*</span> 为必填项，点击“下一步”时自动校验",
                "同一平台类型下平台 ID 唯一，系统在平台信息步骤进行重复检查",
                "本系统不存储任何第三方平台账号密码",
                "草稿保留 30 天，可在“我的申请”中继续填写"]) + "</ul>")
    return (card("填写进度", f'<div class="side-steps">{prog}</div>')
            + card("关联办理 · 平台ID变更", linked, cls="mt16")
            + card("填写说明", tips, cls="mt16"))


def wiz_page(idx, file, body, prev, nxt, nxt_text="下一步", nxt_toast=None, js=""):
    prev_btn = btn("上一步", prev, "default", "arrow-left") if prev else ""
    cancel_btn = btn("取消", ACC_LIST, "default")
    inner = f"""<div data-form>
{page_hd('新建备案申请', '申请类型：新建备案 · 发起人：王晓琳（业务教师代为办理）· 草稿编号 CG20260930015',
         tag('草稿 · 自动保存于 15:21', 'muted') + btn('原型：剧本四说明', 'apply-change-id.html', 'text', 'info', 'sm'))}
<div class="card wiz-hd">{steps(WIZ, idx)}</div>
<div class="split mt16"><div>{body}</div><div class="sticky">{wiz_side(idx)}</div></div>
{actbar(f'第 {idx + 1} / 4 步 · {WIZ[idx]}', btn('保存草稿', None, 'default', 'file', toast='草稿已保存，可在“我的申请”中继续填写') + prev_btn + cancel_btn + submit_btn(nxt_text, nxt, ic='arrow-right' if idx < 3 else 'send', toast=nxt_toast))}
</div>"""
    filing_page(file, f"新建备案 {'①②③④'[idx]} {WIZ[idx]}", inner, FILL_JS + js, dialog_title=f"新建备案申请 · {WIZ[idx]}")


def apply_create_basic():
    sugg = "".join(f'<button class="chip" type="button" data-fill="{x}" data-fill-target="#org-input" data-toast="已填入：{x}">{x}</button>'
                   for x in ORG_PROMPTS)
    levels = "".join(
        f'<div class="choice{" on" if n == IDC["level"] else ""}" data-choice style="align-items:flex-start"><span class="ck" style="margin-top:2px"></span>'
        f'<div><div class="bold">{n}</div>' + (f'<div class="small muted mt4">{d}</div>' if d else '') + '</div></div>'
        for n, d in ((n, LEVEL_TEXT[n]) for n in LEVELS))
    banner = (f'<div class="hl-box"><div class="flex gap16">{role_ic("swap", "orange")}<div class="grow">'
              f'<div class="bold">剧本四 · 平台 ID 变更转新建：计院科协（哔哩哔哩）</div>'
              f'<div class="small sub mt4">原 ID <span class="num">{IDC["pid"]}</span> → 新 ID <span class="num bold c-primary">{IDC["new_pid"]}</span>，已按原档案预填归属与平台信息，请核对后提交。</div></div>'
              f'{btn("查看原 ID 注销申请", "apply-cancel.html", "ghost", "power", "sm")}</div>'
              f'<div class="mt12">{alert("由平台ID变更转入，原ID注销申请将同步提交：新建备案审核通过后，原 ID 账号状态转为“已注销”，历史数据全部保留。", "info")}</div></div>')
    body = (banner
            + card("归属信息", f"""<div class="form-grid">
  {field('所属学院', sel(COLLEGES, '计算机学院', True), True)}
  {field('所属团学组织', inp('请输入团学组织名称', IDC['org'], True, attrs='id="org-input"') + f'<div class="chips mt4">{sugg}</div>', True, ORG_HINT)}
  <div class="full">{field('组织类别', radios('org_type', ORG_TYPES, IDC['org_type'], True), True)}</div>
</div>""", cls="mt16")
            + card("平台管理层级", f'<div class="field-label mb8"><span class="req">*</span>平台管理层级：一级平台、二级平台、三级平台、社团平台</div><div class="choices g2 grid" data-single style="gap:10px">{levels}</div>'
                   + '<div class="mt12">' + alert(LEVEL_NOTE, "info") + "</div>",
                   cls="mt16"))
    wiz_page(0, "apply-create-basic.html", body, None, "apply-create-platform.html")


def mech_row(no, title, hint, name):
    return (f'<div class="mech"><div><div class="mech-t"><span class="no">{no}</span><span class="req">*</span>{title}</div>'
            f'<div class="mech-h">{hint}</div></div>{radios(name, ["是", "否"], "是", True)}</div>')


def apply_create_platform():
    intro = ("计院科协哔哩哔哩官方账号由计算机学院大学生科学技术协会运营，面向全院本科生与研究生，主要发布学科竞赛经验分享、"
             "科创项目展示、技术讲座回放与实验室开放日等视频内容。账号设有“竞赛直通车”“代码一分钟”“实验室探访”“科创人物志”"
             "四个固定栏目，坚持“先审后发”，所有视频经学生初审、指导教师终审后发布，致力于营造浓厚的科技创新氛围，服务学生成长成才。")
    mechs = "".join(mech_row(m["no"], m["title"], m["body"], m["key"]) for m in MECHANISMS)
    dup = (f'<div class="flex gap8 wrap mt4">{btn("重复检查", None, "light", "search", "sm", toast="重复检查完成：未发现同平台同 ID 账号，发现 1 个名称相似账号")}'
           f'<a class="link small" href="apply-duplicate.html">模拟：ID 重复</a><span class="muted small">|</span>'
           f'<a class="link small" href="apply-similar.html">模拟：名称相似</a></div>')
    body = (card("平台信息", f"""<div class="form-grid c3">
  {field('平台类型', sel(PLATFORM_TYPES, IDC['platform'], True), True, PLATFORM_TYPE_HINT)}
  {field('账号名称', inp(ACCOUNT_NAME_HINT, IDC['name'], True), True, ACCOUNT_NAME_HINT)}
  {field('曾用名', inp(FORMER_NAME_HINT), hint='非必填。' + FORMER_NAME_HINT)}
  <div class="span2">{field('平台ID', inp(PID_HINT, IDC['new_pid'], True) + dup, True, PID_HINT)}</div>
  {field('是否认证', radios('verify', ['是', '否'], '是', True), True, '单选，是 / 否')}
  {field('粉丝数', inp(FANS_HINT, '126', True, 'number'), True, FANS_HINT)}
  {field(TEAM_LABEL, inp('请输入人数', '8', True, 'number'), True)}
  {field('开通时间', inp('', '2026-09-26', True, 'date'), True)}
  <div class="full">{field('主页链接', inp('https://', 'https://space.bilibili.com/' + IDC['new_pid'], True), True)}</div>
</div>""")
            + card("平台头像与二维码", f'<div class="grid g2">{field("平台头像", upload("上传平台头像", "jpg / png", ["计院科协头像.png"]), True)}'
                   f'{field("二维码", upload("上传平台二维码", "jpg / png", []), hint=QR_HINT)}</div>', cls="mt16")
            + card("平台信息确认", mechs, tag("（10）至（13）", "muted"), cls="mt16")
            + card("平台介绍与发布范围", f"""<div class="form-grid c1">
  {field('平台介绍', textarea(INTRO_HINT, intro, True, 800, 5), True, INTRO_HINT)}
  {field('信息发布范围', textarea('请填写信息发布范围', '学科竞赛与科创成果展示、技术讲座与学术活动、实验室开放日、科协品牌活动及学院团学通知', True, 0, 2), True)}
  {field('备注', inp('', '原 B 站账号 386620915 因实名主体变更无法继续使用，迁移至新账号运营'))}
</div>""", cls="mt16"))
    wiz_page(1, "apply-create-platform.html", body, "apply-create-basic.html", "apply-create-staff.html")


def people_picker(pid, into, rolecol, maxn):
    cap = f"，最多 {maxn} 人" if maxn else ""
    items = []
    for name, no, phone, meta in STUDENTS:
        items.append(
            f'<button type="button" class="pick-item" data-cat="{esc(name)} {no}" onclick="pickStudent(this)" '
            f'data-into="#{into}" data-max="{maxn}" data-rolecol="{rolecol}" data-name="{esc(name)}" data-no="{no}" '
            f'data-phone="{esc(phone)}" data-extra="{esc(meta)}"><span><b>{name}</b> '
            f'<span class="muted small">{no}</span></span><span class="small muted">{phone} · {meta}</span></button>'
        )
    return (f'<div id="{pid}" class="picker hidden"><div class="small muted">输入学号或姓名检索，选中后加入列表{cap}</div>'
            f'<label class="top-search" style="width:100%;margin-top:8px">{icon("search")}'
            f'<input placeholder="输入学号或姓名" data-search="#{pid}-list"></label>'
            f'<div id="{pid}-list" class="pick-list">{"".join(items)}</div></div>')


def add_people_btn(pid, into, maxn):
    return (f'<button type="button" class="btn btn-light btn-sm" data-toggle="#{pid}" data-cap="#{into} tbody tr" '
            f'data-max="{maxn}">{icon("plus")}添加</button>')


STAFF_JS = """
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-cap]');if(!b)return;
  var max=+b.getAttribute('data-max');if(!max)return;
  var n=document.querySelectorAll(b.getAttribute('data-cap')).length;
  if(n>=max){e.stopPropagation();toast('管理员最多 '+max+' 人，不能再添加');}
},true);
function pickStudent(btn){
  var into=btn.getAttribute('data-into');
  var max=+btn.getAttribute('data-max')||0;
  var tb=document.querySelector(into+' tbody');
  var no=btn.getAttribute('data-no');
  if(tb.querySelector('[data-no="'+no+'"]')){toast('该学生已在列表中');return;}
  if(max&&tb.querySelectorAll('tr').length>=max){toast('管理员最多 '+max+' 人，不能再添加');return;}
  var name=btn.getAttribute('data-name'),phone=btn.getAttribute('data-phone'),extra=btn.getAttribute('data-extra')||'';
  var tr=document.createElement('tr');
  var cells='<td><b>'+name+'</b></td><td><span data-no="'+no+'">'+no+'</span></td><td>'+phone+'</td>';
  if(btn.getAttribute('data-rolecol')==='leader'){cells+='<td>'+extra+'</td><td>成员</td><td>2026-09-30</td>';}
  else{cells+='<td>'+extra+'</td>';}
  cells+='<td><button class="link" type="button" data-remove>删除</button></td>';
  tr.innerHTML=cells;tb.appendChild(tr);
  var panel=btn.closest('.picker');if(panel)panel.classList.add('hidden');
  toast('已添加：'+name);
}
"""


def apply_create_staff():
    hy = PEOPLE["何雨桐"]
    wx = PEOPLE["王晓琳"]
    rm = '<button class="link" type="button" data-remove>删除</button>'
    leaders = table(["姓名", "学号", "手机号", "所属组织", "学生职务", "任期开始", "操作"], [
        ["<b>何雨桐</b>", f'<span data-no="{hy["no"]}">{hy["no"]}</span>', hy["phone"], "计院科协", "新媒体部部长", "2025-09-15", rm],
    ], id_="leader-table")
    admins = table(["姓名", "学号", "手机号", "负责内容", "操作"], [
        ["<b>彭俊熙</b>", '<span data-no="8209240733">8209240733</span>', "180 7316 2285", "视频剪辑与发布", rm],
        ["<b>谢雨萌</b>", '<span data-no="8209250412">8209250412</span>', "132 1738 5570", "评论区管理与数据统计", rm],
    ], id_="admin-table")
    body = (card("运行信息", f"""<div class="form-grid c3">
  {field(PUBLISH_TIME_LABEL, inp('', '2026-09-28', True, 'date'), True, '日期选择')}
  {field('更新频率', sel(UPDATE_FREQ, UPDATE_FREQ[0], True), True)}
  {field('运行状态', sel(RUN_STATUS, '正常运行', True), True, '正常运行、不活跃、整改中、暂停运行、申请注销、已注销')}
  <div class="full">{field('异常情况', textarea('请填写异常情况', '', False, 0, 2))}</div>
</div>""")
            + card("当前管理教师", f"""<div class="form-grid c3">
  {field('姓名', inp('', '王晓琳', True), True)}
  {field('工号', inp('', wx['no'], True), True)}
  {field('职务', inp('', '宣传工作辅导员', True), True)}
  {field('手机号', inp('', wx['phone'], True), True)}
  {field('是否为专职教师', radios('fulltime', ['是', '否'], '是', True), True)}
</div>""", "收集姓名、工号、职务、手机号、是否为专职教师", cls="mt16")
            + card("当前学生运营负责人 · 具体负责人", leaders + people_picker("pick-leader", "leader-table", "leader", 0),
                   add_people_btn("pick-leader", "leader-table", 0), cls="mt16")
            + card("当前学生运营负责人 · 管理员", admins + people_picker("pick-admin", "admin-table", "admin", 5),
                   add_people_btn("pick-admin", "admin-table", 5) + '<span class="small muted">最多 5 人</span>', cls="mt16")
            + card("制度责任人", f'<div class="grid g2">'
                   + person("张卫东", f'第一责任人 · 计算机学院党委 · {PEOPLE["张卫东"]["job"]}', tag("自动带出", "muted"))
                   + person("周建华", f'直接责任人 · 计算机学院团委 · {PEOPLE["周建华"]["job"]}', tag("自动带出", "muted"))
                   + '</div><div class="mt12">' + alert("二级、三级平台由所在单位党委统一指导：分管领导为第一责任人，二级团组织书记为直接责任人，按所属学院自动带出。", "info") + "</div>",
                   cls="mt16"))
    wiz_page(2, "apply-create-staff.html", body, "apply-create-platform.html", "apply-create-reviewer.html", js=STAFF_JS)


def audit_person(title, name):
    p = PEOPLE[name]
    return (f'<div style="border:1px solid var(--c-line);border-radius:8px;padding:12px 14px"><div class="bold mb8">{title}</div>'
            f'{kv([("姓名", name), ("工号/学号", p["no"]), ("职务", p["job"]), ("手机号", p["phone"])], 2)}</div>')


def apply_create_reviewer():
    rv = person("王晓琳", f'宣传工作辅导员 · 计算机学院 · {PEOPLE["王晓琳"]["no"]} · {PEOPLE["王晓琳"]["phone"]}',
                btn("更换审核老师", "modal-reviewer.html", "ghost", "user-switch", "sm"), on=True)
    flow = timeline([
        ("now", f'① 指导教师审核 {tag("王晓琳", "primary")}', "一审负责人", ""),
        ("wait", f'② 学院团委审核 {tag("周建华", "muted")}', "二审负责人", ""),
        ("wait", f'③ 校团委审核 {tag("陈静", "muted")}', "三审负责人 · 通过后自动生成档案与备案表", ""),
    ])
    mech_sum = "、".join(f'（{m["no"]}）{m["title"]}：是' for m in MECHANISMS)
    summary = kv([("所属学院", "计算机学院"), ("所属团学组织", IDC["org"]), ("组织类别 / 层级", f'{IDC["org_type"]} · {IDC["level"]}'),
                  ("平台类型", IDC["platform"]), ("账号名称", IDC["name"]), ("平台ID", f'<span class="num bold c-primary">{IDC["new_pid"]}</span>'),
                  ("平台信息确认", mech_sum, True), ("更新频率", UPDATE_FREQ[0]), ("管理教师 / 负责人", "王晓琳 / 何雨桐"),
                  ("关联申请", f'原 ID {IDC["pid"]} 注销申请（同步提交） <a class="link" href="apply-cancel.html">查看</a>', True)], 3)
    promise = ('<label class="field promise" style="flex-direction:row;align-items:center;gap:8px;cursor:pointer">'
               '<input type="checkbox" id="promise" checked style="accent-color:var(--c-primary);width:16px;height:16px">'
               '<span class="fs13">本人承诺所填信息真实、准确、完整，平台将严格落实“先审后发”及信息安全管理要求。</span>'
               '<span class="err-msg" style="margin-left:8px">请勾选承诺</span></label>')
    body = (card("审核信息", '<div class="small muted mb12">一审、二审、三审负责人，收集姓名、工号/学号、职务、手机号。指导教师审核阶段，允许学生任意选择审核老师。</div>'
                 + rv + '<div class="small muted mt8">一审负责人按“组织 + 账号”授权范围推荐，也可点击更换。</div>'
                 + '<div class="grid g2 mt16">' + audit_person("二审负责人", "周建华") + audit_person("三审负责人", "陈静") + "</div>")
            + card("审核流程预览", flow, tag("新建备案 · 三级审核", "primary"), cls="mt16")
            + card("申请信息汇总", summary, btn("返回修改", "apply-create-basic.html", "text", "edit", "sm"), cls="mt16")
            + card("信息真实性承诺", promise, cls="mt16"))
    wiz_page(3, "apply-create-reviewer.html", body, "apply-create-staff.html", "apply-success.html", "提交申请", "申请已提交，进入审核流程", PROMISE_JS)


# ---------------------------------------------------------------- 重复检查
def apply_duplicate():
    a = ACCOUNTS["new"]
    exist = (f'<a class="card card-hover" href="archive-basic.html" style="display:block;padding:18px 20px;text-align:left">'
             f'<div class="flex gap12">{pf(a["platform"], "lg")}<div class="grow"><div class="flex gap8"><b class="fs16">{a["name"]}</b>{st("已备案")}{st("正常运行")}</div>'
             f'<div class="small muted mt4">{a["platform"]} · 平台ID {a["pid"]} · {a["level"]}</div>'
             f'<div class="small muted">{a["org"]} · 管理教师 {a["teacher"]} · 负责人 {a["student"]}</div></div>'
             f'<span class="link small flex gap4">查看档案{icon("chevron-right", 14)}</span></div></a>')
    cmp_tbl = table(["比对项", "本次填写", "系统已有账号", "结果"], [
        ["平台类型", "微信公众号", "微信公众号", tag("一致", "danger")],
        ["平台ID", "csu_cs_youth", "csu_cs_youth", tag("一致", "danger")],
        ["账号名称", "计院青年", "中南计算机青年", tag("不同", "muted")],
        ["所属组织", "计算机学院团委", a["org"], tag("相近", "warning")],
    ])
    ops_html = (back_btn("apply-create-platform.html", "返回修改") + btn("申请认领该账号", "apply-claim.html", "ghost", "hand")
                + btn("查看已有档案", "archive-basic.html", "primary", "eye"))
    content = f"""<div class="card">{result('err', '该账号已存在，禁止重复新建', '同一平台类型下平台 ID 唯一。系统检测到“微信公众号 · csu_cs_youth”已在全校账号主库中备案，本次新建申请无法提交。', ops_html)}</div>
<div class="grid g2 mt16">
  {card('系统中已存在的账号', exist + '<div class="mt12">' + alert('如该账号确属本组织但负责人信息缺失，可通过“申请认领”补充责任关系，无需重新新建。', 'info') + '</div>')}
  {card('重复检查比对结果', cmp_tbl + '<div class="small muted mt12">检查时间 2026-09-30 15:16 · 检查规则：平台类型 + 平台ID 完全一致即判定重复</div>')}
</div>"""
    filing_page("apply-duplicate.html", "重复检查 · 禁止提交", content, shell_back="apply-create-platform.html")


def apply_similar():
    sims = [
        ("计院科协", "哔哩哔哩", "386620915", "计算机学院大学生科学技术协会", 100, "名称完全一致，为本次平台 ID 变更的原账号，注销申请将同步提交", "danger"),
        ("计算机学院科协", "微信公众号", "csu_cs_kx", "计算机学院大学生科学技术协会", 83, "同一组织在其他平台的账号，平台不同可并存", "warning"),
        ("中南大学科协", "哔哩哔哩", "401127733", "中南大学大学生科学技术协会", 67, "校级组织账号，归属与层级不同", "primary"),
    ]
    rows = "".join(
        f'<div class="sim"><div>{acct(n, p, f"{p} · ID {pid} · {org}")}</div>'
        f'<div><div class="flex gap8">{progress(pct, "red" if c == "danger" else ("orange" if c == "warning" else ""))}<b class="num">{pct}%</b></div>'
        f'<div class="small muted mt4">{d}</div></div><div style="text-align:right">{tag("相似度" + ("极高" if pct >= 90 else ("较高" if pct >= 80 else "一般")), c)}</div></div>'
        for n, p, pid, org, pct, d, c in sims)
    ops_html = back_btn("apply-create-platform.html", "返回修改") + btn("确认不是同一账号，继续", "apply-create-staff.html", "primary", "arrow-right", toast="已记录确认结果，继续填写")
    content = f"""<div class="card">{result('warn', '发现名称高度相似的账号', f'本次填写“哔哩哔哩 · 计院科协 · ID {IDC["new_pid"]}”，平台 ID 未重复，但与以下 3 个在册账号名称相似。请确认不是同一账号后继续。', ops_html)}</div>
<div class="split mt16" style="grid-template-columns:minmax(0,1fr) 360px">
  {card('相似账号列表', rows, tag('按名称相似度排序', 'muted'))}
  <div>{card('处理说明', '<ul class="small sub" style="list-style:none;display:grid;gap:10px">' + ''.join(f'<li class="flex top-align gap8">{icon("info", 14, "c-primary")}<span>{x}</span></li>' for x in ['名称相似不阻止提交，仅作提示；平台类型 + 平台 ID 一致才判定重复并禁止提交', '确认继续后，“相似提示已确认”将记入申请材料，供审核老师参考', '若为同一账号，请返回修改或改为认领已有账号']) + '</ul>')}
  {card('确认信息', kv([('确认人', '王晓琳'), ('确认时间', '2026-09-30 15:17'), ('相似账号数', '3 个'), ('最高相似度', '100%')], 2), cls='mt16')}</div>
</div>"""
    filing_page("apply-similar.html", "重复检查 · 名称相似", content, shell_back="apply-create-platform.html")


# ---------------------------------------------------------------- 信息变更
def apply_change():
    fields = [
        ("name", "账号名称", IDC["name"], "", False), ("leader", "负责人", "何雨桐", "", False),
        ("teacher", "指导教师", "王晓琳", "", False), ("mgr", "具体管理教师", "王晓琳", "", False),
        ("auditor", "内容审核人员", "王晓琳、彭俊熙", "", False), ("org", "所属组织", IDC["org"], "", False),
        ("contact", "联系方式", PEOPLE["何雨桐"]["phone"], "", False), ("qr", "二维码", "2020-05-18 上传版本", "新账号二维码（2026-09-26）", True),
        ("home", "主页链接", "https://space.bilibili.com/" + IDC["pid"], "https://space.bilibili.com/" + IDC["new_pid"], True),
        ("usage", "运营用途", "科创宣传与学术活动推广", "", False), ("pid", "平台ID", IDC["pid"], IDC["new_pid"], True),
        ("other", "其他", "—", "", False),
    ]
    checks = "".join(check_item(n, on, f'data-field="{k}"') for k, n, _, _, on in fields)
    rows = []
    for k, n, cur, new, on in fields:
        hid = "" if on else " hidden"
        extra = ""
        if k == "pid":
            extra = ('<div class="mt8">' + alert("平台唯一 ID 发生变化：提交后将不按普通变更办理，系统自动转为“新 ID 新建备案 + 原 ID 注销”。", "warning") + "</div>")
        diff_attr = 'data-diff="%s"' % k
        cur_in = inp("", cur, readonly=True)
        new_in = inp("请输入变更后的内容", new, attrs=diff_attr)
        rows.append(f'<div class="cg-row{hid}" id="fr-{k}"><div class="lb">{n}</div>{cur_in}'
                    f'<div class="ar">{icon("arrow-right")}</div><div>{new_in}{extra}</div></div>')
    diff_rows = []
    for k, n, cur, new, on in fields:
        hid = "" if on else " hidden"
        ch = bool(new) and new != cur
        cls = (" changed" if ch else "") + hid
        mk = tag("已变更", "warning") if ch else '<span class="muted small">未变更</span>'
        diff_rows.append(f'<tr class="{cls.strip()}" id="dr-{k}"><td class="bold">{n}</td><td class="dv-old{" old" if ch else ""}">{cur}</td>'
                         f'<td class="dv-new{" new" if ch else ""}">{new or "—"}</td><td class="dv-mk">{mk}</td></tr>')
    diff = (f'<div class="table-wrap diff diff-side"><table class="table"><thead><tr><th style="width:76px">字段</th><th>变更前</th><th>变更后</th>'
            f'<th style="width:78px">状态</th></tr></thead><tbody>{"".join(diff_rows)}</tbody></table></div>')
    my = sel(["计院科协 · 哔哩哔哩 · 386620915", "中南计院团委 · 微信公众号", "中南计院学生会 · 微博", "计院街舞社 · 抖音", "计院ACM协会 · QQ", "计院青年志愿者 · 小红书"],
             "计院科协 · 哔哩哔哩 · 386620915", True)
    picked = (f'<div class="flex gap12">{pf(IDC["platform"], "lg")}<div class="grow"><div class="flex gap8"><b class="fs16">{IDC["name"]}</b>{st("正常运行")}{st("已备案")}</div>'
              f'<div class="small muted mt4">{IDC["platform"]} · 平台ID {IDC["pid"]} · {IDC["level"]} · {IDC["org"]}</div>'
              f'<div class="small muted">管理教师 王晓琳 · 学生负责人 何雨桐 · 粉丝 {IDC["fans"]}</div></div>'
              f'<a class="link small" href="archive-basic.html">查看档案</a></div>')
    content = f"""<div data-form>
{page_hd('信息变更申请', '发起人：王晓琳（业务教师）· 变更内容自动生成前后对比，审核通过后更新档案并留痕', tag('剧本四 · 计院科协', 'warning'))}
{alert('审核规则：<b>重要变更</b>（账号名称、所属组织、运营用途、平台ID）经指导教师、学院团委审核后<b>报校团委</b>；<b>日常维护</b>（联系方式、二维码、主页链接等）<b>学院审核后生效</b>。', 'info')}
<div class="split mt16" style="grid-template-columns:minmax(0,1fr) 440px">
  <div>
    {card('选择变更账号', field('变更账号', my, True) + '<div class="divider"></div>' + picked)}
    {card('选择变更字段', f'<div class="check-grid">{checks}</div>', '<span class="small muted">已选 <b id="field-count" class="c-primary">3</b> 项</span>', cls='mt16')}
    {card('填写变更内容', '<div class="cg-hd"><span>字段</span><span>当前值</span><span></span><span>变更后</span></div>' + ''.join(rows), cls='mt16')}
    {card('变更说明与材料', field('变更说明', textarea('请说明变更原因', '原 B 站账号因实名认证主体为已毕业学生，无法完成主体变更，科协已于 2026-09-26 注册新账号并完成机构认证，申请将平台 ID、主页链接和二维码更新为新账号信息。', True, 500, 3), True)
          + '<div class="mt16"></div>' + field('佐证材料', upload(files=['新账号认证截图.png', '科协情况说明.pdf'])), cls='mt16')}
  </div>
  <div class="sticky">{card('变更前后对比 · 实时预览', diff + '<div class="small muted mt12">勾选字段或修改“变更后”内容时，对比表同步刷新</div>')}
  {card('审核路径预测', timeline([('now', '指导教师审核 · 王晓琳', '发起人为指导教师本人，自动确认', ''), ('wait', '学院团委审核 · 周建华', '含重要变更', ''), ('wait', '校团委审核 · 陈静', '平台ID变化，需转新建办理', '')]), cls='mt16')}</div>
</div>
{actbar('提交前系统将校验平台 ID 是否变化', back_btn(ACC_LIST, '取消') + btn('保存草稿', None, 'default', 'file', toast='草稿已保存') + submit_btn('提交变更', 'apply-change-id.html', ic='send', toast='检测到平台 ID 变化，转入专项办理'))}
</div>"""
    pc_common_page(D + "apply-change.html", "信息变更申请", [("我负责的账号", ACC_LIST), ("计院科协", "archive-basic.html"), ("信息变更", None)],
                   content, css=CSS, js=DIFF_JS, back=ACC_LIST)


def apply_change_id():
    cmp = (f'<div class="id-cmp"><div class="box"><div class="small muted">原平台 ID（将注销）</div><b class="c-danger" style="text-decoration:line-through">{IDC["pid"]}</b>'
           f'<div class="small muted mt4">哔哩哔哩 · 开通于 {IDC["opened"]} · 粉丝 {IDC["fans"]}</div></div>'
           f'<div class="mid">{icon("swap", 20)}</div>'
           f'<div class="box" style="border-color:var(--c-primary-border);background:#F7FBFE"><div class="small muted">新平台 ID（需新建备案）</div><b class="c-primary">{IDC["new_pid"]}</b>'
           f'<div class="small muted mt4">哔哩哔哩 · 开通于 2026-09-26 · 已机构认证</div></div></div>')
    t1 = (f'<div class="task"><div class="flex gap12"><span class="task-no">1</span><div class="grow"><div class="bold fs16">新 ID 新建备案</div>'
          f'<div class="small muted">编号预生成 XJ20260930007</div></div>{tag("按新建办理", "primary")}</div>'
          '<ul>' + "".join(f'<li>{icon("check", 14)}<span>{x}</span></li>' for x in [
              "自动带入原档案的归属信息、四项机制与责任人员", f'平台 ID 填写为新 ID {IDC["new_pid"]}，需重新进行重复检查',
              "审核链路：指导教师 → 学院团委 → 校团委", "通过后生成新档案与新备案表"]) + '</ul>'
          f'<div class="flex gap8">{btn("填写新建备案", "apply-create-basic.html", "ghost", "file-add", "sm")}</div></div>')
    t2 = (f'<div class="task"><div class="flex gap12"><span class="task-no red">2</span><div class="grow"><div class="bold fs16">原 ID 注销申请</div>'
          f'<div class="small muted">编号预生成 ZX20260930008</div></div>{tag("同步提交", "danger")}</div>'
          '<ul>' + "".join(f'<li>{icon("check", 14)}<span>{x}</span></li>' for x in [
              "注销原因预选“平台整合”，说明“因平台ID变更注销原账号”", f'原 ID {IDC["pid"]} 状态变为“注销申请中”',
              "审核完成后账号不删除，状态改为“已注销”", "原账号全部历史记录永久保留，并与新档案关联"]) + '</ul>'
          f'<div class="flex gap8">{btn("查看注销申请", "apply-cancel.html", "danger", "power", "sm")}</div></div>')
    why = kv([("识别时间", FLOWS["idchange"]["steps"][0][0]), ("识别方式", "提交变更时比对平台 ID 字段"), ("发起人", "王晓琳 · 业务教师"),
              ("原因", "平台唯一 ID 是账号身份标识，ID 变化意味着平台上已是另一个账号，粉丝与历史内容无法继承", True)], 2)
    content = f"""{page_hd('平台 ID 变化 · 转为新建办理', '系统拦截：本次变更包含平台唯一 ID 变化', tag('剧本四', 'warning'))}
<div class="card" style="padding:24px 28px;border-color:var(--c-warning-bd);background:linear-gradient(135deg,#FFFBF3,#FFFFFF)">
  <div class="flex gap16 top-align">{role_ic('alert', 'orange')}<div class="grow">
    <div class="fs18 bold">平台唯一ID发生变化，不按普通变更办理</div>
    <div class="sub mt4">须<b>重新办理新建备案</b>，同时<b>注销原 ID 账号</b>。系统将为“计院科协”一次生成以下两项关联申请，二者共用审核链路并互相关联。</div>
    <div class="mt16">{cmp}</div>
  </div></div>
</div>
<div class="grid mt16" style="grid-template-columns:1fr 40px 1fr;align-items:stretch">{t1}<div style="display:grid;place-items:center;color:var(--c-text-3)">{icon('plus', 22)}</div>{t2}</div>
<div class="grid g2 mt16">
  {card('识别说明', why)}
  {card('办理记录', timeline([('done', FLOWS['idchange']['steps'][0][2], '王晓琳 · ' + FLOWS['idchange']['steps'][0][0], FLOWS['idchange']['steps'][0][3]), ('now', '待生成两项关联申请', '点击“一键生成两项申请”继续', '')]))}
</div>
{actbar('生成后先填写新建备案（已预填），原 ID 注销申请随后同步提交', back_btn('apply-change.html', '返回修改平台ID') + btn('一键生成两项申请', 'apply-create-basic.html', 'primary', 'zap', toast='已生成新建备案与注销申请，请核对新建信息'))}"""
    pc_common_page(D + "apply-change-id.html", "平台 ID 变化 · 转新建", [("我负责的账号", ACC_LIST), ("信息变更", "apply-change.html"), ("平台 ID 变化", None)],
                   content, css=CSS, back="apply-change.html")


# ---------------------------------------------------------------- 交接 / 注销 / 认领
def apply_handover():
    a = ACCOUNTS["handover"]
    lm, l4 = PEOPLE["李明"], PEOPLE["李四"]
    old = (f'<div class="side-box"><div class="flex between mb12"><span class="bold">原负责人</span>{tag("卸任", "muted")}</div>'
           + person("李明", lm["grade"])
           + f'<div class="form-grid c1 mt12">{field("学号", inp("", lm["no"], readonly=True))}{field("联系方式", inp("", lm["phone"], readonly=True))}'
           f'{field("任职起止", inp("", "2024-09-10 ~ 2026-09-30", readonly=True))}</div></div>')
    new = (f'<div class="side-box new"><div class="flex between mb12"><span class="bold">新负责人</span>{tag("接任", "primary")}</div>'
           + person("李四", l4["grade"])
           + f'<div class="form-grid c1 mt12">{field("姓名", inp("请输入姓名", "李四", True), True)}{field("学号", inp("请输入学号", l4["no"], True), True)}'
           f'{field("联系方式", inp("请输入手机号", l4["phone"], True), True)}{field("学生职务", inp("", l4["job"], True), True)}</div></div>')
    flow = timeline([
        ("now", "学生提交", "李明 · 原负责人发起", ""),
        ("wait", f'具体管理教师审核 {tag("王晓琳", "muted")}', "社团指导教师 · 审核通过即生效", ""),
        ("wait", "交接生效", "2026-10-01 起李四为负责人，写入责任人员历史", ""),
    ])
    rights = "".join(check_item(x, True) for x in ["平台登录绑定手机号换绑", "管理员 / 运营者权限转移", "内容审核权限转移", "历史素材与数据交接"])
    ho_form = f"""<div class="form-grid">
      {field('生效时间', inp('', '2026-10-01', True, 'date'), True, '生效后新负责人获得账号业务办理权限')}
      {field('交接类型', sel(['换届交接', '职务调整', '毕业离校', '其他'], '换届交接', True), True)}
      <div class="full">{field('交接事项', f'<div class="check-grid">{rights}</div>', hint='系统不存储第三方平台账号密码，请线下完成登录权限交接')}</div>
      <div class="full">{field('交接说明', textarea('请说明交接原因', FLOWS['handover']['steps'][0][3], True, 300, 3), True)}</div>
      <div class="full">{field('交接材料', upload(files=['街舞社换届会议纪要.pdf']), hint='换届纪要、任命文件等，非必填')}</div>
    </div>"""
    content = f"""<div data-form>
{page_hd('负责人交接申请', '学生运营负责人换届交接 · 审核通过即生效，原负责人记录不覆盖', tag('剧本三 · 计院街舞社', 'primary'))}
<div class="split" style="grid-template-columns:minmax(0,1fr) 360px">
  <div>
    {card('交接账号', acct(a['name'], a['platform'], f"{a['platform']} · 平台ID {a['pid']} · {a['level']} · 指导教师 {a['teacher']}", 'lg'), st('正常运行'))}
    {card('交接双方', f'<div class="ho">{old}<div class="mid"><span>{icon("arrow-right", 20)}</span></div>{new}</div>', cls='mt16')}
    {card('交接信息', ho_form, cls='mt16')}
  </div>
  <div class="sticky">
    {card('审核流程', flow + '<div class="small muted mt12">负责人交接属于日常维护，具体管理教师审核通过即生效，无需报学院和校团委。</div>')}
    {card('历史保留', alert('原负责人任职起止时间保留：李明 2024-09-10 ~ 2026-09-30 将写入“历任学生负责人”，可在档案中追溯。', 'success') + '<div class="mt12"><a class="link small" href="archive-staff.html">查看责任人员档案</a></div>', cls='mt16')}
  </div>
</div>
{actbar('提交后将通知指导教师王晓琳审核', back_btn('archive-staff.html', '取消') + btn('保存草稿', None, 'default', 'file', toast='草稿已保存') + submit_btn('提交交接申请', 'apply-success.html', ic='send', toast='交接申请已提交'))}
</div>"""
    pc_common_page(D + "apply-handover.html", "负责人交接申请", [("我负责的账号", ACC_LIST), ("计院街舞社", "archive-staff.html"), ("负责人交接", None)],
                   content, css=CSS, back=ACC_LIST)


def apply_cancel():
    reasons = "".join(
        f'<label class="ck-item"><input type="radio" name="reason"{" checked" if r == "平台整合" else ""}{" required" if i == 0 else ""}>{r}</label>'
        for i, r in enumerate(CANCEL_REASONS))
    flow = timeline([
        ("done", "教师发起注销申请 · 王晓琳", "2026-09-30 15:18 · 与新 ID 新建备案同步提交", ""),
        ("now", f'学院团委审核 {tag("周建华", "muted")}', "核验注销原因与佐证材料", ""),
        ("wait", f'校团委审核 {tag("陈静", "muted")}', "确认注销，账号状态转为“已注销”", ""),
    ])
    content = f"""<div data-form>
{page_hd('账号注销申请', '注销后账号不删除，状态改为“已注销”，档案与历史数据永久保留', tag('剧本四 · 原 ID 注销', 'danger'))}
<div class="split" style="grid-template-columns:minmax(0,1fr) 360px">
  <div>
    {card('注销账号', f'''<div class="flex gap12">{pf(IDC['platform'], 'lg')}<div class="grow"><div class="flex gap8"><b class="fs16">{IDC['name']}</b>{tag('原 ID', 'danger')}{st('正常运行')}{st('已备案')}</div>
      <div class="small muted mt4">{IDC['platform']} · 平台ID <b class="num">{IDC['pid']}</b> · {IDC['level']} · {IDC['org']}</div>
      <div class="small muted">开通于 {IDC['opened']} · 粉丝 {IDC['fans']} · 管理教师 王晓琳 · 负责人 何雨桐</div></div>
      <a class="link small" href="archive-basic.html">查看档案</a></div>
      <div class="mt12">{alert(f'关联申请：新 ID {IDC["new_pid"]} 新建备案（XJ20260930007）与本注销申请同步提交，审核结果互相关联。', 'info', 'link')}</div>''')}
    {card('注销原因', f'<div class="check-grid">{reasons}</div><div class="mt12">{alert("已预选“平台整合”：因平台ID变更注销原账号，原账号运营内容迁移至新 ID 账号。", "warning")}</div>', tag('单选 · 必填', 'muted'), cls='mt16')}
    {card('注销说明与佐证', field('注销说明', textarea('请说明注销原因及账号后续处置', '因平台ID变更注销原账号：原 B 站账号（ID 386620915）实名主体为已毕业学生，无法完成主体变更。科协已注册新账号（ID 1928840012）并完成机构认证，原账号将停止更新并在简介中引导关注新账号。', True, 500, 4), True)
          + '<div class="mt16"></div>' + field('佐证材料', upload(files=['原账号停更公告截图.png', '科协情况说明（盖章）.pdf']), True), cls='mt16')}
  </div>
  <div class="sticky">
    {card('审批流程预览', flow)}
    {card('数据保留', alert('审核完成后账号不删除，状态改为已注销，保留全部历史：基本信息、历任负责人、年审、变更、整改记录及操作日志。', 'success', 'shield'), cls='mt16')}
  </div>
</div>
{actbar('提交后原账号备案状态变为“注销申请中”', back_btn(ACC_LIST, '取消') + btn('保存草稿', None, 'default', 'file', toast='草稿已保存') + submit_btn('提交注销申请', 'apply-success.html', 'danger-solid', 'send', toast='注销申请已与新建备案同步提交'))}
</div>"""
    pc_common_page(D + "apply-cancel.html", "账号注销申请", [("我负责的账号", ACC_LIST), ("计院科协", "archive-basic.html"), ("账号注销", None)],
                   content, css=CSS, back=ACC_LIST)


def apply_claim():
    items = [
        ("计算机学院研究生会", "微信公众号", "csu_cs_gsu", "二级平台"), ("计院网络安全协会", "哔哩哔哩", "552031876", "社团平台"),
        ("2023级计算机科学3班团支部", "QQ", "781290346", "三级平台"), ("计院大数据协会", "抖音", "csu_cs_bigdata", "社团平台"),
        ("计院朋辈辅导中心", "微信公众号", "csu_cs_peer", "二级平台"), ("2022级物联网1班团支部", "微信公众号", "csu_iot2201", "三级平台"),
        ("计院羽毛球协会", "小红书", "csu_cs_badminton", "社团平台"), ("计院就业服务中心", "视频号", "sph_csu_cs_job", "二级平台"),
    ]
    rows = []
    for i, (n, p, pid, lv) in enumerate(items):
        c = " checked" if i == 0 else ""
        rows.append([f'<input type="radio" name="claim"{c} style="accent-color:var(--c-primary);width:15px;height:15px" aria-label="选择">',
                     acct(n, p, p, "sm"), f'<span class="num">{pid}</span>', lv, "2025 年度底库导入", "2026-01-10",
                     '<span class="c-danger small">负责人为空</span>' if i % 3 == 0 else '<span class="small muted">管理教师为空</span>',
                     tag("待认领", "warning"),
                     f'<button class="link" type="button" data-toast="已选择认领：{n}">认领</button>'])
    tbl = table(["", "账号", "平台ID", "层级", "导入来源", "导入时间", "缺失信息", "状态", "操作"], rows, id_="claim-tbl")
    claim_form = f"""<div class="form-grid">
    {field('认领后管理教师', inp('', '王晓琳', True), True)}
    {field('学生负责人', inp('请输入学生姓名 / 学号', '何雨桐 8209230509', True), True)}
    <div class="full">{field('认领说明', textarea('说明该账号与本组织的关系', '该账号为计算机学院研究生会官方公众号，系统导入时缺少负责人信息，现由指导教师认领并补充责任关系。', True, 300, 3), True)}</div>
    <div class="full">{field('佐证材料', upload(files=['公众号后台主体信息截图.png']), True, '账号后台主体信息截图或组织证明')}</div>
  </div>"""
    claim_block = f"""<div data-cat="claim" data-form>
  {card('认领已导入账号', f'<div class="toolbar"><label class="top-search" style="width:320px">{icon("search")}<input placeholder="搜索账号名称 / 平台ID" data-search="#claim-tbl"></label><span class="small muted">计算机学院待认领 8 个 · 仅显示本人授权范围</span></div>' + tbl)}
  {card('认领信息', claim_form, cls='mt16')}
  {actbar('认领需学院团委审核确认', back_btn(ACC_LIST, '取消') + submit_btn('提交认领申请', 'apply-success.html', ic='send', toast='认领申请已提交'))}
</div>"""
    backfill_form = f"""<div class="form-grid c3">
    {field('平台类型', sel(PLATFORM_TYPES, '抖音', True), True)}
    {field('账号名称', inp('', '计院电竞社', True), True)}
    {field('平台ID', inp('', 'csu_cs_esports', True), True)}
    {field('所属团学组织', inp('', '计院电子竞技协会', True), True)}
    {field('组织类别', sel(ORG_TYPES, '社团组织', True), True)}
    {field('开通时间', inp('', '2022-04-16', True, 'date'), True)}
    {field('学生负责人', inp('', '邱子墨 8209240519', True), True)}
    {field('粉丝数', inp('', '2860', True, 'number'), True)}
    {field('最近发布时间', inp('', '2026-09-21', True, 'date'), True)}
    <div class="full">{field('未备案原因', textarea('', '社团成立初期由学生自行开设，未及时报备；现按学院要求补录备案。', True, 300, 2), True)}</div>
    <div class="full">{field('佐证材料', upload(files=['账号主页截图.png']), True)}</div>
  </div>"""
    backfill_block = f"""<div data-cat="backfill" class="hidden" data-form>
  {alert('历史补录适用于系统上线前已开通、但未在 2025 年度底库中的账号。补录后按新建备案流程审核。', 'info')}
  {card('补录账号信息', backfill_form, cls='mt16')}
  {actbar('补录申请按新建备案三级审核', back_btn(ACC_LIST, '取消') + submit_btn('提交补录申请', 'apply-success.html', ic='send', toast='历史补录申请已提交'))}
</div>"""
    content = f"""{page_hd('账号认领 / 历史补录', '认领学校已导入但缺少责任关系的账号，或补录系统上线前未备案的历史账号',
         seg([('认领已导入账号', 'claim'), ('历史补录', 'backfill')], target='#claim-box'))}
<div id="claim-box">{claim_block}{backfill_block}</div>"""
    pc_common_page(D + "apply-claim.html", "账号认领 / 历史补录", [("我负责的账号", ACC_LIST), ("账号认领", None)],
                   content, css=CSS, back=ACC_LIST)


# ---------------------------------------------------------------- 提交成功
def apply_success():
    def sub_item(ic, color, no, typ, title, meta, node, right=""):
        return (f'<div class="sub-item">{role_ic(ic, color)}<div><div class="flex gap8"><span class="no-code">{no}</span>{tag(typ, "primary" if color == "" else ("danger" if color == "red" else "muted"))}</div>'
                f'<div class="bold mt4">{title}</div><div class="small muted">{meta}</div></div>'
                f'<div style="text-align:right"><div class="small muted">当前节点</div><div class="bold c-warning">{node}</div>{right}</div></div>')
    items = (sub_item("file-add", "", "XJ20260930007", "新建备案", f'计院科协 · 新 ID {IDC["new_pid"]}', "哔哩哔哩 · 二级平台 · 2026-09-30 15:18 提交", "待学院团委审核")
             + sub_item("power", "red", "ZX20260930008", "账号注销", f'计院科协 · 原 ID {IDC["pid"]}', "注销原因：平台整合（因平台ID变更注销原账号）", "待学院团委审核"))
    proxy = sub_item("hand", "gray", FLOWS["proxy"]["no"], "负责人交接 · 教师代办", "计院ACM协会 · 赵磊 → 孙悦", "发起方式：教师代办 · 2026-09-30 09:20 提交", "待学院管理员审核",
                     '<a class="link small" href="../college/approval-proxy.html">去学院审核</a>')
    flow = timeline([
        ("done", "发起信息变更，系统识别平台 ID 变化", "王晓琳 · " + FLOWS["idchange"]["steps"][0][0], FLOWS["idchange"]["steps"][0][3]),
        ("done", FLOWS["idchange"]["steps"][1][2], "王晓琳 · " + FLOWS["idchange"]["steps"][1][0], "发起人为指导教师本人，一审自动确认"),
        ("now", "学院团委审核", "周建华 · 预计 2 个工作日内", ""),
        ("wait", "校团委审核", "陈静 · 通过后生成新档案，原 ID 状态转为已注销", ""),
    ])
    actions = (btn("查看我负责的账号", ACC_LIST, "primary", "database") + btn("继续发起", "apply-create-basic.html", "ghost", "plus")
               + btn("返回工作台", "../teacher/workbench.html", "default", "home"))
    content = f"""<div class="card">{result('ok', '申请已提交', '系统已生成申请编号并推送至审核人待办，审核进度可在“我负责的账号”及消息提醒中查看。', actions)}</div>
<div class="split mt16" style="grid-template-columns:minmax(0,1fr) 400px">
  <div>
    {card('本次提交 · 剧本四（平台 ID 变更）', items, tag('2 项关联申请', 'primary'))}
    {card('同日提交 · 剧本八（教师代办）', proxy + '<div class="mt12">' + alert('教师代办的申请在日志中记录“发起方式：教师代办”，并留存代办原因，可在日志详情中追溯。', 'info') + '</div>', btn('查看代办日志', '../school/log-detail.html', 'text', 'log', 'sm'), cls='mt16')}
  </div>
  <div>
    {card('审核流程', flow)}
    {card('下一步', ''.join(li(t, m, role_ic(ic, c), icon('chevron-right'), h) for t, m, ic, c, h in [
        ('查看学院审核（演示下一角色）', '周建华 · 学院审核中心', 'hierarchy', 'green', '../college/approvals.html'),
        ('查看代办日志', '剧本八 · 发起方式：教师代办', 'log', 'gray', '../school/log-detail.html'),
        ('查看账号档案 · 操作日志', '计院ACM协会', 'archive', '', 'archive-logs.html')]), cls='mt16')}
  </div>
</div>"""
    pc_common_page(D + "apply-success.html", "申请提交成功", [("我负责的账号", ACC_LIST), ("申请提交成功", None)],
                   content, css=CSS)


# ---------------------------------------------------------------- 审核弹窗
def review_backdrop():
    a = ACCOUNTS["new"]
    info = kv([("申请类型", "新建备案"), ("账号名称", a["name"]), ("平台类型", a["platform"]), ("平台ID", a["pid"]),
               ("所属组织", a["org"]), ("组织类别 / 层级", f'{a["org_type"]} · {a["level"]}'), ("开通时间", a["opened"]),
               ("运营团队规模", "12 人"), ("四项机制", "均已建立")], 3)
    intro = ("“中南计算机青年”是计算机学院团委新媒体中心主办的官方微信公众号，面向学院全体学生，围绕思想引领、学业发展、"
             "科创实践、青春风采开展内容建设，及时发布学院团学活动与通知公告。")
    tl = timeline(flow_items("new", 3) + [("now", "指导教师审核", "王晓琳 · 待审核", "")])
    return f"""<div class="backdrop">
{page_hd('新建备案审核', f'申请编号 {FLOWS["new"]["no"]} · 提交人 李明 · 2026-09-26 20:05 重新提交', tag('待我审核', 'warning'))}
<div class="split" style="grid-template-columns:minmax(0,1fr) 360px">
  <div>{card('申请信息', info)}{card('平台介绍', f'<div class="txt">{intro}</div>', cls='mt16')}{card('责任人员', kv([('学生负责人', '李明'), ('管理教师', '王晓琳'), ('管理员', '陈思远、周可欣')], 3), cls='mt16')}</div>
  <div>{card('审核流转', tl)}</div>
</div></div>"""


def modal_page(file, title, mbody, mfoot, size="", close=REVIEW, backdrop=None, crumbs=None):
    content = (backdrop if backdrop is not None else review_backdrop()) + modal(title, mbody, mfoot, size, close_href=close)
    pc_common_page(D + file, title, crumbs or [("待办", "../teacher/todo.html"), ("新建备案审核", REVIEW), (title, None)],
                   content, css=CSS, back=close)


def modal_head_info():
    a = ACCOUNTS["new"]
    return (f'<div class="flex gap12 mb16" style="padding:12px 14px;border-radius:10px;background:var(--c-bg)">{pf(a["platform"])}'
            f'<div class="grow"><div class="bold">{a["name"]} · 新建备案</div><div class="small muted">{FLOWS["new"]["no"]} · 申请人 李明 · {a["org"]}</div></div>{tag("指导教师审核", "warning")}</div>')


def modal_approve():
    body = (modal_head_info()
            + field("审核意见", textarea("请输入审核意见", FLOWS["new"]["steps"][3][3], True, 300, 3), True)
            + '<div class="chips mt8">' + "".join(f'<button class="chip" type="button" data-choice>{x}</button>' for x in ["信息完整", "四项机制健全", "同意备案", "请学院审核"]) + "</div>"
            + '<div class="mt16">' + alert('通过后将流转至<b>学院团委审核（周建华）</b>，并通知申请人李明。<a class="link" href="../college/approval-detail.html">预览学院审核页</a>', "info") + "</div>"
            + f'<label class="radio mt12"><input type="checkbox" checked>同时发送消息通知申请人</label>')
    foot = back_btn(REVIEW, "取消") + submit_btn("确认通过", "review-done.html", "success", "check", toast="审核通过，已流转至学院团委")
    modal_page("modal-approve.html", "审核通过确认", body, foot)


def modal_return():
    fields = "".join(check_item(x, x == "平台介绍") for x in ["平台介绍", "信息发布范围", "平台头像", "二维码", "运营团队规模", "四项机制", "学生负责人", "管理员"])
    reasons = "".join(f'<button class="chip{" on" if i == 0 else ""}" type="button" data-choice>{x}</button>'
                      for i, x in enumerate(["平台介绍不足 100 字", "信息发布范围未填写", "材料不清晰", "负责人信息有误", "机制佐证缺失"]))
    body = (modal_head_info()
            + field("需修改的字段", f'<div class="check-grid">{fields}</div>', True, "勾选的字段将在学生端高亮提示")
            + '<div class="mt16"></div>' + field("退回原因", f'<div class="chips">{reasons}</div>')
            + '<div class="mt16"></div>' + field("退回说明", textarea("请填写具体修改要求", FLOWS["new"]["steps"][1][3], True, 300, 3), True)
            + '<div class="mt12">' + alert("退回后申请回到学生端“退回修改”，学生修改后重新提交仍由您审核。", "warning") + "</div>")
    foot = back_btn(REVIEW, "取消") + submit_btn("确认退回", "../../app/student/application-returned.html", "warning", "undo", toast="已退回，已通知学生李明")
    modal_page("modal-return.html", "退回修改", body, foot, "lg")


def modal_reject():
    reasons = radios("rej", ["不属于团学组织平台", "重复申请", "平台主体与组织不符", "材料虚假", "其他"], "平台主体与组织不符", True)
    body = (modal_head_info()
            + alert("驳回即不予办理，流程终止；申请人如需办理须重新发起申请。如仅需补充材料，请使用“退回修改”。", "danger")
            + '<div class="mt16"></div>' + field("驳回原因", reasons, True)
            + '<div class="mt12"></div>' + field("驳回说明", textarea("请说明驳回理由", "经核实，该公众号注册主体为个人，非学院团委或所属学生组织，不符合团学组织新媒体平台备案条件，请以组织名义重新注册后再申请。", True, 300, 3), True))
    foot = back_btn(REVIEW, "取消") + submit_btn("确认驳回", "../../app/student/application-rejected.html", "danger-solid", "ban", toast="已驳回，流程终止，已通知学生李明")
    modal_page("modal-reject.html", "驳回申请", body, foot)


def modal_reviewer():
    teachers = [
        ("王晓琳", "宣传工作辅导员", "计算机学院团委及直属学生组织 · 24 个账号", "推荐", True),
        ("刘洋", "2023级辅导员", "2023 级各班团支部 · 15 个账号", "", False),
        ("陈立新", "学生组织指导教师", "学生会、研究生会 · 6 个账号", "", False),
        ("黄敏", "2024级辅导员", "2024 级各班团支部 · 18 个账号", "", False),
        ("李卫国", "科协指导教师", "计院科协、ACM 协会 · 4 个账号", "", False),
        ("邓倩", "志愿服务负责教师", "青年志愿者协会 · 3 个账号", "", False),
    ]
    lst = "".join(
        f'<div class="choice{" on" if on else ""}" data-choice><span class="ck"></span>{avatar(n, "sm") if n in ("王晓琳", "刘洋") else ini(n)}'
        f'<div class="grow"><div class="flex gap8"><b>{n}</b><span class="small muted">{job}</span>{tag(badge, "success") if badge else ""}</div>'
        f'<div class="small muted">负责范围：{scope}</div></div></div>'
        for n, job, scope, badge, on in teachers)
    body = (f'<label class="top-search" style="width:100%;height:38px">{icon("search")}<input placeholder="搜索教师姓名 / 工号 / 负责范围" data-search="#rv-list"></label>'
            + '<div class="small muted mt12 mb8">按“组织 + 账号”授权范围匹配，推荐负责本组织的指导教师</div>'
            + f'<div class="choices" id="rv-list" data-single>{lst}</div>')
    foot = back_btn("apply-create-reviewer.html", "取消") + btn("确认选择", "apply-create-reviewer.html", "primary", "check", toast="已选择一审老师：王晓琳")
    backdrop = (f'<div class="backdrop">{page_hd("新建备案申请", "申请类型：新建备案 · 草稿编号 CG20260930015", "")}'
                f'<div class="card wiz-hd">{steps(WIZ, 3)}</div>'
                + card("一审指导教师", person("王晓琳", "宣传工作辅导员 · 计算机学院", "", True), cls="mt16")
                + card("审核流程预览", timeline([("now", "① 指导教师审核", "一审", ""), ("wait", "② 学院团委审核", "二审", ""), ("wait", "③ 校团委审核", "终审", "")]), cls="mt16")
                + "</div>")
    modal_page("modal-reviewer.html", "选择审核老师", body, foot, "", "apply-create-reviewer.html", backdrop,
               [("新建备案", "apply-create-basic.html"), ("审核人与流程", "apply-create-reviewer.html"), ("选择审核老师", None)])


def review_done():
    a = ACCOUNTS["new"]
    s = FLOWS["new"]["steps"]
    tl = timeline(flow_items("new", 4) + [("now", "学院团委审核", "周建华 · 待审核", ""), ("wait", "校团委审核", "陈静", "")])
    info = kv([("申请编号", f'<span class="no-code">{FLOWS["new"]["no"]}</span>'), ("账号", f'{a["name"]} · {a["platform"]}'),
               ("审核人", "王晓琳 · 指导教师"), ("审核时间", s[3][0]), ("审核结果", st("已通过")), ("下一节点", "学院团委审核 · 周建华"),
               ("审核意见", s[3][3], True)], 3)
    nxt = "".join(li(t, m, role_ic(ic, c), tag(k, kc), h) for t, m, ic, c, k, kc, h in [
        ("计算机学院学生会 · 名称变更", "李明 · 2026-09-26 提交 · 拟改名“中南计院学生会”", "file-edit", "orange", "变更", "warning", "../teacher/review-change.html"),
        ("计院街舞社 · 负责人交接", "李明 → 李四 · 2026-09-27 提交", "user-switch", "green", "交接", "success", "../teacher/review-handover.html"),
        ("计院青年志愿者 · 年度年审", "何雨桐 · 2026-09-18 提交", "calendar", "", "年审", "primary", "../teacher/review-annual.html"),
    ])
    actions = (btn("处理下一条", "../teacher/review-change.html", "primary", "arrow-right") + btn("返回待办", "../teacher/todo.html", "default", "inbox")
               + btn("查看学院审核（演示下一角色）", "../college/approval-detail.html", "ghost", "hierarchy")
               + btn("查看学生端进度", "../../app/student/application-detail.html", "default", "smartphone"))
    content = f"""<div class="card">{result('ok', '审核通过，已流转至学院团委审核', '“中南计算机青年”新建备案已由您审核通过，系统已通知学院团委周建华与申请人李明。', actions)}</div>
<div class="split mt16" style="grid-template-columns:minmax(0,1fr) 400px">
  <div>{card('审核结果', info)}{card('待我审核 · 还有 8 条', nxt, btn('全部待办', '../teacher/todo.html', 'text', size='sm'), cls='mt16')}</div>
  <div>{card('流程进度', tl)}</div>
</div>"""
    pc_common_page(D + "review-done.html", "审核完成", [("待办", "../teacher/todo.html"), ("审核完成", None)], content, css=CSS,
                   back="../teacher/todo.html")


# ---------------------------------------------------------------- 登录与身份
def login():
    pwd_form = f"""<div data-cat="pwd" data-form>
  <label class="cas-in field">{icon('user')}<input placeholder="请输入学号 / 工号" value="T20180427" required></label>
  <label class="cas-in field">{icon('lock')}<input type="password" placeholder="请输入密码" value="csu@2026" required></label>
  <div class="cas-row"><label class="radio"><input type="checkbox" checked>7天免登录</label>
    <span class="links"><button class="link" type="button" data-toast="请前往学校统一身份认证平台找回密码">忘记密码</button><i></i><button class="link" type="button" data-toast="在线帮助：如无法登录请联系信息与网络中心">在线帮助</button></span></div>
  {submit_btn('登录', 'identity-switch.html', toast='统一身份认证成功').replace('class="btn btn-primary"', 'class="btn btn-primary cas-btn"')}
</div>"""
    sms_form = f"""<div data-cat="sms" class="hidden" data-form>
  <label class="cas-in field">{icon('phone')}<input placeholder="请输入手机号" value="176****0432" required></label>
  <label class="cas-in field">{icon('shield')}<input id="sms-code" placeholder="请输入短信验证码" required><button class="sms" type="button" onclick="var i=document.getElementById('sms-code');if(i)i.value='246810';" data-toast="验证码 246810 已发送至绑定手机 151****2233">获取验证码</button></label>
  {submit_btn('登录', 'identity-switch.html', toast='验证码登录成功').replace('class="btn btn-primary"', 'class="btn btn-primary cas-btn"')}
</div>"""
    qr_block = f"""<div data-cat="qr" class="hidden"><div class="cas-qr">{qr(176, 3)}
  <div class="mt12 bold">请使用“中南大学”APP 或企业微信扫码</div><div class="small muted mt4">二维码 120 秒内有效</div>
  <div class="flex center gap12 mt16">{btn('模拟扫码成功', 'identity-switch.html', 'primary', 'check', 'sm', toast='扫码确认成功')}{btn('刷新二维码', None, 'default', 'refresh', 'sm', toast='二维码已刷新')}</div>
</div></div>"""
    tabs = seg([('账号登录', 'pwd'), ('扫码登录', 'qr'), ('验证码登录', 'sms')], target='#login-box').replace('class="seg"', 'class="seg cas-tabs"')
    body = f"""<div class="cas">
  <div class="cas-logo" role="img" aria-label="中南大学智慧学工"></div>
  <section class="cas-box">
    <div class="cas-hd"><h2>统一身份认证</h2><div class="cas-lang"><button class="on" type="button" data-toast="当前语言：中文">中文</button><button type="button" data-toast="原型仅提供中文版本">Eng</button></div></div>
    {tabs}
    <div id="login-box">{pwd_form}{qr_block}{sms_form}</div>
    <div class="cas-row"><button class="link" type="button" data-toast="账号激活请使用学校统一身份认证平台">账号激活</button>
      <span>还没有账号？<button class="link" type="button" data-toast="请联系学院团委开通平台使用权限">去申请</button></span></div>
    <div class="cas-note">{icon('info')}<span>团学新媒体平台通过学校统一身份认证登录，不存储任何第三方平台（微信、抖音、微博等）的账号密码。</span></div>
  </section>
  <div class="cas-foot">技术支持：中南大学信息与网络中心<br>Copyright © 共青团中南大学委员会</div>
  <div class="cas-proto"><a href="../../app/common/login.html">{icon('smartphone', 14)}移动端登录</a><a href="identity-switch.html">{icon('user-switch', 14)}多身份说明</a><a href="{NAV}">{icon('grid', 14)}返回原型导航</a></div>
</div>"""
    write(D + "login.html", "统一身份认证登录", body, CSS + LOGIN_CSS, kind="pc")


def identity_switch():
    roles = [
        ("陈静", "学校管理员", "校团委宣传部 · 宣传部部长", "building", "", "../school/dashboard.html", "进入数据驾驶舱",
         ["全校 35 个二级团组织、986 个账号", "校级审核、年审发起与批量审核", "僵尸号监管、数据导入导出、系统配置",
          "移动端可办理终审并查看账号、组织与年审节点"], False),
        ("周建华", "学院管理员", "计算机学院团委 · 学院团委书记", "hierarchy", "green", "../college/workbench.html", "进入学院工作台",
         ["计算机学院 36 个账号", "学院审核、年审统一提交校团委", "任务分派、整改下发、本院授权"], False),
        ("王晓琳", "业务教师", "计算机学院 · 3 项授权身份", "user", "orange", "../teacher/workbench.html", "进入教师工作台",
         ["宣传工作辅导员 · 2021级辅导员 · 街舞社指导教师", "审核本人授权范围内的申请与年审", "学生毕业 / 失联时教师代办"], True),
        ("李明", "学生用户", "计算机学院 · 2023级软件工程2班 · 学号 8209230117", "user", "", "../student/home.html", "进入学生首页",
         ["本人负责的 5 个新媒体账号", "发起备案、变更、交接、注销与认领", "在线年审、整改提交与僵尸号核实"], False),
    ]
    cards = []
    for n, r, org, ic, c, h, cta, pts, cur in roles:
        badge = tag("当前登录", "success") if cur else tag("演示账号", "muted")
        lis = "".join(f'<li>{icon("check-circle", 14)}<span>{p}</span></li>' for p in pts)
        go = btn(cta, h, "primary" if cur else "ghost", "arrow-right", toast="已切换身份：" + r + " · " + n)
        if n == "陈静":
            go = (f'<div class="flex gap8 wrap">{go}'
                  f'{btn("移动端", "../../app/school/home.html", "default", "smartphone", toast="已进入学校管理员移动端")}</div>')
        cards.append(f'<div class="card role-card{" cur" if cur else ""}"><div class="top">{avatar(n, "lg")}<div class="grow">'
                     f'<div class="flex gap8"><b class="fs18">{n}</b>{badge}</div><div class="small muted">{org}</div></div>{role_ic(ic, c)}</div>'
                     f'<div class="flex gap8">{tag(r, "primary")}<span class="small muted">PC 端</span></div><ul>{lis}</ul>'
                     f'{go}</div>')
    scope_rows = [
        ["<b>宣传工作辅导员</b>", "计算机学院团委及直属学生组织（学生会、研究生会、科协、青协等）", "24 个", '<div class="scope">' + tag("新建/变更审核", "primary") + tag("年审审核", "primary") + tag("教师代办", "primary") + "</div>", "2023-09-01 至今"],
        ["<b>2021级辅导员</b>", "2021 级各班团支部（含已毕业团支部）", "12 个", '<div class="scope">' + tag("年审审核", "primary") + tag("僵尸号核实", "warning") + tag("注销建议", "danger") + "</div>", "2021-09-01 至今"],
        ["<b>街舞社指导教师</b>", "计院街舞社", "1 个", '<div class="scope">' + tag("交接审核", "primary") + tag("年审审核", "primary") + "</div>", "2023-09-01 至今"],
    ]
    dims = "".join(f'<div class="dim">{role_ic(ic, c)}<div><div class="bold">{t}</div><div class="small sub mt4">{d}</div></div></div>'
                   for t, d, ic, c in [("组织维度", "可管理哪些学院、团支部、学生组织、社团", "hierarchy", ""),
                                       ("账号维度", "在组织范围内可查看、审核哪些具体账号", "database", "green"),
                                       ("操作维度", "可执行审核、代办、核实、导出等哪些操作", "key", "orange")])
    content = f"""{page_hd('选择本次进入的身份', '统一身份认证已通过 · 工号 T20180427 · 2026-09-30 16:30 · 一人多身份时，按本次办理事项选择身份进入',
         btn('移动端身份选择', '../../app/common/identity-switch.html', 'default', 'smartphone', 'sm') + btn('退出登录', 'login.html', 'default', 'logout', 'sm'))}
<div class="grid g2">{''.join(cards)}</div>
<div class="split mt16" style="grid-template-columns:minmax(0,1fr) 380px">
  {card('王晓琳 · 授权范围明细', table(['授权身份', '组织范围', '账号数', '可执行操作', '生效期限'], scope_rows)
        + '<div class="small muted mt12">同一教师在不同身份下看到的数据范围不同：例如以“2021级辅导员”身份可核实 2021 级团支部僵尸号，但不一定能查看学院全部社团的负责人信息。</div>',
        btn('查看授权配置', '../school/user-permission.html', 'text', size='sm'))}
  {card('一人多身份，按“组织 + 账号 + 操作”授权', f'<div class="grid" style="gap:10px">{dims}</div>')}
</div>"""
    pc_common_page(D + "identity-switch.html", "多身份选择", [("统一身份认证", "login.html"), ("选择身份", None)], content, css=CSS,
                   back="login.html", side=False)


def build():
    login()
    identity_switch()
    archive_basic()
    archive_staff()
    archive_audit()
    archive_changes()
    archive_rectify()
    archive_cancel()
    archive_logs()
    apply_create_basic()
    apply_create_platform()
    apply_create_staff()
    apply_create_reviewer()
    apply_duplicate()
    apply_similar()
    apply_change()
    apply_change_id()
    apply_handover()
    apply_cancel()
    apply_claim()
    apply_success()
    modal_approve()
    modal_return()
    modal_reject()
    modal_reviewer()
    review_done()
