"""手机账号档案正文。分区与 PC 账号档案一致，只读或带上各角色原有操作。

学校、学院、教师、学生打开同一账号时，字段来自同一份演示数据（data.py、
全校账号行，以及 PC 档案页里已经写明的沿革）。不另做一套缩略字段。
"""
from base import esc, mechanism_blocks, re_strip, tag, timeline
from data import (ACCOUNTS, FLOWS, LEVEL_TEXT, PEOPLE, PUBLISH_TIME_LABEL, STUDENTS, TEAM_LABEL,
                  UPDATE_FREQ)

ARCHIVE_CSS = """
.arch .sec-t{font-size:16px;font-weight:700;display:flex;align-items:center;gap:8px;margin-bottom:8px;color:#222}
.arch .sec-t::before{content:"";width:3px;height:16px;border-radius:2px;background:var(--c-primary);flex:none}
.arch .row{display:flex;justify-content:space-between;gap:12px;padding:11px 0;border-bottom:1px dashed #EEF0F3;align-items:flex-start}
.arch .row:last-child{border-bottom:none;padding-bottom:0}
.arch .row>span:first-child{color:#666;flex:none;font-size:15px;line-height:1.5}
.arch .row>span:last-child{text-align:right;color:#222;font-size:15px;line-height:1.5;word-break:break-all}
.arch .row.stack{flex-direction:column;gap:4px}
.arch .row.stack>span:last-child{text-align:left;font-size:15px;line-height:1.7;color:#222}
.arch .intro{margin-top:8px;padding:12px;background:#F7F9FB;border-radius:8px;font-size:15px;line-height:1.75;color:#222}
.arch .tl-title{font-size:15px}
.arch .tl-meta{font-size:13px;color:#666;line-height:1.5}
.arch .tl-comment{font-size:14px;line-height:1.65;color:#333}
.arch .small.sub{font-size:14px;line-height:1.7;color:#333}
.arch .log-item{padding:12px 0;border-bottom:1px dashed #E6E8EB}
.arch .log-item:last-child{border-bottom:none;padding-bottom:0}
.arch .qr{display:inline-block;padding:8px;background:#fff;border:1px solid var(--c-line);border-radius:8px}
.arch .qr svg{display:block}
.arch-ops{display:flex;gap:8px;flex-wrap:nowrap;overflow-x:auto;margin-top:4px}
.arch-ops .btn{flex:none;white-space:nowrap}
"""

ARCH_JS = r"""
(function(){
  var boxes=document.querySelectorAll('[data-case]');
  if(!boxes.length)return;
  var m=location.search.match(/[?&](?:c|acct)=([\w-]+)/);
  var key=m?decodeURIComponent(m[1]):boxes[0].getAttribute('data-case');
  var found=false;
  boxes.forEach(function(x){
    var on=x.getAttribute('data-case')===key;
    if(on)found=true;
    x.classList.toggle('hidden',!on);
  });
  if(!found){boxes.forEach(function(x,i){x.classList.toggle('hidden',i!==0);});}
  var box=document.querySelector('[data-case]:not(.hidden)');
  if(!box)return;
  ['chg','hand','cancel','more'].forEach(function(k){
    var a=document.getElementById('op-'+k);
    var v=box.getAttribute('data-'+k);
    if(a&&v)a.setAttribute('href',v);
  });
  var lab=document.getElementById('op-more-tx');
  var t=box.getAttribute('data-more-label');
  if(lab&&t)lab.textContent=t;
})();
"""

YOUTH_INTRO = (
    "“中南计算机青年”是计算机学院团委新媒体中心主办的官方微信公众号，面向学院 4600 余名本科生和研究生，"
    "围绕“思想引领、学业发展、科创实践、青春风采”四条主线开展内容建设。平台设置“计院青年说”“竞赛直通车”"
    "“实验室开放日”“学长学姐来了”“团学快讯”五个固定栏目，及时发布学院团学活动、主题团日、学科竞赛与"
    "科创成果、志愿服务及就业实习信息。平台严格执行“先审后发”三审制度，所有推文经学生编辑初审、新媒体中心"
    "主任复审、指导教师终审后发布，坚持正确政治方向和舆论导向，讲好计院青年成长故事。"
)
YOUTH_SCOPE = "学院团学活动与主题团日、青年思想引领、学科竞赛与科创成果、志愿服务、学院通知公告及就业实习信息"


def rows(items):
    out = []
    for k, v in items:
        cls = "row stack" if len(re_strip(v)) > 16 else "row"
        out.append('<div class="' + cls + '"><span>' + k + '</span><span>' + v + '</span></div>')
    return "".join(out)


def sec(title, body):
    return '<div class="m-card"><div class="sec-t">' + title + '</div>' + body + '</div>'


def dv(v):
    if v is None or v == "":
        return "—"
    return str(v)


def scene_of(pid):
    for key, acc in ACCOUNTS.items():
        if acc.get("pid") == pid:
            return key
    return ""


def guess_org_type(a):
    if a.get("org_type"):
        return a["org_type"]
    org = a.get("org") or ""
    level = a.get("level") or ""
    if "团支部" in org or "三级" in level:
        return "班级团支部"
    if "社团" in level or "社团" in org or "协会" in org or "社" in org:
        return "社团组织"
    if "一级" in level:
        return "校级学生组织"
    return "院级学生组织"


def guess_college(a):
    if a.get("college"):
        return a["college"]
    org = a.get("org") or ""
    level = a.get("level") or ""
    if org.startswith("校团委") or "一级" in level:
        return "校团委"
    return "计算机学院"


def student_bits(name):
    if not name or name == "—":
        return "—"
    base = name.split("（")[0]
    for n, no, phone, grade in STUDENTS:
        if n == base:
            return name + " · " + no + " · " + phone + " · " + grade
    person = PEOPLE.get(base)
    if not person:
        return name
    extra = person.get("grade") or person.get("job") or ""
    text = name + " · " + person["no"] + " · " + person["phone"]
    if extra:
        text += " · " + extra
    return text


def teacher_bits(name):
    if not name or "空" in name or name in ("—", "未分配"):
        return dv(name)
    person = PEOPLE.get(name)
    if not person:
        return name
    return name + " · " + person["no"] + " · " + person["job"] + " · " + person["phone"]


def copy_val(val):
    if not val or val == "—":
        return "—"
    return (val + ' <button type="button" class="btn btn-text btn-sm" data-copy="'
            + esc(val) + '">复制</button>')


def flow_tl(key, end=None, now=None):
    steps = FLOWS[key]["steps"]
    if end is not None:
        steps = steps[:end]
    items = []
    for when, who, title, cm in steps:
        state = "back" if ("退回" in title or "继续整改" in title or "要求整改" in title) else "done"
        items.append((state, title, who + " · " + when, cm))
    if now:
        items.append(now)
    return timeline(items)


def chg(date, field, old, new, no, kind, who, state):
    return (
        '<div class="log-item"><div class="flex between gap8"><b>' + field + '</b><span>' + kind + '</span></div>'
        '<div style="margin-top:4px;font-size:13px;color:#666">' + date + " · " + who + " · " + no + '</div>'
        '<div style="margin-top:6px;font-size:15px;line-height:1.6"><span style="color:#888">' + old
        + '</span> → <span style="color:#0E8A55">' + new + '</span></div>'
        '<div style="margin-top:4px;font-size:14px">' + state + '</div></div>'
    )


def decorate(raw):
    a = dict(raw)
    a["scene"] = a.get("scene") or scene_of(a.get("pid"))
    a["college"] = guess_college(a)
    a["org_type"] = guess_org_type(a)
    src = ACCOUNTS.get(a["scene"]) if a["scene"] else None
    if src:
        for key in ("opened", "fans", "change", "last_post", "idle_days", "new_name", "new_student"):
            if src.get(key) and not a.get(key):
                a[key] = src[key]
        if not a.get("org_type"):
            a["org_type"] = src.get("org_type") or guess_org_type(a)
    a["former"] = a.get("former") or "无"
    a["change"] = a.get("change") or (src.get("change") if src else "") or ""
    if a.get("pid") == "3152286640":
        a["former"] = "无"
        a["change"] = "无异动"
        a["org_type"] = "班级团支部"
    if a["scene"] == "rename":
        a["former"] = "中南信息学院学生会"
        a["opened"] = a.get("opened") or "2016-03-12"
        a["fans"] = a.get("fans") or "12,480"
    if a["scene"] == "new":
        a["former"] = "无"
        a["fans"] = a.get("fans") if a.get("fans") not in (None, "", "—") else "—"
        a["opened"] = a.get("opened") or "2026-09-20"
    return a


def basic_rows(a):
    level_note = LEVEL_TEXT.get(a.get("level") or "", "")
    level = dv(a.get("level"))
    if level_note:
        level = level + '<br><span style="color:#666;font-weight:400">' + level_note + '</span>'
    return rows([
        ("平台类型", dv(a.get("platform"))),
        ("平台 ID", copy_val(dv(a.get("pid")))),
        ("账号名称", dv(a.get("name"))),
        ("所属学院", dv(a.get("college"))),
        ("所属组织", dv(a.get("org"))),
        ("组织类别", dv(a.get("org_type"))),
        ("平台层级", level),
        ("管理教师", dv(a.get("teacher"))),
        ("学生负责人", dv(a.get("student"))),
        ("运行状态", dv(a.get("run"))),
        ("备案状态", dv(a.get("filing"))),
        ("年审状态", dv(a.get("annual"))),
        ("年度异动", dv(a.get("change"))),
        (PUBLISH_TIME_LABEL, dv(a.get("last") or a.get("last_post"))),
    ])


def belong_rows(a):
    return rows([
        ("所属学校", "中南大学"),
        ("所属学院", dv(a.get("college"))),
        ("所属团学组织", dv(a.get("org"))),
        ("组织类别", dv(a.get("org_type"))),
        ("平台管理层级", dv(a.get("level"))),
        ("开通时间", dv(a.get("opened"))),
    ])


def platform_rows(a, note):
    body = rows([
        ("平台类型", dv(a.get("platform"))),
        ("账号名称", dv(a.get("name"))),
        ("曾用名", dv(a.get("former"))),
        ("平台 ID", copy_val(dv(a.get("pid")))),
        ("是否认证", dv(a.get("certified"))),
        ("粉丝数", dv(a.get("fans"))),
        (TEAM_LABEL, dv(a.get("team"))),
        ("开通时间", dv(a.get("opened"))),
        ("主页链接", dv(a.get("home"))),
        ("平台头像", dv(a.get("avatar_note"))),
        ("信息发布范围", dv(a.get("scope"))),
    ])
    if a.get("intro"):
        body += '<div class="intro">' + a["intro"] + '</div>'
    if note:
        body += note
    return body


def run_rows(a):
    return rows([
        (PUBLISH_TIME_LABEL, dv(a.get("last") or a.get("last_post"))),
        ("更新频率", dv(a.get("freq"))),
        ("运行状态", dv(a.get("run"))),
        ("异常情况", dv(a.get("abnormal"))),
        ("年度异动", dv(a.get("change"))),
        ("停更天数", (str(a.get("idle_days")) + " 天") if a.get("idle_days") else "—"),
    ])


def staff_rows(a, extra):
    lines = [
        ("管理教师", teacher_bits(a.get("teacher"))),
        ("学生具体负责人", student_bits(a.get("student"))),
        ("账号管理员", dv(a.get("admins"))),
    ]
    if a.get("college") == "计算机学院":
        lines += [
            ("第一责任人", teacher_bits("张卫东")),
            ("直接责任人", teacher_bits("周建华")),
        ]
    body = rows(lines)
    if extra:
        body += extra
    return body


def filing_rows(a, extra):
    body = rows([
        ("备案状态", dv(a.get("filing"))),
        ("申请 / 备案编号", dv(a.get("filing_no"))),
        ("备案时间", dv(a.get("filing_at"))),
        ("终审人", dv(a.get("final_who"))),
    ])
    if extra:
        body += extra
    return body


def annual_rows(a, extra):
    body = rows([
        ("年度", "2026"),
        ("年审状态", dv(a.get("annual"))),
        ("年度异动", dv(a.get("change"))),
        ("年审编号", dv(a.get("annual_no"))),
        (PUBLISH_TIME_LABEL, dv(a.get("last") or a.get("last_post"))),
        ("学生负责人", dv(a.get("student"))),
        ("管理教师", dv(a.get("teacher"))),
    ])
    if extra:
        body += extra
    elif a.get("annual") in (None, "", "—"):
        body += '<div class="intro">本账号尚无年审记录。</div>'
    return body


def change_rows(a, extra):
    filing = a.get("filing") or ""
    if "变更" in filing:
        current = filing
    elif a.get("change") == "变更":
        current = "有变更，见下列记录"
    else:
        current = "无未完成的变更申请"
    body = rows([("曾用名", dv(a.get("former"))), ("当前变更", current)])
    if extra:
        body += extra
    return body


def rectify_rows(a, extra):
    blob = " ".join([a.get("run") or "", a.get("filing") or "", a.get("annual") or ""])
    if extra:
        head = rows([("当前状态", dv(a.get("annual") if "整改" in blob else "无整改任务"))])
        return head + extra
    if "整改" in blob:
        return rows([
            ("运行状态", dv(a.get("run"))),
            ("年审状态", dv(a.get("annual"))),
            ("整改说明", "整改过程见本账号年审与审核记录，材料不在本页修改。"),
        ])
    return rows([("整改记录", "无整改任务")])


def log_rows(a, extra):
    if extra:
        return extra
    return timeline([
        ("done", "档案在册", dv(a.get("name")),
         "运行 " + dv(a.get("run")) + " · 备案 " + dv(a.get("filing")) + " · 年审 " + dv(a.get("annual"))),
    ])


def cancel_rows(a, extra):
    if extra:
        return extra
    blob = " ".join([a.get("run") or "", a.get("filing") or "", a.get("annual") or ""])
    if "注销" in blob:
        return rows([
            ("运行状态", dv(a.get("run"))),
            ("备案状态", dv(a.get("filing"))),
            ("年审状态", dv(a.get("annual"))),
            ("说明", "注销后档案、负责人、年审和日志保留，不删除。"),
        ])
    return rows([("注销状态", "未注销"), ("说明", "账号仍在册，本页不提供注销申请。")])


def qr_block(a):
    from pages_pc_common import qr
    seed = sum(ord(ch) for ch in ((a.get("name") or "") + (a.get("pid") or "x"))) % 90 + 3
    return (
        '<div style="display:flex;flex-direction:column;align-items:flex-start;gap:10px">' + qr(96, seed)
        + '<div><div class="bold" style="font-size:16px;line-height:1.45">' + dv(a.get("name")) + '</div>'
        + '<div style="margin-top:4px;font-size:14px;color:#666;line-height:1.5">' + dv(a.get("platform"))
        + " · " + dv(a.get("pid")) + '</div></div></div>'
    )


def apply_story(a):
    """把 PC 档案里已经写过的沿革补进当前账号，不改当前列表上的状态。"""
    scene = a.get("scene") or ""
    pid = a.get("pid") or ""
    if pid == "3152286640":
        a["certified"] = a.get("certified") or "—"
        a["team"] = a.get("team") or "—"
        a["freq"] = a.get("freq") or "—"
        a["abnormal"] = "无"
        a["admins"] = a.get("admins") or "—"
        a["annual_no"] = "NS2026-CS-0019"
        a["filing_no"] = a.get("filing_no") or "—"
        a["intro"] = a.get("intro") or ""
        a["scope"] = a.get("scope") or "—"
        return {
            "annual": timeline([
                ("done", "学生填报完成", "陈可欣 · 2026 年度", "年度异动：无异动"),
                ("done", "教师审核通过", "刘洋 · 2023级辅导员", "信息无变化。"),
                ("done", "学院统一提交", "周建华 · 计算机学院团委", "纳入学院统一提交"),
                ("done", "学校审核通过", "年审通过", "学生填报、教师审核、学院提交、学校审核均已完成"),
            ]),
            "logs": timeline([
                ("done", "年审通过", "2026 年度 · NS2026-CS-0019", "无异动。教师意见：信息无变化。学院意见：统一提交。"),
                ("done", "档案在册", "QQ · 3152286640", "管理教师刘洋，学生负责人陈可欣，最近发布 2026-09-25"),
            ]),
        }
    if scene == "new":
        a["certified"] = "是 · 微信认证 · 2026-09-22"
        a["team"] = "12"
        a["home"] = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=csu_cs_youth"
        a["avatar_note"] = "已上传 · 2026-09-24"
        a["scope"] = YOUTH_SCOPE
        a["intro"] = YOUTH_INTRO
        a["admins"] = "陈可欣（8209230221）、刘子涵（8209240133）"
        a["freq"] = UPDATE_FREQ[0]
        a["abnormal"] = "无"
        a["filing_no"] = FLOWS["new"]["no"]
        a["change"] = a.get("change") or "新建"
        return {
            "filing": flow_tl("new", 5, ("now", "待校团委终审", "陈静 · 校团委宣传部", "学院已通过，等待终审")),
            "logs": flow_tl("new", 5, ("now", "待校团委终审", "陈静 · 校团委宣传部", "")),
            "annual": '<div class="intro">新建备案尚未终审，2026 年度年审未开始。</div>',
        }
    if scene == "rename":
        a["admins"] = "陈可欣（8209230221）、刘子涵（8209240133）"
        a["freq"] = UPDATE_FREQ[1]
        a["abnormal"] = "无"
        a["scope"] = "学院学生会工作动态、校园文化与通知"
        a["home"] = "weibo.com/u/" + a.get("pid", "")
        a["certified"] = "是"
        a["avatar_note"] = "已上传"
        a["team"] = "—"
        a["filing_no"] = FLOWS["rename"]["no"]
        a["annual_no"] = "—"
        if not a.get("last"):
            a["last"] = "2026-09-18"
        return {
            "staff": timeline([
                ("now", "李明（现任）", "2025-09-20 起 · 待本次名称变更审核", student_bits("李明")),
                ("done", "张涵", "交接至 2025-09-20", "交接单 JJ20250918004"),
                ("done", "罗一鸣", "2024-09-12 前", "历史补录"),
            ]),
            "annual": timeline([
                ("now", "2026 年度 · " + dv(a.get("annual")), "名称变更办理中", "年度异动：变更"),
                ("done", "2025 年度 · 年审通过", "校团委审核通过", "年度异动：变更（负责人交接）"),
                ("done", "2024 年度 · 年审通过", "校团委审核通过", "年度异动：变更（指导教师由刘洋调整为王晓琳）"),
            ]),
            "change": (
                chg("2026-09-26", "账号名称", "计算机学院学生会", "中南计院学生会", FLOWS["rename"]["no"],
                    tag("重要变更", "warning"), "李明", tag("待指导教师审核", "warning"))
                + chg("2025-09-20", "学生负责人", "张涵", "李明", "JJ20250918004",
                      tag("交接", "primary"), "王晓琳", tag("已生效", "success"))
                + chg("2024-09-12", "学生负责人", "罗一鸣", "张涵", "历史补录",
                      tag("交接", "primary"), "刘洋", tag("已生效", "success"))
                + chg("2024-03-05", "指导教师", "刘洋", "王晓琳", "历史补录",
                      tag("日常维护", "muted"), "周建华（学院）", tag("已生效", "success"))
                + chg("2023-06-18", "主页链接", "weibo.com/csuxxxy", "weibo.com/u/7722108845", "历史补录",
                      tag("日常维护", "muted"), "周建华（学院）", tag("已生效", "success"))
                + chg("2022-11-02", "二维码", "旧版二维码", "新版二维码", "历史补录",
                      tag("日常维护", "muted"), "周建华（学院）", tag("已生效", "success"))
                + chg("2019-07-01", "账号名称", "中南信息学院学生会", "计算机学院学生会", "历史补录",
                      tag("重要变更", "warning"), "校团委", tag("已生效", "success"))
                + chg("2019-07-01", "所属组织", "信息科学与工程学院学生会", "计算机学院学生会", "历史补录",
                      tag("重要变更", "warning"), "校团委", tag("已生效", "success"))
            ),
            "logs": flow_tl("rename", 1, ("now", "待指导教师审核", "王晓琳", FLOWS["rename"]["steps"][0][3])),
        }
    if scene == "handover":
        a["admins"] = "吴嘉怡（短视频剪辑与发布）、张博文（评论区管理与数据统计）"
        a["freq"] = UPDATE_FREQ[1]
        a["abnormal"] = "无"
        a["certified"] = "是"
        a["avatar_note"] = "已上传"
        a["team"] = "—"
        a["filing_no"] = FLOWS["handover"]["no"]
        a["opened"] = a.get("opened") or "2019-10-08"
        if not a.get("last"):
            a["last"] = "2026-09-12"
        return {
            "staff": timeline([
                ("now", "李四（拟于 2026-10-01 生效）", PEOPLE["李四"]["grade"] + " · " + PEOPLE["李四"]["job"],
                 student_bits("李四")),
                ("done", "李明", "2024-09-10 ~ 2026-09-30", "原负责人任职保留"),
                ("done", "陈雨萱", "2022-09-05 ~ 2024-09-09", "历史补录"),
                ("done", "黄子轩", "2020-09-12 ~ 2022-09-04", "历史补录"),
                ("done", "刘梦琪", "2019-10-08 ~ 2020-09-11", "创始社长 · 历史补录"),
            ]) + '<div class="intro">具体管理教师：王晓琳（2023-09-01 至今，专职）。刘洋（2020-09-01 ~ 2023-08-31，已卸任）。邓志强（2019-10-08 ~ 2020-08-31，兼职，已卸任）。</div>'
            + flow_tl("handover", 2),
            "annual": '<div class="intro">2026 年度年审待填报。历史年审随账号档案保留。</div>',
            "change": '<div class="intro">本次是负责人交接，不改平台 ID。交接单 ' + FLOWS["handover"]["no"]
            + '，指导教师已通过，拟 2026-10-01 生效。</div>',
            "logs": flow_tl("handover", 2),
        }
    if scene == "annual":
        a["admins"] = "新媒体中心编辑组"
        a["freq"] = UPDATE_FREQ[0]
        a["abnormal"] = "无"
        a["certified"] = "是"
        a["fans"] = a.get("fans") if a.get("fans") not in (None, "", "—") else "36,512"
        a["team"] = "—"
        a["avatar_note"] = "已上传"
        a["annual_no"] = FLOWS["annual"]["no"]
        a["opened"] = a.get("opened") or "2014-09-01"
        a["scope"] = "学院团学工作、思想引领与通知公告"
        if not a.get("last"):
            a["last"] = "2026-09-17"
        return {
            "annual": (
                '<div class="intro">2026 年度年审编号 ' + FLOWS["annual"]["no"]
                + '。学生 09-18 确认无异动，教师 09-20 审核通过，学院 09-29 统一提交。当前年审状态以基本信息为准。</div>'
                + flow_tl("annual", 4)
                + timeline([
                    ("done", "2025 年度 · 年审通过", "NS2025-CS-0011", "线下年审 · 初始化导入"),
                    ("done", "2024 年度 · 年审通过", "NS2024-CS-0010", "历史补录 · 无异动"),
                    ("done", "2023 年度 · 年审通过", "NS2023-CS-0013", "历史补录 · 整改后通过"),
                    ("done", "2022 年度 · 年审通过", "NS2022-CS-0009", "历史补录"),
                    ("done", "2021 年度 · 年审通过", "NS2021-CS-0012", "历史补录"),
                ])
            ),
            "logs": flow_tl("annual", 4),
        }
    if scene == "rectify":
        a["admins"] = "—"
        a["freq"] = UPDATE_FREQ[1]
        a["abnormal"] = "年审整改：未建立信息发布审查机制"
        a["certified"] = "—"
        a["filing_no"] = FLOWS["rectify"]["no"]
        a["annual_no"] = FLOWS["rectify"]["no"]
        a["opened"] = a.get("opened") or "2021-04-22"
        if not a.get("last"):
            a["last"] = "2026-09-26"
        return {
            "rectify": (
                rows([
                    ("整改编号", FLOWS["rectify"]["no"]),
                    ("整改来源", "2026 年度年审 · 指导教师要求整改"),
                    ("下发人", "周建华 · 学院团委"),
                    ("整改责任人", student_bits("何雨桐")),
                    ("下发时间", "2026-09-20"),
                    ("截止时间", FLOWS["rectify"]["deadline"]),
                    ("整改问题", FLOWS["rectify"]["steps"][0][3]),
                    ("整改要求", FLOWS["rectify"]["steps"][1][3]),
                ])
                + flow_tl("rectify")
                + '<div class="intro">历次整改：ZG20241105003（2024 年审，账号管理员信息为空，已通过）；ZG20230518001（专项检查，二维码与主页链接失效，已通过）。</div>'
            ),
            "logs": flow_tl("rectify"),
        }
    if scene == "zombie":
        a["abnormal"] = "疑似僵尸号 · 停更 " + str(a.get("idle_days") or 412) + " 天"
        a["freq"] = UPDATE_FREQ[4]
        a["last"] = a.get("last") or a.get("last_post") or "2025-08-14"
        a["idle_days"] = a.get("idle_days") or 412
        a["filing_no"] = FLOWS["zombie"]["no"]
        a["admins"] = "—"
        a["opened"] = a.get("opened") or "2021-10-15"
        return {
            "cancel": rows([
                ("处置编号", FLOWS["zombie"]["no"]),
                ("当前处置", "待校团委确认"),
                ("注销原因", "团支部毕业"),
                ("最近发布", dv(a.get("last"))),
                ("停更天数", str(a.get("idle_days")) + " 天"),
                ("核实意见", FLOWS["zombie"]["steps"][1][3]),
                ("学院意见", FLOWS["zombie"]["steps"][2][3]),
                ("说明", "尚未注销。确认前档案保持可查，确认后也不删除历史。"),
            ]) + flow_tl("zombie", 3, ("now", "待校团委确认", "陈静 · 校团委宣传部", "")),
            "logs": flow_tl("zombie", 3, ("now", "待校团委确认", "陈静", "")),
            "annual": '<div class="intro">年审状态见本页顶部。僵尸号处置单独流转，不替代年审字段。</div>',
        }
    if scene == "proxy":
        a["admins"] = "—"
        a["freq"] = "—"
        a["abnormal"] = "无"
        a["certified"] = "—"
        a["opened"] = a.get("opened") or "2018-11-03"
        a["filing_no"] = FLOWS["proxy"]["no"]
        if not a.get("last"):
            a["last"] = "2026-09-24"
        return {
            "staff": timeline([
                ("now", "孙悦（现任）", student_bits("孙悦"), "学院审核通过后接任"),
                ("done", "赵磊（已毕业）", "2021级 · 原会长", "无法本人办理，由教师代办交接"),
            ]) + flow_tl("proxy"),
            "logs": timeline([
                ("done", "审核通过", "周建华 · 学院管理员 · 2026-09-30 13:45", "负责人交接生效：赵磊 → 孙悦（" + FLOWS["proxy"]["no"] + "）"),
                ("done", "发起负责人交接", "王晓琳 · 业务教师 · 2026-09-30 09:20", "发起方式：教师代办。原负责人已毕业，无法本人办理。"),
                ("done", "查看档案", "王晓琳 · 2026-09-30 09:12", "查看账号档案 · 责任人员"),
                ("done", "生成年审记录", "系统 · 2026-09-15 09:00", "2026 年度年审任务发布"),
                ("done", "负责人预警", "系统 · 2026-07-01 02:00", "学生负责人赵磊已毕业离校"),
                ("done", "审核通过", "王晓琳 · 2026-06-11 10:26", "信息变更：更新二维码（BG20260610004）"),
                ("done", "发起信息变更", "赵磊 · 学生 · 2026-06-10 21:03", "更新 QQ 群二维码与主页链接"),
                ("done", "导出备案表", "王晓琳 · 2026-04-18 15:40", "导出备案表留痕"),
                ("done", "确认导入数据", "周建华 · 2026-03-02 11:15", "补充确认组织类别、管理教师"),
                ("done", "历史数据导入", "陈静 · 2026-01-10 09:30", "导入批次 IMP20260110"),
            ]),
            "change": '<div class="intro">2026-09-30 负责人由赵磊交接为孙悦，平台 ID 不变。更早的二维码、主页变更留在操作记录中。</div>',
        }
    if scene == "photo":
        a["abnormal"] = "疑似僵尸号，待负责人核实"
        a["freq"] = UPDATE_FREQ[3]
        a["last"] = a.get("last") or a.get("last_post") or "2026-03-02"
        a["idle_days"] = a.get("idle_days") or 212
        a["admins"] = "—"
        a["opened"] = a.get("opened") or "2022-03-09"
        return {
            "annual": '<div class="intro">须先完成僵尸号核实，再进入年审填报。系统只预警，不直接注销。</div>',
            "cancel": rows([
                ("注销状态", "未注销"),
                ("最近发布", dv(a.get("last"))),
                ("停更天数", str(a.get("idle_days")) + " 天"),
                ("说明", "学生可核实仍在运营，或另行申请注销。"),
            ]),
            "logs": timeline([
                ("now", "待负责人核实", "李明", "停更 " + str(a.get("idle_days")) + " 天，最近发布 " + dv(a.get("last"))),
                ("done", "系统预警", "2026-09-22", "标记疑似僵尸号，不直接注销"),
            ]),
        }
    if scene == "idchange":
        a["abnormal"] = "平台 ID 发生变化，须新建备案并注销原 ID"
        a["admins"] = "—"
        a["opened"] = a.get("opened") or "2020-05-18"
        return {
            "change": '<div class="intro">原平台 ID ' + ACCOUNTS["idchange"]["pid"] + "，新 ID "
            + ACCOUNTS["idchange"]["new_pid"] + "。ID 变化不按普通变更办理。</div>"
            + flow_tl("idchange"),
            "logs": flow_tl("idchange"),
        }
    return {}


def render_archive(raw):
    a = decorate(raw)
    extra = apply_story(a)
    parts = [
        sec("基本信息", basic_rows(a)),
        sec("归属信息", belong_rows(a)),
        sec("平台信息", platform_rows(a, extra.get("platform") or "")),
        sec("平台信息确认", mechanism_blocks(("11",) if a.get("scene") == "rectify" else ())),
        sec("运行信息", run_rows(a)),
        sec("负责人与管理员", staff_rows(a, extra.get("staff") or "")),
        sec("备案信息", filing_rows(a, extra.get("filing") or "")),
        sec("年审记录", annual_rows(a, extra.get("annual") or "")),
        sec("变更记录", change_rows(a, extra.get("change") or "")),
        sec("整改记录", rectify_rows(a, extra.get("rectify") or "")),
        sec("操作记录", log_rows(a, extra.get("logs") or "")),
        sec("注销信息", cancel_rows(a, extra.get("cancel") or "")),
        sec("平台二维码", qr_block(a)),
    ]
    return '<div class="arch">' + "".join(parts) + '</div>'


def action_row(pairs):
    if not pairs:
        return ""
    btns = []
    for label, href, kind in pairs:
        btns.append('<a class="btn btn-' + kind + ' btn-sm" href="' + href + '">' + label + '</a>')
    return '<div class="m-card"><div class="sec-t">可办理</div><div class="arch-ops">' + "".join(btns) + '</div></div>'
