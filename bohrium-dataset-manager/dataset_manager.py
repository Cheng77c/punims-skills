"""
Dataset lifecycle management: detail, versions, quota, permissions.

Usage:
    python dataset_manager.py quota --project_id YOUR_PROJECT_ID
    python dataset_manager.py detail --id YOUR_DATASET_ID
    python dataset_manager.py versions --id YOUR_DATASET_ID
    python dataset_manager.py files --id YOUR_DATASET_ID          # 列出内部文件 + 确切挂载路径
    python dataset_manager.py new_version --id YOUR_DATASET_ID --desc "v2 with more data"
"""

import argparse
import json
import os
import sys

import requests

# Accept either var name: BOHR_ACCESS_KEY (platform-injected) or ACCESS_KEY (what the
# proteomics .bohr_env exports for the bohr CLI). Avoids the "set BOHR_ACCESS_KEY" dead-end
# when this runs inside the BU/TD flow.
AK = os.environ.get("BOHR_ACCESS_KEY") or os.environ.get("ACCESS_KEY") or ""
BASE = "https://open.bohrium.com/openapi/v2/ds"
HEADERS = {"Authorization": f"Bearer {AK}"}
HEADERS_JSON = {**HEADERS, "Content-Type": "application/json"}


def die(what: str, *, fix: str, never: str = None, code: int = 1):
    """Fail loudly, and tell the caller exactly what to do next.

    An LLM agent reads this output and decides its next move. "Error: failed" gives it
    nothing to act on, so it improvises — inventing API endpoints, guessing a dataset by
    name, downloading a 900MB spectrum into the workspace. Every failure here therefore
    states WHAT broke, HOW to fix it, and where relevant WHAT MUST NOT be done instead.
    """
    print(f"ERROR: {what}", file=sys.stderr)
    print(f"FIX:   {fix}", file=sys.stderr)
    if never:
        print(f"NEVER: {never}", file=sys.stderr)
    sys.exit(code)


def api(method: str, url: str, **kw):
    """HTTP against the Bohrium OpenAPI, with actionable failures instead of tracebacks.

    Turns the three ways this bites us — dead network, bad key, API-level error code —
    into messages an agent can act on, rather than a stack trace it will guess around.
    """
    kw.setdefault("timeout", 60)
    kw.setdefault("headers", HEADERS)
    try:
        r = requests.request(method, url, **kw)
    except requests.exceptions.Timeout:
        die(f"Bohrium API timed out: {method} {url}",
            fix="Transient. Retry the same command once or twice. If it keeps timing out, "
                "report a platform outage and stop.",
            never="Do not switch to a different endpoint or invent an alternative API path.",
            code=8)
    except requests.exceptions.RequestException as e:
        die(f"cannot reach the Bohrium API: {e}",
            fix="Check network egress from the sandbox, then retry the same command.",
            never="Do not fall back to downloading large data into the workspace.", code=8)

    if r.status_code in (401, 403):
        die(f"Bohrium rejected the access key ({r.status_code}) on {url}",
            fix="Run the skill's setup.sh, then `source /bohr-workspace/.bohr_env`. It sets "
                "ACCESS_KEY and BOHR_ACCESS_KEY to the same value. If it still fails, ask the "
                "user for a valid key — do not guess one.",
            code=1)
    if r.status_code == 404:
        die(f"no such Bohrium endpoint: {url} (404)",
            fix="This URL does not exist. Use only the subcommands of this script "
                "(`dataset_manager.py --help`).",
            never="Do NOT hand-craft REST calls or invent endpoints — /v1/dataset, "
                  "/v2/dataset/list and /openapi/cli/install are all 404s that have "
                  "burned us before.",
            code=8)
    if r.status_code >= 500:
        die(f"Bohrium server error {r.status_code} on {url}",
            fix="Platform-side and usually transient. Retry once or twice, then report the "
                "outage to the user and stop.",
            never="Do not work around it by downloading spectra into the workspace.", code=8)

    try:
        data = r.json()
    except ValueError:
        die(f"Bohrium returned non-JSON from {url}: {r.text[:120]!r}",
            fix="Almost always an auth or URL problem. Verify the key is loaded and that the "
                "path came from this script, not from memory.", code=8)

    if isinstance(data, dict) and data.get("code") not in (0, None):
        die(f"Bohrium API error {data.get('code')} on {url}: {data.get('message') or data}",
            fix="Read the message above — it is the real cause. Fix the inputs it names "
                "(project id, path, dataset id) and retry.",
            never="Do not retry blindly with the same inputs, and do not substitute a "
                  "different dataset to move on.", code=8)
    return data


def check_quota(project_id: int):
    """Check dataset quota for a project."""
    r = requests.get(
        f"{BASE}/quota/check",
        headers=HEADERS,
        params={"projectId": project_id},
    )
    data = r.json().get("data", {})
    limit = data.get("limit", "?")
    used = data.get("used", "?")
    available = data.get("result", "?")
    print(f"Dataset quota for project {project_id}:")
    print(f"  Limit:     {limit}")
    print(f"  Used:      {used}")
    print(f"  Available: {available}")


def get_detail(dataset_id: int):
    """Get dataset details."""
    r = requests.get(f"{BASE}/{dataset_id}", headers=HEADERS)
    data = r.json().get("data", {})
    # /v2/ds/{id} 详情端点不含 status,从列表端点(唯一带 status 的)按 id 兜底补上,
    # 使 detail 成为一站式(path+status),agent 不必再手搓 /v2/ds/?projectId= REST。
    status = data.get("status")
    if status is None and data.get("projectId"):
        try:
            items = requests.get(f"{BASE}/?projectId={data['projectId']}&page=1&pageSize=100",
                                 headers=HEADERS).json().get("data", {}).get("items", []) or []
            hit = next((i for i in items if i.get("id") == data.get("id")), None)
            if hit:
                status = hit.get("status")
        except Exception:
            pass
    print(f"Dataset: {data.get('title', '?')}")
    print(f"  ID:      {data.get('id')}")
    print(f"  Path:    {data.get('path')}")
    print(f"  Project: {data.get('projectName')}")
    print(f"  Creator: {data.get('creatorName')}")
    print(f"  Status:  {status}  (2=可用)")
    print(f"  Version: {data.get('versionId')}")


def list_versions(dataset_id: int):
    """List all versions of a dataset."""
    r = requests.get(f"{BASE}/{dataset_id}/version", headers=HEADERS)
    data = r.json().get("data", {})
    items = data if isinstance(data, list) else data.get("items", [])

    print(f"Versions for dataset {dataset_id}:\n")
    for v in items:
        version = v.get("version", "?")
        total_count = v.get("totalCount", 0)
        total_size = v.get("totalSize", 0)
        path = v.get("datasetPath", "?")
        size_mb = total_size / (1024 * 1024) if total_size else 0
        print(f"  v{version}: {total_count} files, {size_mb:.1f} MB")
        print(f"    Mount path: {path}")
        if v.get("downloadUri"):
            print(f"    Download:   {v['downloadUri']}")
        print()


def create_version(dataset_id: int, desc: str):
    """Create a new version of an existing dataset."""
    r = requests.post(
        f"{BASE}/{dataset_id}/version",
        headers=HEADERS_JSON,
        json={"versionDesc": desc},
    )
    result = r.json()
    if result.get("code") == 0:
        print(f"New version created for dataset {dataset_id}")
        print(f"Description: {desc}")
        print("Note: Version preparation may take a few minutes for large datasets.")
    else:
        print(f"Failed: {result}")


def check_permission(dataset_id: int):
    """Check dataset permissions."""
    r = requests.get(f"{BASE}/{dataset_id}/permission", headers=HEADERS)
    data = r.json().get("data", {})
    print(f"Permissions for dataset {dataset_id}:")
    print(json.dumps(data, indent=2, ensure_ascii=False))


def _iterate_all(host, token, prefix, _depth=0, _max_depth=20):
    """Recursively list all LEAF files under prefix. Returns [{path, size}].

    tiefblue /api/iterate lists ONE level (dir entries come back with isDir=true, e.g.
    the `upload/` layer that `bohr dataset create -l <dir>` produces). We must descend
    into each dir, or callers see only `upload/` and mistake it for a file.
    """
    out, next_token = [], ""
    while True:
        data = requests.post(
            f"{host}/api/iterate",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={"maxObjects": 200, "prefix": prefix, "nextToken": next_token},
        ).json().get("data", {})
        for o in (data.get("objects") or []):
            p = o.get("path", "")
            if p.rstrip("/") == prefix.rstrip("/"):
                continue  # the prefix dir entry itself
            if o.get("isDir") or p.endswith("/"):
                if _depth < _max_depth:
                    sub = p if p.endswith("/") else p + "/"
                    out.extend(_iterate_all(host, token, sub, _depth + 1, _max_depth))
            else:
                out.append({"path": p, "size": o.get("size", 0)})
        next_token = data.get("nextToken", "")
        if not data.get("hasNext") or not next_token:
            break
    return out


def list_files(dataset_id: int, version: str = None, as_json: bool = False, quiet: bool = False):
    """List files INSIDE a dataset and resolve each to its exact in-job mount path.

    Chain (all verified): detail -> projectId + mount root; version -> tiefbluePath;
    input/token -> tiefblue JWT; tiefblue /api/iterate -> objects. Use this instead of
    guessing filenames or asking the user which file a dataset contains.
    """
    detail = requests.get(f"{BASE}/{dataset_id}", headers=HEADERS).json().get("data", {})
    project_id = detail.get("projectId")
    mount_root = detail.get("path", "")  # e.g. /bohr/<name>-<suffix>/v1
    if not project_id or not mount_root:
        print(f"Failed to get dataset {dataset_id} detail (check id / permission).")
        return

    vr = requests.get(f"{BASE}/{dataset_id}/version", headers=HEADERS).json().get("data", [])
    versions = vr if isinstance(vr, list) else vr.get("items", [])
    if not versions:
        print(f"No versions for dataset {dataset_id}.")
        return
    ver = versions[0]
    if version:
        want = str(version).lstrip("v")
        ver = next((v for v in versions if str(v.get("version")).lstrip("v") == want), None)
        if ver is None:
            print(f"Version {version} not found (have: {[v.get('version') for v in versions]}).")
            return
    tb_path = (ver.get("tiefbluePath") or "").rstrip("/")
    if not tb_path:
        print("Version has no tiefbluePath.")
        return

    tk = requests.get(
        f"{BASE}/input/token", headers=HEADERS,
        params={"projectId": project_id, "path": tb_path},
    ).json().get("data", {})
    token = tk.get("token", "")
    host = tk.get("host") or "https://tiefblue.dp.tech"
    if not token:
        print("Failed to get tiefblue token.")
        return

    prefix = tb_path + "/"
    leaves = _iterate_all(host, token, prefix)  # recurses through upload/ etc.

    results = []
    for o in leaves:
        p = o["path"]
        rel = p[len(prefix):] if p.startswith(prefix) else p.rsplit("/", 1)[-1]
        if not rel:
            continue
        results.append({
            "file": rel,                       # may include a dir layer, e.g. upload/st_1.raw
            "size": o.get("size", 0),
            "isDir": False,
            "mount_path": f"{mount_root}/{rel}",
        })

    if quiet:
        return results

    if as_json:
        print(json.dumps(
            {"dataset_id": dataset_id, "title": detail.get("title"),
             "mount_root": mount_root, "files": results},
            ensure_ascii=False, indent=2))
        return results

    print(f"Dataset {dataset_id} ({detail.get('title', '?')}) — mount root {mount_root}:\n")
    if not results:
        print("  (empty)")
    for it in results:
        tag = "DIR " if it["isDir"] else "FILE"
        mb = it["size"] / (1024 * 1024) if it["size"] else 0
        print(f"  [{tag}] {it['file']}  ({mb:.1f} MB)")
        print(f"         → 填入 pipeline: {it['mount_path']}")
    return results


def _stat_disk_file(disk_path: str, project_id: int):
    """Size of a file on the share/personal disk, via the v1 file API.

    The agent sandbox does NOT mount /share or /personal, so os.path.getsize() is not an
    option here — the size has to come from the platform.
    Returns (basename, size) or (basename, None) when the file does not exist.
    """
    p = disk_path.strip().lstrip("/")
    if not p.startswith(("share/", "personal/")):
        die(f"--disk-path must be a disk path, got: {disk_path}",
            fix="Pass the path as it appears on the disk, starting with share/ or personal/ — "
                "e.g. share/jubao/run1/sample.mzML. Not a /bohr/... mount path, not a local "
                "workspace path.", code=2)

    v1 = "https://open.bohrium.com/openapi/v1"
    uid = (api("GET", f"{v1}/ak/get").get("data") or {}).get("user_id")
    if not uid:
        die("could not resolve the Bohrium user id from the access key",
            fix="The key is loaded but the platform will not identify it. Re-run setup.sh and "
                "`source /bohr-workspace/.bohr_env`, then retry.", code=1)
    pid = 0 if p.startswith("personal/") else project_id
    d = (api("GET", f"{v1}/file/stat/{p}",
             params={"projectId": pid, "userId": uid}).get("data") or {})
    base = os.path.basename(p)
    if not d.get("exist") or not d.get("contentLength"):
        return base, None
    return base, int(d["contentLength"])


def _iter_datasets(project_id: int, page_size: int = 100):
    """Yield EVERY dataset in the project, walking pagination to the end.

    The list endpoint silently defaults to pageSize=10. Scanning only that first page
    makes dedup report "not found" for a file that IS on the platform — which is exactly
    how a multi-GB re-upload happens. So: never trust one page, and if we cannot account
    for all `total` datasets, fail loudly rather than return a miss we cannot stand behind.
    """
    page, seen, total = 1, 0, None
    while True:
        r = api("GET", f"{BASE}/", params={"projectId": project_id,
                                           "page": page, "pageSize": page_size})
        data = r.get("data") or {}
        items = data.get("items") or []
        if total is None:
            total = data.get("total")
        for d in items:
            seen += 1
            yield d
        if not items or (total is not None and seen >= total):
            break
        page += 1
        if page > 200:                # runaway guard: a broken endpoint must not loop forever
            break
    if total is not None and seen < total:
        die(f"dataset scan incomplete: saw {seen} of {total} datasets in project {project_id}",
            fix="Retry — the listing endpoint truncated. Do NOT treat this as 'file not on "
                "the platform': an unscanned dataset may already contain it.",
            never="Do NOT proceed to upload after an incomplete scan. That is how the same "
                  "multi-GB file gets uploaded twice.")


def _find_hit(project_id: int, name: str, size: int):
    """Scan the project's datasets for a file with this exact basename + byte size.

    Content identity, not title. Returns (hit_dict_or_None, datasets_scanned).
    The scan count is part of the answer: a MISS is only trustworthy if it looked at all
    of them. No printing, no exit.
    """
    if not name or not size:
        return None, 0
    scanned = 0
    for d in _iter_datasets(project_id):
        scanned += 1
        if d.get("status") != 2:      # 2 = committed/usable
            continue
        try:
            files = list_files(d["id"], quiet=True) or []
        except Exception:
            continue                  # unreadable dataset: skip, don't abort the scan
        for f in files:
            if os.path.basename(f.get("file", "")) == name and int(f.get("size", 0)) == size:
                return {"found": True, "dataset_id": d["id"], "title": d.get("title"),
                        "file": f["file"], "size": f["size"], "mount_path": f["mount_path"],
                        "scanned": scanned}, scanned
    return None, scanned


def find_dataset_for_file(project_id: int, disk_path: str = None,
                          name: str = None, size: int = None, as_json: bool = False):
    """Find an existing dataset already containing this exact file — the dedup primitive.

    Matches on CONTENT IDENTITY (basename + byte size), never on dataset title. Titles are
    a naming convention and break the moment the same file is staged under a new path, which
    silently causes a multi-GB re-upload of data that is already on the platform.

    Exit codes: 0 = hit (reuse it), 4 = no hit (safe to create), 2 = bad input / missing source.
    """
    if disk_path:
        name, size = _stat_disk_file(disk_path, project_id)
        if size is None:
            die(f"source file does not exist on the disk: {disk_path}",
                fix="List the parent directory and check the exact path/spelling, then retry. "
                    "If the user gave this path, tell them the file is not there — do not "
                    "silently pick something else.",
                never="Do NOT reuse a dataset whose title merely looks similar. That feeds the "
                      "WRONG DATA into the pipeline and the results will be silently invalid.",
                code=2)
    if not name or not size:
        die("nothing to look up",
            fix="Pass --disk-path share/... (preferred), or both --name and --size.", code=2)

    hit, scanned = _find_hit(project_id, name, size)
    if hit:
        if as_json:
            print(json.dumps(hit, ensure_ascii=False, indent=2))
        else:
            print("✅ HIT — this file is already on the platform. Reuse it, upload nothing.\n")
            print(f"   dataset : {hit['title']}  (id {hit['dataset_id']})")
            print(f"   size    : {hit['size']} bytes (exact match)")
            print(f"   mount   : {hit['mount_path']}")
        return hit

    miss = {"found": False, "name": name, "size": size, "scanned": scanned}
    if as_json:
        print(json.dumps(miss, ensure_ascii=False, indent=2))
    else:
        print(f"❌ MISS — scanned all {scanned} datasets in project {project_id}; none contains {name} ({size} bytes).")
        print("   FIX: create it (no download involved):")
        print(f"        dataset_manager.py create-from-disk --project-id {project_id} "
              "--disk-path share/<path>")
    sys.exit(4)


SDBX_PY = "/data/skills/bohrium-sandbox/sdbx.py"
BOHR_INSTALL = ("https://dp-public.oss-cn-beijing.aliyuncs.com/bohrctl/1.0.0/"
                "install_bohr_linux_curl.sh")


def _sdbx_base():
    """The sandbox CLI to shell out to: the bohrium-sandbox skill's sdbx.py, or `lbg sdbx`.

    Falling back to `lbg sdbx` silently is how we got burned: when the skill is not loaded,
    sdbx.py does not exist, and most installed `lbg` builds have no `sdbx` subcommand at all —
    so every call came back as an argparse usage error, which this script then reported as
    "the sandbox gateway is failing". It was not. The skill just was not there.
    """
    import subprocess

    def has_sdbx():
        return subprocess.run(["lbg", "sdbx", "--help"],
                              capture_output=True, text=True).returncode == 0

    # `lbg sdbx` only exists in the PRERELEASE lbg (4.0.0b*). A plain `pip install lbg` lands
    # 1.2.29, whose subcommands are {node,program,project,image,...} — no sdbx at all. Every
    # call then dies with an argparse usage error that looks nothing like "wrong lbg version",
    # which is how this got misread for so long as "the sandbox gateway is down".
    if not has_sdbx():
        print("[sandbox] lbg has no `sdbx` subcommand — installing the prerelease lbg…")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--pre", "--upgrade", "lbg"],
                       capture_output=True, text=True, timeout=600)
        if not has_sdbx():
            die("`lbg sdbx` is unavailable even after installing the prerelease lbg",
                fix="Run `python3 -m pip install --pre --upgrade lbg` and check "
                    "`lbg sdbx --help`. The sandbox subcommand ships ONLY in the prerelease "
                    "(4.0.0b*); the stable 1.2.29 does not have it.",
                never="Do NOT read this as a platform outage, and do NOT work around it by "
                      "downloading the spectra into the workspace to build the dataset from "
                      "there. Fix the CLI.",
                code=5)

    return [sys.executable, SDBX_PY] if os.path.exists(SDBX_PY) else ["lbg", "sdbx"]


def _sdbx(*args, timeout=900):
    """Invoke the sandbox CLI.

    Also strips the `{"kind":"upgrade_available",...}` banner sdbx.py can prepend, which
    otherwise breaks json.loads on the caller side.
    """
    import subprocess
    base = _sdbx_base()
    # The prerelease lbg reads the key from BOHRIUM_ACCESS_KEY — a third spelling, next to our
    # ACCESS_KEY and BOHR_ACCESS_KEY. Without it lbg exits with SdbxConfigError, which this
    # script used to report as "the sandbox gateway is failing". Map it here so the sandbox
    # works whether or not the bohrium-sandbox skill (whose sdbx.py does only this) is loaded.
    env = os.environ.copy()
    ak = env.get("BOHR_ACCESS_KEY") or env.get("ACCESS_KEY")
    if ak:
        env.setdefault("BOHRIUM_ACCESS_KEY", ak)
    r = subprocess.run(base + list(args), capture_output=True, text=True, timeout=timeout, env=env)
    out = "\n".join(l for l in (r.stdout or "").splitlines()
                    if "upgrade_available" not in l)
    return r.returncode, out.strip(), (r.stderr or "").strip()


def _sandbox_ready(project_id: int, reuse: bool = True):
    """Get a sandbox with the project's share disk mounted. Reuses a live one when possible.

    Handles the 502 gateway timeout on create: the sandbox is often built server-side anyway
    (image cold-pull outlasts the gateway deadline), so we re-list instead of blindly retrying,
    which would otherwise pile up orphan sandboxes.
    """
    import time

    def find_live():
        rc, out, _ = _sdbx("ls", "--json", timeout=120)
        if rc != 0 or not out:
            return None
        try:
            for s in json.loads(out):
                if s.get("template") == "sdbxagent" and s.get("status_name") == "running":
                    return s.get("sandbox_id")
        except Exception:
            pass
        return None

    if reuse:
        sid = find_live()
        if sid:
            print(f"[sandbox] reusing {sid}")
            return sid

    for attempt in (1, 2, 3):
        print(f"[sandbox] creating (attempt {attempt}/3)…")
        rc, out, err = _sdbx("create", "sdbxagent", "--mount-user-storage",
                             "--project-id", str(project_id), "--timeout", "3600",
                             "--json", timeout=900)
        if rc == 0 and out:
            try:
                sid = json.loads(out).get("sandboxID")
                if sid:
                    print(f"[sandbox] created {sid}")
                    return sid
            except Exception:
                pass
        # 502 / gateway timeout: it may exist anyway — look before leaping
        time.sleep(10)
        sid = find_live()
        if sid:
            print(f"[sandbox] gateway timed out but the sandbox came up: {sid}")
            return sid
        last = (out or err or "").strip()
        print(f"[sandbox] attempt {attempt} failed: {last[:160]}")

        # Only a 5xx/timeout is worth retrying. A config or CLI error will fail identically
        # three times and then get reported as a platform outage — which is exactly how a
        # missing env var and a wrong lbg version both got misdiagnosed as "the gateway is
        # down". Anything we can name, we name, and we stop.
        for marker, what, fix in (
            ("SdbxConfigError", "the sandbox CLI has no access key",
             "Export BOHRIUM_ACCESS_KEY (the prerelease lbg reads that spelling, not "
             "ACCESS_KEY / BOHR_ACCESS_KEY), or re-run `source /bohr-workspace/.bohr_env`."),
            ("usage: lbg", "the installed lbg is too old to have a `sdbx` subcommand",
             "Run `python3 -m pip install --pre --upgrade lbg`. sdbx ships only in the "
             "prerelease (4.0.0b*); the stable 1.2.29 does not have it."),
        ):
            if marker in last:
                die(f"cannot create a sandbox: {what}", fix=fix,
                    never="This is NOT a platform outage — do not tell the user to retry later, "
                          "and do not download the spectra into the workspace to work around it.",
                    code=5)

    die("could not get a sandbox after 3 attempts — the Bohrium sandbox gateway is failing",
        fix="The failure was not a config or CLI problem (those are detected separately), so "
            "this looks platform-side. Report the message above verbatim to the user and stop; "
            "suggest retrying later.",
        never="Do NOT download the spectra into the workspace to 'work around' it — a "
              "multi-GB download will blow the workspace and is not the supported path. "
              "Do NOT invent another upload route or hand-craft REST calls.",
        code=5)


def create_from_disk(project_id: int, disk_path: str, name: str = None,
                     reuse_sandbox: bool = True, as_json: bool = False):
    """Turn a file already sitting on the share/personal disk into a dataset — no download.

    One command on purpose. Every step below has bitten us when left to freehand shell:
    the CLI install URL gets invented, `--user root` gets dropped (then /root is unwritable),
    plain `pip install -U lbg` lands a stable build with no `dataset` subcommand, and the
    foreground 60s exec timeout silently truncates a multi-GB upload.
    """
    import time

    # 0) dedup first — the whole sandbox dance is pointless if the file is already up there
    hit, _ = _find_hit(project_id, *_stat_disk_file(disk_path, project_id))
    if hit:
        print("✅ already on the platform — nothing to upload.")
        if as_json:
            print(json.dumps(hit, ensure_ascii=False, indent=2))
        else:
            print(f"   dataset: {hit['title']}  (id {hit['dataset_id']})")
            print(f"   mount  : {hit['mount_path']}")
        return hit

    base, size = _stat_disk_file(disk_path, project_id)
    if size is None:
        die(f"source file does not exist on the disk: {disk_path}",
            fix="Check the exact path and spelling (list the parent directory). If the user "
                "supplied this path, tell them the file is not there and stop.",
            never="Do NOT reuse a dataset that merely looks similar by name — that feeds the "
                  "WRONG DATA into the pipeline and the results will be silently invalid.",
            code=2)

    p = "/" + disk_path.strip().lstrip("/")          # in-sandbox path: /share/... or /personal/...
    ident = (name or os.path.splitext(base)[0]).lower()
    ident = "".join(c if c.isalnum() else "-" for c in ident).strip("-")[:40] or "dataset"
    print(f"[plan] {p}  ({size/1e6:.1f} MB)  →  dataset '{ident}'")

    # Quota BEFORE the sandbox dance. Registration is the LAST step of the upload, so a full
    # sandbox + multi-hundred-MB transfer gets burned before the platform says "no slots left".
    q = (api("GET", f"{BASE}/quota/check", params={"projectId": project_id}).get("data") or {})
    if q.get("result") is False:
        die(f"project {project_id} is out of dataset slots ({q.get('used')}/{q.get('limit')} used)",
            fix="Free a slot (delete a dataset you no longer need) or use a project with room. "
                "Nothing was uploaded — this was checked before any transfer.",
            never="Do NOT retry as-is, and do NOT read this as a transient platform error: the "
                  "upload will fail at the very end every single time, after wasting the "
                  "whole transfer.",
            code=9)

    sid = _sandbox_ready(project_id, reuse_sandbox)

    # 1) bohr CLI inside the sandbox. --user root is mandatory: the default `user` cannot
    #    read /personal and cannot write /root.
    print("[sandbox] installing bohr CLI…")
    rc, out, err = _sdbx("exec", "--user", "root", "--timeout", "300", sid,
                         f"curl -fsSL {BOHR_INSTALL} | bash", timeout=420)
    rc2, ver, _ = _sdbx("exec", "--user", "root", "--timeout", "60", sid,
                        "export PATH=/root/.bohrium:$PATH && bohr -v", timeout=120)
    if rc2 != 0:
        die(f"the bohr CLI could not be installed in sandbox {sid}\n"
            f"       install output: {(out or '')[:200]}\n"
            f"       verify output : {(err or ver or '')[:200]}",
            fix=f"Usually transient (network inside the sandbox). Retry the same command. "
                f"If it persists, inspect the sandbox: "
                f"`sdbx.py exec --user root {sid} 'curl -sSI {BOHR_INSTALL} | head -1'`.",
            never="Do NOT try a different install URL — this one is the only correct address. "
                  "Do NOT `pip install lbg` as a substitute: the stable lbg has no `dataset` "
                  "subcommand. Do NOT drop --user root.",
            code=6)

    # 2) upload in the background — a foreground exec dies at 60s, which for a multi-GB
    #    spectrum file means a truncated upload reported as success.
    # Per-upload log. The sandbox is REUSED across calls, so a shared /tmp/upload.log gets
    # written by two concurrent uploads at once: their output interleaves and the success
    # check then reads *someone else's* "EXIT_CODE=0 … success" and declares victory for a
    # file that never finished. Has happened. One log per upload, and only ever read this one.
    log = f"/tmp/upload-{ident}-{size}.log"
    print("[sandbox] uploading in background (this is the slow part)…")
    script = (
        "export PATH=/root/.bohrium:$PATH\n"
        "export OPENAPI_HOST=https://open.bohrium.com\n"
        "export TIEFBLUE_HOST=https://tiefblue.dp.tech\n"
        f"export ACCESS_KEY={AK}\n"
        f"echo n | bohr dataset create -n '{ident}' -p '{ident}' -i {project_id} "
        f"-l '{p}' > {log} 2>&1\n"
        f"echo EXIT_CODE=$? >> {log}\n"
    )
    rc, out, err = _sdbx("exec", "--user", "root", "--background", sid, script, timeout=180)
    if rc != 0:
        die(f"could not start the background upload in sandbox {sid}: {(out or err)[:200]}",
            fix="Retry the same command. If it fails again, the sandbox may be unhealthy — "
                "rerun with --fresh-sandbox to get a new one.",
            never="Do NOT run the upload in the foreground instead: exec dies at 60s and a "
                  "large spectrum file will be silently truncated.",
            code=6)

    # 3) poll the log — bounded, never spin forever
    deadline = time.time() + 3600
    while time.time() < deadline:
        time.sleep(20)
        rc, tail, _ = _sdbx("exec", "--user", "root", "--timeout", "30", sid,
                            f"cat {log} 2>/dev/null | tail -3", timeout=90)
        # `bohr dataset create` exits 0 even when it fails ("Failed to create dataset, err:
        # …upper limit…" + EXIT_CODE=0), so the exit code alone proves nothing. Demand the
        # CLI's own success line for THIS dataset name.
        if f"create dataset {ident} success" in tail.lower():
            print("[sandbox] upload finished.")
            break
        if "EXIT_CODE=" in tail:                     # finished, but non-zero
            die(f"the upload failed inside sandbox {sid}. Its log says:\n{tail}",
                fix="Read the log above — it names the real cause (quota exhausted, bad "
                    "project id, unreadable source path). Fix that and retry. Check quota "
                    f"with: dataset_manager.py quota --project_id {project_id}",
                never="Do NOT retry blindly with the same inputs, and do NOT switch to "
                      "downloading the file into the workspace.",
                code=6)
        print(f"   … still uploading ({int(deadline - time.time())}s budget left)")
    else:
        die(f"upload still unfinished after 60 min (sandbox {sid} left running on purpose)",
            fix=f"The upload may still be running. Check it with:\n"
                f"       sdbx.py exec --user root {sid} 'tail -5 {log}'\n"
                f"       Then re-run `find --project-id {project_id} --disk-path {disk_path}` "
                f"— if it HITs, the upload actually completed and you can just use it.",
            never="Do NOT start a second upload of the same file — you will end up with "
                  "duplicate datasets burning quota.",
            code=7)

    # 4) resolve the REAL mount path — Bohrium appends a random suffix (-3gbh), so the
    #    path must be read back, never guessed from the identifier.
    for _ in range(6):
        time.sleep(5)
        hit, _ = _find_hit(project_id, base, size)
        if hit:
            print("\n✅ dataset ready.")
            if as_json:
                print(json.dumps(hit, ensure_ascii=False, indent=2))
            else:
                print(f"   dataset: {hit['title']}  (id {hit['dataset_id']})")
                print(f"   mount  : {hit['mount_path']}")
            return hit
    die("the upload reported success, but the file is not visible in any dataset yet",
        fix=f"Bohrium is still materialising the dataset version (can take a few minutes for "
            f"large files). Wait, then run:\n"
            f"       dataset_manager.py find --project-id {project_id} --disk-path {disk_path}\n"
            f"       When it HITs, use the mount_path it prints.",
        never="Do NOT upload again — the data is already there; a second upload just wastes "
              "quota and creates a duplicate.",
        code=7)


def _resolve_version_token(dataset_id: int, version: str = None):
    """Return (detail, tb_path, token, host) for a dataset version. None on failure."""
    detail = requests.get(f"{BASE}/{dataset_id}", headers=HEADERS).json().get("data", {})
    project_id = detail.get("projectId")
    if not project_id:
        print(f"Failed to get dataset {dataset_id} detail (check id / permission).")
        return None
    vr = requests.get(f"{BASE}/{dataset_id}/version", headers=HEADERS).json().get("data", [])
    versions = vr if isinstance(vr, list) else vr.get("items", [])
    if not versions:
        print(f"No versions for dataset {dataset_id}.")
        return None
    ver = versions[0]
    if version:
        want = str(version).lstrip("v")
        ver = next((v for v in versions if str(v.get("version")).lstrip("v") == want), None)
        if ver is None:
            print(f"Version {version} not found (have: {[v.get('version') for v in versions]}).")
            return None
    tb_path = (ver.get("tiefbluePath") or "").rstrip("/")
    if not tb_path:
        print("Version has no tiefbluePath.")
        return None
    tk = requests.get(
        f"{BASE}/input/token", headers=HEADERS,
        params={"projectId": project_id, "path": tb_path},
    ).json().get("data", {})
    token = tk.get("token", "")
    host = tk.get("host") or "https://tiefblue.dp.tech"
    if not token:
        print("Failed to get tiefblue token.")
        return None
    return detail, tb_path, token, host


def download_file(dataset_id: int, filename: str, out: str = None, version: str = None):
    """Download ONE file out of a dataset to a local path (writable copy).

    Normally you MOUNT a dataset (read-only) in the job. Use this only when you need a
    writable local copy (e.g. a FASTA that lives inside a dataset must go via -p).
    """
    resolved = _resolve_version_token(dataset_id, version)
    if not resolved:
        return
    _detail, tb_path, token, host = resolved
    # Resolve `filename` to a full object path: exact rel match, else unique basename match.
    # (Handles the upload/ layer: `--file st_1.raw` finds `.../upload/st_1.raw`.)
    prefix = tb_path + "/"
    rels = {l["path"][len(prefix):]: l["path"]
            for l in _iterate_all(host, token, prefix) if l["path"].startswith(prefix)}
    if filename in rels:
        obj = rels[filename]
    else:
        base = filename.rsplit("/", 1)[-1]
        cands = [full for rel, full in rels.items() if rel.rsplit("/", 1)[-1] == base]
        if len(cands) == 1:
            obj = cands[0]
        elif not cands:
            print(f"File '{filename}' not found. Available: {sorted(rels)}")
            return
        else:
            print(f"Ambiguous '{filename}': {cands}. Pass the full internal path.")
            return
    out = out or filename.rsplit("/", 1)[-1]
    # tolerate --out being a directory (or dir/): drop the file inside it
    if out.endswith("/") or os.path.isdir(out):
        out = os.path.join(out, filename.rsplit("/", 1)[-1])
    # tiefblue /api/download/<obj> 307-redirects to a presigned OSS URL; requests follows it
    # (and strips our Bearer on the cross-host hop, which is correct — the OSS URL is signed).
    r = requests.get(
        f"{host}/api/download/{obj}",
        headers={"Authorization": f"Bearer {token}"},
        stream=True, allow_redirects=True,
    )
    if r.status_code != 200:
        print(f"Download failed: HTTP {r.status_code} {r.text[:200]}")
        return
    size = 0
    with open(out, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            f.write(chunk)
            size += len(chunk)
    print(f"Downloaded {filename} -> {out}  ({size / (1024 * 1024):.1f} MB)")


def main():
    parser = argparse.ArgumentParser(description="Bohrium dataset manager")
    sub = parser.add_subparsers(dest="cmd")

    p_quota = sub.add_parser("quota", help="Check dataset quota")
    p_quota.add_argument("--project_id", type=int, required=True)

    p_detail = sub.add_parser("detail", help="Get dataset details")
    p_detail.add_argument("--id", type=int, required=True)

    p_versions = sub.add_parser("versions", help="List dataset versions")
    p_versions.add_argument("--id", type=int, required=True)

    p_new = sub.add_parser("new_version", help="Create new version")
    p_new.add_argument("--id", type=int, required=True)
    p_new.add_argument("--desc", type=str, required=True)

    p_perm = sub.add_parser("permission", help="Check permissions")
    p_perm.add_argument("--id", type=int, required=True)

    p_files = sub.add_parser(
        "files", help="List files inside a dataset and resolve exact /bohr/... mount paths")
    p_files.add_argument("--id", type=int, required=True)
    p_files.add_argument("--version", type=str, default=None,
                         help="e.g. 1 or v1 (default: latest)")
    p_files.add_argument("--json", action="store_true")

    p_find = sub.add_parser(
        "find",
        help="DEDUP: find an existing dataset already holding this file (match on name+size, "
             "never on title). Run this BEFORE creating any dataset.",
    )
    p_find.add_argument("--project-id", "--project_id", dest="project_id", type=int, required=True)
    p_find.add_argument("--disk-path", "--disk_path", dest="disk_path",
                        help="file on the share/personal disk, e.g. share/jubao/x/foo.mzML")
    p_find.add_argument("--name", help="basename, if the source is not on a disk")
    p_find.add_argument("--size", type=int, help="byte size, used with --name")
    p_find.add_argument("--json", action="store_true")

    p_cfd = sub.add_parser(
        "create-from-disk",
        help="Make a dataset out of a share/personal disk file WITHOUT downloading it. "
             "Dedups first, then handles sandbox + CLI install + background upload + polling.",
    )
    p_cfd.add_argument("--project-id", "--project_id", dest="project_id", type=int, required=True)
    p_cfd.add_argument("--disk-path", "--disk_path", dest="disk_path", required=True,
                       help="share/... or personal/... (file or directory)")
    p_cfd.add_argument("--name", help="dataset name; defaults to the filename")
    p_cfd.add_argument("--fresh-sandbox", dest="fresh", action="store_true",
                       help="do not reuse a running sandbox")
    p_cfd.add_argument("--json", action="store_true")

    p_dl = sub.add_parser(
        "download", help="Download ONE file out of a dataset (writable local copy)")
    p_dl.add_argument("--id", type=int, required=True)
    p_dl.add_argument("--file", type=str, required=True, help="internal filename (from `files`)")
    p_dl.add_argument("--out", type=str, default=None, help="local output path (default: basename)")
    p_dl.add_argument("--version", type=str, default=None)

    args = parser.parse_args()

    if not AK:
        die("no Bohrium access key in the environment",
            fix="Run the skill's setup.sh, then `source /bohr-workspace/.bohr_env` — it exports "
                "ACCESS_KEY and BOHR_ACCESS_KEY with the same value. Either name works here.",
            never="Do not hardcode or guess a key.", code=1)

    if args.cmd == "quota":
        check_quota(args.project_id)
    elif args.cmd == "detail":
        get_detail(args.id)
    elif args.cmd == "versions":
        list_versions(args.id)
    elif args.cmd == "new_version":
        create_version(args.id, args.desc)
    elif args.cmd == "permission":
        check_permission(args.id)
    elif args.cmd == "files":
        list_files(args.id, args.version, args.json)
    elif args.cmd == "find":
        find_dataset_for_file(args.project_id, args.disk_path, args.name, args.size, args.json)
    elif args.cmd == "create-from-disk":
        create_from_disk(args.project_id, args.disk_path, args.name,
                         reuse_sandbox=not args.fresh, as_json=args.json)
    elif args.cmd == "download":
        download_file(args.id, args.file, args.out, args.version)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
