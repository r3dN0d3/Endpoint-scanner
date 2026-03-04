#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
☠ ENDPOINTSCANNER GUI — Symfony v1.4 — ARCHIVO ÚNICO STANDALONE
Requisitos: pip install requests urllib3 colorama
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading, queue, sys, re, json, csv, time, random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse, urlunparse
from typing import Optional, List, Dict, Any, Set, Tuple

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

# ══════════════════════════════════════════════
#  TEMA
# ══════════════════════════════════════════════
BG="#0d0d0d";BG2="#141414";BG3="#1a1a1a"
ACCENT="#00ff88";ACCENT2="#ff3c5f";ACCENT3="#00cfff"
YELLOW="#ffd700";GRAY="#3a3a3a";GRAY2="#2a2a2a"
FG="#e0e0e0";FG2="#777777"
FONT_MONO=("Courier New",10);FONT_SM=("Courier New",9)

# ══════════════════════════════════════════════
#  RUTAS — copiadas exactas de main.py
# ══════════════════════════════════════════════
COMMON_PATHS: List[str] = [
    "/js/fos_js_routes.json","/.docs/vams-api.md","/.docs/vams-webhooks.md",
    "/Readme.md","/_babel.config.js","/bitbucket-pipelines.yml","/deploy.sh",
    "/phpunit.xml.dist","/symfony.lock","/webpack.config.js","/js/routes.json",
    "/js/routing.json","/js/fos_js_routes.js","/js/routing.js",
    "/bundles/fosjsrouting/js/router.js","/bundles/fosjsrouting/js/router.min.js",
    "/_wdt/{token}","/_profiler/","/_profiler/search","/_profiler/search_bar",
    "/_profiler/phpinfo","/_profiler/xdebug","/_profiler/font/{fontName}.woff2",
    "/_profiler/open","/_profiler/{token}","/_profiler/{token}/router",
    "/_profiler/{token}/exception","/_profiler/{token}/exception.css",
    "/_profiler/{token}/search/results","/account","/movements",
    "/download/{id}","/category/{slug}","/","/categories","/events",
    "/save-cookies","/save-all-cookies","/save-required-cookies",
    "/open-contact","/contact","/exchange-code","/verify-exchange-code",
    "/event/{slug}","/product/{id}","/reset-password",
    "/reset-password/check-email","/reset-password/reset/{token}",
    "/build/manifest.json","/build/entrypoints.json","/build/runtime.js",
    "/build/app.js","/build/app.css","/build/vendor.js",
    "/login","/logout","/admin","/admin/login","/admin/dashboard",
    "/user/login","/dashboard","/easyadmin",
    "/api/users","/api/v1/users","/api/v1/token","/api/login_check",
    "/api/doc","/api/docs","/api/swagger","/api/platform","/api/graphql",
    "/swagger","/swagger-ui","/_docs","/api/doc.json","/api/v1/doc",
    "/debug/","/adminer","/_fragment","/_error/404","/_error/500",
    "app_dev.php/_profiler","app_dev.php/_wdt",
    "/authentication_token","/connect/{provider}","/login/check-{provider}",
    "/graphql-playground","/playground","/voyager","/altair",
    "/.well-known/mercure","/mercure","/phpmyadmin","/pma",
    "/bundles/easyadmin/","/bundles/sonataadmin/",
    "/.env","/.env.test","/.env.example","/.env.local","/.env.prod",
    "/.git/HEAD","/.git/config","/.svn/entries",
    "/composer.json","/package.json","/yarn.lock",
    "/.htaccess","/.htpasswd","/.DS_Store",
    "/server-status","/server-info","package-lock.json",
    "npm-shrinkwrap.json","node_modules/",
    "/maintenance","/register","/register/check-email","/register/confirmed",
    "/resetting/request","/resetting/check-email","/resetting/reset",
    "/resetting/reset/abcdef1234","/profile","/profile/edit",
    "/profile/show","/profile/change-password","/confirm/abcdef1234",
    "/reset-password/reset","/reset-password/reset/abcdef1234",
    "/verify/email","/verify-email","/verify-email/abcdef1234",
    "/2fa","/2fa_check","/2fa/qr-code",
    "/api","/api/docs","/api/docs.jsonld","/api/docs.json",
    "/api/contexts/EntryPoint","/docs","/swagger.json","/openapi.json",
    "/graphql","/graphiql","/login_check","/api/login_check",
    "/token/refresh","/api/token/refresh",
    "/oauth/v2/token","/oauth/v2/auth","/oauth/authorize",
    "/oauth/token","/oauth/refresh_token","/connect/",
    "/admin/logout","/admin/resetting/request","/admin/resetting/reset/abcdef",
    "/adminer.php","/_profiler/abcdef","/_wdt/abcdef","/_errors/500",
    "/phpinfo.php","/info.php","/index.php","/app.php","/app_dev.php",
    "/bundles/","/vendor/","/composer.lock",
    "/health","/healthz","/ready","/status","/ping","/_ping","/metrics",
    "/robots.txt","/sitemap.xml","/sitemap_index.xml","/sitemap.xml.gz",
    "/sitemap1.xml","/sitemap2.xml",
    "/.well-known/security.txt","/.well-known/change-password",
    "/.well-known/openid-configuration","/.well-known/jwks.json",
    "/.well-known/assetlinks.json","/.well-known/apple-app-site-association",
]

BACKUP_PATHS: List[str] = [
    "/backup/","/backups/","/_backup/","/_backups/",
    "/var/backups/","/storage/backups/","/tmp/backups/",
    "/db/backup/","/database/backup/","/mysql/backup/","/pg/backup/",
    "/dump.sql","/dump.sql.gz","/dump.sql.zip","/dump.tar.gz",
    "/database.sql","/database.sql.gz","/database.sql.zip",
    "/db.sql","/db.sql.gz","/db.sql.zip",
    "/export.sql","/export.sql.gz","/mysql.sql","/postgres.sql",
    "/backup.sql","/backup.sql.gz","/backup.tar.gz",
    "/.env.bak","/.env.backup","/.env.old","/.env~",
    "/.env.local.bak","/.env.prod.bak",
    "/parameters.yml.bak","/parameters.yml~","/parameters.yaml.bak",
    "/config/packages/prod/framework.yaml.bak",
    "/composer.json.bak","/composer.lock.bak",
    "/symfony.lock.bak","/.htaccess.bak","/.htaccess~",
    "/backup.zip","/backups.zip","/site-backup.zip",
    "/backup.tar","/backup.tar.gz","/backup.tgz",
    "/full-backup.zip","/public-backup.zip","/app-backup.zip",
    "/.env.save","/.env.tmp","/.env.swp","/.env.swo",
    "/parameters.yml.orig","/parameters.yml.save",
    "/.env.copy","/.env.tmp.bak",
]

SENSITIVE_BASENAMES=[ ".env",".env.local",".env.prod","composer.json",
    "composer.lock","symfony.lock","parameters.yml","parameters.yaml",
    "config/packages/prod/framework.yaml","config/services.yaml",
    ".htaccess","public/index.php","app.php","app_dev.php"]
BACKUP_SUFFIXES=[".bak",".old",".orig",".save","~",".tmp",".swp",".swo",
                 ".zip",".tar",".tar.gz",".tgz",".gz",".7z",".rar"]
BACKUP_DIRS=["/","/public/","/web/","/var/","/var/backups/",
             "/backup/","/backups/","/tmp/","/storage/backups/"]

def gen_backup_candidates() -> List[str]:
    out: List[str]=[]
    for base in SENSITIVE_BASENAMES:
        for d in BACKUP_DIRS:
            for suf in BACKUP_SUFFIXES:
                out.append(f"{d}{base}{suf}")
    for d in BACKUP_DIRS:
        for n in ["dump","database","db","backup","export","mysql","postgres"]:
            for ext in [".sql",".sql.gz",".sql.zip",".tar.gz",".zip",".tgz"]:
                out.append(f"{d}{n}{ext}")
    out+=["/backup/","/backups/","/_backup/","/_backups/","/db/backup/",
          "/database/backup/","/mysql/backup/","/pg/backup/",
          "/storage/backups/","/var/backups/","/tmp/backups/"]
    seen=set();uniq=[]
    for p in out:
        if p not in seen: uniq.append(p);seen.add(p)
    return uniq

# ══════════════════════════════════════════════
#  PLACEHOLDERS & FUZZ — copiados exactos
# ══════════════════════════════════════════════
PLACEHOLDER_RE=re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")
SEED_VALUES: Dict[str,str]={"id":"1","token":"abcdef1234","slug":"test-slug",
    "provider":"google","code":"404","_format":"json","fontName":"OpenSans-Regular"}
FUZZ_CATALOG: Dict[str,List[str]]={
    "id":["1","2","3","5","10","25","50","100","999","0","-1"],
    "token":["abcdef1234","deadbeef","0123456789abcdef",
             "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","12345678","0000000000000000","cafebabedeadbeef"],
    "slug":["test","admin","profile","config","sitemap","api","graphql","docs"],
    "provider":["google","github","facebook","twitter","microsoft","azure","apple"],
    "code":["200","302","400","401","403","404","500"],
    "_format":["json","html","xml","txt"],
    "fontName":["OpenSans-Regular","Roboto-Regular","Inter-Regular","NotoSans-Regular"],
}
DEFAULT_HEADERS={"User-Agent":"Mozilla/5.0 (compatible; SymfonyScanner/1.3.0)","Accept":"*/*"}

def find_placeholders(p):return PLACEHOLDER_RE.findall(p)
def substitute(p,mapping):
    return PLACEHOLDER_RE.sub(lambda m:mapping.get(m.group(1),m.group(0)),p)
def initial_variant_for(p):
    keys=find_placeholders(p)
    if not keys:return p,[]
    return substitute(p,{k:SEED_VALUES.get(k,"1") for k in keys}),keys
def gen_fuzz_variants(tmpl,keys,limit):
    vbk=[(k,FUZZ_CATALOG.get(k,[SEED_VALUES.get(k,"1")])[:limit]) for k in keys]
    variants=[]
    def _r(idx,cur):
        if len(variants)>=max(limit,1)*len(keys):return
        if idx==len(vbk):variants.append(substitute(tmpl,cur));return
        k,vals=vbk[idx]
        for v in vals:cur[k]=v;_r(idx+1,cur)
        cur.pop(k,None)
    _r(0,{})
    seen=set();out=[]
    for v in variants:
        if v not in seen:out.append(v);seen.add(v)
    return out

# ══════════════════════════════════════════════
#  HTTP — copiado exacto de main.py
# ══════════════════════════════════════════════
class RateLimiter:
    def __init__(self,rps):
        self.interval=1.0/float(rps);self._lock=threading.Lock()
        self._next=time.monotonic()
    def acquire(self):
        with self._lock:
            now=time.monotonic()
            if now<self._next:time.sleep(self._next-now);now=time.monotonic()
            self._next=now+self.interval

host_status_lock=threading.Lock()
host_status:Dict[str,str]={}

def set_host_status(netloc,status):
    with host_status_lock:
        prev=host_status.get(netloc)
        if prev==status:return
        if not prev or prev=="Unknown":host_status[netloc]=status;return
        if prev=="HTTPS-only" and status=="HTTP-only":host_status[netloc]="Dual";return
        if prev=="HTTP-only" and status=="HTTPS-only":host_status[netloc]="Dual";return
        if status=="HTTPS-broken-API":host_status[netloc]=status;return

def get_host_status(netloc):
    with host_status_lock:return host_status.get(netloc,"Unknown")

def build_session(timeout,retries,backoff,verify_tls,proxy):
    sess=requests.Session()
    retry=Retry(total=retries,read=retries,connect=retries,status=retries,
        backoff_factor=backoff,status_forcelist=[429,500,502,503,504],
        allowed_methods=frozenset(["GET","HEAD"]))
    a=HTTPAdapter(max_retries=retry,pool_connections=50,pool_maxsize=50)
    sess.mount("http://",a);sess.mount("https://",a)
    sess.verify=verify_tls
    if proxy:sess.proxies={"http":proxy,"https":proxy}
    sess.headers.update(DEFAULT_HEADERS)
    sess.request_timeout=timeout
    sess._rate_limiter=None;sess._request_delay=0.0;sess._request_jitter=0.0
    return sess

def is_interesting_status(code,allow_codes):
    if allow_codes:return code in allow_codes
    return code in (200,301,302,401,403)

def symfony_fingerprints(resp,body_sample):
    hints=[]
    if resp.headers.get("X-Debug-Token"):hints.append("X-Debug-Token (Symfony Profiler)")
    if resp.headers.get("X-Debug-Token-Link"):hints.append("X-Debug-Token-Link")
    if "easyadmin" in resp.url.lower():hints.append("EasyAdmin")
    try:
        if body_sample and "routes" in body_sample and "base_url" in body_sample:
            hints.append("FOSJsRouting detectado")
    except:pass
    return hints

def probe_host(session,netloc,follow,head_first):
    https_url=urlunparse(("https",netloc,"/","","",""))
    http_url=urlunparse(("http",netloc,"/","","",""))
    https_ok=http_ok=https_broken=False
    for url,flag in [(https_url,"https"),(http_url,"http")]:
        try:
            r=session.get(url,allow_redirects=follow,timeout=session.request_timeout)
            if r.status_code<500:
                if flag=="https":https_ok=True
                else:http_ok=True
            else:
                if flag=="https":https_broken=True
        except:pass
    if https_ok and http_ok:set_host_status(netloc,"Dual")
    elif https_ok:set_host_status(netloc,"HTTPS-only")
    elif http_ok:set_host_status(netloc,"HTTP-only")
    elif https_broken and http_ok:set_host_status(netloc,"HTTPS-broken-API")
    else:set_host_status(netloc,"Unknown")

def fetch(session,base,path,follow,head_first,extra_headers,head_fallback_get=True,prefer_http=False):
    rl=getattr(session,"_rate_limiter",None)
    if rl:
        try:rl.acquire()
        except:pass
    try:
        d=float(getattr(session,"_request_delay",0.0) or 0.0)
        j=float(getattr(session,"_request_jitter",0.0) or 0.0)
        if d>0 or j>0:
            to_sleep=max(0.0,d+(random.uniform(-j,j) if j>0 else 0))
            if to_sleep>0:time.sleep(to_sleep)
    except:pass

    url=urljoin(base.rstrip("/")+"/",path.lstrip("/"))
    parsed=urlparse(url);netloc=parsed.netloc;scheme=parsed.scheme
    t0=time.time();tried_http_fallback=False

    def _do(u):
        if head_first:
            r=session.head(u,allow_redirects=follow,timeout=session.request_timeout,headers=extra_headers)
            if r.status_code in (405,501) or ("content-type" not in r.headers and head_fallback_get):
                r=session.get(u,allow_redirects=follow,timeout=session.request_timeout,headers=extra_headers)
        else:
            r=session.get(u,allow_redirects=follow,timeout=session.request_timeout,headers=extra_headers)
        return r

    try:
        resp=None;host_state=get_host_status(netloc)
        if prefer_http or host_state=="HTTP-only":
            alt=urlunparse(("http",netloc,parsed.path,parsed.params,parsed.query,parsed.fragment))
            try:resp=_do(alt);url_used=alt
            except:resp=_do(url);url_used=url
        else:
            try:resp=_do(url);url_used=url
            except Exception as e:
                if scheme=="https":
                    hu=urlunparse(("http",netloc,parsed.path,parsed.params,parsed.query,parsed.fragment))
                    try:resp=_do(hu);tried_http_fallback=True;url_used=hu
                    except:raise
                else:raise

        dt=time.time()-t0
        body_sample=None
        try:
            ct=resp.headers.get("Content-Type","")
            if ct and (ct.startswith("text/") or "json" in ct):body_sample=resp.text[:1000]
        except:pass

        if resp.status_code>=500 and scheme=="https" and not tried_http_fallback and get_host_status(netloc)!="HTTP-only":
            hu=urlunparse(("http",netloc,parsed.path,parsed.params,parsed.query,parsed.fragment))
            try:
                r2=_do(hu)
                if r2.status_code<500:set_host_status(netloc,"HTTPS-broken-API");resp=r2;url_used=hu
            except:pass

        if resp.status_code<500:
            if scheme=="https" and get_host_status(netloc)=="Unknown":set_host_status(netloc,"HTTPS-only")
            if scheme=="http"  and get_host_status(netloc)=="Unknown":set_host_status(netloc,"HTTP-only")

        hints=symfony_fingerprints(resp,body_sample)
        return {"url":url_used,"path":path,"status":resp.status_code,
                "reason":getattr(resp,"reason",""),
                "content_type":resp.headers.get("Content-Type",""),
                "length":resp.headers.get("Content-Length",""),
                "location":resp.headers.get("Location",""),
                "elapsed_ms":int(dt*1000),"hints":hints}

    except requests.RequestException as e:
        if scheme=="https" and not tried_http_fallback and get_host_status(netloc)!="HTTP-only":
            hu=urlunparse(("http",netloc,parsed.path,parsed.params,parsed.query,parsed.fragment))
            try:
                r2=_do(hu);dt=time.time()-t0
                body_sample=None
                try:
                    ct=r2.headers.get("Content-Type","")
                    if ct and (ct.startswith("text/") or "json" in ct):body_sample=r2.text[:1000]
                except:pass
                hints=symfony_fingerprints(r2,body_sample)
                set_host_status(netloc,"HTTP-only")
                return {"url":hu,"path":path,"status":r2.status_code,
                        "reason":getattr(r2,"reason",""),
                        "content_type":r2.headers.get("Content-Type",""),
                        "length":r2.headers.get("Content-Length",""),
                        "location":r2.headers.get("Location",""),
                        "elapsed_ms":int(dt*1000),"hints":hints}
            except:pass
        return {"url":url,"path":path,"error":str(e)}

def load_wordlist(path):
    if not path:return []
    p=Path(path)
    if not p.exists():return []
    items=[]
    for line in p.read_text(encoding="utf-8",errors="ignore").splitlines():
        line=line.strip()
        if line and not line.startswith("#"):
            items.append(line if line.startswith("/") else "/"+line)
    return items

def save_results(results,out_path,fmt):
    if fmt=="json":
        with open(out_path,"w",encoding="utf-8") as f:json.dump(results,f,ensure_ascii=False,indent=2)
    elif fmt=="csv":
        keys=sorted({k for r in results for k in r.keys()})
        with open(out_path,"w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
            for r in results:w.writerow(r)

# ══════════════════════════════════════════════
#  SCANNER CORE — misma lógica que main()
# ══════════════════════════════════════════════
class Scanner:
    def __init__(self,cfg,log_q,result_q):
        self.cfg=cfg;self.log_q=log_q;self.result_q=result_q
        self._stop=threading.Event()
    def stop(self):self._stop.set()
    def _log(self,lvl,msg):self.log_q.put((lvl,msg))

    def run(self):
        if not REQUESTS_OK:
            self._log("ERR","❌ Instala: pip install requests urllib3 colorama")
            self.result_q.put(("DONE",0,0));return

        cfg=self.cfg
        session=build_session(cfg["timeout"],cfg["retries"],cfg["backoff"],
                               not cfg["insecure"],cfg.get("proxy"))
        extra_headers=cfg.get("extra_headers",{})
        if extra_headers:session.headers.update(extra_headers)
        if cfg.get("rps",0.0)>0:
            try:session._rate_limiter=RateLimiter(cfg["rps"])
            except:pass
        session._request_delay=cfg.get("delay",0.0)
        session._request_jitter=cfg.get("jitter",0.0)

        base_input=cfg["url"]
        parsed_base=urlparse(base_input)
        base_netloc=parsed_base.netloc
        base_scheme=parsed_base.scheme
        allow_codes:Set[int]=cfg.get("allow_codes",set())

        self._log("INFO",f"» Probeando esquemas: {base_netloc}")
        set_host_status(base_netloc,"Unknown")
        try:probe_host(session,base_netloc,cfg["follow"],cfg["head_first"])
        except:pass
        self._log("INFO",f"» Estado: {get_host_status(base_netloc)}")
        self._log("DIVIDER","")

        raw_targets=(COMMON_PATHS+BACKUP_PATHS+gen_backup_candidates()
                     +cfg.get("extra_paths",[])+load_wordlist(cfg.get("wordlist")))
        seen=set();raw_targets=[t for t in raw_targets if not(t in seen or seen.add(t))]

        host_state=get_host_status(base_netloc)
        chosen_scheme=base_scheme
        if cfg.get("prefer_http"):chosen_scheme="http"
        elif host_state=="HTTP-only":chosen_scheme="http"
        elif host_state=="HTTPS-only":chosen_scheme="https"

        scan_items:List[Dict]=[]
        for p in raw_targets:
            sub,keys=initial_variant_for(p)
            if cfg.get("dual"):
                for s in ["https","http"]:
                    b=urlunparse((s,base_netloc,"","","",""))
                    scan_items.append({"base":b,"template":p if keys else None,"path":sub,"keys":keys,"phase":"base"})
            else:
                b=urlunparse((chosen_scheme,base_netloc,"","","",""))
                scan_items.append({"base":b,"template":p if keys else None,"path":sub,"keys":keys,"phase":"base"})

        total=len(scan_items)
        self._log("INFO",f"☠️  Objetivo: {base_input}")
        self._log("INFO",f"☠️  Objetivos: {total} | Hilos: {cfg['threads']} | Timeout: {cfg['timeout']}s")
        self._log("DIVIDER","")

        results=[];ok_count=err_count=match_count=0
        fuzz_queue:List[Dict]=[]

        with ThreadPoolExecutor(max_workers=cfg["threads"]) as ex:
            future_map={ex.submit(fetch,session,it["base"],it["path"],
                cfg["follow"],cfg["head_first"],extra_headers,True,
                cfg.get("prefer_http",False)):it for it in scan_items}

            for fut in as_completed(future_map):
                if self._stop.is_set():
                    ex.shutdown(wait=False,cancel_futures=True)
                    self._log("WARN","⚠️ Detenido por el usuario.");break

                r=fut.result();it=future_map[fut]
                r["phase"]=it["phase"]
                if it["template"]:r["template"]=it["template"];r["placeholders"]=",".join(it["keys"])
                results.append(r)
                self.result_q.put(("PROGRESS",len(results),total))

                if "error" in r:
                    err_count+=1
                    self._log("ERR",f"[ERR] {r.get('url','?')} => {r['error']}");continue

                code=r.get("status")
                interesting=is_interesting_status(code,allow_codes) if code is not None else False
                if interesting:
                    ok_count+=1
                    if allow_codes:match_count+=1
                    self.result_q.put(("HIT",r))

                if interesting or cfg.get("verbose"):
                    sign="[+]" if interesting else "[-]"
                    loc=f" -> {r.get('location')}" if r.get("location") else ""
                    ct=f" [{r.get('content_type')}]" if r.get("content_type") else ""
                    sz=f" len={r.get('length')}" if r.get("length") else ""
                    ms=f" ({r.get('elapsed_ms')} ms)" if r.get("elapsed_ms") is not None else ""
                    hints=(" | "+"; ".join(r.get("hints",[]))) if r.get("hints") else ""
                    lvl="SUCCESS" if interesting else "DIM"
                    self._log(lvl,f"{sign} [{r['phase']}] {r.get('url','?')} (Status {code}){ms}{ct}{sz}{loc}{hints}")

                if cfg.get("smart_fuzz") and code==200 and it.get("template") and it.get("keys"):
                    variants=gen_fuzz_variants(it["template"],it["keys"],cfg.get("fuzz_limit",8))
                    for v in [x for x in variants if x!=it["path"]]:
                        fuzz_queue.append({"base":it["base"],"template":it["template"],
                                           "path":v,"keys":it["keys"],"phase":"fuzz","parent":it["path"]})

        # Fase fuzz
        if cfg.get("smart_fuzz") and fuzz_queue and not self._stop.is_set():
            self._log("DIVIDER","")
            self._log("WARN",f"» Lanzando fuzzing: {len(fuzz_queue)} variantes | hilos={cfg.get('fuzz_threads',8)}")
            with ThreadPoolExecutor(max_workers=cfg.get("fuzz_threads",8)) as ex2:
                fm2={ex2.submit(fetch,session,it["base"],it["path"],
                    cfg["follow"],cfg["head_first"],extra_headers,True,
                    cfg.get("prefer_http",False)):it for it in fuzz_queue}
                for fut in as_completed(fm2):
                    if self._stop.is_set():ex2.shutdown(wait=False,cancel_futures=True);break
                    r=fut.result();it=fm2[fut]
                    r["phase"]=it["phase"];r["template"]=it.get("template")
                    r["placeholders"]=",".join(it.get("keys",[]));r["parent"]=it.get("parent")
                    results.append(r)
                    if "error" in r:err_count+=1;continue
                    code=r.get("status")
                    interesting=is_interesting_status(code,allow_codes) if code is not None else False
                    if interesting:
                        ok_count+=1
                        if allow_codes:match_count+=1
                        self.result_q.put(("HIT",r))
                        loc=f" -> {r.get('location')}" if r.get("location") else ""
                        ms=f" ({r.get('elapsed_ms')} ms)" if r.get("elapsed_ms") is not None else ""
                        self._log("SUCCESS",f"[+] [fuzz] {r.get('url','?')} (Status {code}){ms}{loc} [parent={it.get('parent','')}]")

        # Guardar si se pidió
        fmt=cfg.get("fmt");out=cfg.get("out")
        if fmt and out:
            to_save=results
            if allow_codes and not cfg.get("save_all"):
                to_save=[r for r in results if "status" in r and is_interesting_status(r["status"],allow_codes)]
            try:save_results(to_save,out,fmt);self._log("INFO",f"Guardado: {out} ({fmt})")
            except Exception as e:self._log("ERR",f"Error guardando: {e}")

        self._log("DIVIDER","")
        if allow_codes:
            self._log("INFO",f"Resumen: coinciden={match_count} | interesantes={ok_count} | errores={err_count} | total={len(results)}")
        else:
            self._log("INFO",f"Resumen: interesantes={ok_count} | errores={err_count} | total={len(results)}")
        self._log("INFO",f"Host status: {base_netloc} = {get_host_status(base_netloc)}")
        self.result_q.put(("DONE",ok_count,len(results)))

# ══════════════════════════════════════════════
#  GUI
# ══════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("☠  ENDPOINTSCANNER — Symfony v1.4")
        self.configure(bg=BG)
        self.geometry("1160x820")
        self.minsize(940,640)
        self._scanner=None;self._thread=None
        self._log_q:queue.Queue=queue.Queue()
        self._result_q:queue.Queue=queue.Queue()
        self._results:List[Dict]=[]
        self._build_styles();self._build_ui();self._poll()

    def _build_styles(self):
        s=ttk.Style(self);s.theme_use("clam")
        s.configure(".",background=BG,foreground=FG,font=FONT_SM,
                    fieldbackground=BG3,borderwidth=0,relief="flat")
        s.configure("TFrame",background=BG)
        s.configure("TLabel",background=BG,foreground=FG,font=FONT_SM)
        s.configure("TEntry",fieldbackground=BG3,foreground=ACCENT,insertcolor=ACCENT,relief="flat",borderwidth=1)
        s.configure("TCheckbutton",background=BG,foreground=FG2,indicatorcolor=GRAY,font=FONT_SM)
        s.map("TCheckbutton",foreground=[("active",ACCENT)])
        s.configure("TLabelframe",background=BG2,foreground=ACCENT2,relief="flat",borderwidth=1)
        s.configure("TLabelframe.Label",background=BG2,foreground=ACCENT2,font=("Courier New",9,"bold"))
        s.configure("Horizontal.TProgressbar",troughcolor=BG3,background=ACCENT,thickness=5)
        s.configure("TNotebook",background=BG,tabmargins=[2,4,0,0])
        s.configure("TNotebook.Tab",background=BG2,foreground=FG2,padding=[10,4],font=FONT_SM)
        s.map("TNotebook.Tab",background=[("selected",BG3)],foreground=[("selected",ACCENT)])
        s.configure("Treeview",background=BG2,fieldbackground=BG2,foreground=FG,rowheight=22,borderwidth=0,font=FONT_SM)
        s.configure("Treeview.Heading",background=BG3,foreground=ACCENT,relief="flat",font=("Courier New",9,"bold"))
        s.map("Treeview",background=[("selected",GRAY2)])

    def _build_ui(self):
        hdr=tk.Frame(self,bg=BG,pady=6);hdr.pack(fill="x",padx=18)
        tk.Label(hdr,text="☠  ENDPOINTSCANNER",bg=BG,fg=ACCENT,
                 font=("Courier New",16,"bold")).pack(side="left")
        tk.Label(hdr,text="  Symfony v1.4  —  standalone",bg=BG,fg=FG2,font=FONT_SM).pack(side="left")
        rc=ACCENT if REQUESTS_OK else ACCENT2
        rt="requests OK" if REQUESTS_OK else "❌ pip install requests urllib3"
        tk.Label(hdr,text=rt,bg=BG,fg=rc,font=FONT_SM).pack(side="right")
        tk.Frame(self,bg=ACCENT,height=1).pack(fill="x",padx=18)

        body=tk.Frame(self,bg=BG);body.pack(fill="both",expand=True,padx=18,pady=8)

        # Panel izq con scroll
        lo=tk.Frame(body,bg=BG,width=320);lo.pack(side="left",fill="y",padx=(0,10))
        lo.pack_propagate(False)
        cv=tk.Canvas(lo,bg=BG,highlightthickness=0)
        sb=ttk.Scrollbar(lo,orient="vertical",command=cv.yview)
        cv.configure(yscrollcommand=sb.set)
        sb.pack(side="right",fill="y");cv.pack(side="left",fill="both",expand=True)
        left=tk.Frame(cv,bg=BG)
        win=cv.create_window((0,0),window=left,anchor="nw")
        left.bind("<Configure>",lambda e:cv.configure(scrollregion=cv.bbox("all")))
        cv.bind("<Configure>",lambda e:cv.itemconfig(win,width=e.width))
        left.bind("<Enter>",lambda e:cv.bind_all("<MouseWheel>",lambda ev:cv.yview_scroll(int(-1*(ev.delta/120)),"units")))
        left.bind("<Leave>",lambda e:cv.unbind_all("<MouseWheel>"))

        right=tk.Frame(body,bg=BG);right.pack(side="left",fill="both",expand=True)
        self._build_config(left);self._build_output(right)

        bot=tk.Frame(self,bg=BG2,pady=3);bot.pack(fill="x",side="bottom")
        self._status_var=tk.StringVar(value="Listo.")
        tk.Label(bot,textvariable=self._status_var,bg=BG2,fg=FG2,font=FONT_SM).pack(side="left",padx=12)
        self._prog=ttk.Progressbar(bot,orient="horizontal",length=180,mode="determinate",style="Horizontal.TProgressbar")
        self._prog.pack(side="right",padx=12)
        self._prog_lbl=tk.Label(bot,text="",bg=BG2,fg=FG2,font=FONT_SM);self._prog_lbl.pack(side="right")

    def _build_config(self,p):
        pad={"pady":(0,5)}
        # TARGET
        f=ttk.LabelFrame(p,text=" TARGET ",padding=6);f.pack(fill="x",**pad)
        tk.Label(f,text="URL Base:",bg=BG2,fg=FG2,font=FONT_SM).pack(anchor="w")
        self._url_var=tk.StringVar(value="https://")
        ttk.Entry(f,textvariable=self._url_var).pack(fill="x",pady=2)
        # OPCIONES
        f2=ttk.LabelFrame(p,text=" OPCIONES ",padding=6);f2.pack(fill="x",**pad)
        self._threads_var=tk.StringVar(value="20")
        self._timeout_var=tk.StringVar(value="7")
        self._retries_var=tk.StringVar(value="2")
        self._backoff_var=tk.StringVar(value="0.4")
        self._codes_var=tk.StringVar(value="")
        self._proxy_var=tk.StringVar(value="")
        self._delay_var=tk.StringVar(value="0.0")
        self._jitter_var=tk.StringVar(value="0.0")
        self._rps_var=tk.StringVar(value="0.0")
        for lbl,var in [("--threads",self._threads_var),("--timeout",self._timeout_var),
                        ("--retries",self._retries_var),("--backoff",self._backoff_var),
                        ("--codes",self._codes_var),("--proxy",self._proxy_var),
                        ("--delay",self._delay_var),("--jitter",self._jitter_var),("--rps",self._rps_var)]:
            row=tk.Frame(f2,bg=BG2);row.pack(fill="x",pady=1)
            tk.Label(row,text=lbl,bg=BG2,fg=FG2,width=12,anchor="w",font=FONT_SM).pack(side="left")
            ttk.Entry(row,textvariable=var,width=16).pack(side="left")
        # FLAGS
        f3=ttk.LabelFrame(p,text=" FLAGS ",padding=6);f3.pack(fill="x",**pad)
        self._follow_var=tk.BooleanVar();self._head_var=tk.BooleanVar()
        self._insecure_var=tk.BooleanVar();self._verbose_var=tk.BooleanVar()
        self._save_all_var=tk.BooleanVar();self._smart_fuzz_var=tk.BooleanVar()
        self._prefer_http_var=tk.BooleanVar();self._dual_var=tk.BooleanVar()
        self._backup_var=tk.BooleanVar(value=True)
        for desc,flag,var in [
            ("Incluir rutas backup","--backup",self._backup_var),
            ("Seguir redirecciones","--follow",self._follow_var),
            ("HEAD antes de GET","--head-first",self._head_var),
            ("Ignorar TLS","--insecure",self._insecure_var),
            ("Verbose (mostrar todo)","--verbose",self._verbose_var),
            ("Guardar todos","--save-all",self._save_all_var),
            ("Smart Fuzz","--smart-fuzz",self._smart_fuzz_var),
            ("Preferir HTTP","--prefer-http",self._prefer_http_var),
            ("Dual scan HTTP+HTTPS","--dual",self._dual_var)]:
            row=tk.Frame(f3,bg=BG2);row.pack(fill="x",pady=1)
            ttk.Checkbutton(row,text=desc,variable=var).pack(side="left")
            tk.Label(row,text=flag,bg=BG2,fg=GRAY,font=FONT_SM).pack(side="right")
        # SMART FUZZ
        f4=ttk.LabelFrame(p,text=" SMART FUZZ ",padding=6);f4.pack(fill="x",**pad)
        self._fuzz_limit_var=tk.StringVar(value="8")
        self._fuzz_threads_var=tk.StringVar(value="8")
        for lbl,var in [("--fuzz-limit",self._fuzz_limit_var),("--fuzz-threads",self._fuzz_threads_var)]:
            row=tk.Frame(f4,bg=BG2);row.pack(fill="x",pady=1)
            tk.Label(row,text=lbl,bg=BG2,fg=FG2,width=14,anchor="w",font=FONT_SM).pack(side="left")
            ttk.Entry(row,textvariable=var,width=6).pack(side="left")
        # HEADERS
        f5=ttk.LabelFrame(p,text=" -H HEADERS ",padding=6);f5.pack(fill="x",**pad)
        tk.Label(f5,text="Clave: Valor (uno por linea)",bg=BG2,fg=FG2,font=FONT_SM).pack(anchor="w")
        self._headers_text=tk.Text(f5,height=3,bg=BG3,fg=ACCENT3,insertbackground=ACCENT3,font=FONT_MONO,relief="flat",border=0)
        self._headers_text.pack(fill="x")
        # WORDLIST
        f6=ttk.LabelFrame(p,text=" -w WORDLIST / -p PATHS ",padding=6);f6.pack(fill="x",**pad)
        wr=tk.Frame(f6,bg=BG2);wr.pack(fill="x")
        self._wordlist_var=tk.StringVar()
        ttk.Entry(wr,textvariable=self._wordlist_var).pack(side="left",fill="x",expand=True)
        tk.Button(wr,text="...",bg=GRAY,fg=FG,relief="flat",font=FONT_SM,command=self._browse_wl).pack(side="left",padx=2)
        tk.Label(f6,text="-p rutas extra (una por linea):",bg=BG2,fg=FG2,font=FONT_SM).pack(anchor="w",pady=(3,0))
        self._extra_text=tk.Text(f6,height=3,bg=BG3,fg=ACCENT3,insertbackground=ACCENT3,font=FONT_MONO,relief="flat",border=0)
        self._extra_text.pack(fill="x")
        # OUTPUT
        f7=ttk.LabelFrame(p,text=" --format / --out ",padding=6);f7.pack(fill="x",**pad)
        or_=tk.Frame(f7,bg=BG2);or_.pack(fill="x")
        self._out_var=tk.StringVar()
        ttk.Entry(or_,textvariable=self._out_var).pack(side="left",fill="x",expand=True)
        tk.Button(or_,text="...",bg=GRAY,fg=FG,relief="flat",font=FONT_SM,command=self._browse_out).pack(side="left",padx=2)
        fr=tk.Frame(f7,bg=BG2);fr.pack(fill="x",pady=(3,0))
        self._fmt_var=tk.StringVar(value="")
        for val,lbl in [("","No guardar"),("json","JSON"),("csv","CSV")]:
            tk.Radiobutton(fr,text=lbl,variable=self._fmt_var,value=val,bg=BG2,fg=FG2,
                           selectcolor=BG3,activebackground=BG2,font=FONT_SM).pack(side="left",padx=3)
        # BOTONES
        tk.Frame(p,bg=BG,height=8).pack()
        self._scan_btn=tk.Button(p,text="▶  ESCANEAR",bg=ACCENT,fg=BG,
            font=("Courier New",11,"bold"),relief="flat",activebackground="#00cc70",
            cursor="hand2",command=self._start)
        self._scan_btn.pack(fill="x",pady=2,padx=4)
        self._stop_btn=tk.Button(p,text="■  DETENER",bg=ACCENT2,fg="white",
            font=("Courier New",10,"bold"),relief="flat",activebackground="#cc2040",
            cursor="hand2",state="disabled",command=self._stop)
        self._stop_btn.pack(fill="x",pady=2,padx=4)
        tk.Button(p,text="🗑  LIMPIAR",bg=GRAY,fg=FG,font=FONT_SM,relief="flat",
            cursor="hand2",command=self._clear).pack(fill="x",pady=2,padx=4)
        tk.Frame(p,bg=BG,height=10).pack()

    def _build_output(self,p):
        nb=ttk.Notebook(p);nb.pack(fill="both",expand=True)
        # LOG
        t1=tk.Frame(nb,bg=BG);nb.add(t1,text="  LOG  ")
        self._log_box=scrolledtext.ScrolledText(t1,bg=BG,fg=FG,insertbackground=ACCENT,
            font=FONT_MONO,relief="flat",border=0,state="disabled",wrap="none")
        self._log_box.pack(fill="both",expand=True)
        self._log_box.tag_config("SUCCESS",foreground=ACCENT,font=("Courier New",10,"bold"))
        self._log_box.tag_config("ERR",foreground=ACCENT2)
        self._log_box.tag_config("WARN",foreground=YELLOW)
        self._log_box.tag_config("INFO",foreground=ACCENT3)
        self._log_box.tag_config("DIVIDER",foreground=GRAY)
        self._log_box.tag_config("DIM",foreground="#3a3a3a")
        self._log_box.tag_config("NORMAL",foreground=FG2)
        # HITS
        t2=tk.Frame(nb,bg=BG);nb.add(t2,text="  HITS  ")
        cols=("status","url","type","ms","location")
        self._tree=ttk.Treeview(t2,columns=cols,show="headings",selectmode="extended")
        for c,lbl,w in [("status","Status",60),("url","URL",510),("type","Content-Type",160),("ms","ms",55),("location","Location",180)]:
            self._tree.heading(c,text=lbl);self._tree.column(c,width=w,minwidth=40,stretch=(c=="url"))
        self._tree.tag_configure("200",foreground=ACCENT);self._tree.tag_configure("3xx",foreground=ACCENT3)
        self._tree.tag_configure("401",foreground=YELLOW);self._tree.tag_configure("403",foreground=YELLOW)
        vsb=ttk.Scrollbar(t2,orient="vertical",command=self._tree.yview)
        hsb=ttk.Scrollbar(t2,orient="horizontal",command=self._tree.xview)
        self._tree.configure(yscrollcommand=vsb.set,xscrollcommand=hsb.set)
        self._tree.grid(row=0,column=0,sticky="nsew");vsb.grid(row=0,column=1,sticky="ns")
        hsb.grid(row=1,column=0,sticky="ew");t2.rowconfigure(0,weight=1);t2.columnconfigure(0,weight=1)
        bar=tk.Frame(t2,bg=BG2,pady=3);bar.grid(row=2,column=0,columnspan=2,sticky="ew")
        tk.Button(bar,text="Exportar JSON",bg=BG3,fg=ACCENT,relief="flat",font=FONT_SM,cursor="hand2",
            command=lambda:self._export("json")).pack(side="left",padx=8)
        tk.Button(bar,text="Exportar CSV",bg=BG3,fg=ACCENT3,relief="flat",font=FONT_SM,cursor="hand2",
            command=lambda:self._export("csv")).pack(side="left")
        self._hits_lbl=tk.Label(bar,text="0 hits",bg=BG2,fg=FG2,font=FONT_SM);self._hits_lbl.pack(side="right",padx=8)
        # INFO
        t3=tk.Frame(nb,bg=BG);nb.add(t3,text="  INFO  ")
        tk.Label(t3,text=(
            "\n\n  ☠  ENDPOINTSCANNER GUI — standalone\n\n"
            f"  COMMON_PATHS:          {len(COMMON_PATHS)} rutas\n"
            f"  BACKUP_PATHS:          {len(BACKUP_PATHS)} rutas\n"
            f"  gen_backup_candidates: ~{len(gen_backup_candidates())} rutas\n\n"
            "  Motor: mismo código que main.py\n"
            "  Smart Fuzz, dual scan, rate limiter,\n"
            "  fallback HTTPS->HTTP, fingerprinting.\n\n"
            "  pip install requests urllib3 colorama\n"
        ),bg=BG,fg=FG2,font=FONT_MONO,justify="left").pack(anchor="nw",padx=16,pady=8)

    def _browse_wl(self):
        f=filedialog.askopenfilename(filetypes=[("Text","*.txt"),("All","*.*")])
        if f:self._wordlist_var.set(f)
    def _browse_out(self):
        fmt=self._fmt_var.get() or "json"
        f=filedialog.asksaveasfilename(defaultextension=f".{fmt}",
            filetypes=[("JSON","*.json"),("CSV","*.csv"),("All","*.*")])
        if f:self._out_var.set(f)

    def _parse_headers(self):
        out={}
        for line in self._headers_text.get("1.0","end").splitlines():
            line=line.strip()
            if ":"in line:k,v=line.split(":",1);out[k.strip()]=v.strip()
        return out
    def _parse_codes(self):
        raw=self._codes_var.get().strip()
        if not raw:return set()
        try:return {int(x.strip()) for x in raw.split(",") if x.strip()}
        except:return set()
    def _parse_extra_paths(self):
        paths=[]
        for line in self._extra_text.get("1.0","end").splitlines():
            p=line.strip()
            if p:paths.append(p if p.startswith("/") else "/"+p)
        return paths

    def _start(self):
        if not REQUESTS_OK:
            messagebox.showerror("Error","pip install requests urllib3 colorama");return
        url=self._url_var.get().strip()
        if not url or url in("https://","http://"):
            messagebox.showwarning("URL","Introduce una URL válida.");return
        if not url.startswith(("http://","https://")):url="https://"+url
        try:
            threads=int(self._threads_var.get());timeout=int(self._timeout_var.get())
            retries=int(self._retries_var.get());fuzz_limit=int(self._fuzz_limit_var.get())
            fuzz_threads=int(self._fuzz_threads_var.get());backoff=float(self._backoff_var.get())
            delay=float(self._delay_var.get());jitter=float(self._jitter_var.get())
            rps=float(self._rps_var.get())
        except ValueError:messagebox.showerror("Error","Verifica los valores numéricos.");return

        cfg={"url":url,"threads":threads,"timeout":timeout,"retries":retries,"backoff":backoff,
             "follow":self._follow_var.get(),"head_first":self._head_var.get(),
             "insecure":self._insecure_var.get(),"verbose":self._verbose_var.get(),
             "save_all":self._save_all_var.get(),"smart_fuzz":self._smart_fuzz_var.get(),
             "prefer_http":self._prefer_http_var.get(),"dual":self._dual_var.get(),
             "include_backup":self._backup_var.get(),"allow_codes":self._parse_codes(),
             "extra_headers":self._parse_headers(),"extra_paths":self._parse_extra_paths(),
             "wordlist":self._wordlist_var.get().strip() or None,
             "proxy":self._proxy_var.get().strip() or None,
             "delay":delay,"jitter":jitter,"rps":rps,
             "fuzz_limit":fuzz_limit,"fuzz_threads":fuzz_threads,
             "fmt":self._fmt_var.get().strip() or None,
             "out":self._out_var.get().strip() or None}

        self._results.clear()
        for i in self._tree.get_children():self._tree.delete(i)
        self._hits_lbl.config(text="0 hits")
        self._prog["value"]=0;self._prog_lbl.config(text="")
        self._status_var.set("Escaneando...")
        self._scan_btn.config(state="disabled");self._stop_btn.config(state="normal")

        self._scanner=Scanner(cfg,self._log_q,self._result_q)
        self._thread=threading.Thread(target=self._scanner.run,daemon=True)
        self._thread.start()

    def _stop(self):
        if self._scanner:self._scanner.stop()
        self._stop_btn.config(state="disabled");self._status_var.set("Deteniendo...")

    def _clear(self):
        self._log_box.config(state="normal");self._log_box.delete("1.0","end")
        self._log_box.config(state="disabled")
        for i in self._tree.get_children():self._tree.delete(i)
        self._results.clear();self._hits_lbl.config(text="0 hits")
        self._prog["value"]=0;self._prog_lbl.config(text="")
        self._status_var.set("Listo.")

    def _export(self,fmt):
        if not self._results:messagebox.showinfo("Exportar","No hay hits.");return
        ext=".json" if fmt=="json" else ".csv"
        path=filedialog.asksaveasfilename(defaultextension=ext,
            filetypes=[("JSON","*.json")] if fmt=="json" else [("CSV","*.csv")])
        if not path:return
        try:
            if fmt=="json":
                with open(path,"w",encoding="utf-8") as f:json.dump(self._results,f,ensure_ascii=False,indent=2)
            else:
                keys=sorted({k for r in self._results for k in r})
                with open(path,"w",newline="",encoding="utf-8") as f:
                    w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
                    for r in self._results:w.writerow(r)
            messagebox.showinfo("Exportar",f"Guardado:\n{path}")
        except Exception as e:messagebox.showerror("Error",str(e))

    def _log_write(self,tag,msg):
        self._log_box.config(state="normal")
        self._log_box.insert("end",msg+"\n",tag)
        self._log_box.see("end");self._log_box.config(state="disabled")

    def _poll(self):
        try:
            while True:
                lvl,msg=self._log_q.get_nowait()
                if lvl=="DIVIDER":self._log_write("DIVIDER","─"*80)
                else:self._log_write(lvl,msg)
        except queue.Empty:pass
        try:
            while True:
                item=self._result_q.get_nowait();kind=item[0]
                if kind=="PROGRESS":
                    _,done,total=item
                    pct=int(done/total*100) if total else 0
                    self._prog["value"]=pct
                    self._prog_lbl.config(text=f"{done}/{total}")
                    self._status_var.set(f"Escaneando... {pct}%")
                elif kind=="HIT":
                    r=item[1];self._results.append(r)
                    code=str(r.get("status",""))
                    tag=code if code in("200","401","403") else("3xx" if code.startswith("3") else "")
                    self._tree.insert("","end",
                        values=(code,r.get("url",""),
                                (r.get("content_type","") or "").split(";")[0][:40],
                                r.get("elapsed_ms",""),r.get("location","") or ""),
                        tags=(tag,))
                    self._hits_lbl.config(text=f"{len(self._results)} hits")
                elif kind=="DONE":
                    _,ok,total=item
                    self._status_var.set(f"✅  Completado | {ok} hits de {total} rutas")
                    self._scan_btn.config(state="normal");self._stop_btn.config(state="disabled")
                    self._prog["value"]=100
        except queue.Empty:pass
        self.after(60,self._poll)

if __name__=="__main__":
    App().mainloop()