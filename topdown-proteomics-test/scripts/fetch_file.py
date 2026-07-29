#!/usr/bin/env python3
"""从个人盘/共享盘下载单个文件到工作区(OpenAPI,无需 TTY)。输出 JSON。

存在的唯一理由:让 agent **永远不必手写带 access key 的 curl**。
平台有密钥脱敏:key 的明文值一旦进入命令文本/中转变量/写文件/回显,就被替换成
`[REDACTED]`,轻则破坏命令引号语法(unexpected EOF),重则把假值发出去(Invalid AccessKey)。
本脚本把 key 全程关在 os.environ 里,agent 只传"远端路径 + 本地目标",不碰 key、不拼 URL、
不取 userId。这是那条反复翻车的 FASTA 下载链路的根治写法。

用法:
  python3 fetch_file.py --remote personal/msryzen-test/xx/uniprot-st.fasta --out ./uniprot-st.fasta
  python3 fetch_file.py --remote share/jubao/xx/db.fasta --out /bohr-workspace/td-runs/run/db.fasta

--remote 是盘内路径,以 personal/ 或 share/ 开头(个人盘 / 共享盘),原样拼进下载 URL 段。
projectId:personal 盘用 0(个人空间与项目无关);share 盘用 --project-id(默认取 PROJECT_ID)。
认证走 HTTP 头(accessKey/Bearer 均可),key 不进 URL、不进 query,故打印 URL 不泄露。
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def _fail(what: str, next_: str = "", forbidden: str = ""):
    """一律硬失败:ok:false + 非 0 退出码,别让 agent 拿着半截结果往下走。"""
    out = {"ok": False, "error": what}
    if next_:
        out["next"] = next_
    if forbidden:
        out["forbidden"] = forbidden
    print(json.dumps(out, ensure_ascii=False))
    sys.exit(2)


def _api() -> str:
    # 地址唯一来源:OPENAPI_HOST(setup.sh 导出)。不要自己拼别的域名。
    return os.environ.get("OPENAPI_HOST", "https://open.bohrium.com").rstrip("/")


# ── 鉴权失败的统一口径 ────────────────────────────────────────────────
# 平台 401 的 body 是**合法 JSON**(`{"code":2000,"message":"Invalid AccessKey",
# "error":{"retryable":false}}`)。不读 body 就会把"密钥失效"误判成别的东西 ——
# 2026-07-27 事故里它一路被当成网络问题、路径问题、作业不存在。
_AUTH_NEXT = ("平台注入的密钥已失效。这是**终局错误**(响应里带 retryable:false),重试、换写法、"
              "换认证头都没用。**这是平台侧的密钥注入问题,不在本 skill 的处理范围** —— "
              "如实把这一条告知用户,然后停止本轮,不要尝试自行修复、也不要替平台猜处置步骤。")
_AUTH_NEVER = ("不要向用户索取 key,不要手写 .bohr_env,不要 `bohr auth login`(该子命令不存在),"
               "不要重试,不要改用别的端点或认证头。")


def _biz(e):
    """从 HTTPError 的 body 里取业务码与消息(body 已被读走,调用方别再 read)。"""
    try:
        j = json.loads(e.read().decode("utf-8", "replace"))
        return j.get("code"), j.get("message")
    except Exception:  # noqa: BLE001
        return None, None


def _is_auth(http_code, biz_code) -> bool:
    return http_code in (401, 403) or biz_code == 2000


def _key() -> str:
    # 平台注入的是 BOHR_ACCESS_KEY;setup.sh 会把它也写一份 ACCESS_KEY。两个都认。
    # key 只在这里从环境读一次,绝不打印、绝不写回任何输出。
    # 优先平台权威 BOHR_ACCESS_KEY;ACCESS_KEY 可能是 .bohr_env 残留的陈旧值(Codex round2 #1)。
    ak = os.environ.get("BOHR_ACCESS_KEY") or os.environ.get("ACCESS_KEY")
    if not ak:
        _fail("环境里没有 access key(ACCESS_KEY / BOHR_ACCESS_KEY 都为空)。",
              next_="先 `bash scripts/setup.sh` 落环境,或确认平台已注入密钥。",
              forbidden="不要手写 key、不要向用户要 key —— 平台会注入,缺了是授权/环境问题。")
    return ak


def _user_id(ak: str) -> int:
    """取 user_id —— 下载 URL 的 query 需要它。字段名是 user_id(不是 id)。"""
    url = f"{_api()}/openapi/v1/ak/get"
    req = urllib.request.Request(url, headers={"accessKey": ak})
    try:
        data = json.load(urllib.request.urlopen(req, timeout=20))
    except urllib.error.HTTPError as e:
        code, msg = _biz(e)
        if _is_auth(e.code, code):
            _fail(f"密钥被拒:HTTP {e.code} code={code} {msg or ''}".strip(),
                  next_=_AUTH_NEXT, forbidden=_AUTH_NEVER)
        _fail(f"取 user_id 失败:HTTP {e.code} code={code}。",
              next_="非鉴权错(网关/网络抖动),原样重试一次;仍失败就把原文报给用户并停。",
              forbidden="别把 key 写进命令来'试' —— 会被平台脱敏成 [REDACTED],制造假的认证失败。")
    except Exception as e:  # noqa: BLE001
        _fail(f"取 user_id 失败:{e}")
    uid = (data.get("data") or {}).get("user_id")
    if not uid:
        _fail(f"取 user_id:响应里没有 user_id 字段。原始 code={data.get('code')}")
    return uid


def main():
    ap = argparse.ArgumentParser(prog="fetch_file")
    ap.add_argument("--remote", required=True,
                    help="盘内路径,以 personal/ 或 share/ 开头,如 personal/msryzen-test/xx.fasta")
    ap.add_argument("--out", required=True, help="本地目标路径")
    ap.add_argument("--project-id", default=os.environ.get("PROJECT_ID", ""),
                    help="share 盘需要;personal 盘忽略(用 0)")
    a = ap.parse_args()

    remote = a.remote.strip().lstrip("/")
    if not (remote.startswith("personal/") or remote.startswith("share/")):
        _fail(f"--remote 必须以 personal/ 或 share/ 开头,收到:{a.remote!r}",
              next_="个人盘用 personal/<路径>;共享盘用 share/<路径>。")

    # personal 盘与项目无关,projectId 恒 0;share 盘用真实项目号。
    if remote.startswith("personal/"):
        project_id = "0"
    else:
        project_id = str(a.project_id or "").strip()
        if not project_id:
            _fail("share 盘下载需要 project_id(--project-id 或环境 PROJECT_ID)。")

    ak = _key()
    uid = _user_id(ak)

    # key 走 HTTP 头,不进 URL/query —— 所以下面这个 URL 打印出来不泄露密钥。
    url = (f"{_api()}/openapi/v1/file/download/{remote}"
           f"?projectId={project_id}&userId={uid}")
    req = urllib.request.Request(url, headers={"accessKey": ak})

    out_path = os.path.abspath(a.out)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = resp.read()
    except urllib.error.HTTPError as e:
        code, msg = _biz(e)
        if _is_auth(e.code, code):
            _fail(f"下载被拒:HTTP {e.code} code={code} {msg or ''}  路径={remote}".strip(),
                  next_=_AUTH_NEXT, forbidden=_AUTH_NEVER)
        _fail(f"下载失败:HTTP {e.code}  路径={remote}",
              next_="核对盘内路径是否真实存在(个人盘 personal/…、共享盘 share/…)。")
    except Exception as e:  # noqa: BLE001
        _fail(f"下载失败:{e}  路径={remote}")

    # 反劫持:下载接口出错时会回一段 JSON 而非文件内容,别把它当文件存下去。
    # 典型是 {"code":2000,"message":"Invalid AccessKey"} 之类,几十~几百字节。
    head = body[:200].lstrip()
    if head[:1] in (b"{", b"[") and b'"code"' in body[:200]:
        try:
            j = json.loads(body.decode("utf-8", "replace"))
            if j.get("code") == 2000:
                _fail(f"下载返回的是鉴权错误 JSON 不是文件:code=2000 "
                      f"message={j.get('message')}",
                      next_=_AUTH_NEXT, forbidden=_AUTH_NEVER)
            _fail(f"下载返回的是错误 JSON 不是文件:code={j.get('code')} "
                  f"message={j.get('message')}",
                  next_="路径不存在或无权限;核对 --remote。",
                  forbidden="不要把这段 JSON 当文件用 —— 它不是你要的数据。")
        except Exception:  # noqa: BLE001
            pass  # 不是合法 JSON,当真文件处理

    with open(out_path, "wb") as f:
        f.write(body)

    print(json.dumps({
        "ok": True, "remote": remote, "out": out_path,
        "bytes": len(body), "url": url,  # url 不含 key,可安全展示
        "hint": "下载完成;后续随作业打包上传(FASTA 用 -p,勿做 dataset)。",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
