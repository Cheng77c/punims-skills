#!/usr/bin/env python3
"""轮询 Bohrium job 状态(OpenAPI,无需 TTY)。输出 JSON。

按 jobId 匹配(共享项目有他人并发 job,故 pageSize 取大些;别按 jobName)。
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

STATUS = {0: "pending", 1: "running", 2: "completed", 3: "scheduling", -1: "failed"}


def _fail(job_id: str, what: str, next_: str, forbidden: str):
    """作业查询失败一律硬失败:ok:false + 非 0 退出码。

    这里曾经把"查不到"当成 status:"unknown" + ok:true + "仍在运行,稍后再查"返回,
    退出码还是 0 —— agent 于是永远等一个不存在的作业。查不到就是错,必须说清怎么办。
    """
    print(json.dumps({"ok": False, "jobId": job_id, "status": "not_found",
                      "done": False, "error": what, "next": next_,
                      "forbidden": forbidden}, ensure_ascii=False))
    sys.exit(2)


def decide(job_id: str, code) -> dict:
    status = STATUS.get(code, "unknown")
    done = status in ("completed", "failed")
    out = {
        "ok": True, "jobId": job_id, "status": status, "done": done,
        # 完成或失败都去 collect:失败时 collect 也 download 失败 summary + 失败日志,不断链
        "nextTool": "collect_results.py" if done else None,
    }
    if done:
        out["hint"] = "已终态:运行 collect_results.py 取结果。"
    else:
        # 不返回 pollAfterMs 之类"稍后再轮询"的信号——那会诱导 agent 自旋。
        out["hint"] = ("仍在运行:向用户报告 jobId + 状态后**结束本轮**,不要自旋轮询;"
                       "作业在后台独立运行,用户稍后回来或下次调用时再查一次。")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job-id", required=True)
    a = ap.parse_args()
    ak = os.environ.get("ACCESS_KEY") or os.environ.get("BOHR_ACCESS_KEY")
    if not ak:
        sys.exit("missing env: ACCESS_KEY(也没 BOHR_ACCESS_KEY;先 source .bohr_env 或完成授权)")

    # 地址唯一来源:OPENAPI_HOST(setup.sh 导出)。不要自己拼别的域名。
    api = os.environ.get("OPENAPI_HOST", "https://openapi.dp.tech").rstrip("/")
    url = f"{api}/openapi/v1/job/list?page=1&pageSize=50"
    req = urllib.request.Request(url, headers={"accessKey": ak})
    try:
        data = json.load(urllib.request.urlopen(req, timeout=20))
    except urllib.error.HTTPError as e:
        _fail(a.job_id, f"查询作业列表失败:HTTP {e.code}",
              next_="401/403 说明凭据失效:重新 `source /bohr-workspace/.bohr_env`;"
                    "5xx 是平台抖动,原样重跑本命令一次。",
              forbidden="不要改用别的 API 域名或自己拼 REST 端点,不要把作业当成已完成继续往下走。")
    except Exception as e:
        _fail(a.job_id, f"查询作业列表失败:{e}",
              next_="多半是网络/代理问题(代理返回 HTML 会导致 JSON 解析失败):"
                    "`unset http_proxy https_proxy` 后原样重跑本命令。",
              forbidden="不要换端点,不要假设作业仍在运行。")

    items = (data.get("data") or {}).get("items") or []
    code = None
    for j in items:
        if str(j.get("id")) == str(a.job_id):
            code = j.get("status")
            break

    # 查不到 = 硬错误。绝不能退化成 status:"unknown" + "仍在运行" —— 那会让 agent
    # 永远等一个不存在的作业(jobId 抄错 / 提交时 PROJECT_ID 与当前 env 不一致 / 作业被删)。
    if code is None:
        _fail(a.job_id,
              f"在最近 {len(items)} 条作业里找不到 jobId={a.job_id}",
              next_="① 回看 submit 的输出,核对 jobId 原文有没有抄错;"
                    "② `echo $PROJECT_ID` 确认与提交时是同一个项目;"
                    "③ 仍找不到就说明作业没提交成功或已被删除,需要重新 submit。",
              forbidden="不要猜别的 jobId,不要自己 curl 其它端点去找,"
                        "更不要把状态当成 running 继续等下去 —— 这个作业并不存在。")

    print(json.dumps(decide(a.job_id, code), ensure_ascii=False))


if __name__ == "__main__":
    main()
