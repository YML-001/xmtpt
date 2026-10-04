"""我的待办（统一待办）：待办 / 已办 / 已发起 / 催办/抄送 / 批量审批，三个 PC 角色各一套，表头对齐正式系统。"""
from base import (pc_page, filter_bar, field, inp, sel, table, pager, tag, icon, esc, WF_MENU)
from wf import PROC, TODO, DONE, STARTED, URGE, CC, BATCH

ROLES = ("teacher", "college", "school")
STATUS_KIND = {"已完成": "success", "已提交": "primary", "审批中": "primary", "已终止": "danger", "已退回": "warning", "已撤销": "muted"}
OP_KIND = {"同意": "success", "退回": "warning", "驳回": "danger"}
PROC_NAME = dict(PROC, proxy=PROC["handover"])


def menu_href(role, key):
    return next(h for k, _, _, h, _ in WF_MENU[role] if k == key)


def wf_filter(fields, extra=""):
    bar = filter_bar(fields).replace('class="filter"', 'class="filter wf-filter"', 1)
    return bar.replace("重置</button>", "重置</button>" + extra, 1) if extra else bar


def name_cell(key, sub):
    return f'<div class="wf-name"><span>{PROC_NAME[key]}</span><small>{sub}</small></div>'


def page(role, key, title, content):
    pc_page(f"pc/{role}/{menu_href(role, key)}", role, key, title, [(title, None)], content, module="wf")


def todo_content(role):
    rows = []
    for i, (k, sub, node, who, st_tm, at_tm, href) in enumerate(TODO[role]):
        op = (f'<a class="link" href="{href}">办理</a>' if href else
              '<div class="ops"><button class="link" type="button" data-toast="已审核通过，交接即时生效，已通知新旧负责人与指导教师">通过</button>'
              '<a class="link" href="../school/log-detail.html">详情</a></div>')
        rows.append([str(i + 1), name_cell(k, sub), node, who, st_tm, at_tm, op])
    return (wf_filter([field("流程名称", inp("请输入流程名称")), field("发起人", inp("请输入发起人"))])
            + f'<div class="wf-list">{table(["序号", "流程名称", "当前节点", "发起人", "发起时间", "到达时间", "操作"], rows)}'
            + f'{pager(len(rows), 1)}</div>')


def todo(role):
    page(role, "todo", "待办", todo_content(role))


def done(role):
    rows = []
    for i, (k, sub, node, who, status, op, cm, tm, href) in enumerate(DONE[role]):
        rows.append([str(i + 1), name_cell(k, sub), node, who, tag(status, STATUS_KIND[status]),
                     f'<span class="wf-cm" title="{esc(cm)}">{tag(op, OP_KIND.get(op, "primary"))} {cm}</span>', tm,
                     f'<a class="link" href="{href}">详情</a>'])
    content = (wf_filter([field("流程名称", inp("请输入流程名称")), field("发起人", inp("请输入发起人"))])
               + f'<div class="wf-list">{table(["序号", "流程名称", "节点", "发起人", "流程状态", "意见", "处理时间", "操作"], rows)}'
               + f'{pager(len(rows) + 28, 3)}</div>')
    page(role, "done", "已办", content)


def started(role):
    rows = []
    for i, (k, sub, tm, node, status, href, revocable) in enumerate(STARTED[role]):
        op = f'<a class="link" href="{href}">详情</a>'
        if revocable:
            op += ('<button class="link danger" type="button" data-toast="已撤销该流程，审批人待办已同步移除">撤销</button>')
        rows.append([str(i + 1), name_cell(k, sub), tm, node or "—", tag(status, STATUS_KIND[status]), f'<div class="ops">{op}</div>'])
    rng = ('<div class="wf-range"><input class="input" type="text" placeholder="开始日期" onfocus="this.type=\'date\'" aria-label="开始日期"><span>至</span>'
           '<input class="input" type="text" placeholder="结束日期" onfocus="this.type=\'date\'" aria-label="结束日期"></div>')
    tools = (f'<div class="wf-tools"><button class="icon-btn" type="button" data-toast="已刷新" aria-label="刷新">{icon("refresh")}</button>'
             f'<button class="icon-btn" type="button" data-toast="已按发起时间倒序排列" aria-label="排序">{icon("sort")}</button>'
             f'<button class="icon-btn" type="button" data-toast="已导出当前查询结果（Excel）" aria-label="导出">{icon("download")}</button></div>')
    content = (wf_filter([field("所属流程", sel(list(PROC.values()))), field("流程状态", sel(["已提交", "已完成", "已撤销"])),
                          field("发起时间", rng)])
               + f'<div class="wf-list">{tools}{table(["序号", "所属流程", "发起时间", "审批节点", "流程状态", "操作"], rows)}'
               + f'{pager(len(rows), 1)}</div>')
    page(role, "started", "已发起", content)


def cc(role):
    urge_rows = [[str(i + 1), PROC_NAME[k], task, who, ct, ut, f'<a class="link" href="{href}">去办理</a>']
                 for i, (k, task, who, ct, ut, href, _) in enumerate(URGE[role])]
    cc_rows = [dict(cells=[str(i + 1), PROC_NAME[k], task, who, ct, ut, f'<a class="link" href="{href}">查看</a>'],
                    cat="unread" if unread else "read", cls="" if unread else "hidden")
               for i, (k, task, who, ct, ut, href, unread) in enumerate(CC[role])]
    read = ('<div class="wf-read" data-target="#wf-cc-tbl"><button type="button" data-seg="read">已读消息</button>'
            '<button type="button" class="on" data-seg="unread">未读消息</button></div>')
    urge_pane = (wf_filter([field("流程名称", inp("请输入流程名称")), field("任务名称", inp("请输入任务名称")),
                            field("催办人", inp("请输入催办人"))])
                 + f'<div class="wf-list">{table(["序号", "流程名称", "任务名称", "催办人", "任务创建时间", "催办时间", "操作"], urge_rows)}'
                 + f'{pager(len(urge_rows), 1)}</div>')
    cc_pane = (wf_filter([field("流程名称", inp("请输入流程名称")), field("任务名称", inp("请输入任务名称")),
                          field("抄送人", inp("请输入抄送人"))])
               + f'<div class="wf-list"><div class="wf-tools" style="justify-content:flex-start">{read}</div>'
               + table(["序号", "流程名称", "任务名称", "抄送人", "任务创建时间", "抄送时间", "操作"], cc_rows, id_="wf-cc-tbl")
               + f'{pager(len(cc_rows), 1)}</div>')
    content = (f'<div class="wf-list" style="padding-bottom:0;margin-bottom:10px;border-radius:0 0 8px 8px">'
               f'<div class="wf-inner-tabs" data-single=".wf-msg" style="margin-bottom:0;border-bottom:0">'
               f'<button type="button" class="on" data-choice="#wf-urge">催办消息</button>'
               f'<button type="button" data-choice="#wf-ccmsg">抄送消息</button></div></div>'
               f'<div class="wf-msg" id="wf-urge">{urge_pane}</div><div class="wf-msg hidden" id="wf-ccmsg">{cc_pane}</div>')
    page(role, "cc", "催办/抄送", content)


def batch(role):
    groups = BATCH[role]
    total = sum(len(r) for _, r in groups)
    cats = []
    rows = []
    for gi, (k, items) in enumerate(groups):
        on = ' class="on"' if gi == 0 else ""
        cats.append(f'<button type="button"{on} data-seg="{k}" data-name="{PROC[k]}" '
                    f'onclick="document.getElementById(\'wf-cur\').textContent=this.dataset.name">'
                    f'<span>{PROC[k]}</span><em>{len(items)}</em></button>')
        for college, sno, task, who, tm, href in items:
            rows.append(dict(cells=[str(len(rows) + 1), PROC[k], college, sno, task, who, tm, f'<a class="link" href="{href}">办理</a>'],
                             cat=k, cls="" if gi == 0 else "hidden"))
    first = PROC[groups[0][0]]
    bar = ('<div class="wf-bar">'
           '<button class="btn btn-pass" type="button" data-toast="请先勾选需要审批的流程">批量通过</button>'
           '<button class="btn btn-nopass" type="button" data-toast="请先勾选需要审批的流程">批量不通过</button>'
           '<span class="small muted">已选 <b data-checked-count="#wf-batch-tbl">0</b> 项</span>'
           f'<span class="cur">当前流程 <span class="tag tag-primary" id="wf-cur">{first}</span></span></div>')
    content = (wf_filter([field("流程名称", inp("请输入流程名称")), field("学院名称", inp("请输入学院名称")), field("学号", inp("请输入学号"))],
                         '<button class="btn btn-default" type="button" data-toast="已展开更多查询条件">展开</button>')
               + f'<div class="wf-batch"><div class="wf-cats" data-target="#wf-batch-tbl"><h3>流程分类<span class="badge">{total}</span></h3>'
               + "".join(cats) + '</div>'
               + f'<div class="wf-list">{bar}'
               + table(["序号", "流程名称", "学院名称", "学号", "当前任务", "发起人", "发起时间", "操作"], rows, check=True, id_="wf-batch-tbl")
               + f'{pager(total, 1)}</div></div>')
    page(role, "batch", "批量审批", content)


def build():
    for role in ROLES:
        todo(role)
        done(role)
        started(role)
        cc(role)
        batch(role)
