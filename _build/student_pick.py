"""李明可办理的账号。列表带账号进入表单；业务申请不带账号时先选择。"""
import json

from data import ACCOUNTS, FLOWS

# key、PC 查看页、手机查看页。顺序与「我的账号」一致。
_SPEC = (
    ("annual", "account-annual.html", "account-detail.html?acct=annual"),
    ("rename", "account-detail.html", "account-detail.html?acct=rename"),
    ("handover", "account-handover.html", "account-detail.html?acct=handover"),
    ("photo", "account-photo.html", "account-detail.html?acct=photo"),
    ("new", "application-detail.html", "application-detail.html"),
)

_REASON = FLOWS["rename"]["steps"][0][3]


def liming_rows():
    rows = []
    for key, pc_view, app_view in _SPEC:
        a = ACCOUNTS[key]
        rows.append({
            "key": key,
            "name": a["name"],
            "platform": a["platform"],
            "pid": a["pid"],
            "run": a.get("run") or "",
            "filing": a.get("filing") or "",
            "after": a.get("new_name") or "",
            "pc_view": pc_view,
            "app_view": app_view,
        })
    return rows


def is_cancelled(row):
    return row["run"] == "已注销" or row["filing"] == "已注销"


def operable():
    return [r for r in liming_rows() if not is_cancelled(r)]


def pick_buttons():
    items = []
    for r in operable():
        items.append(
            '<button type="button" class="pick-item" onclick="pickAcct(\'' + r["key"] + '\')">'
            "<span><b>" + r["name"] + "</b>"
            '<span class="muted small"> 平台 ' + r["platform"] + " · 编号 " + r["pid"] + "</span></span>"
            '<span class="pick-act" style="color:var(--c-primary)">选择</span></button>'
        )
    return "".join(items)


def picked_input():
    return '<input type="hidden" id="picked-acct" value="">'


def _payload():
    data = []
    for r in operable():
        data.append({
            "key": r["key"],
            "name": r["name"],
            "platform": r["platform"],
            "pid": r["pid"],
            "after": r["after"],
            "run": r["run"],
            "reason": _REASON if r["key"] == "rename" else "",
        })
    return json.dumps(data, ensure_ascii=False)


_JS = """
function pickAcct(key, silent){
  var a=null,i;
  for(i=0;i<ACCTS.length;i++){if(ACCTS[i].key===key){a=ACCTS[i];break;}}
  if(!a){if(!silent)toast('请先选择账号');return;}
  var hid=document.getElementById('picked-acct');
  if(hid)hid.value=key;
  var pick=document.getElementById('acct-pick');
  var form=document.getElementById('acct-form');
  if(pick)pick.classList.add('hidden');
  if(form)form.classList.remove('hidden');
  var label=a.name+' · '+a.platform+' · '+a.pid;
  var sub=document.getElementById('acct-sub');
  if(sub)sub.textContent='当前办理：'+label;
  var now=document.getElementById('acct-now-name');
  var meta=document.getElementById('acct-now-meta');
  if(now)now.textContent=a.name;
  if(meta)meta.textContent=a.platform+' · '+a.pid;
  var map={
    'chg-acct':a.name+' · '+a.pid,
    'chg-before':a.name,
    'chg-after':a.after||'',
    'chg-id-label':a.name+' · '+a.pid,
    'cancel-acct':a.name+'（'+a.platform+'）',
    'cancel-pid':a.pid,
    'cancel-run':a.run||'',
    'ho-acct':label
  };
  Object.keys(map).forEach(function(id){
    var el=document.getElementById(id);
    if(!el)return;
    if(el.tagName==='INPUT'||el.tagName==='TEXTAREA'||el.tagName==='SELECT'){
      el.value=map[id];
      if(el.tagName==='TEXTAREA')el.dispatchEvent(new Event('input',{bubbles:true}));
    }else el.textContent=map[id];
  });
  var reason=document.getElementById('chg-reason');
  if(reason){
    reason.value=a.reason||'';
    reason.dispatchEvent(new Event('input',{bubbles:true}));
  }
  if(!silent)toast('已选择：'+a.name);
}
function bootAcct(){
  var q=location.search||'';
  var m=q.match(/[?&]acct=([^&]*)/);
  if(!m)return;
  var key=decodeURIComponent(m[1]||'');
  if(key)pickAcct(key,true);
}
document.addEventListener('click',function(e){
  var node=e.target;
  if(!node||!node.closest)return;
  var t=node.closest('[data-submit]');
  if(!t)return;
  var hid=document.getElementById('picked-acct');
  if(hid&&!hid.value){
    e.stopPropagation();
    e.preventDefault();
    toast('请先选择账号');
  }
},true);
bootAcct();
"""


def page_js():
    return "var ACCTS=" + _payload() + ";" + _JS
