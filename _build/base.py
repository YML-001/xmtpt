"""原型生成器基础库：设计令牌、通用样式、交互脚本、图标、页面外壳与常用组件。

所有页面最终都输出为独立 HTML 文件，样式与脚本内联在文件内。
除 index.html 外，所有页面都位于两级目录下（如 pc/school/xxx.html），
因此页面内链接统一按“当前目录相对路径”书写：同目录直接写文件名，
跨目录写 ../common/xxx.html，返回导航页写 ../../index.html。
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAV = "../../index.html"

# ---------------------------------------------------------------- 样式
BASE_CSS = """
/* ===== 设计令牌（对齐中南大学智慧学工正式系统 · Element Plus 主题） ===== */
:root{
  --c-primary:#2A8DC7;--c-primary-dark:#246991;--c-primary-hover:#55A4D2;--c-primary-light:#EAF4F9;--c-primary-border:#95C6E3;
  --c-success:#67C23A;--c-success-bg:#F0F9EB;--c-success-bd:#B3E19D;--c-success-tx:#529B2E;
  --c-warning:#E6A23C;--c-warning-bg:#FDF6EC;--c-warning-bd:#F3D19E;--c-warning-tx:#B88230;
  --c-danger:#F56C6C;--c-danger-bg:#FEF0F0;--c-danger-bd:#FAB6B6;--c-danger-tx:#C45656;
  --c-muted:#909399;--c-muted-bg:#F4F4F5;
  --c-text:#303133;--c-text-2:#606266;--c-text-3:#909399;--c-placeholder:#A8ABB2;
  --c-border:#DCDFE6;--c-line:#EBEEF5;--c-bg:#E3F1F9;--c-fill:#F5F7FA;
  --radius:8px;--radius-sm:4px;--shadow-sm:none;--shadow-md:0 2px 12px rgba(0,0,0,.06);--shadow-lg:0 6px 20px rgba(42,141,199,.14);
  --font:'OPPOSans',-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:var(--font);color:var(--c-text);background:var(--c-bg);font-size:14px;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
button{font:inherit;color:inherit;background:none;border:none;cursor:pointer}
input,select,textarea{font:inherit;color:inherit}
img{display:block;max-width:100%}
.i{width:16px;height:16px;flex:none;stroke:currentColor;fill:none;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
:focus-visible{outline:2px solid var(--c-primary);outline-offset:2px}

/* ===== 工具类 ===== */
.flex{display:flex;align-items:center}.col{display:flex;flex-direction:column}.wrap{flex-wrap:wrap}
.between{justify-content:space-between}.end{justify-content:flex-end}.center{justify-content:center}.top-align{align-items:flex-start}
.gap4{gap:4px}.gap6{gap:6px}.gap8{gap:8px}.gap12{gap:12px}.gap16{gap:16px}.gap20{gap:20px}.gap24{gap:24px}
.mt4{margin-top:4px}.mt8{margin-top:8px}.mt12{margin-top:12px}.mt16{margin-top:16px}.mt20{margin-top:20px}.mt24{margin-top:24px}
.mb8{margin-bottom:8px}.mb12{margin-bottom:12px}.mb16{margin-bottom:16px}.ml-auto{margin-left:auto}.grow{flex:1;min-width:0}
.grid{display:grid;gap:16px}.g2{grid-template-columns:repeat(2,minmax(0,1fr))}.g3{grid-template-columns:repeat(3,minmax(0,1fr))}
.g4{grid-template-columns:repeat(4,minmax(0,1fr))}.g5{grid-template-columns:repeat(5,minmax(0,1fr))}.g6{grid-template-columns:repeat(6,minmax(0,1fr))}
.span2{grid-column:span 2}.span3{grid-column:span 3}.full{grid-column:1/-1}
.muted{color:var(--c-text-3)}.sub{color:var(--c-text-2)}.small{font-size:12px}.fs13{font-size:13px}.fs16{font-size:16px}.fs18{font-size:18px}
.bold{font-weight:600}.num{font-variant-numeric:tabular-nums}.nowrap{white-space:nowrap}.ellipsis{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.c-primary{color:var(--c-primary)}.c-success{color:var(--c-success)}.c-warning{color:var(--c-warning)}.c-danger{color:var(--c-danger)}
.link{color:var(--c-primary);cursor:pointer}.link:hover{color:var(--c-primary-dark);text-decoration:underline}
.divider{height:1px;background:var(--c-line);margin:16px 0}
.hidden{display:none!important}

/* ===== 按钮 ===== */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;height:32px;padding:0 15px;border-radius:var(--radius-sm);font-size:14px;font-weight:500;border:1px solid transparent;white-space:nowrap;transition:background .15s,color .15s,border-color .15s,box-shadow .15s;cursor:pointer;line-height:1}
.btn-primary{background:var(--c-primary);border-color:var(--c-primary);color:#fff}.btn-primary:hover{background:var(--c-primary-hover);border-color:var(--c-primary-hover)}
.btn-ghost{background:#fff;color:var(--c-primary);border-color:var(--c-primary)}.btn-ghost:hover{background:var(--c-primary-light)}
.btn-default{background:#fff;color:var(--c-text-2);border-color:var(--c-border)}.btn-default:hover{color:var(--c-primary);border-color:var(--c-primary-border);background:var(--c-primary-light)}
.btn-light{background:var(--c-primary-light);color:var(--c-primary);border-color:var(--c-primary-border)}.btn-light:hover{background:var(--c-primary);color:#fff}
.btn-success{background:var(--c-success);border-color:var(--c-success);color:#fff}.btn-success:hover{background:#85CE61;border-color:#85CE61}
.btn-warning{background:var(--c-warning-bg);color:var(--c-warning);border-color:var(--c-warning-bd)}.btn-warning:hover{background:var(--c-warning);color:#fff}
.btn-danger{background:var(--c-danger-bg);color:var(--c-danger);border-color:var(--c-danger-bd)}.btn-danger:hover{background:var(--c-danger);color:#fff}
.btn-danger-solid{background:var(--c-danger);border-color:var(--c-danger);color:#fff}.btn-danger-solid:hover{background:#F78989}
.btn-text{padding:0 4px;height:auto;color:var(--c-primary);font-weight:500;border:none}.btn-text:hover{color:var(--c-primary-hover)}
.btn-sm{height:28px;padding:0 12px;font-size:13px}.btn-lg{height:40px;padding:0 22px;font-size:16px}
.btn[disabled],.btn.disabled{opacity:.45;pointer-events:none}

/* ===== 标签 ===== */
.tag{display:inline-flex;align-items:center;gap:4px;height:24px;padding:0 9px;border-radius:var(--radius-sm);font-size:12px;font-weight:500;border:1px solid;white-space:nowrap;line-height:1}
.tag-success{color:var(--c-success);background:var(--c-success-bg);border-color:var(--c-success-bd)}
.tag-warning{color:var(--c-warning);background:var(--c-warning-bg);border-color:var(--c-warning-bd)}
.tag-danger{color:var(--c-danger);background:var(--c-danger-bg);border-color:var(--c-danger-bd)}
/* 行内操作完成态 */
tr.row-done>td{opacity:.55}
button.is-done{opacity:.6;cursor:default;pointer-events:none}
.tag-muted{color:var(--c-muted);background:var(--c-muted-bg);border-color:var(--c-border)}
.tag-primary{color:var(--c-primary);background:var(--c-primary-light);border-color:var(--c-primary-border)}
.tag-dot::before{content:"";width:6px;height:6px;border-radius:50%;background:currentColor}
.badge{display:inline-flex;align-items:center;justify-content:center;min-width:18px;height:18px;padding:0 5px;border-radius:9px;background:var(--c-danger);color:#fff;font-size:11px;font-weight:600;line-height:1}

/* ===== 卡片 ===== */
.card{background:#fff;border-radius:var(--radius);box-shadow:var(--shadow-sm);border:none}
.card-hd{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:52px;padding:10px 20px;border-bottom:1px solid var(--c-line)}
.card-title{display:flex;align-items:center;gap:8px;font-size:16px;font-weight:700;color:var(--c-text)}
.card-title::before{content:"";width:3px;height:14px;border-radius:2px;background:var(--c-primary)}
.card-bd{padding:20px}
.card-hover{transition:box-shadow .2s,transform .2s;cursor:pointer}.card-hover:hover{box-shadow:var(--shadow-lg)}

/* ===== 统计卡 ===== */
.stat{padding:18px 20px;display:flex;align-items:flex-start;gap:14px}
.stat-ic{width:46px;height:46px;border-radius:10px;display:grid;place-items:center;flex:none;background:var(--c-primary-light);color:var(--c-primary)}
.stat-ic .i{width:24px;height:24px}
.stat-ic.green{background:var(--c-success-bg);color:var(--c-success)}.stat-ic.orange{background:var(--c-warning-bg);color:var(--c-warning)}
.stat-ic.red{background:var(--c-danger-bg);color:var(--c-danger)}.stat-ic.gray{background:var(--c-muted-bg);color:var(--c-muted)}
.stat-label{font-size:14px;color:var(--c-text-2)}
.stat-value{font-size:28px;font-weight:700;line-height:1.25;font-variant-numeric:tabular-nums;color:var(--c-text)}
.stat-sub{font-size:12px;color:var(--c-text-3)}
.up{color:var(--c-success)}.down{color:var(--c-danger)}

/* ===== 表格（vxe-table 蓝表头） ===== */
.table-wrap{overflow:auto;border:1px solid #E8EAEC;border-radius:4px 4px 0 0;background:#fff}
.table{width:100%;border-collapse:collapse;font-size:14px;color:#333}
.table th{background:#D6EAF9;color:var(--c-primary);font-weight:700;text-align:left;height:48px;padding:0 12px;white-space:nowrap;border-bottom:none;position:relative}
.table th+th::before{content:"";position:absolute;left:0;top:14px;bottom:14px;width:1px;background:#BADEF3}
.table td{height:49px;padding:10px 12px;border-bottom:1px solid #E8EAEC;vertical-align:middle}
.table tr:last-child td{border-bottom:none}
.table tbody tr{transition:background .15s}.table tbody tr:hover td{background:#F5F9FC}
.table tr.sel td{background:var(--c-primary-light)}
.table .ops{display:flex;gap:12px;white-space:nowrap}
.table .ops .link{font-size:13px;font-weight:500}
.link.danger{color:var(--c-danger)}.link.danger:hover{color:#F78989}
.table input[type=checkbox]{accent-color:var(--c-primary);width:15px;height:15px;cursor:pointer}
[data-href]{cursor:pointer}

/* ===== 表单 ===== */
.field{display:flex;flex-direction:column;gap:6px;min-width:0}
.field>label,.field-label{font-size:14px;color:var(--c-text-2);font-weight:500}
.req{color:var(--c-danger);margin-right:2px}
.hint{font-size:12px;color:var(--c-text-3)}
.input,.select,.textarea{width:100%;height:32px;padding:0 11px;border:1px solid var(--c-border);border-radius:var(--radius-sm);background:#fff;font-size:14px;transition:border-color .15s,box-shadow .15s}
.input::placeholder,.textarea::placeholder{color:var(--c-placeholder)}
.input:hover,.select:hover,.textarea:hover{border-color:#C0C4CC}
.input:focus,.select:focus,.textarea:focus{outline:none;border-color:var(--c-primary);box-shadow:0 0 0 1px var(--c-primary) inset}
.input[readonly],.input:disabled,.select:disabled{background:var(--c-fill);color:var(--c-text-2)}
.select{appearance:none;padding-right:32px;background:#fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%239096A2' stroke-width='2' stroke-linecap='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E") no-repeat right 10px center/14px}
.textarea{height:auto;min-height:88px;padding:8px 12px;resize:vertical;line-height:1.6}
.field.invalid .input,.field.invalid .select,.field.invalid .textarea{border-color:var(--c-danger);background:var(--c-danger-bg)}
.err-msg{display:none;font-size:12px;color:var(--c-danger)}.field.invalid .err-msg{display:block}
.count-tip{font-size:12px;color:var(--c-text-3);text-align:right}
.form-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px 24px}
.form-grid.c3{grid-template-columns:repeat(3,minmax(0,1fr))}.form-grid.c1{grid-template-columns:1fr}
.form-section{font-size:16px;font-weight:700;color:var(--c-text);margin:4px 0 14px;display:flex;align-items:center;gap:8px}
.form-section::before{content:"";width:3px;height:14px;border-radius:2px;background:var(--c-primary)}
.radios{display:flex;flex-wrap:wrap;gap:8px 20px;min-height:36px;align-items:center}
.radio{display:inline-flex;align-items:center;gap:6px;cursor:pointer;font-size:14px}
.radio input{accent-color:var(--c-primary);width:15px;height:15px}
.choices{display:grid;gap:10px}
.choice{display:flex;align-items:center;gap:10px;padding:12px 14px;border:1px solid var(--c-line);border-radius:var(--radius);background:#fff;cursor:pointer;transition:border-color .15s,background .15s}
.choice:hover{border-color:var(--c-primary-border)}
.choice.on{border-color:var(--c-primary);background:#F3F9FD;box-shadow:inset 0 0 0 1px var(--c-primary)}
.choice .ck{width:18px;height:18px;border-radius:50%;border:1.5px solid var(--c-border);flex:none;display:grid;place-items:center}
.choice.on .ck{border-color:var(--c-primary);background:var(--c-primary);box-shadow:inset 0 0 0 3px #fff}
.upload{border:1.5px dashed var(--c-border);border-radius:var(--radius);padding:18px;text-align:center;color:var(--c-text-3);cursor:pointer;background:#FAFBFC;transition:border-color .15s,background .15s;position:relative;display:block}
.upload:hover{border-color:var(--c-primary);background:#F3F9FD;color:var(--c-primary)}
.upload input{position:absolute;inset:0;opacity:0;cursor:pointer}
.upload-list{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
.file-chip{display:inline-flex;align-items:center;gap:6px;height:28px;padding:0 10px;border-radius:6px;background:var(--c-primary-light);color:var(--c-primary);font-size:12px}
.switch{width:40px;height:22px;border-radius:11px;background:var(--c-border);position:relative;transition:background .2s;flex:none;cursor:pointer}
.switch::after{content:"";position:absolute;top:2px;left:2px;width:18px;height:18px;border-radius:50%;background:#fff;box-shadow:0 1px 2px rgba(0,0,0,.2);transition:left .2s}
.switch.on{background:var(--c-primary)}.switch.on::after{left:20px}

/* ===== 提示条 ===== */
.alert{display:flex;align-items:flex-start;gap:10px;padding:9px 16px;border-radius:var(--radius-sm);border:1px solid transparent;font-size:14px;line-height:1.7}
.alert .i{margin-top:4px}
.alert-info{background:var(--c-primary-light);color:var(--c-primary-dark)}
.alert-warning{background:var(--c-warning-bg);color:var(--c-warning-tx)}
.alert-danger{background:var(--c-danger-bg);color:var(--c-danger-tx)}
.alert-success{background:var(--c-success-bg);color:var(--c-success-tx)}

/* ===== 描述列表 ===== */
.kv{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px 24px}
.kv.c2{grid-template-columns:repeat(2,minmax(0,1fr))}.kv.c4{grid-template-columns:repeat(4,minmax(0,1fr))}
.kv dt{font-size:12px;color:var(--c-text-3);margin-bottom:2px}.kv dd{font-size:14px;color:var(--c-text);word-break:break-all}
.kv .full{grid-column:1/-1}

/* ===== 时间线 ===== */
.tl{position:relative}
.tl-item{position:relative;padding:0 0 18px 26px}
.tl-item::before{content:"";position:absolute;left:5px;top:16px;bottom:-2px;width:2px;background:var(--c-line)}
.tl-item:last-child{padding-bottom:0}.tl-item:last-child::before{display:none}
.tl-dot{position:absolute;left:0;top:5px;width:12px;height:12px;border-radius:50%;background:#fff;border:2px solid var(--c-border)}
.tl-item.done .tl-dot{border-color:var(--c-success);background:var(--c-success)}
.tl-item.done::before{background:var(--c-success-bd)}
.tl-item.now .tl-dot{border-color:var(--c-primary);background:#fff;box-shadow:0 0 0 4px rgba(42,141,199,.18)}
.tl-item.back .tl-dot{border-color:var(--c-warning);background:var(--c-warning)}
.tl-item.reject .tl-dot{border-color:var(--c-danger);background:var(--c-danger)}
.tl-title{font-weight:600;font-size:14px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.tl-meta{font-size:12px;color:var(--c-text-3);margin-top:2px}
.tl-comment{margin-top:6px;padding:8px 10px;background:#F7F9FB;border-radius:6px;font-size:13px;color:var(--c-text-2);border-left:3px solid var(--c-line)}
.tl-item.back .tl-comment{background:var(--c-warning-bg);border-left-color:var(--c-warning)}
.tl-item.reject .tl-comment{background:var(--c-danger-bg);border-left-color:var(--c-danger)}

/* ===== 步骤条 ===== */
.steps{display:flex;align-items:center;gap:8px}
.step{display:flex;align-items:center;gap:8px;flex:1;min-width:0;color:var(--c-text-3);font-size:14px}
.step:last-child{flex:none}
.step-no{width:26px;height:26px;border-radius:50%;display:grid;place-items:center;border:1.5px solid var(--c-border);font-size:13px;font-weight:600;flex:none;background:#fff}
.step-line{flex:1;height:2px;background:var(--c-line);border-radius:2px;min-width:20px}
.step.done{color:var(--c-text-2)}.step.done .step-no{background:var(--c-success);border-color:var(--c-success);color:#fff}.step.done .step-line{background:var(--c-success-bd)}
.step.now{color:var(--c-primary);font-weight:600}.step.now .step-no{background:var(--c-primary);border-color:var(--c-primary);color:#fff}

/* ===== 页签与分段 ===== */
.ptabs{display:flex;gap:28px;border-bottom:1px solid var(--c-line);margin-bottom:16px}
.ptabs a{position:relative;padding:12px 0;color:var(--c-text-2);font-size:14px;display:flex;align-items:center;gap:6px}
.ptabs a:hover{color:var(--c-primary)}
.ptabs a.on{color:var(--c-primary);font-weight:600}
.ptabs a.on::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:var(--c-primary);border-radius:2px}
.seg{display:inline-flex;background:var(--c-bg);border-radius:18px;padding:3px;gap:2px}
.seg button{padding:5px 16px;border-radius:15px;color:var(--c-primary);font-size:14px;white-space:nowrap;display:inline-flex;align-items:center;gap:4px;line-height:1.4}
.seg button:hover{background:rgba(255,255,255,.6)}
.seg button.on{background:var(--c-primary);color:#fff;font-weight:600}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{height:28px;padding:0 14px;border-radius:14px;background:#fff;border:1px solid var(--c-border);color:var(--c-text-2);font-size:13px;display:inline-flex;align-items:center;gap:4px;cursor:pointer}
.chip:hover{color:var(--c-primary);border-color:var(--c-primary-border)}
.chip.on{background:var(--c-primary-light);border-color:var(--c-primary);color:var(--c-primary);font-weight:500}

/* ===== 进度条 ===== */
.progress{height:8px;background:#EEF1F4;border-radius:8px;overflow:hidden;flex:1}
.progress>i{display:block;height:100%;background:var(--c-primary);border-radius:8px}
.progress.green>i{background:var(--c-success)}.progress.orange>i{background:var(--c-warning)}.progress.red>i{background:var(--c-danger)}

/* ===== 平台图标 / 头像 ===== */
.pf{width:36px;height:36px;border-radius:9px;display:grid;place-items:center;color:#fff;font-size:14px;font-weight:700;flex:none}
.pf.sm{width:28px;height:28px;font-size:12px;border-radius:7px}.pf.lg{width:56px;height:56px;font-size:22px;border-radius:14px}
.pf-wx{background:#07C160}.pf-wb{background:#E6162D}.pf-dy{background:#1F1F1F}.pf-bz{background:#FB7299}.pf-xhs{background:#FF2442}
.pf-sph{background:#FA9D3B}.pf-qq{background:#12B7F5}.pf-ks{background:#FF4906}.pf-zh{background:#0066FF}.pf-web{background:#2A8DC7}.pf-app{background:#6B5BD2}
.avatar{width:32px;height:32px;border-radius:50%;object-fit:cover;flex:none;background:var(--c-muted-bg)}
.avatar.lg{width:56px;height:56px}.avatar.sm{width:24px;height:24px}
.acct{display:flex;align-items:center;gap:10px;min-width:0}
.acct-name{font-weight:600;color:var(--c-text)}.acct-meta{font-size:12px;color:var(--c-text-3)}

/* ===== 图表 ===== */
.bars{display:flex;align-items:flex-end;gap:14px;height:180px;padding-top:10px}
.bar{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;height:100%;justify-content:flex-end}
.bar i{display:block;width:100%;max-width:34px;border-radius:6px 6px 2px 2px;background:linear-gradient(180deg,#6AAFD8,#2A8DC7)}
.bar b{font-size:12px;font-weight:600;color:var(--c-text-2)}.bar span{font-size:12px;color:var(--c-text-3);white-space:nowrap}
.hbar{display:flex;align-items:center;gap:10px;font-size:13px;margin-bottom:10px}
.hbar-label{width:88px;color:var(--c-text-2);flex:none}.hbar-val{width:48px;text-align:right;font-weight:600;flex:none}
.donut{width:150px;height:150px;border-radius:50%;position:relative;flex:none}
.donut::after{content:"";position:absolute;inset:24px;border-radius:50%;background:#fff}
.donut-center{position:absolute;inset:0;display:grid;place-items:center;text-align:center;z-index:1}
.legend{display:grid;gap:8px;font-size:13px}.legend-item{display:flex;align-items:center;gap:8px}
.legend-dot{width:10px;height:10px;border-radius:3px;flex:none}

/* ===== 空状态 / 结果 ===== */
.result{text-align:center;padding:40px 20px}
.result-ic{width:72px;height:72px;border-radius:50%;display:grid;place-items:center;margin:0 auto 16px}
.result-ic .i{width:36px;height:36px;stroke-width:2}
.result-ic.ok{background:var(--c-success-bg);color:var(--c-success)}.result-ic.warn{background:var(--c-warning-bg);color:var(--c-warning)}
.result-ic.err{background:var(--c-danger-bg);color:var(--c-danger)}.result-ic.info{background:var(--c-primary-light);color:var(--c-primary)}
.result h2{font-size:20px;margin-bottom:6px}.result p{color:var(--c-text-2)}

/* ===== 变更对比 ===== */
.diff td.old{color:var(--c-text-3);text-decoration:line-through;text-decoration-color:rgba(223,32,39,.5)}
.diff td.new{color:var(--c-success);font-weight:600}
.diff tr.changed td{background:#FFFCF5}

/* ===== 分页 ===== */
.pager{display:flex;align-items:center;justify-content:flex-end;gap:4px;padding-top:14px;font-size:14px;color:var(--c-text-2)}
.pager>span{margin-right:8px}
.pager button{min-width:32px;height:32px;padding:0 6px;border:none;border-radius:var(--radius-sm);background:transparent;color:var(--c-text);font-weight:500;display:inline-grid;place-items:center}
.pager button:hover{color:var(--c-primary)}
.pager button.on{color:var(--c-primary);font-weight:700}
.pager button .i{width:14px;height:14px}
.pager .pager-size{width:100px;height:32px;margin-left:12px}

/* ===== 弹窗 / 抽屉 ===== */
.mask{position:fixed;inset:0;background:rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;z-index:60;padding:20px}
.modal{width:600px;max-width:100%;background:#fff;border-radius:12px;box-shadow:0 10px 20px 10px rgba(0,0,0,.05);display:flex;flex-direction:column;max-height:calc(100vh - 40px)}
.modal.lg{width:900px}.modal.sm{width:480px}
.modal-hd{display:flex;align-items:center;justify-content:space-between;padding:16px 20px;border-bottom:1px solid #C8CAD1;font-size:18px;font-weight:700;color:var(--c-text)}
.modal-bd{padding:20px;overflow:auto}
.modal-ft{display:flex;justify-content:flex-end;gap:12px;padding:12px 20px 20px}
.x-btn{width:30px;height:30px;border-radius:6px;display:grid;place-items:center;color:var(--c-text-3)}.x-btn:hover{color:var(--c-primary)}
.drawer-mask{justify-content:flex-end;padding:0}
.drawer{width:640px;max-width:100%;height:100%;background:#fff;box-shadow:-8px 0 24px rgba(0,0,0,.12);display:flex;flex-direction:column}
.drawer .modal-bd{flex:1}
.backdrop{pointer-events:none;user-select:none}

/* ===== Toast（Element Message 样式）与原型悬浮导航 ===== */
.toast{position:fixed;left:50%;top:28px;transform:translate(-50%,-12px);opacity:0;z-index:999;display:flex;align-items:center;gap:10px;padding:11px 16px;border-radius:var(--radius-sm);background:#F0F9EB;border:1px solid #E1F3D8;color:#67C23A;font-size:14px;box-shadow:0 4px 12px rgba(0,0,0,.08);transition:opacity .25s,transform .25s;pointer-events:none}
.toast.show{opacity:1;transform:translate(-50%,0)}
.toast .i{color:#67C23A}
.proto-nav{position:fixed;left:16px;bottom:16px;z-index:200;display:inline-flex;align-items:center;gap:6px;height:34px;padding:0 14px;border-radius:17px;background:rgba(36,105,145,.92);color:#fff;font-size:12px;box-shadow:0 6px 20px rgba(0,0,0,.2);transition:background .15s}
.proto-nav:hover{background:var(--c-primary)}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""

PC_CSS = """
/* ===== PC 布局（按 1920 设计稿，脚本按视口宽度整体缩放，与正式系统 rem 适配一致） ===== */
body.pc{background:var(--c-bg);font-size:14px;color:rgba(0,0,0,.85);overflow:hidden}
.zx-app{display:flex;flex-direction:column;height:calc(100vh / var(--z,1));background:var(--c-bg)}
.zx-hd{height:140px;flex:none;position:relative;background:url(../../assets/pc-topbg.png) top center/100% 140px no-repeat;z-index:5}
.zx-logo{position:absolute;left:0;top:0;width:540px;height:140px;background:url(../../assets/pc-logo-title.webp) 0 0/540px 140px no-repeat}
.zx-topnav{position:absolute;left:596px;right:24px;bottom:0;height:64px;display:flex;align-items:center;gap:50px;font-size:16px;color:rgba(0,0,0,.85)}
.zx-topnav>a,.zx-topnav>button{position:relative;height:100%;display:flex;align-items:center;white-space:nowrap;font-size:16px;color:inherit}
.zx-topnav>a:hover,.zx-topnav>button:hover{color:#3589CF}
.zx-topnav>.on{color:#3589CF;font-weight:700}
.zx-topnav>.on::after{content:"";position:absolute;left:50%;bottom:12px;width:14px;height:3px;border-radius:2px;background:#3589CF;transform:translateX(-50%)}
.zx-topnav>.zx-more{width:28px;height:28px;margin:auto 0;border-radius:50%;background:rgba(53,137,207,.12);color:#3589CF;display:grid;place-items:center;margin-left:-26px}
.zx-user{position:absolute;right:24px;top:0;height:76px;display:flex;align-items:center;gap:18px;color:#fff}
.zx-me{display:flex;align-items:center;gap:10px;color:#fff}
.zx-me img{width:36px;height:36px;border-radius:50%;border:2px solid rgba(255,255,255,.9);object-fit:cover;background:#fff}
.zx-me b{display:block;font-size:14px;line-height:1.3}.zx-me small{display:block;font-size:12px;opacity:.85;line-height:1.3}
.zx-me .i{width:14px;height:14px;opacity:.85}
.zx-bell{position:relative;color:#fff;display:grid;place-items:center;width:32px;height:32px}
.zx-bell .badge{position:absolute;top:-2px;right:-6px;transform:scale(.85)}
.zx-manual{height:32px;padding:0 14px;border-radius:16px;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.55);display:flex;align-items:center;gap:6px;font-size:14px;color:#fff}
.zx-manual:hover{background:rgba(255,255,255,.3)}
.zx-body{flex:1;min-height:0;display:flex;gap:20px;padding:10px 20px 16px}
/* 左侧菜单（蓝色浮层 + 校门剪影） */
.zx-aside{width:225px;flex:none;background:#458FD8 url(../../assets/pc-side-bottom.png) center bottom/191px auto no-repeat;border-radius:8px;padding:10px 0 120px;overflow-y:auto;scrollbar-width:none}
.zx-aside::-webkit-scrollbar{width:0}
.zx-group{display:flex;align-items:center;gap:6px;padding:12px 14px 6px;font-size:12px;font-weight:700;color:#E3F1F9}
.zx-group::before{content:"";width:3px;height:12px;border-radius:2px;background:#E3F1F9}
.zx-aside a{display:flex;align-items:center;gap:8px;height:34px;margin:2px 8px;padding:0 8px;border-radius:4px;color:#fff;font-size:14px;transition:background .15s}
.zx-aside a .i{width:18px;height:18px;flex:none}
.zx-aside a:hover{background:rgba(255,255,255,.12)}
.zx-aside a.on{background:rgba(255,255,255,.2);font-weight:700}
.zx-aside a .badge{margin-left:auto;background:#fff;color:#F56C6C}
.zx-main{flex:1;min-width:0;min-height:0;display:flex;flex-direction:column}
/* 页签栏 */
.zx-tabs{height:45px;flex:none;background:#fff;border-radius:8px;margin-bottom:10px;display:flex;align-items:stretch;padding:0 8px 0 12px;font-size:14px;overflow:hidden}
.zx-main:has(.content>.page-hd:first-child) .zx-tabs,.zx-main:has(.content>.filter:first-child) .zx-tabs{border-radius:8px 8px 0 0;margin-bottom:0;border-bottom:1px solid var(--c-bg)}
.zx-back{display:flex;align-items:center;gap:2px;color:#AFAFAF;padding-right:12px;margin-right:6px;font-size:14px;position:relative}
.zx-back::after{content:"";position:absolute;right:0;top:15px;bottom:15px;width:1px;background:#E4E7ED}
.zx-back:hover{color:var(--c-primary)}
.zx-back .i{width:14px;height:14px}
.zx-tab{display:flex;align-items:center;gap:8px;padding:0 22px;color:#AFAFAF;white-space:nowrap}
.zx-tab:hover{color:var(--c-primary)}
.zx-tab.on{background:var(--c-primary-light);color:var(--c-primary);font-weight:700}
.zx-tab .zx-x{display:grid;place-items:center;width:16px;height:16px;border-radius:50%;color:inherit}
.zx-tab .zx-x .i{width:12px;height:12px}
.zx-tab .zx-x:hover{background:var(--c-primary);color:#fff}
.zx-tabs .zx-fold{margin-left:auto;display:grid;place-items:center;width:36px;color:#909399}
.content{flex:1;min-height:0;overflow-y:auto;scrollbar-width:thin;scrollbar-color:#BFDDEE transparent;padding-bottom:2px}
.zx-ft{height:32px;flex:none;background:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;color:#909399}
/* 页面标题条：紧贴页签栏，对应正式系统检索区 */
.page-hd{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:10px;background:#fff;border-radius:8px;padding:14px 24px}
.content>.page-hd:first-child{border-radius:0 0 8px 8px}
.page-hd h1{font-size:18px;font-weight:700;line-height:1.4;color:var(--c-text)}
.page-hd p{font-size:14px;color:var(--c-text-3);margin-top:2px}
/* 检索区（.msearch）：带边框的“标签｜输入框”组合 */
.filter{background:#fff;border-radius:8px;padding:16px 24px;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px 16px;align-items:center;margin-bottom:10px}
.content>.filter:first-child{border-radius:0 0 8px 8px}
.filter .field{flex-direction:row;align-items:center;gap:0;height:42px;border:1px solid var(--c-bg);border-radius:4px;padding:0 8px}
.filter .field>label{flex:none;font-size:14px;font-weight:700;color:#485066;padding:0 10px 0 4px;margin-right:4px;border-right:1px solid var(--c-bg);line-height:16px;white-space:nowrap}
.filter .field .input,.filter .field .select{border:none;box-shadow:none;height:38px;background-color:transparent}
.filter .field .hint,.filter .field .err-msg{display:none}
.filter-ops{display:flex;gap:12px;justify-content:flex-end;grid-column:-2/-1}
.toolbar{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px;flex-wrap:wrap}
.split{display:grid;grid-template-columns:minmax(0,1fr) 400px;gap:16px;align-items:start}
.sticky{position:sticky;top:0}
.actbar{position:sticky;bottom:0;z-index:20;background:#fff;border-radius:8px;box-shadow:0 -4px 16px rgba(42,141,199,.10);padding:12px 24px;display:flex;align-items:center;gap:12px;margin-top:16px}
.actbar .grow{font-size:14px;color:var(--c-text-3)}
.cm-content{width:100%}
.zx-body.is-full .zx-main{max-width:1600px;margin:0 auto}
/* 详情表格（低代码表单栅格） */
.kv{gap:0;border-top:1px solid #C7E1F0;border-left:1px solid #C7E1F0;border-radius:4px;overflow:hidden}
.kv>div{padding:10px 14px;border-right:1px solid #C7E1F0;border-bottom:1px solid #C7E1F0;background:linear-gradient(180deg,#EDF8FF 0%,#fff 100%);min-width:0}
.kv dt{font-size:14px;color:#627079;margin-bottom:4px}.kv dd{font-size:14px;color:var(--c-text)}
/* 页面页签（低代码详情页签） */
.ptabs{gap:8px;border-bottom:1px solid #C7E1F0;margin-bottom:16px}
.ptabs a{padding:0 22px;height:40px;border-radius:8px 8px 0 0;background:linear-gradient(180deg,#EEEEEE 0%,rgba(238,238,238,0) 100%);color:#9096A2;font-size:15px}
.ptabs a:hover{color:#006DAD}
.ptabs a.on{background:linear-gradient(180deg,#C7E1F0 0%,#fff 100%);color:#006DAD;font-weight:700}
.ptabs a.on::after{height:1px;background:#006DAD;border-radius:0;left:0;right:0}
.crumb{display:flex;align-items:center;gap:6px;font-size:13px;color:var(--c-text-3)}
.top-search{display:flex;align-items:center;gap:8px;height:32px;width:240px;padding:0 12px;border-radius:4px;border:1px solid var(--c-border);background:#fff;color:var(--c-text-3);font-size:14px}
.top-search input{border:none;background:none;outline:none;flex:1;min-width:0}
.icon-btn{width:32px;height:32px;border-radius:4px;display:grid;place-items:center;color:var(--c-text-2);position:relative}
.icon-btn:hover{background:var(--c-primary-light);color:var(--c-primary)}
.id-pill{display:flex;align-items:center;gap:6px;height:32px;padding:0 12px;border-radius:16px;background:var(--c-primary-light);color:var(--c-primary);font-size:13px;font-weight:500}
.logo{width:32px;height:32px;border-radius:50%;background:var(--c-primary);color:#fff;display:grid;place-items:center;font-weight:800;font-size:16px;flex:none}
/* ===== 我的待办（统一待办） ===== */
.zx-main:has(.content>.backdrop>.filter:first-child) .zx-tabs{border-radius:8px 8px 0 0;margin-bottom:0;border-bottom:1px solid var(--c-bg)}
.content>.backdrop>.filter:first-child{border-radius:0 0 8px 8px}
.filter.wf-filter{grid-template-columns:repeat(3,minmax(0,1fr)) auto}
.filter.wf-filter .filter-ops{grid-column:auto}
.wf-range{display:flex;align-items:center;gap:6px;flex:1;min-width:0}
.wf-range .input{flex:1;min-width:0;border:none;height:38px;background:transparent}
.wf-range span{color:var(--c-text-3)}
.wf-list{background:#fff;border-radius:8px;padding:16px 20px}
.wf-list .table td,.wf-list .table th{text-align:center}
.wf-list .table td.l,.wf-list .table th.l{text-align:left}
.wf-name{display:flex;flex-direction:column;align-items:flex-start;gap:2px;text-align:left}
.wf-name small{font-size:12px;color:var(--c-text-3)}
.wf-tools{display:flex;justify-content:flex-end;gap:8px;margin-bottom:12px}
.wf-tools .icon-btn{border:1px solid var(--c-border)}
.wf-inner-tabs{display:flex;gap:28px;border-bottom:1px solid #E4E7ED;margin-bottom:16px}
.wf-inner-tabs button{height:40px;font-size:15px;color:#606266;position:relative}
.wf-inner-tabs button.on{color:var(--c-primary);font-weight:700}
.wf-inner-tabs button.on::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:var(--c-primary)}
.wf-read{display:flex;gap:18px;align-items:center;font-size:14px;color:#606266}
.wf-read button{display:flex;align-items:center;gap:6px}
.wf-read button::before{content:"";width:14px;height:14px;border-radius:50%;border:1px solid var(--c-border);box-sizing:border-box}
.wf-read button.on{color:var(--c-primary)}
.wf-read button.on::before{border:4px solid var(--c-primary)}
.wf-batch{display:grid;grid-template-columns:260px minmax(0,1fr);gap:16px;align-items:start}
.wf-cats{background:#fff;border-radius:8px;overflow:hidden}
.wf-cats h3{display:flex;align-items:center;gap:8px;height:48px;padding:0 16px;font-size:15px;background:#D6EAF9;color:var(--c-primary)}
.wf-cats h3 .badge{background:var(--c-primary)}
.wf-cats button{display:flex;align-items:center;justify-content:space-between;width:100%;height:44px;padding:0 16px;font-size:14px;color:#606266;border-bottom:1px solid #F0F2F5;text-align:left}
.wf-cats button:hover{background:#F5F9FC}
.wf-cats button.on{background:var(--c-primary-light);color:var(--c-primary);font-weight:700}
.wf-cats button em{font-style:normal;min-width:22px;height:20px;padding:0 6px;border-radius:10px;background:#F0F2F5;color:#909399;font-size:12px;display:grid;place-items:center}
.wf-cats button.on em{background:var(--c-primary);color:#fff}
.wf-bar{display:flex;align-items:center;gap:10px;margin-bottom:12px}
.wf-bar .cur{margin-left:auto;display:flex;align-items:center;gap:8px;font-size:14px;color:#606266}
.btn.btn-pass{background:#ECF5FF;color:#409EFF;border:1px solid #A0CFFF}
.btn.btn-pass:hover{background:#409EFF;color:#fff}
.btn.btn-nopass{background:#FEF0F0;color:#F56C6C;border:1px solid #FAB6B6}
.btn.btn-nopass:hover{background:#F56C6C;color:#fff}
/* 流程办理弹窗 */
.wf-mask{z-index:80;padding:0}
.wf-dialog{width:1500px;max-width:calc(100% - 80px);height:calc(100vh / var(--z,1) - 80px);background:#fff;border-radius:8px;display:flex;flex-direction:column;box-shadow:0 12px 40px rgba(0,0,0,.25);overflow:hidden}
.wf-hd{height:56px;flex:none;display:flex;align-items:center;justify-content:space-between;padding:0 24px;border-bottom:1px solid #C8CAD1;font-size:18px}
.wf-bd{flex:1;min-height:0;overflow-y:auto;padding:16px 24px 0;scrollbar-width:thin;scrollbar-color:#BFDDEE transparent}
.wf-tabs{display:flex;gap:12px;margin-bottom:14px}
.wf-tabs button{height:36px;padding:0 24px;border-radius:18px;background:#F0F4F8;color:#606266;font-size:15px}
.wf-tabs button:hover{color:var(--c-primary)}
.wf-tabs button.on{background:linear-gradient(90deg,#55A4D2,#2A8DC7);color:#fff;font-weight:700}
.wf-meta{display:flex;align-items:center;gap:12px;padding:12px 16px;background:#F5F9FC;border:1px solid #E1EEF7;border-radius:6px;margin-bottom:14px;font-size:15px}
.wf-chip{display:inline-flex;align-items:center;gap:4px;height:26px;padding:0 12px;border-radius:13px;background:var(--c-primary-light);color:var(--c-primary);font-size:13px;border:1px solid var(--c-primary-border)}
.wf-sub{font-size:13px;color:var(--c-text-3)}
.wf-pane{padding-bottom:16px}
.wf-pane .page-hd{padding:0 0 12px;border-radius:0;border-bottom:1px dashed #E4E7ED;margin-bottom:14px}
.wf-pane .page-hd h1{font-size:16px}
.wf-pane .actbar{margin:16px -24px 0;border-radius:0;box-shadow:0 -4px 16px rgba(42,141,199,.12)}
.wf-empty{text-align:center;color:var(--c-text-3);height:120px}
.wf-cm{display:inline-block;max-width:420px;text-align:left}
.wf-chart{position:relative;border:1px solid #E4E7ED;border-radius:6px;min-height:420px;background:#FAFCFE radial-gradient(#E4ECF3 1px,transparent 1px) 0 0/16px 16px;overflow:auto;padding:80px 40px}
.wf-zoom{position:absolute;top:12px;right:12px;display:flex;align-items:center;gap:6px;background:#fff;border:1px solid #E4E7ED;border-radius:4px;padding:4px 8px;z-index:2}
.wf-zoom button{width:26px;height:26px;display:grid;place-items:center;color:#606266;border-radius:4px}
.wf-zoom button:hover{background:var(--c-primary-light);color:var(--c-primary)}
.wf-pct{min-width:44px;text-align:center;font-size:13px;color:#606266}
.wf-flow{display:flex;align-items:center;justify-content:center;transform-origin:center top;transition:transform .2s}
.wf-end{width:64px;height:64px;border-radius:50%;border:2px solid #909399;background:#fff;display:grid;place-items:center;font-size:13px;color:#606266;flex:none}
.wf-node{width:150px;min-height:76px;border-radius:10px;border:2px solid #C0C4CC;background:#F4F4F5;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;padding:8px;flex:none;color:#909399}
.wf-node b{font-size:14px;color:inherit}.wf-node small{font-size:12px}
.wf-node.done{border-color:#67C23A;background:#F0F9EB;color:#529B2E}
.wf-node.now{border-color:#2A8DC7;background:#EAF4F9;color:#2A8DC7;box-shadow:0 0 0 4px rgba(42,141,199,.15)}
.wf-arrow{width:56px;height:2px;background:#C0C4CC;position:relative;flex:none}
.wf-arrow::after{content:"";position:absolute;right:-1px;top:-5px;border:6px solid transparent;border-left:8px solid #C0C4CC;border-right:0}
.wf-arrow.done,.wf-arrow.now{background:#67C23A}.wf-arrow.done::after,.wf-arrow.now::after{border-left-color:#67C23A}
.wf-legend{position:absolute;left:16px;bottom:12px;display:flex;gap:16px;font-size:12px;color:#606266}
.wf-legend span{display:flex;align-items:center;gap:6px}
.wf-legend span::before{content:"";width:14px;height:10px;border-radius:3px;border:2px solid #C0C4CC;background:#F4F4F5}
.wf-legend .done::before{border-color:#67C23A;background:#F0F9EB}.wf-legend .now::before{border-color:#2A8DC7;background:#EAF4F9}
.wf-stats{display:grid;grid-template-columns:repeat(5,1fr);gap:16px;margin-bottom:16px}
.wf-stat{display:flex;align-items:center;gap:14px;padding:16px 20px;border:1px solid #E1EEF7;border-radius:8px;background:linear-gradient(180deg,#F5FAFE,#fff)}
.wf-stat>span{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;color:#fff;flex:none}
.wf-stat b{display:block;font-size:24px;line-height:1.2;color:var(--c-text)}.wf-stat small{font-size:13px;color:var(--c-text-3)}
"""

APP_CSS = """
/* ===== APP 展示台 ===== */
body.app-stage{min-height:100vh;display:flex;justify-content:center;align-items:flex-start;gap:40px;padding:36px 20px 60px;background:radial-gradient(1100px 560px at 15% 0%,#D6EAF9 0%,transparent 60%),radial-gradient(900px 500px at 100% 100%,#E6EFFF 0%,transparent 55%),#EEF5FB}
/* 手机内采用正式版 H5 品牌色 */
.phone{--c-primary:#0057F0;--c-primary-dark:#0047C7;--c-primary-hover:#3A7DF5;--c-primary-light:#E6EFFF;--c-primary-border:#B3CDFB;--c-text:#333;--c-text-2:#666;--c-text-3:#999;--c-placeholder:#C8C9CC;--c-bg:#E5F4FF;
  width:375px;height:812px;background:#E5F4FF linear-gradient(180deg,#2479FF 0,#5B9BFF 120px,#B7D6FF 260px,#E5F4FF 380px) no-repeat;border-radius:46px;position:relative;overflow:hidden;display:flex;flex-direction:column;flex:none;box-shadow:0 0 0 10px #1E2530,0 0 0 11px #3A4452,0 40px 80px rgba(15,40,80,.28);color:#333}
.phone::before{content:"";position:absolute;top:10px;left:50%;transform:translateX(-50%);width:120px;height:32px;border-radius:18px;background:#0B0F14;z-index:40}
.status{height:48px;flex:none;display:flex;align-items:center;justify-content:space-between;padding:6px 28px 0 34px;font-size:15px;font-weight:600;position:relative;z-index:30;color:#fff}
.status .sig{display:flex;gap:5px;align-items:center}.status .sig .i{width:17px;height:17px;stroke-width:2}
.navbar{height:44px;flex:none;display:flex;align-items:center;justify-content:center;position:relative;font-size:17px;font-weight:600;padding:0 56px;z-index:30;color:#fff}
.navbar .title{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.nav-l,.nav-r{position:absolute;top:0;height:44px;display:flex;align-items:center;gap:4px;font-size:15px;font-weight:500;color:#fff}
.nav-l{left:10px}.nav-r{right:14px}
.nav-r .link,.nav-r a,.nav-r button{color:#fff}
.nav-l .i{width:24px;height:24px}
.blue-top .status,.blue-top .navbar{background:transparent}
.scroll{flex:1;overflow-y:auto;padding:12px 16px 24px;position:relative}
.scroll::-webkit-scrollbar{width:0}
/* 底部 TabBar：服务大厅 / 首页（校徽） / 个人中心 */
.tabbar{height:92px;flex:none;margin-top:-14px;padding:16px 0 22px;background:url(../../assets/m-tabbar.webp) top center/100% 92px no-repeat;display:flex;z-index:30;position:relative}
.tabbar a{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;font-size:10px;color:#696F7D;position:relative}
.tabbar a .i{width:24px;height:24px;stroke-width:1.5}
.tabbar a.on{font-weight:600}
.tabbar a.on .i{color:#0057F0}
.tabbar a.on span:not(.badge){background:linear-gradient(100deg,#065CF8,#469FFF);-webkit-background-clip:text;background-clip:text;color:transparent}
.tabbar a.tab-c{flex:none;width:92px;justify-content:flex-end}
.tabbar a.tab-c img{position:absolute;top:-26px;left:50%;transform:translateX(-50%);width:52px;height:52px;border-radius:50%;box-shadow:0 4px 12px rgba(0,87,240,.3)}
.tabbar .badge{position:absolute;top:2px;left:calc(50% + 6px);transform:scale(.85)}
.home-ind{position:absolute;bottom:8px;left:50%;transform:translateX(-50%);width:134px;height:5px;border-radius:3px;background:#1E2530;z-index:50}
.bottom-bar{flex:none;background:#fff;padding:10px 16px 30px;box-shadow:0 -2px 10px rgba(0,0,0,.05);display:flex;gap:10px;z-index:30}
.bottom-bar .btn{flex:1;height:44px;border-radius:22px;font-size:16px}
/* 手机内按钮、提示条 */
.phone .btn{border-radius:8px}
.phone .btn-primary{background:linear-gradient(270deg,#469FFF,#065CF8);border:none;color:#fff}
.phone .btn-primary:hover{background:linear-gradient(270deg,#5AAAFF,#1A6BFA)}
.phone .btn-ghost{border-color:#0057F0;color:#0057F0}
.phone .btn-default{border-color:#DCDEE0;color:#333}
.phone .alert{border:none;border-radius:8px;font-size:13px;padding:9px 12px}
.phone .alert-warning{background:#FFFBE6;color:#D46B08;box-shadow:0 2px 8px rgba(212,107,8,.08)}
.phone .alert-info{background:#E6EFFF;color:#0057F0}
.phone .seg{background:#E6EFFF}.phone .seg button{color:#0057F0}.phone .seg button.on{background:linear-gradient(270deg,#469FFF,#065CF8);color:#fff}
.phone .toast{top:70px}
/* 移动端组件 */
.m-card{background:#fff;border-radius:8px;padding:16px;margin-bottom:12px}
.m-title{font-size:16px;font-weight:900;color:#303133;display:flex;align-items:center;justify-content:space-between;margin:8px 2px 14px;position:relative}
.m-title::after{content:"";position:absolute;left:4px;bottom:-7px;width:32px;height:6px;background:url(../../assets/m-title-deco.svg) no-repeat 0 0/32px 6px}
.m-title a{font-size:13px;font-weight:400;color:#666;display:flex;align-items:center;height:24px;padding:0 4px 0 10px;border-radius:12px;background:rgba(255,255,255,.7)}
.m-group{background:#fff;border-radius:8px;overflow:hidden;margin-bottom:12px}
.m-group-title{font-size:14px;color:#666;padding:6px 4px 8px;font-weight:500}
.cell{display:flex;align-items:center;gap:10px;min-height:50px;padding:12px 16px;border-bottom:1px solid #EBEDF0;font-size:15px}
.cell:last-child{border-bottom:none}
.cell-label{color:#333;flex:none}.cell-value{margin-left:auto;color:#666;text-align:right;font-size:14px}
.cell .i.arrow{color:#C8C9CC;width:16px;height:16px}
.cell.col-cell{flex-direction:column;align-items:stretch;gap:8px}
.m-input{width:100%;border:none;outline:none;background:none;font-size:15px;text-align:right}
.m-input::placeholder{color:#C8C9CC}
.col-cell .m-input{text-align:left}
.m-textarea{width:100%;border:none;outline:none;background:#F7F8FA;border-radius:6px;padding:10px;min-height:96px;font-size:14px;resize:none}
.cell.invalid{background:var(--c-danger-bg)}.cell.invalid .err-msg{display:block}
.m-hero{background:linear-gradient(270deg,#469FFF 0%,#065CF8 100%);color:#fff;border-radius:8px;padding:16px;position:relative;overflow:hidden;box-shadow:0 6px 16px rgba(6,92,248,.25)}
.m-hero::after{content:"";position:absolute;right:-30px;top:-30px;width:140px;height:140px;border-radius:50%;background:rgba(255,255,255,.1)}
.quick{display:grid;grid-template-columns:repeat(4,1fr);gap:4px}
.quick a{display:flex;flex-direction:column;align-items:center;gap:6px;padding:8px 0;font-size:12px;color:#333}
.quick .qi{width:46px;height:46px;border-radius:12px;display:grid;place-items:center;background:linear-gradient(135deg,#E8F1FF,#C9DCFF);color:#0057F0}
.quick .qi .i{width:22px;height:22px;stroke-width:1.8}
.quick .qi.green{background:linear-gradient(135deg,#E2F9EF,#C2EFDB);color:#12A866}.quick .qi.orange{background:linear-gradient(135deg,#FFF1E3,#FFDAB9);color:#F2761B}
.quick .qi.red{background:linear-gradient(135deg,#FFE9EE,#FFCAD5);color:#EE3F66}.quick .qi.purple{background:linear-gradient(135deg,#EFEBFF,#D9D0FF);color:#6E4FF0}
.todo-item{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid #EBEDF0}
.todo-item:last-child{border-bottom:none}
.m-tabs{display:flex;background:linear-gradient(180deg,#F0F6FF,#E6EFFF);margin:-12px -16px 12px;padding:0 8px;position:sticky;top:-12px;z-index:10}
.m-tabs a,.m-tabs button{flex:1;text-align:center;padding:12px 0 14px;font-size:15px;color:rgba(30,50,63,.7);position:relative}
.m-tabs .on{color:#1E323F;font-weight:700}
.m-tabs .on::after{content:"";position:absolute;left:50%;bottom:5px;transform:translateX(-50%);width:32px;height:6px;background:url(../../assets/m-title-deco.svg) no-repeat 0 0/32px 6px}
.m-steps{display:flex;justify-content:space-between;background:#fff;border-radius:8px;padding:14px 10px;margin-bottom:12px}
.m-step{flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;font-size:11px;color:#999;position:relative}
.m-step::before{content:"";position:absolute;top:11px;left:-50%;right:50%;height:2px;background:#EBEDF0}
.m-step:first-child::before{display:none}
.m-step b{width:24px;height:24px;border-radius:50%;display:grid;place-items:center;background:#fff;border:1.5px solid #DCDEE0;font-size:12px;position:relative;z-index:1}
.m-step.done b{background:var(--c-success);border-color:var(--c-success);color:#fff}.m-step.done::before{background:var(--c-success-bd)}
.m-step.now{color:#0057F0;font-weight:600}.m-step.now b{background:linear-gradient(270deg,#469FFF,#065CF8);border-color:#0057F0;color:#fff}
.m-stamp{position:absolute;right:14px;top:50%;transform:translateY(-50%) rotate(-8deg);width:76px;height:auto;opacity:.92;pointer-events:none}
.sheet-mask{position:absolute;inset:0;background:rgba(0,0,0,.5);z-index:45;display:flex;align-items:flex-end}
.sheet{background:#fff;width:100%;border-radius:12px 12px 0 0;padding:16px 16px 34px;max-height:80%;overflow:auto}
.m-dialog-mask{position:absolute;inset:0;background:rgba(0,0,0,.5);z-index:45;display:flex;align-items:center;justify-content:center;padding:32px}
.m-dialog{background:#fff;border-radius:12px;width:100%;overflow:hidden}
/* 右侧页面说明 */
.notes{width:340px;flex:none;position:sticky;top:36px;display:flex;flex-direction:column;gap:14px}
.notes .card{padding:18px 20px}
.notes h3{font-size:18px;margin-bottom:4px}
.notes ul{list-style:none;display:grid;gap:8px;font-size:13px;color:var(--c-text-2)}
.notes li{display:flex;gap:8px;line-height:1.6}
.notes li::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--c-primary-border);margin-top:8px;flex:none}
.notes .flow a{display:flex;align-items:center;gap:8px;padding:8px 10px;border-radius:6px;background:var(--c-primary-light);font-size:13px;margin-top:6px;color:var(--c-primary-dark)}
.notes .flow a:hover{background:var(--c-primary);color:#fff}
@media (max-width:820px){.notes{display:none}}
"""

# ---------------------------------------------------------------- 交互脚本
BASE_JS = r"""
// 通用微交互：toast 提示、行点击跳转、返回、分段切换、全选、必填校验、上传、复制、搜索过滤
(function(){
  var toastEl;
  function toast(msg){
    if(!toastEl){toastEl=document.createElement('div');toastEl.className='toast';document.body.appendChild(toastEl);}
    toastEl.innerHTML='<svg class="i" viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>'+msg;
    toastEl.classList.add('show');clearTimeout(toastEl._t);
    toastEl._t=setTimeout(function(){toastEl.classList.remove('show');},1800);
  }
  window.toast=toast;
  function go(url,delay){if(delay){setTimeout(function(){location.href=url;},delay);}else{location.href=url;}}

  // 必填校验：容器内所有可见的 [required] 均有值才通过；复选框须勾选
  function validate(scope){
    var ok=true,first=null;
    scope.querySelectorAll('[required]').forEach(function(el){
      if(el.closest('.hidden'))return;
      var box=el.closest('.field,.cell');var empty=!String(el.value||'').trim();
      if(el.type==='radio'){empty=!scope.querySelector('input[name="'+el.name+'"]:checked');}
      if(el.type==='checkbox'){empty=!el.checked;}
      if(box){box.classList.toggle('invalid',empty);}
      if(empty){ok=false;first=first||el;}
    });
    if(!ok){toast('请完善标红的必填项');first&&first.focus&&first.focus();}
    return ok;
  }

  document.addEventListener('click',function(e){
    var t=e.target.closest('[data-toast],[data-href],[data-back],[data-submit],[data-seg],[data-toggle],[data-copy],[data-choice],.switch,.pager button,[data-remove]');
    if(!t)return;
    if(t.matches('input,select,textarea,label')&&!t.dataset.href)return;
    if(t.dataset.remove!==undefined){var r=t.closest(t.dataset.remove||'tr');r&&r.remove();toast('已移除');return;}
    if(t.dataset.seg!==undefined){
      var g=t.parentElement;g.querySelectorAll('[data-seg]').forEach(function(b){b.classList.remove('on');});t.classList.add('on');
      var target=g.dataset.target&&document.querySelector(g.dataset.target);
      if(target){var v=t.dataset.seg;target.querySelectorAll('[data-cat]').forEach(function(row){row.classList.toggle('hidden',!(v==='all'||(' '+row.dataset.cat+' ').indexOf(' '+v+' ')>-1));});}
      if(!t.dataset.toast)return;
    }
    if(t.dataset.choice!==undefined){
      var grp=t.closest('[data-single]');
      if(grp){grp.querySelectorAll('[data-choice]').forEach(function(c){c.classList.remove('on');});t.classList.add('on');}
      else{t.classList.toggle('on');}
      var tg=t.dataset.choice&&document.querySelectorAll(t.dataset.choice);
      if(tg&&tg.length&&grp){document.querySelectorAll(grp.dataset.single).forEach(function(x){x.classList.add('hidden');});tg.forEach(function(x){x.classList.remove('hidden');});}
      return;
    }
    if(t.classList.contains('switch')){t.classList.toggle('on');toast(t.classList.contains('on')?'已开启':'已关闭');return;}
    if(t.matches('.pager button')){
      var nums=[].slice.call(t.parentElement.querySelectorAll('button:not([data-nav])'));var cur=nums.filter(function(b){return b.classList.contains('on');})[0]||nums[0];
      var nx=t.dataset.nav?nums[nums.indexOf(cur)+(t.dataset.nav==='prev'?-1:1)]:t;
      if(!nx){toast(t.dataset.nav==='prev'?'已经是第一页':'已经是最后一页');return;}
      nums.forEach(function(b){b.classList.remove('on');});nx.classList.add('on');toast('已加载第 '+nx.textContent.trim()+' 页数据');return;}
    if(t.dataset.toggle){e.preventDefault();document.querySelectorAll(t.dataset.toggle).forEach(function(x){x.classList.toggle('hidden');});if(t.dataset.toast)toast(t.dataset.toast);return;}
    if(t.dataset.copy){if(navigator.clipboard)navigator.clipboard.writeText(t.dataset.copy);toast('已复制到剪贴板');return;}
    if(t.dataset.back!==undefined){e.preventDefault();if(history.length>1&&document.referrer){history.back();}else{go(t.dataset.back);}return;}
    if(t.dataset.submit){
      e.preventDefault();var scope=t.closest('[data-form]')||document;
      if(!validate(scope))return;
      if(t.dataset.toast){toast(t.dataset.toast);go(t.dataset.submit,700);}else{go(t.dataset.submit);}
      return;
    }
    if(t.dataset.href){if(e.target.closest('a,button,input,label')&&e.target.closest('a,button,input,label')!==t)return;
      if(t.dataset.toast){toast(t.dataset.toast);go(t.dataset.href,700);}else{go(t.dataset.href);}return;}
    if(t.dataset.toast&&t.tagName==='BUTTON'&&!t.classList.contains('chip')&&!t.hasAttribute('onclick')&&!t.dataset.fill){
      var label=t.textContent.trim();
      // 批量操作：作用于已勾选的行
      if(/^批量/.test(label)){
        var picked=[].slice.call(document.querySelectorAll('tbody input[type=checkbox]:checked'));
        if(picked.length){if(/通过|确认|退回|移交|下发|注销/.test(label))picked.forEach(function(c){markRow(c.closest('tr'));});refreshCount();
          toast('已'+label.replace(/^批量/,'').replace(/所选$/,'')+' '+picked.length+' 项');return;}
      // 表格行内操作：执行后变为完成态，避免重复操作
      }else if(t.closest('td')&&!/^已|查看|下载|预览|复制|详情|编辑/.test(label)){
        toast(t.dataset.toast);t.classList.add('is-done');
        var tn=t.lastChild;if(tn&&tn.nodeType===3){tn.textContent='已'+label;}else{t.appendChild(document.createTextNode('（已'+label+'）'));}return;
      }
    }
    if(t.dataset.toast){e.preventDefault();toast(t.dataset.toast);
      var h=t.tagName==='A'&&t.getAttribute('href');if(h&&h!=='#')go(h,700);}
  });
  function markRow(tr){
    if(!tr)return;tr.classList.add('row-done');tr.classList.remove('sel');
    var cb=tr.querySelector('input[type=checkbox]');if(cb){cb.checked=false;cb.disabled=true;}
    var last=tr.lastElementChild;if(last)last.innerHTML='<span class="tag tag-success">已处理</span>';
  }
  function refreshCount(){
    document.querySelectorAll('[data-check-all]').forEach(function(a){a.checked=false;});
    document.querySelectorAll('[data-checked-count]').forEach(function(n){
      var tb=document.querySelector(n.dataset.checkedCount);if(tb)n.textContent=tb.querySelectorAll('tbody input[type=checkbox]:checked').length;
    });
  }

  // 表格全选与已选计数
  document.addEventListener('change',function(e){
    var el=e.target;
    if(el.matches('[data-check-all]')){
      var tb=el.closest('table');tb.querySelectorAll('tbody input[type=checkbox]').forEach(function(c){if(!c.closest('tr').classList.contains('hidden')){c.checked=el.checked;c.closest('tr').classList.toggle('sel',el.checked);}});
    }else if(el.matches('tbody input[type=checkbox]')){el.closest('tr').classList.toggle('sel',el.checked);}
    if(el.matches('input[type=checkbox]')){
      document.querySelectorAll('[data-checked-count]').forEach(function(n){
        var tb=document.querySelector(n.dataset.checkedCount);if(tb)n.textContent=tb.querySelectorAll('tbody input[type=checkbox]:checked').length;
      });
    }
    if(el.matches('.upload input[type=file]')){
      var list=el.closest('.upload').nextElementSibling;
      if(list&&list.classList.contains('upload-list')){
        Array.prototype.forEach.call(el.files,function(f){var s=document.createElement('span');s.className='file-chip';s.textContent=f.name;list.appendChild(s);});
      }
      toast('已上传 '+el.files.length+' 个文件');
    }
    var box=el.closest('.field.invalid,.cell.invalid');if(box&&String(el.value).trim())box.classList.remove('invalid');
  });

  // 字数统计与列表搜索
  document.addEventListener('input',function(e){
    var el=e.target;
    if(el.maxLength>0&&el.dataset.count!==undefined){var tip=el.parentElement.querySelector('.count-tip');if(tip)tip.textContent=el.value.length+' / '+el.maxLength;}
    if(el.dataset.search){
      var kw=el.value.trim();document.querySelectorAll(el.dataset.search+' [data-cat], '+el.dataset.search+' tbody tr').forEach(function(r){r.classList.toggle('hidden',kw&&r.textContent.indexOf(kw)<0);});
    }
    var box=el.closest('.field.invalid,.cell.invalid');if(box&&String(el.value).trim())box.classList.remove('invalid');
  });
})();
"""

# ---------------------------------------------------------------- 图标（Hugeicons 风格线性图标，24 栅格）
ICONS = {
    "zoom-in": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5M8 11h6M11 8v6"/>',
    "zoom-out": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5M8 11h6"/>',
    "sort": '<path d="M7 4v16M3 8l4-4 4 4M17 20V4M13 16l4 4 4-4"/>',
    "paperclip": '<path d="m20 11-8.5 8.5a5 5 0 0 1-7-7L13 4a3.5 3.5 0 0 1 5 5l-8.5 8.5a2 2 0 0 1-3-3L14 7"/>',
    "home": '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V20h14V9.5"/><path d="M10 20v-6h4v6"/>',
    "dashboard": '<rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c1.2-3.5 3.6-5.2 6.5-5.2s5.3 1.7 6.5 5.2"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8"/><path d="M18 14.8c1.8.6 3 2.3 3.6 5.2"/>',
    "user-add": '<circle cx="10" cy="8" r="4"/><path d="M3 21c1.4-4 4-6 7-6 1.6 0 3 .5 4.2 1.4"/><path d="M19 14v6M16 17h6"/>',
    "user-switch": '<circle cx="8" cy="7" r="3"/><path d="M2.5 18c1-3 3-4.5 5.5-4.5"/><circle cx="16" cy="11" r="3"/><path d="M10.5 22c1-3 3-4.5 5.5-4.5s4.5 1.5 5.5 4.5"/><path d="M14 3h5l-1.5-1.5M19 3l-1.5 1.5"/>',
    "file": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h4"/>',
    "file-add": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M12 11v6M9 14h6"/>',
    "file-check": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="m9 14.5 2 2 4-4"/>',
    "file-edit": '<path d="M13 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h4"/><path d="M13 3v5h5v3"/><path d="m14 21 .6-2.6 5-5a1.4 1.4 0 0 1 2 2l-5 5z"/>',
    "clipboard": '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3h6v1"/><path d="M9 11h6M9 15h4"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "check-circle": '<circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.8 2.8L16.5 9.5"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "x-circle": '<circle cx="12" cy="12" r="9"/><path d="m15 9-6 6M9 9l6 6"/>',
    "alert": '<path d="M12 3.5 2.5 20h19z"/><path d="M12 10v4.5"/><path d="M12 17.5v.01"/>',
    "alert-circle": '<circle cx="12" cy="12" r="9"/><path d="M12 7.5v5.5"/><path d="M12 16.5v.01"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5"/><path d="M12 7.5v.01"/>',
    "bell": '<path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15z"/><path d="M10 20.5a2 2 0 0 0 4 0"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
    "filter": '<path d="M3 5h18l-7 8.5V20l-4-2v-4.5z"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "edit": '<path d="M4 20h4L19 9a2.8 2.8 0 0 0-4-4L4 16z"/><path d="m13.5 6.5 4 4"/>',
    "trash": '<path d="M4 7h16"/><path d="M10 11v6M14 11v6"/><path d="M6 7l1 13h10l1-13"/><path d="M9 7V4h6v3"/>',
    "eye": '<path d="M2.5 12S6 5 12 5s9.5 7 9.5 7-3.5 7-9.5 7S2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
    "download": '<path d="M12 4v11"/><path d="m7 10 5 5 5-5"/><path d="M4 20h16"/>',
    "upload": '<path d="M12 16V5"/><path d="m7 10 5-5 5 5"/><path d="M4 20h16"/>',
    "refresh": '<path d="M20 11a8 8 0 0 0-14.5-4.5L4 8"/><path d="M4 4v4h4"/><path d="M4 13a8 8 0 0 0 14.5 4.5L20 16"/><path d="M20 20v-4h-4"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "chevron-right": '<path d="m9 6 6 6-6 6"/>',
    "chevron-left": '<path d="m15 6-6 6 6 6"/>',
    "chevron-down": '<path d="m6 9 6 6 6-6"/>',
    "chevrons-right": '<path d="m6 7 5 5-5 5"/><path d="m13 7 5 5-5 5"/>',
    "arrow-right": '<path d="M4 12h16"/><path d="m14 6 6 6-6 6"/>',
    "arrow-left": '<path d="M20 12H4"/><path d="m10 6-6 6 6 6"/>',
    "logout": '<path d="M14 4h4a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-4"/><path d="M9 16l-4-4 4-4"/><path d="M5 12h11"/>',
    "settings": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
    "shield": '<path d="M12 3 4.5 6v5.5c0 4.5 3.2 8.3 7.5 9.5 4.3-1.2 7.5-5 7.5-9.5V6z"/><path d="m9 12 2 2 4-4"/>',
    "lock": '<rect x="4.5" y="10.5" width="15" height="10" rx="2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="m11 12 9-9M17 6l2.5 2.5M14.5 8.5 17 11"/>',
    "link": '<path d="M10 14a4.5 4.5 0 0 0 6.4 0l3-3a4.5 4.5 0 0 0-6.4-6.4l-1 1"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0l-3 3a4.5 4.5 0 0 0 6.4 6.4l1-1"/>',
    "copy": '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2"/>',
    "image": '<rect x="3.5" y="4.5" width="17" height="15" rx="2"/><circle cx="9" cy="10" r="1.8"/><path d="m20.5 16-5-5-9 8.5"/>',
    "camera": '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
    "message": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    "flag": '<path d="M5 21V4"/><path d="M5 4h11l-2 4 2 4H5"/>',
    "radar": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><path d="M12 12 18.5 5.5"/><circle cx="12" cy="12" r="1"/>',
    "ghost": '<path d="M5 20V10a7 7 0 0 1 14 0v10l-2.3-1.6L14.3 20 12 18.4 9.7 20l-2.4-1.6z"/><path d="M9.5 10.5v.01M14.5 10.5v.01"/>',
    "building": '<path d="M4 21V5l8-2v18"/><path d="M12 8h8v13"/><path d="M7.5 8h1.5M7.5 12h1.5M7.5 16h1.5M15.5 12h1.5M15.5 16h1.5"/><path d="M2.5 21h19"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
    "list": '<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4.5 6h.01M4.5 12h.01M4.5 18h.01"/>',
    "hierarchy": '<rect x="9" y="3" width="6" height="5" rx="1"/><rect x="3" y="16" width="6" height="5" rx="1"/><rect x="15" y="16" width="6" height="5" rx="1"/><path d="M12 8v4M6 16v-4h12v4"/>',
    "database": '<ellipse cx="12" cy="5.5" rx="7.5" ry="2.8"/><path d="M4.5 5.5v13c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8v-13"/><path d="M4.5 12c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8"/>',
    "chart": '<path d="M4 20V4"/><path d="M4 20h16"/><rect x="7" y="11" width="3" height="6" rx=".5"/><rect x="12" y="7" width="3" height="10" rx=".5"/><rect x="17" y="13" width="3" height="4" rx=".5"/>',
    "pie": '<path d="M21 13A9 9 0 1 1 11 3v10z"/><path d="M14 3.3A8 8 0 0 1 20.7 10H14z"/>',
    "trending": '<path d="m3 17 6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    "swap": '<path d="M4 8h14l-3.5-3.5"/><path d="M20 16H6l3.5 3.5"/>',
    "send": '<path d="M21 3 10 14"/><path d="m21 3-7 18-4-7-7-4z"/>',
    "undo": '<path d="M9 14 4 9l5-5"/><path d="M4 9h10.5a5.5 5.5 0 0 1 0 11H11"/>',
    "ban": '<circle cx="12" cy="12" r="9"/><path d="m5.6 5.6 12.8 12.8"/>',
    "wrench": '<path d="M14.7 6.3a4 4 0 0 0 5 5L21 10a6 6 0 0 1-8 1.5L6 18.5a2 2 0 1 1-2.8-2.8L10.2 8.7A6 6 0 0 1 11.7 1L10.4 2.3a4 4 0 0 0 4.3 4z"/>',
    "archive": '<rect x="3" y="4" width="18" height="4.5" rx="1"/><path d="M5 8.5V20h14V8.5"/><path d="M10 12.5h4"/>',
    "history": '<path d="M3.5 12a8.5 8.5 0 1 0 2.5-6"/><path d="M3 4v4h4"/><path d="M12 8v4l3 2"/>',
    "star": '<path d="m12 3.5 2.6 5.3 5.9.9-4.3 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8L3.5 9.7l5.9-.9z"/>',
    "more": '<circle cx="5.5" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="18.5" cy="12" r="1"/>',
    "qr": '<rect x="4" y="4" width="6" height="6" rx="1"/><rect x="14" y="4" width="6" height="6" rx="1"/><rect x="4" y="14" width="6" height="6" rx="1"/><path d="M14 14h2v2h-2zM18 18h2v2h-2zM14 18h2M18 14h2"/>',
    "help": '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .8-1 1.5v.7"/><path d="M12 17v.01"/>',
    "log": '<path d="M8 3h9a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/><path d="M5 6h3V3"/><path d="M9 11h6M9 15h6"/>',
    "hand": '<path d="M8 13V5.5a1.5 1.5 0 0 1 3 0V12"/><path d="M11 11V4.5a1.5 1.5 0 0 1 3 0V12"/><path d="M14 11.5V6a1.5 1.5 0 0 1 3 0v8c0 4-2.5 7-6.5 7-2.5 0-4-1-5.5-3L3 14.5a1.5 1.5 0 0 1 2.5-1.8L8 15.5"/>',
    "inbox": '<path d="M3 13h5l1.5 3h5L16 13h5"/><path d="M5 5h14l2 8v6H3v-6z"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    "grid": '<rect x="4" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.5"/>',
    "monitor": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
    "smartphone": '<rect x="6.5" y="2.5" width="11" height="19" rx="2.5"/><path d="M11 18h2"/>',
    "route": '<circle cx="6" cy="19" r="2"/><circle cx="18" cy="5" r="2"/><path d="M8 19h8a3.5 3.5 0 0 0 0-7H8a3.5 3.5 0 0 1 0-7h8"/>',
    "sparkle": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4"/><path d="m6 6 2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
    "signal": '<path d="M4 18v-2M9 18v-5M14 18V9M19 18V5"/>',
    "wifi": '<path d="M2.5 9a14 14 0 0 1 19 0"/><path d="M5.5 12.5a9.5 9.5 0 0 1 13 0"/><path d="M9 16a4.5 4.5 0 0 1 6 0"/><path d="M12 19.5v.01"/>',
    "battery": '<rect x="2.5" y="7.5" width="17" height="9" rx="2"/><path d="M21.5 11v2"/><rect x="4.5" y="9.5" width="11" height="5" rx="1" fill="currentColor"/>',
    "zap": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    "power": '<path d="M12 3v8"/><path d="M6.5 6.5a8 8 0 1 0 11 0"/>',
    "tag": '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.3"/>',
    "print": '<path d="M7 9V3h10v6"/><rect x="3" y="9" width="18" height="8" rx="2"/><path d="M7 14h10v7H7z"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18 14 14 0 0 1 0-18z"/>',
}


def icon(name, size=None, cls=""):
    style = f' style="width:{size}px;height:{size}px"' if size else ""
    return f'<svg class="i {cls}" viewBox="0 0 24 24"{style}>{ICONS[name]}</svg>'


# ---------------------------------------------------------------- 图片（Unsplash）
def unsplash(photo_id, w=96, h=96):
    return f"https://images.unsplash.com/photo-{photo_id}?w={w}&h={h}&fit=crop&crop=faces&auto=format&q=70"


AVATARS = {
    "陈静": unsplash("1494790108377-be9c29b29330"),
    "周建华": unsplash("1507003211169-0a1dd7228f2d"),
    "王晓琳": unsplash("1438761681033-6461ffad8d80"),
    "李明": unsplash("1500648767791-00dcc994a43e"),
    "李四": unsplash("1506794778202-cad84cf45f1d"),
    "孙悦": unsplash("1534528741775-53994a69daeb"),
    "赵磊": unsplash("1472099645785-5658abf4ff4e"),
    "何雨桐": unsplash("1544005313-94ddf0286df2"),
    "刘洋": unsplash("1519085360753-af0119f7cbe7"),
}
PHOTOS = {
    "campus": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=1600&q=70&auto=format&fit=crop",
    "students": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1200&q=70&auto=format&fit=crop",
    "media": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=1200&q=70&auto=format&fit=crop",
    "phone": "https://images.unsplash.com/photo-1611162616305-c69b3fa7fbe0?w=900&q=70&auto=format&fit=crop",
    "meeting": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=900&q=70&auto=format&fit=crop",
    "screenshot": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=600&q=70&auto=format&fit=crop",
}


def avatar(name, cls=""):
    src = AVATARS.get(name, AVATARS["李明"])
    return f'<img class="avatar {cls}" src="{src}" alt="{name}的头像">'


# ---------------------------------------------------------------- 常用组件
def esc(s):
    return escape(str(s), quote=True)


def btn(text, href=None, kind="primary", ic=None, size="", toast=None, attrs=""):
    """按钮：有 href 时输出链接；否则输出带 data-toast 的按钮，保证点击都有反馈。"""
    cls = f"btn btn-{kind}" + (f" btn-{size}" if size else "")
    inner = (icon(ic) if ic else "") + text
    if href:
        t = f' data-toast="{esc(toast)}"' if toast else ""
        return f'<a class="{cls}" href="{href}"{t} {attrs}>{inner}</a>'
    return f'<button class="{cls}" type="button" data-toast="{esc(toast or "操作成功")}" {attrs}>{inner}</button>'


def back_btn(fallback, text="返回", kind="default", size=""):
    cls = f"btn btn-{kind}" + (f" btn-{size}" if size else "")
    return f'<button class="{cls}" type="button" data-back="{fallback}">{icon("arrow-left")}{text}</button>'


def submit_btn(text, target, kind="primary", ic=None, toast=None, size=""):
    cls = f"btn btn-{kind}" + (f" btn-{size}" if size else "")
    t = f' data-toast="{esc(toast)}"' if toast else ""
    return f'<button class="{cls}" type="button" data-submit="{target}"{t}>{icon(ic) if ic else ""}{text}</button>'


def tag(text, kind="primary", dot=False):
    return f'<span class="tag tag-{kind}{" tag-dot" if dot else ""}">{text}</span>'


# 四套状态统一配色
STATUS_KIND = {
    # 运行状态
    "正常运行": "success", "不活跃": "warning", "整改中": "warning", "暂停运行": "danger", "申请注销": "warning", "已注销": "muted",
    # 备案状态
    "未备案": "muted", "备案申请中": "warning", "已备案": "success", "变更申请中": "warning", "注销申请中": "warning",
    # 年审状态
    "未开始": "muted", "待填报": "primary", "待指导教师审核": "warning", "待学院审核": "warning", "待学校审核": "warning",
    "审核退回": "danger", "待整改": "danger", "整改复核中": "warning", "年审通过": "success", "年审不通过": "danger", "本年度注销": "muted",
    # 年度异动
    "无异动": "muted", "新建": "primary", "变更": "warning", "注销": "danger",
    # 流程通用
    "审核中": "warning", "已通过": "success", "已退回": "danger", "已驳回": "danger", "待审核": "warning", "已完成": "success",
    "疑似僵尸号": "danger", "高风险": "danger", "中风险": "warning", "低风险": "primary", "已处置": "success", "待核实": "warning",
    "进行中": "primary", "已结束": "muted", "草稿": "muted", "已发布": "success", "继续整改": "danger", "整改通过": "success",
    "已撤销": "muted", "启用": "success", "停用": "muted", "教师代办": "primary", "待确认": "warning", "已确认": "success",
}


def st(text, dot=True):
    return tag(text, STATUS_KIND.get(text, "primary"), dot)


PLATFORMS = {
    "微信公众号": ("wx", "微"), "微博": ("wb", "博"), "抖音": ("dy", "抖"), "哔哩哔哩": ("bz", "B"), "小红书": ("xhs", "书"),
    "视频号": ("sph", "视"), "QQ": ("qq", "Q"), "快手": ("ks", "快"), "知乎": ("zh", "知"), "网站": ("web", "网"), "APP": ("app", "A"),
}


def pf(platform, size=""):
    k, ch = PLATFORMS.get(platform, ("web", "媒"))
    return f'<span class="pf pf-{k} {size}" title="{platform}">{ch}</span>'


def acct(name, platform, meta=None, size=""):
    meta = meta if meta is not None else platform
    return f'<div class="acct">{pf(platform, size)}<div class="grow"><div class="acct-name ellipsis">{name}</div><div class="acct-meta ellipsis">{meta}</div></div></div>'


def card(title, body, extra="", cls="", bd_cls="card-bd", id_=""):
    hd = f'<div class="card-hd"><div class="card-title">{title}</div><div class="flex gap8">{extra}</div></div>' if title else ""
    idattr = f' id="{id_}"' if id_ else ""
    return f'<div class="card {cls}"{idattr}>{hd}<div class="{bd_cls}">{body}</div></div>'


def stat(label, value, sub="", ic="chart", color="", href=None):
    inner = (f'<div class="stat-ic {color}">{icon(ic)}</div><div class="grow"><div class="stat-label">{label}</div>'
             f'<div class="stat-value">{value}</div><div class="stat-sub">{sub}</div></div>')
    if href:
        return f'<a class="card card-hover stat" href="{href}">{inner}</a>'
    return f'<div class="card stat">{inner}</div>'


def table(headers, rows, check=False, id_="", cls=""):
    """rows: 每行为单元格列表；或 dict(cells=[...], href="x.html", cat="分类")。"""
    th = "".join(f"<th>{h}</th>" for h in headers)
    if check:
        th = '<th style="width:36px"><input type="checkbox" data-check-all aria-label="全选"></th>' + th
    body = []
    for r in rows:
        attrs = ""
        cells = r
        if isinstance(r, dict):
            cells = r["cells"]
            if r.get("href"):
                attrs += f' data-href="{r["href"]}"'
            if r.get("cat"):
                attrs += f' data-cat="{r["cat"]}"'
            if r.get("cls"):
                attrs += f' class="{r["cls"]}"'
        tds = "".join(f"<td>{c}</td>" for c in cells)
        if check:
            tds = '<td><input type="checkbox" aria-label="选择"></td>' + tds
        body.append(f"<tr{attrs}>{tds}</tr>")
    idattr = f' id="{id_}"' if id_ else ""
    return f'<div class="table-wrap {cls}"><table class="table"{idattr}><thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def pager(total, pages=5):
    nums = "".join(f'<button type="button" class="{"on" if i == 1 else ""}">{i}</button>' for i in range(1, pages + 1))
    size = '<select class="select pager-size" aria-label="每页条数"><option>15条/页</option><option>30条/页</option><option>50条/页</option></select>'
    return (f'<div class="pager"><span>共 {total} 条</span><button type="button" data-nav="prev" aria-label="上一页">{icon("chevron-left")}</button>{nums}'
            f'<button type="button" data-nav="next" aria-label="下一页">{icon("chevron-right")}</button>{size}</div>')


DANGER_OPS = {"删除", "注销", "驳回", "移除", "停用", "撤销", "转注销", "禁用"}


def ops(*links):
    """表格操作列：links 为 (文字, href) 或 (文字, None, toast)。"""
    out = []
    for l in links:
        cls = "link danger" if re_strip(l[0]) in DANGER_OPS else "link"
        if l[1]:
            out.append(f'<a class="{cls}" href="{l[1]}">{l[0]}</a>')
        else:
            out.append(f'<button class="{cls}" type="button" data-toast="{esc(l[2] if len(l) > 2 else "操作成功")}">{l[0]}</button>')
    return f'<div class="ops">{"".join(out)}</div>'


def field(label, control, req=False, hint="", cls="", err="此项为必填项"):
    r = '<span class="req">*</span>' if req else ""
    h = f'<div class="hint">{hint}</div>' if hint else ""
    e = f'<div class="err-msg">{err}</div>' if req else ""
    return f'<div class="field {cls}"><label>{r}{label}</label>{control}{h}{e}</div>'


def inp(ph="", val="", req=False, typ="text", attrs="", readonly=False):
    r = " required" if req else ""
    ro = " readonly" if readonly else ""
    v = f' value="{esc(val)}"' if val != "" else ""
    return f'<input class="input" type="{typ}" placeholder="{esc(ph)}"{v}{r}{ro} {attrs}>'


def sel(options, val=None, req=False, ph="请选择"):
    r = " required" if req else ""
    opts = f'<option value="">{ph}</option>' if ph else ""
    for o in options:
        s = " selected" if o == val else ""
        opts += f"<option{s}>{o}</option>"
    return f'<select class="select"{r}>{opts}</select>'


def textarea(ph="", val="", req=False, maxlen=0, rows=4):
    r = " required" if req else ""
    m = f' maxlength="{maxlen}" data-count' if maxlen else ""
    tip = f'<div class="count-tip">{len(val)} / {maxlen}</div>' if maxlen else ""
    return f'<textarea class="textarea" rows="{rows}" placeholder="{esc(ph)}"{r}{m}>{esc(val)}</textarea>{tip}'


def radios(name, options, checked=None, req=False):
    out = []
    for i, o in enumerate(options):
        c = " checked" if o == checked else ""
        r = " required" if req and i == 0 else ""
        out.append(f'<label class="radio"><input type="radio" name="{name}"{c}{r}>{o}</label>')
    return f'<div class="radios">{"".join(out)}</div>'


def upload(text="点击或拖拽文件到此处上传", hint="支持 jpg / png / pdf，单个文件不超过 10MB", files=()):
    chips = "".join(f'<span class="file-chip">{icon("file")}{f}</span>' for f in files)
    return (f'<label class="upload">{icon("upload", 22)}<div class="mt4">{text}</div><div class="small muted">{hint}</div>'
            f'<input type="file" multiple></label><div class="upload-list">{chips}</div>')


def alert(text, kind="info", ic=None):
    ic = ic or {"info": "info", "warning": "alert", "danger": "alert-circle", "success": "check-circle"}[kind]
    return f'<div class="alert alert-{kind}">{icon(ic)}<div class="grow">{text}</div></div>'


def kv(items, cols=3):
    c = {2: " c2", 3: "", 4: " c4"}[cols]
    out = []
    for it in items:
        k, v = it[0], it[1]
        full = ' class="full"' if len(it) > 2 and it[2] else ""
        out.append(f"<div{full}><dt>{k}</dt><dd>{v}</dd></div>")
    return f'<dl class="kv{c}">{"".join(out)}</dl>'


def timeline(items):
    """items: (状态 done/now/back/reject/wait, 标题, 元信息, 意见)。"""
    out = []
    for it in items:
        state, title, meta = it[0], it[1], it[2]
        comment = it[3] if len(it) > 3 and it[3] else ""
        c = f'<div class="tl-comment">{comment}</div>' if comment else ""
        out.append(f'<div class="tl-item {state}"><span class="tl-dot"></span><div class="tl-title">{title}</div>'
                   f'<div class="tl-meta">{meta}</div>{c}</div>')
    return f'<div class="tl">{"".join(out)}</div>'


def steps(names, current):
    """current 为当前步骤下标（从 0 开始）。"""
    out = []
    for i, n in enumerate(names):
        s = "done" if i < current else ("now" if i == current else "")
        no = icon("check", 14) if i < current else str(i + 1)
        line = '<span class="step-line"></span>' if i < len(names) - 1 else ""
        out.append(f'<div class="step {s}"><span class="step-no">{no}</span><span class="nowrap">{n}</span>{line}</div>')
    return f'<div class="steps">{"".join(out)}</div>'


def ptabs(items, active):
    """页面级页签：items 为 (文字, href)。"""
    out = []
    for text, href in items:
        on = ' class="on"' if text == active else ""
        out.append(f'<a href="{href}"{on}>{text}</a>')
    return f'<div class="ptabs">{"".join(out)}</div>'


def seg(items, active=None, target=""):
    """页内分段切换：items 为 (文字, 分类值)；target 为被过滤容器选择器。"""
    active = active or items[0][0]
    t = f' data-target="{target}"' if target else ""
    out = []
    for it in items:
        text, val = it[0], it[1]
        on = ' class="on"' if text == active else ""
        tst = "" if target else f' data-toast="已切换到：{esc(re_strip(text))}"'
        out.append(f'<button type="button" data-seg="{val}"{on}{tst}>{text}</button>')
    return f'<div class="seg"{t}>{"".join(out)}</div>'


def re_strip(s):
    import re
    return re.sub(r"<[^>]+>", "", str(s)).strip()


def chips(items, active=None, target=""):
    active = active or items[0][0]
    t = f' data-target="{target}"' if target else ""
    out = []
    for it in items:
        text, val = it[0], it[1]
        on = " on" if text == active else ""
        tst = "" if target else f' data-toast="已筛选：{esc(re_strip(text))}"'
        out.append(f'<button type="button" class="chip{on}" data-seg="{val}"{tst}>{text}</button>')
    return f'<div class="chips"{t}>{"".join(out)}</div>'


def progress(pct, color=""):
    return f'<div class="progress {color}"><i style="width:{pct}%"></i></div>'


def bars(data, max_val=None):
    """柱状图：data 为 (标签, 数值)。"""
    m = max_val or max(v for _, v in data)
    out = "".join(f'<div class="bar"><b>{v}</b><i style="height:{max(4, v / m * 140):.0f}px"></i><span>{k}</span></div>' for k, v in data)
    return f'<div class="bars">{out}</div>'


def hbars(data, color=""):
    m = max(v for _, v in data)
    return "".join(f'<div class="hbar"><span class="hbar-label ellipsis">{k}</span>{progress(v / m * 100, color)}'
                   f'<span class="hbar-val num">{v}</span></div>' for k, v in data)


CHART_COLORS = ["#2A8DC7", "#6AAFD8", "#67C23A", "#E6A23C", "#F56C6C", "#246991", "#95C6E3", "#909399"]


def donut(data, center_value, center_label):
    total = sum(v for _, v in data)
    stops, acc = [], 0
    for i, (_, v) in enumerate(data):
        c = CHART_COLORS[i % len(CHART_COLORS)]
        start = acc / total * 360
        acc += v
        stops.append(f"{c} {start:.1f}deg {acc / total * 360:.1f}deg")
    legend = "".join(f'<div class="legend-item"><span class="legend-dot" style="background:{CHART_COLORS[i % 8]}"></span>'
                     f'<span class="grow">{k}</span><b class="num">{v}</b></div>' for i, (k, v) in enumerate(data))
    return (f'<div class="flex gap24"><div class="donut" style="background:conic-gradient({",".join(stops)})">'
            f'<div class="donut-center"><div><div class="fs18 bold num">{center_value}</div><div class="small muted">{center_label}</div></div></div></div>'
            f'<div class="legend grow">{legend}</div></div>')


def result(kind, title, desc, actions="", extra=""):
    ic = {"ok": "check", "warn": "alert", "err": "x", "info": "info"}[kind]
    return (f'<div class="result"><div class="result-ic {kind}">{icon(ic)}</div><h2>{title}</h2><p>{desc}</p>'
            f'{extra}<div class="flex center gap12 mt24 wrap">{actions}</div></div>')


def diff_table(rows):
    """变更前后对比：rows 为 (字段, 变更前, 变更后)。值相同视为未变更。"""
    out = []
    for f, old, new in rows:
        changed = old != new
        cls = ' class="changed"' if changed else ""
        mark = tag("已变更", "warning") if changed else '<span class="muted small">未变更</span>'
        out.append(f'<tr{cls}><td class="bold">{f}</td><td class="{"old" if changed else ""}">{old}</td>'
                   f'<td class="{"new" if changed else ""}">{new}</td><td>{mark}</td></tr>')
    return (f'<div class="table-wrap diff"><table class="table"><thead><tr><th style="width:140px">字段</th><th>变更前</th>'
            f'<th>变更后</th><th style="width:90px">状态</th></tr></thead><tbody>{"".join(out)}</tbody></table></div>')


def page_hd(title, desc="", actions=""):
    d = f"<p>{desc}</p>" if desc else ""
    return f'<div class="page-hd"><div><h1>{title}</h1>{d}</div><div class="flex gap8">{actions}</div></div>'


def filter_bar(fields, search_target=""):
    """筛选区：fields 为 field() 结果列表；查询按钮给出反馈，重置按钮清空输入。"""
    return (f'<div class="filter" data-form>{"".join(fields)}<div class="filter-ops">'
            f'<button class="btn btn-primary" type="button" data-toast="已按条件查询，共找到符合条件的记录">{icon("search")}立即查询</button>'
            f'<button class="btn btn-ghost" type="button" data-toast="已重置筛选条件" onclick="this.closest(\'.filter\').querySelectorAll(\'input,select\').forEach(function(x){{x.value=\'\'}})">重置</button></div></div>')


def modal(title, body, footer, size="", close_href=None):
    x = (f'<a class="x-btn" href="{close_href}" aria-label="关闭">{icon("x")}</a>' if close_href
         else f'<button class="x-btn" type="button" data-back="{NAV}" aria-label="关闭">{icon("x")}</button>')
    return (f'<div class="mask"><div class="modal {size}"><div class="modal-hd">{title}{x}</div>'
            f'<div class="modal-bd">{body}</div><div class="modal-ft">{footer}</div></div></div>')


def drawer(title, body, footer, close_href):
    return (f'<div class="mask drawer-mask"><div class="drawer"><div class="modal-hd">{title}'
            f'<a class="x-btn" href="{close_href}" aria-label="关闭">{icon("x")}</a></div>'
            f'<div class="modal-bd">{body}</div><div class="modal-ft">{footer}</div></div></div>')


# ---------------------------------------------------------------- 文件输出
PC_ZOOM = ("<script>(function(){var d=document.documentElement;function f(){var z=Math.max(.6,Math.min(innerWidth/1920,1.6));"
           "d.style.zoom=z;d.style.setProperty('--z',z);}f();addEventListener('resize',f);})();</script>")


def _doc(title, body, css, js, body_cls="", head=""):
    bc = f' class="{body_cls}"' if body_cls else ""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · 团学新媒体平台</title>
<style>{css}</style>{head}
</head>
<body{bc}>
{body}
<script>{BASE_JS}{js}</script>
</body>
</html>
"""


WRITTEN = []


def write(rel_path, title, body, css="", js="", body_cls="", kind="plain"):
    css_all = BASE_CSS + (PC_CSS if kind == "pc" else "") + (APP_CSS if kind == "app" else "") + css
    path = ROOT / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if kind == "pc":
        body_cls = (body_cls + " pc").strip()
    path.write_text(_doc(title, body, css_all, js, body_cls, PC_ZOOM if kind == "pc" else ""), encoding="utf-8")
    WRITTEN.append(rel_path)


def proto_nav(href=NAV):
    return f'<a class="proto-nav" href="{href}">{icon("grid", 14)}返回原型导航</a>'


# ---------------------------------------------------------------- PC 外壳
PC_ROLES = {
    "school": {
        "name": "陈静", "role": "学校管理员", "org": "校团委宣传部", "msg": "messages.html",
        "menu": [
            ("工作台", [("dashboard", "数据驾驶舱", "dashboard", "dashboard.html", 0), ("messages", "消息待办", "bell", "messages.html", 6)]),
            ("账号管理", [("accounts", "全校账号库", "database", "accounts.html", 0), ("organizations", "组织管理", "hierarchy", "organizations.html", 0)]),
            ("业务审核", [("approvals", "审核待办", "file-check", "approvals.html", 13),
                        ("annual", "年度年审", "calendar", "annual-tasks.html", 0)]),
            ("风险治理", [("zombie", "僵尸号排查", "ghost", "zombie.html", 47), ("anomalies", "数据异常", "alert", "anomalies.html", 0),
                        ("rectify", "整改管理", "wrench", "rectify.html", 0)]),
            ("数据中心", [("import", "数据导入", "upload", "import.html", 0), ("export", "数据导出", "download", "export.html", 0)]),
            ("系统管理", [("users", "用户权限", "users", "users.html", 0), ("settings", "系统配置", "settings", "settings-workflow.html", 0),
                        ("logs", "操作日志", "log", "logs.html", 0)]),
        ],
    },
    "college": {
        "name": "周建华", "role": "学院管理员", "org": "计算机学院团委", "msg": "messages.html",
        "menu": [
            ("工作台", [("workbench", "学院工作台", "dashboard", "workbench.html", 0), ("messages", "消息待办", "bell", "messages.html", 5)]),
            ("账号管理", [("accounts", "本院账号", "database", "accounts.html", 0), ("organizations", "本院组织", "hierarchy", "organizations.html", 0)]),
            ("业务审核", [("approvals", "审核待办", "file-check", "approvals.html", 6), ("annual", "年审统筹", "calendar", "annual-progress.html", 0)]),
            ("任务与人员", [("assign", "任务分派", "route", "assign.html", 0), ("teachers", "教师工作量", "users", "teachers.html", 0)]),
            ("风险治理", [("zombie", "僵尸号核实", "ghost", "zombie.html", 3), ("rectify", "整改管理", "wrench", "rectify.html", 0)]),
            ("数据与系统", [("import", "导入数据确认", "upload", "import-confirm.html", 0), ("export", "数据导出", "download", "export.html", 0),
                          ("users", "本院授权", "key", "users.html", 0), ("logs", "操作日志", "log", "logs.html", 0)]),
        ],
    },
    "teacher": {
        "name": "王晓琳", "role": "业务教师", "org": "计算机学院 · 宣传工作辅导员", "msg": "messages.html",
        "menu": [
            ("工作台", [("workbench", "教师工作台", "dashboard", "workbench.html", 0), ("messages", "消息提醒", "bell", "messages.html", 3)]),
            ("审核办理", [("todo", "审核待办", "inbox", "todo.html", 9), ("done", "审核已办", "file-check", "done.html", 0)]),
            ("账号管理", [("accounts", "我负责的账号", "database", "accounts.html", 0), ("proxy", "代办中心", "hand", "proxy.html", 0),
                        ("apply", "发起申请", "file-add", "../common/apply-create-basic.html", 0)]),
        ],
    },
}


ROLE_HOME = {"school": "dashboard.html", "college": "workbench.html", "teacher": "workbench.html"}
ROLE_TODO = {"school": "approvals.html", "college": "approvals.html", "teacher": "todo.html"}
# 正式系统“我的待办”模块侧栏：业务审核统一在此办理
WF_MENU = {
    role: [("todo", "待办", "inbox", ROLE_TODO[role], n),
           ("done", "已办", "file-check", "done.html" if role == "teacher" else "wf-done.html", 0),
           ("started", "已发起", "send", "wf-started.html", 0),
           ("cc", "催办/抄送", "bell", "wf-cc.html", m),
           ("batch", "批量审批", "layers", "wf-batch.html", 0)]
    for role, n, m in (("school", 13, 2), ("college", 6, 2), ("teacher", 9, 3))
}
ROLE_BY_NAME = {"学校管理员": "school", "学院管理员": "college", "业务教师": "teacher"}
TOP_NAV = ["首页", "我的待办", "个人信息", "数据统计", "学生事务管理", "学工队伍建设", "第二课堂", "新媒体平台"]
OUT_OF_SCOPE = "原型仅包含「团学新媒体平台」模块，其他模块为正式系统已有功能"


def _pc_shell(role, prefix, title, crumbs, content, back, active=None, side=True, self_file="", module=""):
    """正式系统外壳：顶部横幅 + 顶部模块导航 + 左侧蓝色菜单 + 页签栏 + 页脚。prefix 为到角色目录的相对前缀。
    module="wf" 时切换为“我的待办”模块（顶部导航高亮“我的待办”，侧栏为待办菜单）。"""
    r = PC_ROLES[role]
    home, todo = prefix + ROLE_HOME[role], prefix + ROLE_TODO[role]
    wf = module == "wf"
    on = ' class="on"'
    tops = []
    for t in TOP_NAV:
        if t == "新媒体平台":
            tops.append(f'<a{"" if wf else on} href="{home}">{t}</a>')
        elif t == "首页":
            tops.append(f'<a href="{home}">{t}</a>')
        elif t == "我的待办":
            tops.append(f'<a{on if wf else ""} href="{todo}">{t}</a>')
        else:
            tops.append(f'<button type="button" data-toast="{OUT_OF_SCOPE}">{t}</button>')
    tops.append(f'<button class="zx-more" type="button" data-toast="{OUT_OF_SCOPE}" aria-label="更多模块">{icon("chevrons-right", 16)}</button>')
    msg_badge = r["menu"][0][1][1][4]
    header = f"""<header class="zx-hd">
  <a class="zx-logo" href="{home}" aria-label="中南大学智慧学工"></a>
  <nav class="zx-topnav">{''.join(tops)}</nav>
  <div class="zx-user">
    <a class="zx-bell" href="{prefix}{r['msg']}" aria-label="消息">{icon('bell', 22)}<span class="badge">{msg_badge}</span></a>
    <a class="zx-me" href="{prefix}../common/identity-switch.html" title="切换身份">{avatar(r['name'])}<div><b>{r['name']}</b><small>{r['role']} · {r['org']}</small></div>{icon('chevron-down')}</a>
    <a class="zx-manual" href="{prefix}../common/login.html" title="退出登录">{icon('logout', 14)}退出</a>
    <a class="zx-manual" href="{NAV}">{icon('grid', 14)}原型导航</a>
  </div>
</header>"""
    aside = ""
    if side:
        nav = []
        for group, items in ([("我的待办", WF_MENU[role])] if wf else r["menu"]):
            nav.append(f'<div class="zx-group">{group}</div>')
            for key, text, ic, href, badge in items:
                on = ' class="on"' if key == active else ""
                b = f'<span class="badge">{badge}</span>' if badge else ""
                nav.append(f'<a href="{prefix}{href}"{on}>{icon(ic)}<span class="ellipsis">{text}</span>{b}</a>')
        aside = f'<aside class="zx-aside">{"".join(nav)}</aside>'
    tabs = [f'<button class="zx-back" type="button" data-back="{back}">{icon("chevron-left")}返回上一步</button>']
    seen = set()
    for t, h in crumbs[:-1]:
        if h and t not in seen and h != self_file:
            seen.add(t)
            tabs.append(f'<a class="zx-tab" href="{h}">{t}</a>')
    cur = crumbs[-1][0] if crumbs else title
    tabs.append(f'<span class="zx-tab on">{cur}<button class="zx-x" type="button" data-back="{back}" aria-label="关闭页签">{icon("x")}</button></span>')
    tabs.append(f'<button class="zx-fold" type="button" data-toast="已收起其他页签" aria-label="页签操作">{icon("chevron-down")}</button>')
    return f"""<div class="zx-app">
{header}
<div class="zx-body{'' if side else ' is-full'}">{aside}
<section class="zx-main">
  <div class="zx-tabs">{''.join(tabs)}</div>
  <div class="content">{content}</div>
</section>
</div>
<footer class="zx-ft">2026 © 中南大学智慧学工 · 团学新媒体平台 By wonsun Technology.</footer>
</div>"""


WF_OP_KIND = {"同意": "success", "提交": "success", "重新提交": "success", "发布任务": "success", "下发": "success",
              "自动预警": "warning", "退回": "warning", "要求整改": "warning", "继续整改": "warning", "建议注销": "warning",
              "转注销": "warning", "同意注销": "success", "驳回": "danger", "终止": "danger"}
WF_ZOOM = ("var c=this.closest('.wf-chart'),s=Math.round(Math.max(.5,Math.min(1.5,(+c.dataset.s||1)+{d}))*10)/10;"
           "c.dataset.s=s;c.querySelector('.wf-flow').style.transform='scale('+s+')';"
           "c.querySelector('.wf-pct').textContent=Math.round(s*100)+'%'")


def wf_dialog(spec, content, close):
    """流程办理弹窗（对齐正式系统待办“办理”）：表单信息 / 抄送人 / 流程图 / 当前审批人 / 审批记录。"""
    name, recs, appr = spec["name"], spec["records"], spec["approvers"]
    panes = [("form", "表单信息"), ("cc", "抄送人"), ("chart", "流程图"), ("appr", "当前审批人"), ("rec", "审批记录")]
    on = ' class="on"'
    tabs = "".join(f'<button type="button" data-choice="#wf-p-{k}"{on if k == "form" else ""}>{t}</button>' for k, t in panes)

    def empty(n):
        return f'<tr><td colspan="{n}" class="wf-empty">暂无数据</td></tr>'
    cc_rows = [[str(i + 1), name, c[0], c[1], c[2], c[3], c[4]] for i, c in enumerate(spec["cc"])]
    cc = table(["序号", "流程名称", "任务名称", "抄送人", "被抄送人", "任务创建时间", "抄送时间"], cc_rows)
    if not cc_rows:
        cc = cc.replace("<tbody></tbody>", f"<tbody>{empty(7)}</tbody>")
    boxes = ['<div class="wf-end">开始</div>']
    for n, h, s in spec["nodes"]:
        boxes.append(f'<i class="wf-arrow {s}"></i><div class="wf-node {s}">{icon("user", 16)}<b>{n}</b><small>{h}</small></div>')
    boxes.append(f'<i class="wf-arrow wait"></i><div class="wf-end">结束</div>')
    chart = (f'<div class="wf-chart" data-s="1"><div class="wf-zoom">'
             f'<button type="button" onclick="{WF_ZOOM.format(d="-.1")}" aria-label="缩小">{icon("zoom-out")}</button>'
             f'<span class="wf-pct">100%</span>'
             f'<button type="button" onclick="{WF_ZOOM.format(d=".1")}" aria-label="放大">{icon("zoom-in")}</button></div>'
             f'<div class="wf-flow">{"".join(boxes)}</div>'
             f'<div class="wf-legend"><span class="done">已完成</span><span class="now">当前环节</span><span class="wait">未开始</span></div></div>')
    ap_rows = [[str(i + 1), a[0], a[1], a[2] or "—", a[3] or "—"] for i, a in enumerate(appr)]
    ap = table(["序号", "审批人登录名", "审批人姓名", "被委托人", "处理时间"], ap_rows)
    if not ap_rows:
        ap = ap.replace("<tbody></tbody>", f"<tbody>{empty(5)}</tbody>")
    total, done = len(recs) + len(appr), len(recs)
    stats = [("总人次", total, "users", "#2A8DC7"), ("已提交", done, "check", "#67C23A"), ("未提交", len(appr), "clock", "#E6A23C"),
             ("已查看", total, "eye", "#6AAFD8"), ("未查看", 0, "eye-off" if "eye-off" in ICONS else "eye", "#909399")]
    cards = "".join(f'<div class="wf-stat"><span style="background:{c}">{icon(ic, 20)}</span><div><b>{v}</b><small>{t}</small></div></div>'
                    for t, v, ic, c in stats)
    rec_rows = [[str(i + 1), r[0], r[1], r[2] or "—", tag(r[3], WF_OP_KIND.get(r[3], "primary")),
                 f'<span class="wf-cm">{r[4] or "—"}</span>', r[5], "—"] for i, r in enumerate(recs)]
    for a in appr:
        now = next((n for n, _, s in spec["nodes"] if s == "now"), "")
        rec_rows.append([str(len(rec_rows) + 1), now, a[1], "—", tag("审批中", "primary"), "—", "—", "—"])
    rec = table(["序号", "流程环节", "实际审批人", "受委托人", "审批操作", "审批意见", "处理时间", "附件"], rec_rows)
    return f"""<div class="mask wf-mask"><div class="wf-dialog" role="dialog" aria-label="{name}">
  <div class="wf-hd"><b>{name}</b><button class="x-btn" type="button" data-back="{close}" aria-label="关闭">{icon("x")}</button></div>
  <div class="wf-bd">
    <div class="wf-tabs" data-single=".wf-pane">{tabs}</div>
    <div class="wf-meta"><b>{name}</b><span class="wf-chip">{icon("user", 14)}发起人：{spec["starter"]}</span><span class="wf-sub">{spec["sub"]}</span></div>
    <div class="wf-pane" id="wf-p-form">{content}</div>
    <div class="wf-pane hidden" id="wf-p-cc">{cc}</div>
    <div class="wf-pane hidden" id="wf-p-chart">{chart}</div>
    <div class="wf-pane hidden" id="wf-p-appr">{ap}</div>
    <div class="wf-pane hidden" id="wf-p-rec"><div class="wf-stats">{cards}</div>{rec}</div>
  </div>
</div></div>"""


def pc_page(rel_path, role, active, title, crumbs, content, css="", js="", module=""):
    """PC 角色页面：正式系统外壳 + 角色菜单。crumbs 为 [(文字, href或None)]，渲染为页签。
    已登记流程的审核页自动以“我的待办 · 流程办理”弹窗呈现，背景为本角色待办列表。"""
    from wf import WF_DIALOGS
    spec = WF_DIALOGS.get(rel_path)
    if spec:
        from pages_wf import todo_content
        todo = ROLE_TODO[role]
        content = f'<div class="backdrop">{todo_content(role)}</div>' + wf_dialog(spec, content, todo)
        crumbs, back, active, module = [("待办", None)], todo, "todo", "wf"
    else:
        back = next((h for _, h in reversed(crumbs) if h), ROLE_HOME[role])
    body = _pc_shell(role, "", title, crumbs, content, back, active, self_file=Path(rel_path).name, module=module)
    write(rel_path, title, body, css, js, kind="pc")


def pc_common_page(rel_path, title, crumbs, content, css="", js="", back="../teacher/workbench.html", who="王晓琳", who_role="业务教师",
                   side=True, active=None):
    """PC 公共页面（档案、申请、弹窗等）：沿用当前身份的菜单，菜单高亮按页签文字自动匹配。"""
    role = ROLE_BY_NAME.get(who_role, "teacher")
    if active is None:
        texts = {re_strip(t) for t, _ in crumbs}
        for _, items in PC_ROLES[role]["menu"]:
            for key, text, *_ in items:
                if text in texts and active is None:
                    active = key
    body = _pc_shell(role, f"../{role}/", title, crumbs, content, back, active, side,
                     Path(rel_path).name)
    write(rel_path, title, body, css, js, kind="pc")


# ---------------------------------------------------------------- APP 外壳
APP_TABS = {
    "student": [("apply", "服务大厅", "grid", "apply.html", 0), ("home", "首页", None, "home.html", 0), ("mine", "个人中心", "user", "mine.html", 0)],
    "teacher": [("todo", "待我审核", "inbox", "todo.html", 9), ("home", "工作台", None, "home.html", 0), ("mine", "个人中心", "user", "mine.html", 0)],
    "college": [("todo", "学院审核", "inbox", "todo.html", 4), ("home", "看板", None, "home.html", 0), ("mine", "个人中心", "user", "mine.html", 0)],
}
APP_TAB_ALIAS = {"annual": "apply"}
APP_ROLE_NAME = {"student": "学生用户 · 李明", "teacher": "业务教师 · 王晓琳", "college": "学院管理员 · 周建华", "common": "全部角色"}


def app_page(rel_path, role, title, content, tab=None, back=None, right="", bottom="", overlay="",
             notes=None, flow=None, blue=False, css="", js="", nav_title=None):
    """APP 页面：居中手机外框 + 右侧页面说明。

    back: 返回按钮的兜底页面（有值时显示返回箭头）；tab: 高亮的底部 Tab key（None 不显示 Tab Bar）；
    bottom: 底部固定操作栏 HTML；overlay: 叠加在手机内的弹层（底部面板或对话框）；
    notes: 本页交互说明列表；flow: 业务链路 [(文字, href)]。
    """
    status = (f'<div class="status"><span>9:41</span><span class="sig">{icon("signal")}{icon("wifi")}{icon("battery")}</span></div>')
    left = (f'<button class="nav-l" type="button" data-back="{back}" aria-label="返回">{icon("chevron-left")}</button>' if back else "")
    r = f'<div class="nav-r">{right}</div>' if right else ""
    navbar = f'<div class="navbar">{left}<div class="title">{nav_title if nav_title is not None else title}</div>{r}</div>'
    tabbar = ""
    if tab and role in APP_TABS:
        items = []
        cur = APP_TAB_ALIAS.get(tab, tab)
        for key, text, ic, href, badge in APP_TABS[role]:
            on = " on" if key == cur else ""
            b = f'<span class="badge">{badge}</span>' if badge else ""
            if ic is None:
                items.append(f'<a class="tab-c{on}" href="{href}"><img src="../../assets/m-center-logo.png" alt="中南大学"><span>{text}</span></a>')
            else:
                items.append(f'<a class="{on.strip()}" href="{href}">{icon(ic)}<span>{text}</span>{b}</a>')
        tabbar = f'<nav class="tabbar">{"".join(items)}</nav>'
    bb = f'<div class="bottom-bar">{bottom}</div>' if bottom else ""
    note_items = "".join(f"<li>{n}</li>" for n in (notes or []))
    flow_html = ""
    if flow:
        links = "".join(f'<a href="{h}">{icon("arrow-right", 14)}{t}</a>' for t, h in flow)
        flow_html = f'<div class="card flow"><div class="bold">业务链路 · 下一步</div>{links}</div>'
    body = f"""<div class="phone{' blue-top' if blue else ''}">
  {status}{navbar}
  <div class="scroll">{content}</div>
  {bb}{tabbar}{overlay}<span class="home-ind"></span>
</div>
<aside class="notes">
  <div class="card"><div class="small muted">{APP_ROLE_NAME.get(role, '')} · 移动端</div><h3>{title}</h3>
  <div class="small muted mb12">{rel_path}</div><ul>{note_items}</ul></div>
  {flow_html}
  <a class="btn btn-default" href="{NAV}">{icon('grid')}返回原型导航</a>
</aside>"""
    write(rel_path, title, body, css, js, body_cls="app-stage", kind="app")


# ---------------------------------------------------------------- 移动端组件
def cell(label, value="", href=None, arrow=None, attrs=""):
    arrow = arrow if arrow is not None else bool(href)
    a = icon("chevron-right", cls="arrow") if arrow else ""
    inner = f'<span class="cell-label">{label}</span><span class="cell-value">{value}</span>{a}'
    if href:
        return f'<a class="cell" href="{href}" {attrs}>{inner}</a>'
    return f'<div class="cell" {attrs}>{inner}</div>'


def m_input(label, ph="请输入", val="", req=False, typ="text"):
    r = '<span class="req">*</span>' if req else ""
    rq = " required" if req else ""
    v = f' value="{esc(val)}"' if val else ""
    return (f'<div class="cell"><span class="cell-label">{r}{label}</span><input class="m-input" type="{typ}" placeholder="{ph}"{v}{rq}>'
            f'</div>')


def m_select(label, options, val=None, req=False):
    r = '<span class="req">*</span>' if req else ""
    rq = " required" if req else ""
    opts = '<option value="">请选择</option>' + "".join(f"<option{' selected' if o == val else ''}>{o}</option>" for o in options)
    return (f'<div class="cell"><span class="cell-label">{r}{label}</span>'
            f'<select class="m-input" style="appearance:none;direction:rtl"{rq}>{opts}</select>{icon("chevron-right", cls="arrow")}</div>')


def m_textarea(label, ph="请输入", val="", req=False, maxlen=0):
    r = '<span class="req">*</span>' if req else ""
    rq = " required" if req else ""
    m = f' maxlength="{maxlen}" data-count' if maxlen else ""
    tip = f'<div class="count-tip">{len(val)} / {maxlen}</div>' if maxlen else ""
    return (f'<div class="cell col-cell"><span class="cell-label">{r}{label}</span>'
            f'<textarea class="m-textarea" placeholder="{ph}"{rq}{m}>{esc(val)}</textarea>{tip}<div class="err-msg">此项为必填项</div></div>')


def m_radios(label, name, options, checked=None):
    return f'<div class="cell col-cell"><span class="cell-label">{label}</span>{radios(name, options, checked)}</div>'


def m_steps(names, current):
    out = []
    for i, n in enumerate(names):
        s = "done" if i < current else ("now" if i == current else "")
        no = "✓" if i < current else str(i + 1)
        out.append(f'<div class="m-step {s}"><b>{no}</b><span>{n}</span></div>')
    return f'<div class="m-steps">{"".join(out)}</div>'
