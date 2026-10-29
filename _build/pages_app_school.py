"""移动端 · 学校管理员（陈静，校团委宣传部）。

手机上办理校级终审，并查看全校账号、组织、年审节点和僵尸号。
批量审批、导入导出、权限、字典、风险规则、创建年审或整改任务留在 PC 端。
"""
from base import *  # noqa: F401,F403
from data import ACCOUNTS, FLOWS, PEOPLE, SCHOOL_STATS as S, ANNUAL_TASK as T
from mobile_archive import ARCHIVE_CSS, render_archive
from pages_app_staff import (INTRO, badge, fold, head, list_item, opinion, page_t, rows, sec, todo_card, toggle_btn)
from pages_school import ACCT_LIST, ANNUAL_COUNTS, ANNUAL_NODES, ORG_LIST
from wf import TODO

DS = "app/school/"

SCHOOL_CSS = """
.sub13{font-size:13px;line-height:1.65;color:#333}
.tree-a{display:flex;align-items:center;gap:8px;padding:11px 2px;border-bottom:1px solid #F0F2F5;font-size:14px;color:#333}
.tree-a .cnt{margin-left:auto;color:#666;font-size:12px;font-weight:500}
.tree-sub{margin:0 0 6px 14px;padding-left:8px;border-left:1px dashed #B3CDFB}
.tree-sub .tree-a{font-size:13px}
.node-row{display:flex;gap:10px;padding:12px 0;border-bottom:1px solid #F0F2F5}
.node-row:last-child{border-bottom:none}
.node-dot{width:10px;height:10px;border-radius:50%;margin-top:6px;flex:none;background:#C8C9CC}
.node-dot.done{background:#1BB975}
.node-dot.now{background:#E6A23C;box-shadow:0 0 0 4px rgba(230,162,60,.25)}
.ro{display:flex;align-items:flex-start;gap:8px;padding:10px 12px;border-radius:8px;background:#E6EFFF;color:#333;font-size:13px;line-height:1.65}
.ro .i{color:#0057F0;flex:none;margin-top:2px}
.alert a{color:#0057F0;font-weight:600;margin-left:8px}
.bottom-bar{gap:8px;padding-left:12px;padding-right:12px}
.bottom-bar .btn.slim{flex:0 0 auto;padding:0 12px}
.bottom-bar .btn.wide{flex:1 1 auto}
.stat-link{display:block;background:#fff;border-radius:10px;padding:10px 8px;text-align:center}
.stat-link b{display:block;font-size:18px;font-variant-numeric:tabular-nums}
.stat-link small{display:block;font-size:11px;color:#666;margin-top:2px}
"""

CASE_JS = r"""
(function(){
  var boxes=document.querySelectorAll('[data-case]');
  if(!boxes.length)return;
  var m=location.search.match(/[?&]c=([\w-]+)/);
  var key=m?m[1]:boxes[0].getAttribute('data-case');
  var found=false;
  boxes.forEach(function(x){
    var on=x.getAttribute('data-case')===key;
    if(on)found=true;
    x.classList.toggle('hidden',!on);
  });
  if(!found){
    boxes.forEach(function(x,i){x.classList.toggle('hidden',i!==0);});
    key=boxes[0].getAttribute('data-case');
  }
  var box=document.querySelector('[data-case="'+key+'"]');
  if(!box)return;
  document.querySelectorAll('[data-act]').forEach(function(btn){
    var href=box.getAttribute('data-'+btn.getAttribute('data-act'));
    if(!href)return;
    if(btn.hasAttribute('data-href'))btn.setAttribute('data-href',href);
    if(btn.hasAttribute('data-submit'))btn.setAttribute('data-submit',href);
  });
})();
"""

SEARCH_JS = r"""
(function(){
  var m=location.search.match(/[?&]q=([^&]+)/);
  if(!m)return;
  var el=document.querySelector('[data-search]');
  if(!el)return;
  el.value=decodeURIComponent(m[1].replace(/\+/g,' '));
  el.dispatchEvent(new Event('input',{bubbles:true}));
})();
"""

ACCT_KEYS = [
    "csu-youth", "csu-stu", "cs-tw", "cs-stu", "cs-new", "cs-vol", "se2101", "se2302",
    "dance", "acm", "photo", "bs-tw", "xy-voice", "wx-shu", "civil20", "jd-maker",
]
PC_REVIEW = {
    "new": "../../pc/school/approval-detail.html",
    "change": "../../pc/school/approval-change.html",
    "cancel": "../../pc/school/approval-cancel.html",
    "zombie": "../../pc/school/zombie-detail.html",
    "annual": "../../pc/school/annual-review-detail.html",
    "rectify": "../../pc/school/rectify-detail.html",
}
KIND_NAME = {"new": "新建", "change": "变更", "cancel": "注销", "zombie": "僵尸号", "annual": "年审", "rectify": "整改"}
KIND_TAG = {
    "new": ("新建备案", "primary"), "change": ("重要变更", "warning"), "cancel": ("账号注销", "danger"),
    "zombie": ("僵尸号确认", "danger"), "annual": ("年审校审", "primary"), "rectify": ("整改复核", "warning"),
}
STEPS = {
    "new": (["学生提交", "教师审核", "学院审核", "校级审核"], 3),
    "change": (["学生提交", "教师审核", "学院审核", "校级审核"], 3),
    "cancel": (["学生提交", "教师审核", "学院审核", "校级审核"], 3),
    "zombie": (["系统预警", "教师核实", "学院审核", "校团委确认"], 3),
    "annual": (["学生填报", "教师审核", "学院提交", "校级审核"], 3),
    "rectify": (["下发整改", "提交材料", "学院初审", "校级复核"], 3),
}
OPINION = {
    "new": "准予备案。",
    "change": "同意变更，原名称记入曾用名。",
    "cancel": "同意注销，保留历史数据。",
    "zombie": "账号状态转为已注销，数据永久保留。",
    "annual": "整改已闭环，同意本账号年审通过。",
    "rectify": "账号已恢复访问，整改通过。",
}
PASS_TOAST = {
    "new": "已通过，将建立档案并生成备案表",
    "change": "已同意变更，原名称记入曾用名",
    "cancel": "已同意注销，数据永久保留",
    "zombie": "已确认注销，数据永久保留",
    "annual": "本账号年审已通过",
    "rectify": "整改通过，任务已关闭",
}
PASS_NAME = {
    "new": "准予备案", "change": "同意变更", "cancel": "同意注销",
    "zombie": "确认注销", "annual": "年审通过", "rectify": "整改通过",
}
EFFECT = {
    "new": {
        "pass": "已准予备案。系统将建立账号档案并生成备案表，已通知申请人与学院。",
        "back": "已退回申请人修改。重新提交后需再次逐级审核，原审批记录保留。",
        "reject": "已驳回，不予备案。流程终止，已通知申请人与学院。",
    },
    "change": {
        "pass": "已同意变更。原名称记入曾用名，历史发布与年审仍在同一档案。",
        "back": "已退回申请人修改名称或补充材料。",
        "reject": "已驳回本次变更。账号名称保持不变。",
    },
    "cancel": {
        "pass": "已同意注销。运行状态与备案状态将转为已注销，档案永久保留。",
        "back": "已退回补充佐证或说明。账号尚未注销。",
        "reject": "已驳回注销申请。账号保持当前状态。",
    },
    "zombie": {
        "pass": "已确认注销。账号状态转为已注销，数据永久保留，系统不直接删除。",
        "back": "已退回学院补充核实。本次不注销。",
        "reject": "已驳回本次注销建议。如需转整改或解除预警，请在 PC 端处置。",
    },
    "annual": {
        "pass": "本账号年审已通过。无异动账号的批量通过请在 PC 端办理。",
        "back": "已退回学院或指导教师补充。本账号不计入批量通过。",
        "reject": "本年审未通过。如需整改或注销，请在 PC 端继续办理。",
    },
    "rectify": {
        "pass": "整改通过。任务关闭，账号恢复正常运行。",
        "back": "已退回继续整改，并通知学生负责人与学院。",
        "reject": "已驳回本次整改。如需转注销，请在 PC 端发起。",
    },
}
REVIEW_PAGE = {
    "new": "review-new.html", "change": "review-change.html", "cancel": "review-cancel.html",
    "zombie": "review-zombie.html", "annual": "review-annual.html", "rectify": "review-rectify.html",
}
REVIEW_TITLE = {
    "new": "新建备案审核", "change": "重要变更审核", "cancel": "注销审核",
    "zombie": "僵尸号确认", "annual": "年审校审", "rectify": "整改复核",
}
COLLEGE_TREE = [
    ("col-csu", "校团委（直属）", 24), ("col-cs", "计算机学院", 36), ("col-bs", "商学院", 42),
    ("col-wx", "文学院", 28), ("col-jd", "机电工程学院", 51), ("col-za", "资源与安全工程学院", 33),
    ("col-xy", "湘雅医学院", 64), ("col-law", "法学院", 22), ("col-math", "数学与统计学院", 24),
    ("col-chem", "化学化工学院", 31), ("col-mat", "材料科学与工程学院", 33), ("col-civil", "土木工程学院", 45),
]


def page_s(file, title, content, notes, flow, **kw):
    extra = kw.pop("css", "")
    kw["css"] = SCHOOL_CSS + extra
    page_t("school", DS + file, title, content, notes, flow, **kw)


def filechips(names):
    return "".join('<span class="file-chip">' + icon("file") + n + "</span>" for n in names)


def ro(text):
    return '<div class="ro mb12">' + icon("eye") + "<div>" + text + "</div></div>"


def past_now(steps, now_title, now_meta):
    items = []
    for when, who, title, cm in steps:
        kind = "back" if ("退回" in title or "继续整改" in title or "要求整改" in title) else "done"
        items.append((kind, title, who + " · " + when, cm))
    items.append(("now", now_title, now_meta, ""))
    return timeline(items)


def now_of(it):
    if it["kind"] == "zombie":
        return "校团委确认", "陈静 · 待确认（当前节点）"
    if it["kind"] == "rectify":
        return "校团委复核", "陈静 · 待复核（当前节点）"
    return "校团委审核", "陈静 · 待审核（当前节点）"


def item_steps(it):
    if it.get("flow_key"):
        return FLOWS[it["flow_key"]]["steps"][:it["flow_n"]]
    return it.get("steps") or []


def node_comments(it):
    if it["key"] == "cs-new":
        st = FLOWS["new"]["steps"]
        return ("教师意见", "王晓琳", st[3][3], "学院意见", "周建华", st[4][3])
    if it["key"] == "cs-stu":
        st = FLOWS["rename"]["steps"]
        return ("教师意见", "王晓琳", st[1][3], "学院意见", "周建华", st[2][3])
    if it["key"] == "se2101":
        st = FLOWS["zombie"]["steps"]
        return ("核实意见", "王晓琳", st[1][3], "学院意见", "周建华", st[2][3])
    return (
        it.get("t_label", "教师意见"), it.get("teacher", ""), it.get("teacher_cm", ""),
        it.get("c_label", "学院意见"), it.get("college_by", ""), it.get("college_cm", ""),
    )


def opinion_card(it):
    t_label, teacher, t_cm, c_label, college, c_cm = node_comments(it)
    if not t_cm and not c_cm:
        return ""
    body = ""
    if c_cm:
        body += '<div class="bold fs13">' + c_label + " · " + college + "</div>"
        body += '<div class="mt8" style="font-size:15px;font-weight:600;line-height:1.65;color:#333">' + c_cm + "</div>"
    if t_cm:
        body += '<div class="mt8 sub13">' + t_label + " · " + teacher + "：" + t_cm + "</div>"
    return '<div class="m-card" style="border-left:3px solid var(--c-success)">' + body + "</div>"


def change_reason(it):
    if it["key"] == "cs-stu":
        return FLOWS["rename"]["steps"][0][3]
    return it.get("reason", "")


def new_name_of(it):
    if it["key"] == "cs-stu":
        return ACCOUNTS["rename"]["new_name"]
    return it.get("new_name", "")


def simple(**kw):
    kw.setdefault("student", kw.get("who", ""))
    kw.setdefault("org_type", "院级学生组织")
    kw.setdefault("level", "二级平台")
    return kw


def three(submit_who, submit_at, teacher, t_at, t_cm, college, c_at, c_cm, submit_title="提交申请"):
    t_title = "指导教师审核通过"
    c_title = "学院团委审核通过"
    return [
        (submit_at, submit_who, submit_title, ""),
        (t_at, teacher, t_title, t_cm),
        (c_at, college, c_title, c_cm),
    ]


def build_todo_items():
    new = ACCOUNTS["new"]
    ren = ACCOUNTS["rename"]
    zb = ACCOUNTS["zombie"]
    vol = ACCOUNTS["rectify"]
    return [
        simple(key="cs-new", kind="new", flow_key="new", flow_n=5, name=new["name"], platform=new["platform"],
               pid=new["pid"], no=FLOWS["new"]["no"], who="李明", student="李明", college="计算机学院", org=new["org"],
               org_type=new["org_type"], level=new["level"], teacher="王晓琳", arrive="2026-09-28 16:40",
               note="已按退回意见补充平台介绍（326 字）"),
        simple(key="bs-youth", kind="new", name="商学院青年", platform="微信公众号", pid="csu_bs_youth",
               no="XJ20260925004", who="林嘉怡", college="商学院", org="商学院团委", teacher="杨帆",
               college_by="商学院团委", arrive="2026-09-28 10:20", note="学院已审核，待校团委终审",
               teacher_cm="栏目、信息发布范围和四项机制已写明，同意备案。", college_cm="材料齐全，报校团委终审。",
               intro="商学院团委面向本院学生的思想引领与学业服务账号，发布团学动态与招聘实习信息。",
               steps=three("林嘉怡", "2026-09-25 14:36", "杨帆", "2026-09-26 11:05",
                           "栏目、信息发布范围和四项机制已写明，同意备案。", "商学院团委", "2026-09-28 10:20",
                           "材料齐全，报校团委终审。")),
        simple(key="xy-stu", kind="new", name="湘雅医学生", platform="微信公众号", pid="csu_xy_stu",
               no="XJ20260926011", who="许哲", college="湘雅医学院", org="湘雅医学院学生会", teacher="郑敏",
               college_by="湘雅医学院团委", arrive="2026-09-29 09:12", note="学院已审核，待校团委终审",
               teacher_cm="医学科普栏目与三审制度已说明，同意备案。", college_cm="同意，报校团委终审。",
               intro="湘雅医学院学生会官方公众号，发布院内团学活动、志愿服务与健康科普。",
               steps=three("许哲", "2026-09-26 09:48", "郑敏", "2026-09-27 15:20",
                           "医学科普栏目与三审制度已说明，同意备案。", "湘雅医学院团委", "2026-09-29 09:12",
                           "同意，报校团委终审。")),
        simple(key="law-court", kind="new", name="法学院模拟法庭", platform="微信公众号", pid="csu_law_court",
               no="XJ20260927002", who="孟婧", college="法学院", org="法学院模拟法庭", teacher="指导教师",
               college_by="法学院团委", arrive="2026-09-29 15:36", note="学院已审核，待校团委终审",
               t_label="教师意见", teacher_cm="活动记录与信息发布范围已补充，同意备案。",
               college_cm="同意，报校团委终审。",
               intro="法学院模拟法庭学生组织的公众号，发布模拟法庭活动与法学实践通知。",
               steps=three("孟婧", "2026-09-27 16:20", "指导教师", "2026-09-28 10:40",
                           "活动记录与信息发布范围已补充，同意备案。", "法学院团委", "2026-09-29 15:36",
                           "同意，报校团委终审。")),
        simple(key="ls-wy", kind="new", name="麓山文苑", platform="微信公众号", pid="csu_ls_wy",
               no="XJ20260928006", who="苏晴", college="文学院", org="麓山文苑", teacher="指导教师",
               college_by="文学院团委", arrive="2026-09-30 08:45", note="学院已审核，待校团委终审",
               teacher_cm="文学栏目定位清楚，同意备案。", college_cm="同意，报校团委终审。",
               intro="文学院学生文学社团的公众号，发布作品、读书会与征文通知。",
               steps=three("苏晴", "2026-09-28 11:02", "指导教师", "2026-09-29 09:18",
                           "文学栏目定位清楚，同意备案。", "文学院团委", "2026-09-30 08:45", "同意，报校团委终审。")),
        simple(key="cs-stu", kind="change", flow_key="rename", flow_n=3, name=ren["name"], platform=ren["platform"],
               pid=ren["pid"], no=FLOWS["rename"]["no"], who="李明", student="李明", college="计算机学院",
               org=ren["org"], org_type=ren["org_type"], level=ren["level"], teacher="王晓琳",
               arrive="2026-09-29 15:20", note="拟更名，属重要变更"),
        simple(key="jd-youth", kind="change", name="机电青年", platform="微信公众号", pid="csu_jd_youth",
               no="BG20260927008", who="邓子豪", college="机电工程学院", org="机电学院团委", teacher="罗志强",
               college_by="机电学院团委", arrive="2026-09-29 11:30", new_name="中南机电青年",
               note="拟更名为中南机电青年", reason="统一学院新媒体品牌名称。",
               teacher_cm="名称符合命名规范，同意变更。", college_cm="属重要变更，报校团委审核。",
               steps=three("邓子豪", "2026-09-27 10:15", "罗志强", "2026-09-28 09:40",
                           "名称符合命名规范，同意变更。", "机电学院团委", "2026-09-29 11:30",
                           "属重要变更，报校团委审核。", "提交名称变更")),
        simple(key="fl-voice", kind="change", name="外院之声", platform="微博", pid="csu_fl_voice",
               no="BG20260928012", who="韩雪", college="外国语学院", org="外国语学院学生会", teacher="指导教师",
               college_by="外国语学院团委", arrive="2026-09-30 09:05", new_name="中南外院之声",
               note="拟更名为中南外院之声", reason="原名称与备案名称不一致，申请更名。",
               teacher_cm="更名理由清楚，同意报学校。", college_cm="属重要变更，报校团委审核。",
               steps=three("韩雪", "2026-09-28 15:40", "指导教师", "2026-09-29 16:10",
                           "更名理由清楚，同意报学校。", "外国语学院团委", "2026-09-30 09:05",
                           "属重要变更，报校团委审核。", "提交名称变更")),
        simple(key="mk2202", kind="cancel", name="2022级市场营销2班团支部", platform="微信公众号", pid="csu_mk2202",
               no="ZX20260923006", who="王一帆", student="王一帆（已毕业）", college="商学院",
               org="2022级市场营销2班团支部", org_type="班级团支部", level="三级平台", teacher="陈立新",
               college_by="杨帆", arrive="2026-09-23 18:22", note="团支部毕业，申请注销",
               reason="团支部毕业", intro="2022级市场营销2班已于 2026 年 6 月整体毕业，无学生继续运营。",
               files=["2026届毕业班级名单.pdf", "团支部撤销说明.pdf"],
               teacher_cm="情况属实，已核对毕业名单。", college_cm="团支部已毕业，同意注销。",
               t_label="教师意见",
               steps=[
                   ("2026-09-23 18:22", "王一帆", "学生提交注销申请", "班级已于 2026 年 6 月毕业，申请注销团支部公众号。"),
                   ("2026-09-24 10:40", "陈立新", "指导教师审核通过", "情况属实，已核对毕业名单。"),
                   ("2026-09-27 17:05", "杨帆", "学院团委审核通过", "团支部已毕业，同意注销。"),
               ]),
        simple(key="za-youth", kind="cancel", name="资安青年说", platform="微信公众号", pid="csu_za_youth",
               no="ZX20260925010", who="卢俊", college="资源与安全工程学院", org="资安青年说", teacher="指导教师",
               college_by="资源与安全工程学院团委", arrive="2026-09-25 20:10", note="社团停止运行，申请注销",
               reason="社团停止运行", intro="组织已停止活动，账号无人运营，申请注销并保留档案。",
               teacher_cm="已核实组织停摆，同意注销。", college_cm="同意注销，报校团委。",
               steps=three("卢俊", "2026-09-24 16:00", "指导教师", "2026-09-25 09:30",
                           "已核实组织停摆，同意注销。", "资源与安全工程学院团委", "2026-09-25 20:10",
                           "同意注销，报校团委。", "提交注销申请")),
        simple(key="se2101", kind="zombie", flow_key="zombie", flow_n=3, name=zb["name"], platform=zb["platform"],
               pid=zb["pid"], no=FLOWS["zombie"]["no"], who="系统预警", student=zb["student"], college="计算机学院",
               org=zb["org"], org_type=zb["org_type"], level=zb["level"], teacher=zb["teacher"],
               arrive="2026-09-29 10:10", note="停更 412 天，学院已转注销",
               idle="412 天", last=zb["last_post"], rules="停更 ≥ 180 天；团支部已毕业",
               files=["团支部毕业证明.pdf", "2021级软件工程1班毕业名单.xlsx"]),
        simple(key="cs-vol", kind="annual", name=vol["name"], platform=vol["platform"], pid=vol["pid"],
               no="NS2026-CS-0027", who="何雨桐", student="何雨桐", college="计算机学院", org=vol["org"],
               org_type=vol["org_type"], level=vol["level"], teacher="王晓琳", college_by="周建华",
               arrive="2026-09-29 17:00", note="整改闭环后随学院提交，需单独校审",
               teacher_cm="未提交信息发布审查制度，要求整改。",
               college_cm="整改通过，年审恢复流转。学院已统一提交校团委。",
               steps=[
                   ("2026-09-17 20:30", "何雨桐", "学生填报", "确认账号仍在运营。"),
                   ("2026-09-19 16:00", "王晓琳", "指导教师审核：要求整改", "未提交信息发布审查制度，要求整改。"),
                   ("2026-09-28 09:40", "周建华", "学院团委审核通过", "整改通过，年审恢复流转。"),
                   ("2026-09-29 17:00", "周建华", "学院统一提交校团委", "计算机学院 36 个账号全部完成。"),
               ]),
        simple(key="jd-maker", kind="rectify", name="机电创客空间", platform="哔哩哔哩", pid="402218876",
               no="ZG20260915003", who="邓子豪", student="邓子豪", college="机电工程学院",
               org="机电学院大学生创新协会", level="二级平台", teacher="罗志强", college_by="罗志强",
               arrive="2026-09-28 15:30", note="账号无法访问，第 1 轮材料已提交",
               problem="账号无法正常访问", deadline="2026-10-15", round="第 1 轮",
               files=["学院申诉公函.pdf", "账号异常原因说明.docx"],
               t_label="整改提交", teacher_cm="已完成实名申诉并恢复账号，补发 3 条内容。",
               college_cm="账号已恢复访问，报校团委复核。",
               steps=[
                   ("2026-09-15 10:20", "陈静", "校团委下发整改任务", "账号主页无法访问，请于 10 月 15 日前恢复并说明原因。"),
                   ("2026-09-15 16:40", "罗志强", "学院转发并指定责任人", "请邓子豪同学限期处理。"),
                   ("2026-09-27 21:30", "邓子豪", "第 1 次提交整改材料", "已完成实名申诉并恢复账号，补发 3 条内容。"),
                   ("2026-09-28 09:15", "罗志强", "学院初审通过", "账号已恢复访问，报校团委复核。"),
               ]),
    ]


def build_mat20():
    return simple(
        key="mat20", kind="zombie", name="2020级材料2班团支部", platform="微信公众号", pid="csu_mat2002",
        no="ZX20260918009", who="系统预警", student="—（已毕业）", college="材料科学与工程学院",
        org="2020级材料2班团支部", org_type="班级团支部", level="三级平台", teacher="指导教师",
        college_by="材料学院团委", arrive="2026-09-28 11:20", note="停更 391 天，学院建议注销",
        idle="391 天", last="2025-09-04", rules="停更 ≥ 365 天；团支部已毕业",
        teacher_cm="团支部已毕业，建议注销。", college_cm="同意注销，报校团委确认。", t_label="核实意见",
        steps=three("系统", "2026-09-18 02:00", "指导教师", "2026-09-26 15:10",
                    "团支部已毕业，建议注销。", "材料学院团委", "2026-09-28 11:20",
                    "同意注销，报校团委确认。", "系统自动预警"),
    )


TODO_ITEMS = build_todo_items()
MAT20 = build_mat20()


def all_review_items():
    return TODO_ITEMS + [MAT20]


def kind_count(kind):
    return sum(1 for it in TODO_ITEMS if it["kind"] == kind)


def extra_accounts():
    def ex(key, name, platform, pid, college, org, level, org_type, teacher, student, run, filing, annual, last, cat, note=""):
        return dict(key=key, name=name, platform=platform, pid=pid, college=college, org=org, level=level,
                    org_type=org_type, teacher=teacher, student=student, run=run, filing=filing, annual=annual,
                    last=last, cat=cat, note=note)

    blank = "—"
    return [
        ex("bs-youth", "商学院青年", "微信公众号", "csu_bs_youth", "商学院", "商学院团委", "二级平台", "院级学生组织",
           "杨帆", "林嘉怡", blank, "备案申请中", blank, blank, "l2", "新建备案待校团委终审"),
        ex("xy-stu", "湘雅医学生", "微信公众号", "csu_xy_stu", "湘雅医学院", "湘雅医学院学生会", "二级平台", "院级学生组织",
           "郑敏", "许哲", blank, "备案申请中", blank, blank, "l2", "新建备案待校团委终审"),
        ex("law-court", "法学院模拟法庭", "微信公众号", "csu_law_court", "法学院", "法学院模拟法庭", "二级平台", "院级学生组织",
           "指导教师", "孟婧", blank, "备案申请中", blank, blank, "l2", "新建备案待校团委终审"),
        ex("ls-wy", "麓山文苑", "微信公众号", "csu_ls_wy", "文学院", "麓山文苑", "二级平台", "院级学生组织",
           "指导教师", "苏晴", blank, "备案申请中", blank, blank, "l2", "新建备案待校团委终审"),
        ex("jd-youth", "机电青年", "微信公众号", "csu_jd_youth", "机电工程学院", "机电学院团委", "二级平台", "院级学生组织",
           "罗志强", "邓子豪", "正常运行", "变更申请中", blank, "2026-09-20", "l2", "重要变更待校团委审核"),
        ex("fl-voice", "外院之声", "微博", "csu_fl_voice", "外国语学院", "外国语学院学生会", "二级平台", "院级学生组织",
           "指导教师", "韩雪", "正常运行", "变更申请中", blank, "2026-09-18", "l2", "重要变更待校团委审核"),
        ex("mk2202", "2022级市场营销2班团支部", "微信公众号", "csu_mk2202", "商学院", "2022级市场营销2班团支部", "三级平台", "班级团支部",
           "陈立新", "王一帆（已毕业）", "申请注销", "注销申请中", blank, "2026-06-20", "l3", "团支部毕业，待校团委审核注销"),
        ex("za-youth", "资安青年说", "微信公众号", "csu_za_youth", "资源与安全工程学院", "资安青年说", "二级平台", "院级学生组织",
           "指导教师", "卢俊", "申请注销", "注销申请中", blank, "2026-04-02", "l2", "社团停止运行，待校团委审核注销"),
        ex("mat20", "2020级材料2班团支部", "微信公众号", "csu_mat2002", "材料科学与工程学院", "2020级材料2班团支部", "三级平台", "班级团支部",
           "指导教师", "—（已毕业）", "不活跃", "已备案", "待填报", "2025-09-04", "l3 zombie", "停更 391 天，待校团委确认注销"),
        ex("xy-health", "湘雅健康说", "小红书", "csu_xy_health", "湘雅医学院", "湘雅健康说", "社团平台", "社团组织",
           "—（空）", "—（空）", "不活跃", "已备案", "待填报", "—", "club zombie", "最近发布为空，待教师核实"),
        ex("chem", "化院科创", "微博", "csu_chem_id", "化学化工学院", "化学化工学院团委", "二级平台", "院级学生组织",
           "指导教师", "学生负责人", "正常运行", "已备案", "待学院审核", "2026-06-26", "l2", "疑似与学院团委重复备案"),
        ex("law-debate", "法学院辩论队", "抖音", "csu_law_debate", "法学院", "法学院辩论队", "社团平台", "社团组织",
           "指导教师", "—（已注销）", "已注销", "已注销", "本年度注销", "2025-08-23", "club", "已处置并注销，档案保留"),
        ex("fl-jp", "外国语学院日语角", "QQ", "csu_fl_jp", "外国语学院", "外国语学院日语角", "社团平台", "社团组织",
           "指导教师", "—（已注销）", "已注销", "已注销", "本年度注销", "2026-02-02", "club", "组织已撤销，账号已注销"),
        ex("jt-youth", "交通学院青年", "视频号", "csu_jt_youth", "交通运输工程学院", "交通学院团委", "二级平台", "院级学生组织",
           "指导教师", "学生负责人", "正常运行", "已备案", "待填报", "2026-03-26", "l2", "已核实正常，预警已解除"),
    ]


def archives():
    if getattr(archives, "cache", None):
        return archives.cache
    if len(ACCT_KEYS) != len(ACCT_LIST):
        raise RuntimeError("账号键与全校账号示例行数不一致")
    notes = {it["key"]: it.get("note", "") for it in all_review_items()}
    recs = []
    for key, row in zip(ACCT_KEYS, ACCT_LIST):
        n, p, pid, col, org, lv, tch, stu, run, fil, ann, last, cat = row
        recs.append(dict(key=key, name=n, platform=p, pid=pid, college=col, org=org, level=lv, org_type="",
                         teacher=tch, student=stu, run=run, filing=fil, annual=ann, last=last, cat=cat,
                         note=notes.get(key, "")))
    have = {r["key"] for r in recs}
    for row in extra_accounts():
        if row["key"] not in have:
            recs.append(row)
    archives.cache = recs
    return recs


def arch_map():
    return {a["key"]: a for a in archives()}


def show_status(v):
    if not v or v == "—":
        return ""
    return st(v)


def known_by_pid(pid):
    for acc in ACCOUNTS.values():
        if acc.get("pid") == pid:
            return acc
    return None


def apply_block(it, extra_rows=(), lead=""):
    pairs = [
        ("申请编号", it["no"]), ("申请人", it["who"]), ("所属学院", it["college"]), ("所属组织", it["org"]),
        ("组织类别", it.get("org_type") or "—"), ("平台层级", it["level"]), ("平台类型", it["platform"]),
        ("平台 ID", it["pid"]), ("管理教师", it["teacher"]), ("学生负责人", it.get("student") or it["who"]),
        ("到达时间", it["arrive"]),
    ]
    pairs.extend(extra_rows)
    return lead + sec("申请内容", rows(pairs)) + opinion_card(it)


def body_of(it):
    lead = ""
    extra = []
    if it["kind"] == "change":
        old, new = it["name"], new_name_of(it)
        lead = (
            '<div class="m-card"><div class="sec-t">变更对比</div>'
            '<div class="cmp old"><div class="small">变更前 · 账号名称</div><div class="v">' + old + "</div></div>"
            '<div class="cmp-arrow"><span class="arrow-c" style="transform:rotate(90deg)">' + icon("arrow-right") + "</span></div>"
            '<div class="cmp new"><div class="small">变更后 · 账号名称</div><div class="v">' + new + "</div></div>"
            '<div class="intro">' + change_reason(it) + "</div></div>"
        )
    elif it["kind"] == "cancel":
        extra = [("注销原因", it.get("reason", "")), ("原因说明", it.get("intro", ""))]
    elif it["kind"] == "zombie":
        extra = [("停更天数", it.get("idle", "")), ("最近发布", it.get("last", "")), ("命中规则", it.get("rules", ""))]
    elif it["kind"] == "rectify":
        extra = [("整改问题", it.get("problem", "")), ("整改轮次", it.get("round", "")), ("截止时间", it.get("deadline", ""))]
    block = apply_block(it, extra, lead)
    if it.get("files"):
        block += '<div class="upload-list">' + filechips(it["files"]) + "</div>"
    if it["key"] == "cs-new":
        block += alert("未发现同平台同 ID。相似名称“中南计科青年”（抖音，已注销）已由申请人确认为不同账号。", "success")
        block += fold("intro-cs-new", "平台介绍（326 字）", '<div class="intro">' + INTRO + "</div>", True)
        block += fold("mech-cs-new", "平台信息确认", mechanism_blocks(), False)
        block += '<div class="upload-list">' + filechips(["四项机制制度文件.pdf", "账号主页截图.png", "信息发布三审制度.pdf"]) + "</div>"
    elif it["kind"] == "new" and it.get("intro"):
        block += '<div class="intro">' + it["intro"] + "</div>"
    if it["kind"] == "change":
        block += alert("名称变更属于重要变更。通过后原名称记入曾用名，历史记录仍在同一档案。", "info")
    if it["kind"] == "cancel":
        block += alert("注销后档案、负责人、年审和日志永久保留，不做删除。", "warning")
    return block


def case_html(it, hidden):
    label, kind = KIND_TAG[it["kind"]]
    names, cur = STEPS[it["kind"]]
    now_title, now_meta = now_of(it)
    cls = "hidden" if hidden else ""
    return (
        '<div data-case="' + it["key"] + '" class="' + cls + '" '
        'data-pass="review-result.html?c=' + it["key"] + '-pass" '
        'data-back="review-result.html?c=' + it["key"] + '-back" '
        'data-reject="review-result.html?c=' + it["key"] + '-reject">'
        + head(it["name"], it["platform"], it["no"] + " · " + it["who"], tag(label, kind) + tag("待您审核", "warning"))
        + m_steps(names, cur)
        + body_of(it)
        + sec("审批记录", past_now(item_steps(it), now_title, now_meta))
        + opinion(OPINION[it["kind"]], "审核意见", "请输入审核意见（选填）")
        + "</div>"
    )


def dlg(id_, title, desc, ok, act, href, toast, danger=True):
    ok_cls = "ok danger" if danger else "ok"
    return (
        '<div class="m-dialog-mask hidden" id="' + id_ + '"><div class="m-dialog" data-form>'
        '<div class="dlg-hd">' + title + '</div><div class="dlg-bd">' + desc
        + '<div class="cell col-cell"><textarea class="m-textarea" placeholder="请填写原因（必填）" required></textarea>'
        '<div class="err-msg">请填写原因</div></div></div>'
        '<div class="dlg-ft"><button type="button" data-toggle="#' + id_ + '">取消</button>'
        '<button type="button" class="' + ok_cls + '" data-act="' + act + '" data-submit="' + href
        + '" data-toast="' + esc(toast) + '">' + ok + "</button></div></div></div>"
    )


def pass_btn(href, toast):
    return ('<button class="btn btn-primary wide" type="button" data-act="pass" data-href="' + href
            + '" data-toast="' + esc(toast) + '">' + icon("check") + "通过</button>")


def review_items(kind):
    rows = [it for it in TODO_ITEMS if it["kind"] == kind]
    if kind == "zombie":
        rows = rows + [MAT20]
    return rows


def emit_review(kind):
    rows = review_items(kind)
    cases = "".join(case_html(it, i > 0) for i, it in enumerate(rows))
    first = rows[0]["key"]
    bottom = (toggle_btn("驳回", "#dlg-reject", "danger", "x", cls="slim")
              + toggle_btn("退回", "#dlg-return", "warning", "undo", cls="slim")
              + pass_btn("review-result.html?c=" + first + "-pass", PASS_TOAST[kind]))
    overlay = (dlg("dlg-reject", "确认驳回？", "驳回后不予办理，流程终止，并通知申请人。", "确认驳回", "reject",
                   "review-result.html?c=" + first + "-reject", "已驳回，已通知申请人", True)
               + dlg("dlg-return", "退回修改", "退回后由申请人修改并重新逐级审核，原审批记录保留。", "确认退回", "back",
                     "review-result.html?c=" + first + "-back", "已退回，已通知申请人", False))
    label = KIND_TAG[kind][0]
    page_s(REVIEW_PAGE[kind], REVIEW_TITLE[kind], cases,
           ["查看申请内容和审批记录后，可以通过、退回或驳回",
            "退回、驳回必须填写原因；通过时可修改预填的审核意见",
            "手机上只处理当前这一条，不在这里做批量审批或流程配置",
            label + "共 " + str(len(rows)) + " 条，切换待办会打开对应申请"],
           [("提交后的结果", "review-result.html?c=" + first + "-pass"),
            ("返回待审", "todo.html"),
            ("PC 端办理此业务", PC_REVIEW[kind]),
            ("批量审批（PC）", "../../pc/school/wf-batch.html")],
           back="todo.html", bottom=bottom, overlay=overlay, js=CASE_JS)


def result_links(it, action):
    return [("只读档案", "archive.html?c=" + it["key"]), ("继续审核", "todo.html")]


def result_case(it, action, hidden):
    icon_name = {"pass": "check", "back": "undo", "reject": "x"}[action]
    box = {"pass": "ok", "back": "warn", "reject": "err"}[action]
    title = {"pass": "审核完成", "back": "已退回", "reject": "已驳回"}[action]
    if action == "pass":
        result = '<span class="c-success bold">' + PASS_NAME[it["kind"]] + "</span>"
        opinion_row = ("审核意见", OPINION[it["kind"]])
    elif action == "back":
        result = '<span class="c-warning bold">已退回</span>'
        opinion_row = ("说明", "已按填写的原因通知申请人，原审批记录保留。")
    else:
        result = '<span class="c-danger bold">已驳回</span>'
        opinion_row = ("说明", "流程已终止，已通知申请人。")
    cls = ' class="hidden"' if hidden else ""
    lk = "".join(
        '<a class="cell" href="' + h + '"><span class="cell-label fs13 c-primary">' + t + '</span><span class="cell-value"></span>'
        + icon("chevron-right", cls="arrow") + "</a>"
        for t, h in result_links(it, action)
    )
    return (
        '<div data-case="' + it["key"] + "-" + action + '"' + cls + '>'
        '<div class="result" style="padding:28px 8px 8px"><div class="result-ic ' + box + '">' + icon(icon_name) + "</div>"
        "<h2>" + title + '</h2><p class="fs13">' + EFFECT[it["kind"]][action] + "</p></div>"
        '<div class="m-card res-card">' + rows([
            ("账号", it["name"]), ("编号", it["no"]), ("处理结果", result), opinion_row,
        ]) + "</div><div class=\"m-group\">" + lk + "</div></div>"
    )


def home():
    me = PEOPLE["陈静"]
    n_todo = len(TODO_ITEMS)
    n_msg = sum(1 for m in MSGS if m[1])
    quick = "".join(
        '<a href="' + h + '"><span class="qi ' + c + '">' + icon(ic) + badge(n) + "</span>" + t + "</a>"
        for t, ic, c, n, h in [
            ("全校账号", "database", "", 0, "accounts.html"),
            ("组织", "hierarchy", "green", 0, "organizations.html"),
            ("年审节点", "calendar", "", 0, "annual.html"),
            ("僵尸号", "ghost", "red", 0, "zombie.html"),
            ("整改复核", "wrench", "orange", kind_count("rectify"), "review-rectify.html"),
        ])
    urgent = "".join([
        list_item("review-new.html?c=cs-new", "file-add", "", "中南计算机青年 · 新建备案", "学院已通过 · 到达 09-28", tag("待终审", "warning")),
        list_item("review-change.html?c=cs-stu", "file-edit", "orange", "计算机学院学生会 · 名称变更", "拟更名为中南计院学生会", tag("重要变更", "warning")),
        list_item("review-zombie.html?c=se2101", "ghost", "red", "2021级软件工程1班团支部", "停更 412 天 · 学院建议注销", tag("待确认", "danger")),
        list_item("review-annual.html?c=cs-vol", "calendar", "", "计院青年志愿者 · 年审校审", "整改闭环后单独审核", tag("待校审", "primary")),
    ])
    content = f"""
<div class="m-hero">
  <div class="flex gap12" style="position:relative;z-index:1">{avatar("陈静", "lg")}
    <div class="grow"><div class="fs18 bold">陈老师，下午好</div><div class="small" style="opacity:.85">{me["org"]} · {me["job"]}</div></div>
    <a href="messages.html" style="position:relative" aria-label="消息">{icon("bell", 22)}<span class="badge" style="position:absolute;top:-6px;right:-8px">{n_msg}</span></a>
  </div>
  <div class="hero-stats">
    <a href="todo.html"><b>{n_todo}</b><span>待审</span></a>
    <a href="accounts.html"><b>{S["total"]}</b><span>全校账号</span></a>
    <a href="annual.html"><b>{len(ANNUAL_NODES)}</b><span>年审节点</span></a>
    <a href="zombie.html"><b>{S["zombie"]}</b><span>僵尸号</span></a>
  </div>
</div>
<div class="alert alert-warning mt12">{icon("clock")}<div class="grow"><b>{T["name"]}</b>正在进行，学生填报截止 <b>{T["stu_end"]}</b>。创建或调整任务请在 PC 端办理。</div></div>
<div class="m-card mt12"><div class="sec-t">常用功能</div><div class="quick pack5">{quick}</div></div>
<div class="m-title">待我终审<a href="todo.html">全部{icon("chevron-right", 14)}</a></div>
<div class="m-card" style="padding:4px 14px">{urgent}</div>"""
    page_s("home.html", "首页", content, tab="home", nav_title="学校管理",
           notes=["陈静，校团委宣传部。四个数字可点进待审、账号、年审节点和僵尸号列表",
                  "待审 " + str(n_todo) + " 条为校级终审：新建、重要变更、注销、僵尸号确认、年审校审、整改复核",
                  "全校在册 " + str(S["total"]) + " 个账号，疑似僵尸号 " + str(S["zombie"]) + " 个，年审节点 " + str(len(ANNUAL_NODES)) + " 个",
                  "手机上只做终审和基础信息查看，不办理批量审批、导入导出、权限和系统配置"],
           flow=[("待审列表", "todo.html"), ("新建备案终审", "review-new.html"), ("全校账号", "accounts.html"),
                 ("年审节点", "annual.html"), ("僵尸号", "zombie.html"), ("PC 数据驾驶舱", "../../pc/school/dashboard.html")])


def todo():
    cards = []
    for it in TODO_ITEMS:
        label, tk = KIND_TAG[it["kind"]]
        foot = tag("待确认", "danger") if it["kind"] == "zombie" else tag("待终审", "warning")
        cards.append(todo_card(
            it["kind"], REVIEW_PAGE[it["kind"]] + "?c=" + it["key"], it["name"], it["platform"], tag(label, tk),
            [it["no"], it["who"] + " · 到达 " + it["arrive"]], it["note"], foot,
        ))
    chips_html = chips([
        ("全部 " + str(len(TODO_ITEMS)), "all"),
        ("新建 " + str(kind_count("new")), "new"),
        ("变更 " + str(kind_count("change")), "change"),
        ("注销 " + str(kind_count("cancel")), "cancel"),
        ("僵尸号 " + str(kind_count("zombie")), "zombie"),
        ("年审 " + str(kind_count("annual")), "annual"),
        ("整改 " + str(kind_count("rectify")), "rectify"),
    ], target="#todo-list").replace('class="chips"', 'class="chips scroll-x"', 1)
    content = f"""
{chips_html}
<div id="todo-list">{"".join(cards)}</div>
<div class="small" style="text-align:center;color:#666;padding:4px 0 8px">共 {len(TODO_ITEMS)} 条校级终审 · 按到达时间查看</div>"""
    page_s("todo.html", "待审", content, tab="todo", nav_title="待审",
           notes=["覆盖学校终审：新建备案 5、重要变更 3、注销 2、僵尸号确认 1、年审校审 1、整改复核 1",
                  "点进事项可看申请内容和审批记录，并可通过、退回、驳回",
                  "手机上逐条终审，不在这里做批量审批或流程配置",
                  "年审无异动批量通过不在手机上操作"],
           flow=[("新建备案", "review-new.html"), ("重要变更", "review-change.html"), ("注销", "review-cancel.html"),
                 ("僵尸号确认", "review-zombie.html"), ("年审校审", "review-annual.html"), ("整改复核", "review-rectify.html"),
                 ("批量审批（PC）", "../../pc/school/wf-batch.html")])


MSGS = [
    ("audit", True, "file-add", "", "新建备案待校级终审", "中南计算机青年已由学院审核通过，请终审。", "2026-09-28 16:40", "review-new.html?c=cs-new"),
    ("audit", True, "file-edit", "orange", "名称变更待校级审核", "计算机学院学生会拟更名为中南计院学生会，属重要变更。", "2026-09-29 15:20", "review-change.html?c=cs-stu"),
    ("audit", True, "ban", "red", "账号注销待校级审核", "2022级市场营销2班团支部因毕业申请注销。", "2026-09-27 17:05", "review-cancel.html?c=mk2202"),
    ("audit", True, "calendar", "green", "计算机学院已提交年审", "无异动批量通过请在 PC 端；计院青年志愿者需单独校审。", "2026-09-29 17:00", "review-annual.html?c=cs-vol"),
    ("handle", True, "ghost", "red", "僵尸号待校团委确认", "2021级软件工程1班团支部停更 412 天，学院建议注销。", "2026-09-29 10:10", "review-zombie.html?c=se2101"),
    ("handle", True, "wrench", "orange", "整改待校团委复核", "机电创客空间已恢复访问，请复核整改材料。", "2026-09-28 15:30", "review-rectify.html?c=jd-maker"),
    ("sys", False, "clock", "", "年审节点提醒", "学生填报将于 10 月 15 日截止，可查看 7 个时间节点。", "2026-09-30 08:00", "annual.html"),
    ("sys", False, "ghost", "red", "风险扫描完成", "累计疑似僵尸号 47 个，可查看清单。", "2026-09-29 02:00", "zombie.html"),
]


def messages():
    cat_name = {"audit": "待审核", "handle": "待处置", "sys": "系统通知"}
    items = "".join(
        '<a class="m-card flex gap12 top-align" href="' + h + '" data-cat="' + c + '">'
        '<span class="stat-ic ' + col + '" style="width:38px;height:38px;border-radius:11px">' + icon(ic, 20) + "</span>"
        '<div class="grow" style="min-width:0"><div class="flex gap6"><span class="msg-dot' + ("" if unread else " read") + '"></span>'
        '<span class="bold fs13 grow ellipsis">' + t + "</span></div>"
        '<div class="small sub mt4">' + d + '</div><div class="small" style="color:#666;margin-top:4px">' + cat_name[c] + " · " + w + "</div></div></a>"
        for c, unread, ic, col, t, d, w, h in MSGS
    )
    counts = {k: sum(1 for x in MSGS if x[0] == k) for k in cat_name}
    unread_n = sum(1 for x in MSGS if x[1])
    content = f"""
{chips([("全部 " + str(len(MSGS)), "all"), ("待审核 " + str(counts["audit"]), "audit"), ("待处置 " + str(counts["handle"]), "handle"), ("系统通知 " + str(counts["sys"]), "sys")], target="#msg-list")}
<div id="msg-list" class="mt12">{items}</div>
<div class="small" style="text-align:center;color:#666">未读 {unread_n} 条 · 点进消息即可办理或查看</div>"""
    page_s("messages.html", "消息", content, tab="messages", nav_title="消息",
           right='<button type="button" data-toast="已将 ' + str(unread_n) + ' 条未读消息标记为已读">全部已读</button>',
           notes=["消息按待审核、待处置、系统通知筛选，未读带红点",
                  "终审类消息进入对应审核页，可直接通过、退回或驳回",
                  "年审节点提醒和僵尸号扫描进入手机上的查看页",
                  "手机消息不跳转到导入、导出、权限或系统配置"],
           flow=[("新建终审", "review-new.html?c=cs-new"), ("年审校审", "review-annual.html?c=cs-vol"),
                 ("僵尸号确认", "review-zombie.html?c=se2101"), ("整改复核", "review-rectify.html?c=jd-maker")])


def review_result():
    parts = []
    first = True
    for it in all_review_items():
        for action in ("pass", "back", "reject"):
            parts.append(result_case(it, action, not first))
            first = False
    content = "".join(parts) + '<div class="m-card flex between"><span class="sub13">剩余待审</span><a class="bold c-primary" href="todo.html">' + str(len(TODO_ITEMS) - 1) + " 项" + icon("chevron-right", 14) + "</a></div>"
    page_s("review-result.html", "审核结果", content, back="todo.html", js=CASE_JS,
           bottom=btn("回首页", "home.html", "default") + btn("返回待审", "todo.html", "primary", "arrow-right", attrs='style="flex:1.6"'),
           notes=["提交通过、退回或驳回后进入本页，能看到账号、编号和处理结果",
                  "可打开只读档案，或返回待审继续处理其余事项",
                  "年审通过只针对当前账号",
                  "结果页不再提供跳到电脑端的办理入口"],
           flow=[("返回待审", "todo.html"), ("备案表（PC）", "../../pc/school/filing-form.html"),
                 ("只读档案", "archive.html?c=cs-new"), ("回首页", "home.html")])


def accounts():
    recs = archives()

    def ncat(name):
        return sum(1 for a in recs if name in a["cat"].split())

    cards = []
    for a in recs:
        flags = show_status(a["run"]) + show_status(a["filing"]) + show_status(a["annual"])
        if "zombie" in a["cat"].split():
            flags += tag("疑似僵尸号", "danger")
        cards.append(
            '<a class="m-card" href="archive.html?c=' + a["key"] + '" data-cat="' + a["cat"] + '" style="display:block">'
            '<div class="tc-top">' + pf(a["platform"], "sm") + '<div class="grow" style="min-width:0">'
            '<div class="bold ellipsis">' + a["name"] + "</div>"
            '<div class="sub13">' + a["college"] + " · " + a["org"] + "</div>"
            '<div class="sub13">' + a["platform"] + " · " + a["teacher"] + " · " + a["student"] + "</div>"
            '<div class="flex gap6 wrap mt4">' + flags + "</div></div></div></a>"
        )
    chip_html = chips([
        ("全部 " + str(len(recs)), "all"), ("一级 " + str(ncat("l1")), "l1"), ("二级 " + str(ncat("l2")), "l2"),
        ("三级 " + str(ncat("l3")), "l3"), ("社团 " + str(ncat("club")), "club"), ("僵尸号 " + str(ncat("zombie")), "zombie"),
    ], target="#acct-list").replace('class="chips"', 'class="chips scroll-x"', 1)
    content = f"""
{ro("全校在册 <b>" + str(S["total"]) + "</b> 个账号。这里列出重点账号，可搜索后进入只读档案。组合筛选、导入导出请在 PC 端办理。")}
<label class="search-box">{icon("search")}<input placeholder="搜索账号名称、学院、平台或负责人" data-search="#acct-list" aria-label="搜索账号"></label>
{chip_html}
<div id="acct-list">{"".join(cards)}</div>"""
    page_s("accounts.html", "全校账号", content, tab="home", nav_title="全校账号", back="home.html", js=SEARCH_JS,
           notes=["首页“全校账号”进入本页，数字口径为在册 " + str(S["total"]) + " 个",
                  "可按名称、学院、平台、负责人搜索，也可按层级和僵尸号筛选",
                  "点进账号是只读档案，不能在手机上修改或导入",
                  "手机上不提供组合筛选、导入和导出"],
           flow=[("只读档案示例", "archive.html?c=cs-new"), ("PC 全校账号库", "../../pc/school/accounts.html"),
                 ("返回首页", "home.html")])


def archive_case(a, hidden):
    known = known_by_pid(a["pid"])
    rec = dict(a)
    if known:
        for key in ("opened", "fans", "org_type", "change", "last_post", "idle_days"):
            if known.get(key) and not rec.get(key):
                rec[key] = known[key]
    note = a.get("note") or ""
    note_html = '<div class="intro">' + note + "</div>" if note else ""
    flags = show_status(a["run"]) + show_status(a["filing"]) + show_status(a["annual"])
    cls = "hidden" if hidden else ""
    return (
        '<div data-case="' + a["key"] + '" class="' + cls + '">'
        + ro("只读档案。手机上只能查看，不能修改、导入、导出或发起申请。")
        + head(a["name"], a["platform"], a["college"] + " · " + a["org"], flags)
        + note_html
        + render_archive(rec)
        + "</div>"
    )


def archive():
    recs = archives()
    cases = "".join(archive_case(a, i > 0) for i, a in enumerate(recs))
    page_s("archive.html", "账号档案", cases, back="accounts.html", js=CASE_JS, nav_title="只读档案",
           css=ARCHIVE_CSS,
           notes=["只读档案按 PC 账号档案分区展示：基本信息、平台信息、归属、负责人与管理员、年审、变更、整改、操作记录、注销信息",
                  "同一账号使用同一套演示数据；手机上不能修改、导入、导出或发起申请",
                  "顶部说明只提示只读，不代替档案内容",
                  "返回全校账号列表可继续搜索"],
           flow=[("返回账号列表", "accounts.html"), ("PC 全校账号库", "../../pc/school/accounts.html"),
                 ("中南计算机青年", "archive.html?c=cs-new")])


def organizations():
    alive = sum(1 for r in ORG_LIST if r[7] == "alive")
    revoked = sum(1 for r in ORG_LIST if r[7] == "revoked")
    grad = sum(1 for r in ORG_LIST if r[7] == "grad")
    tree = []
    for key, name, cnt in COLLEGE_TREE:
        tree.append('<a class="tree-a" href="org-detail.html?c=' + key + '">' + icon("building", 16) + "<b>" + name + '</b><span class="cnt">' + str(cnt) + " 个账号</span></a>")
        if key == "col-cs":
            subs = []
            for i, row in enumerate(ORG_LIST):
                subs.append('<a class="tree-a" href="org-detail.html?c=org-' + str(i) + '">' + icon("hierarchy", 16) + row[0] + "</a>")
            tree.append('<div class="tree-sub">' + "".join(subs) + "</div>")
    rows_html = []
    for i, row in enumerate(ORG_LIST):
        n, typ, parent, grade, tch, cnt, stv, cat, note = row
        rows_html.append(
            '<a class="todo-item" href="org-detail.html?c=org-' + str(i) + '" data-cat="' + cat + '">'
            '<span class="stat-ic" style="width:36px;height:36px;border-radius:10px">' + icon("hierarchy", 18) + "</span>"
            '<div class="grow" style="min-width:0"><div class="bold fs13 ellipsis">' + n + "</div>"
            '<div class="sub13">' + typ + " · " + parent + " · " + tch + "</div></div>"
            + org_tag(stv) + "</a>"
        )
    chip_html = chips([
        ("全部 " + str(len(ORG_LIST)), "all"), ("存续 " + str(alive), "alive"),
        ("已毕业 " + str(grad), "grad"), ("已撤销 " + str(revoked), "revoked"),
    ], target="#org-list").replace('class="chips"', 'class="chips scroll-x"', 1)
    content = f"""
{ro("组织只读。新增、编辑、撤销和毕业状态请在 PC 端办理。")}
<div class="alert alert-warning mb12">{icon("alert")}<div class="grow">2021级软件工程1班团支部已毕业，名下仍有 1 个账号未注销。<a href="review-zombie.html?c=se2101">去确认</a></div></div>
<div class="m-card" style="padding:6px 14px">{"".join(tree)}</div>
<div class="small" style="color:#666;margin:-4px 2px 10px">以上为 12 个学院的重点节点。其余学院的完整组织树请在 PC 端查看。</div>
<label class="search-box">{icon("search")}<input placeholder="搜索组织名称" data-search="#org-list" aria-label="搜索组织"></label>
{chip_html}
<div class="m-card" id="org-list" style="padding:4px 14px">{"".join(rows_html)}</div>"""
    page_s("organizations.html", "组织", content, tab="home", nav_title="组织", back="home.html",
           notes=["可看学院树和计算机学院重点组织列表，点进去是只读详情",
                  "已毕业团支部若仍有账号，可进入僵尸号确认",
                  "不能在手机上新增、编辑或导入组织",
                  "搜索按组织名称过滤列表"],
           flow=[("组织详情", "org-detail.html?c=org-0"), ("僵尸号确认", "review-zombie.html?c=se2101"),
                 ("PC 组织管理", "../../pc/school/organizations.html")])


def org_tag(stv):
    kind = {"存续": "success", "已撤销": "muted", "已毕业": "warning"}[stv]
    return tag(stv, kind)


def org_detail():
    cases = []
    for i, (key, name, cnt) in enumerate(COLLEGE_TREE):
        q = "校团委" if "校团委" in name else name
        body = (
            ro("只读。不能在手机上新增或编辑组织。")
            + sec("学院概况", rows([("名称", name), ("在册账号", str(cnt) + " 个"), ("维护", "请在 PC 端办理")]))
            + '<div class="m-group">' + cell("查看重点账号", "去列表", "accounts.html?q=" + q) + "</div>"
        )
        cases.append('<div data-case="' + key + '" class="' + ("" if i == 0 else "hidden") + '">' + body + "</div>")
    for i, row in enumerate(ORG_LIST):
        n, typ, parent, grade, tch, cnt, stv, cat, note = row
        pairs = [("组织名称", n), ("组织类别", typ), ("上级组织", parent), ("年级", grade),
                 ("指导教师", tch), ("账号数", str(cnt)), ("存续状态", stv)]
        if note:
            pairs.append(("备注", note))
        body = (
            ro("只读。存续状态的变更请在 PC 端办理。")
            + '<div class="m-card"><div class="flex gap8 wrap">' + org_tag(stv) + '<div class="fs16 bold">' + n + "</div></div>"
            + '<div class="sub13" style="margin-top:6px">' + typ + " · " + parent + "</div></div>"
            + sec("组织信息", rows(pairs))
            + '<div class="m-group">' + cell("查看相关账号", "去列表", "accounts.html?q=" + n) + "</div>"
        )
        cases.append('<div data-case="org-' + str(i) + '" class="hidden">' + body + "</div>")
    page_s("org-detail.html", "组织详情", "".join(cases), back="organizations.html", js=CASE_JS, nav_title="组织详情",
           notes=["学院节点和组织节点都是只读",
                  "可转到重点账号列表按名称搜索",
                  "手机上没有编辑、新增或保存表单"],
           flow=[("返回组织列表", "organizations.html"), ("PC 组织管理", "../../pc/school/organizations.html"),
                 ("相关账号", "accounts.html")])


def annual():
    nodes = []
    for i, (name, date) in enumerate(ANNUAL_NODES):
        state = "done" if i == 0 else ("now" if i == 1 else "")
        if i == 0:
            desc = "已完成。陈静已发布，系统按在册账号生成 " + str(S["total"]) + " 条年审记录。"
        elif i == 1:
            desc = "进行中。学生已填报 674，待填报 312。截止日期 " + date + "。"
        elif i == 4:
            desc = "截止日期 " + date + "。单账号校审可在手机办理，批量通过请在 PC 端。"
        elif i == len(ANNUAL_NODES) - 1:
            desc = "未开始。计划 " + date + " 发布年审结果。"
        else:
            desc = "未到截止日。截止日期 " + date + "。"
        nodes.append(
            '<div class="node-row"><i class="node-dot ' + state + '"></i><div><b>' + name + "</b>"
            '<div class="sub13">' + date + (" · 进行中" if state == "now" else (" · 已完成" if state == "done" else " · 未开始")) + "</div>"
            '<div class="sub13">' + desc + "</div></div></div>"
        )
    counts = []
    for name, num, _color in ANNUAL_COUNTS:
        counts.append('<div class="stat-link"><b>' + str(num) + "</b><small>" + name + "</small></div>")
    content = f"""
{ro("年审节点只读。创建任务、调整节点和批量审核不在手机上办理。")}
<div class="m-card"><div class="sec-t">{T["name"]}</div>
  <div class="sub13">NS2026 · 发布人 陈静 · {T["start"]} · 在册 {S["total"]} 个账号</div>
  <div class="node-list">{"".join(nodes)}</div>
</div>
<div class="m-card"><div class="sec-t">记录分布<span class="ml-auto" style="font-weight:400;font-size:12px;color:#666">只读</span></div>
  <div class="grid g3" style="gap:8px">{"".join(counts)}</div>
</div>
<a class="m-card" href="review-annual.html?c=cs-vol" style="display:block">
  <div class="tc-top">{pf("小红书", "sm")}<div class="grow bold ellipsis">计院青年志愿者 · 待校审</div>{tag("去审核", "primary")}</div>
  <div class="sub13" style="margin-top:8px">整改已经闭环，需单独校审。无异动账号不要在手机上批量通过。</div>
</a>"""
    page_s("annual.html", "年审节点", content, tab="home", nav_title="年审节点", back="home.html",
           notes=["首页“年审节点”进入本页，列出本年度 7 个时间节点及当前进度",
                  "学生填报节点进行中，截止 " + T["stu_end"],
                  "待学校审核的单账号可进入手机校审；批量通过留在 PC",
                  "不能在手机上创建年审任务或修改节点"],
           flow=[("年审校审", "review-annual.html?c=cs-vol"), ("PC 年审任务", "../../pc/school/annual-tasks.html"),
                 ("PC 批量审核", "../../pc/school/annual-review.html"), ("返回首页", "home.html")])


def zombie():
    amap = arch_map()
    cards = []
    for key, meta, status, cat, action in ZOMBIE_ROWS:
        a = amap[key]
        if action == "review":
            act = btn("去审核", "review-zombie.html?c=" + key, "primary", size="sm")
        elif action == "rectify":
            act = btn("去复核", "review-rectify.html?c=" + key, "primary", size="sm")
        elif action == "urge":
            act = (btn("催办", None, "light", "bell", "sm", toast="已向负责教师发送核实催办")
                   + btn("查看档案", "archive.html?c=" + key, "default", size="sm"))
        else:
            act = btn("查看档案", "archive.html?c=" + key, "default", size="sm")
        kind = "danger" if cat == "confirm" else ("success" if cat == "done" else "warning")
        cards.append(
            '<div class="m-card" data-cat="' + cat + '"><div class="tc-top">' + pf(a["platform"], "sm")
            + '<div class="grow" style="min-width:0"><div class="bold ellipsis">' + a["name"] + "</div>"
            '<div class="sub13">' + a["college"] + " · " + meta + "</div></div></div>"
            '<div class="tc-ft"><span>' + tag(status, kind, True) + "</span>" + act + "</div></div>"
        )
    chip_html = chips([
        ("全部 " + str(len(ZOMBIE_ROWS)), "all"), ("待确认", "confirm"), ("核实中", "verify"), ("已处置", "done"),
    ], target="#zb-list").replace('class="chips"', 'class="chips scroll-x"', 1)
    content = f"""
<div class="m-card"><div class="grid g3" style="gap:8px">
  <div class="stat-link"><b class="c-danger">{S["zombie"]}</b><small>疑似僵尸号</small></div>
  <div class="stat-link"><b>5</b><small>待校团委确认</small></div>
  <div class="stat-link"><b>12</b><small>已处置</small></div>
</div></div>
{ro("全校疑似僵尸号 " + str(S["zombie"]) + " 个。手机上可确认已报上来的注销建议；规则配置和全量名单不在手机上修改。系统不自动注销。")}
{chip_html}
<div id="zb-list" class="mt12">{"".join(cards)}</div>"""
    page_s("zombie.html", "僵尸号", content, tab="home", nav_title="僵尸号", back="home.html",
           notes=["首页僵尸号数字进入本页，口径为疑似僵尸号 " + str(S["zombie"]) + " 个",
                  "待校团委确认的账号可以打开审核页，通过即确认注销，也可退回或驳回",
                  "仍在核实的账号可查看档案或催办教师",
                  "风险规则编辑、立即扫描和批量下发留在 PC 端"],
           flow=[("确认 2021 级团支部", "review-zombie.html?c=se2101"), ("只读档案", "archive.html?c=se2101"),
                 ("PC 僵尸号排查", "../../pc/school/zombie.html"), ("返回首页", "home.html")])


ZOMBIE_ROWS = [
    ("se2101", "停更 412 天 · 最近发布 2025-08-14", "待校团委确认", "confirm", "review"),
    ("mat20", "停更 391 天 · 团支部已毕业", "待校团委确认", "confirm", "review"),
    ("photo", "停更 212 天 · 最近发布 2026-03-02", "学生核实中", "verify", "archive"),
    ("civil20", "停更 498 天 · 团支部已毕业", "待教师核实", "verify", "urge"),
    ("wx-shu", "负责人为空", "待教师核实", "verify", "urge"),
    ("jd-maker", "账号无法访问", "整改待复核", "verify", "rectify"),
    ("xy-health", "最近发布为空", "待教师核实", "verify", "urge"),
    ("chem", "疑似重复备案", "学院审核中", "verify", "archive"),
    ("law-debate", "停更超过 365 天", "已处置 · 已注销", "done", "archive"),
    ("fl-jp", "组织已撤销", "已处置 · 已注销", "done", "archive"),
    ("jt-youth", "停更超过 180 天", "已处置 · 核实正常", "done", "archive"),
]


def check_counts():
    rows = TODO["school"]
    if len(rows) != len(TODO_ITEMS):
        raise RuntimeError("移动端待办条数与学校 PC 待办不一致")
    for src, it in zip(rows, TODO_ITEMS):
        if src[0] != it["kind"] or it["no"] not in src[1]:
            raise RuntimeError("待办不一致：" + src[1])
    if len(TODO_ITEMS) != 13:
        raise RuntimeError("待审角标应为 13")
    unread = sum(1 for m in MSGS if m[1])
    if unread != 6:
        raise RuntimeError("消息角标应为 6")
    keys = {a["key"] for a in archives()}
    for it in all_review_items():
        if it["key"] not in keys:
            raise RuntimeError("档案缺少 " + it["key"])
    for key, *_rest in ZOMBIE_ROWS:
        if key not in keys:
            raise RuntimeError("僵尸号清单缺少档案 " + key)
    if len(ANNUAL_NODES) != 7:
        raise RuntimeError("年审节点应为 7 个")


def build():
    check_counts()
    home()
    todo()
    messages()
    for kind in ("new", "change", "cancel", "zombie", "annual", "rectify"):
        emit_review(kind)
    review_result()
    accounts()
    archive()
    organizations()
    org_detail()
    annual()
    zombie()
