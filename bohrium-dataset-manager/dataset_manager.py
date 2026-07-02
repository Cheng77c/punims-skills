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
    print(f"Dataset: {data.get('title', '?')}")
    print(f"  ID:      {data.get('id')}")
    print(f"  Path:    {data.get('path')}")
    print(f"  Project: {data.get('projectName')}")
    print(f"  Creator: {data.get('creatorName')}")
    print(f"  Status:  {data.get('status')}")
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


def list_files(dataset_id: int, version: str = None, as_json: bool = False):
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

    if as_json:
        print(json.dumps(
            {"dataset_id": dataset_id, "title": detail.get("title"),
             "mount_root": mount_root, "files": results},
            ensure_ascii=False, indent=2))
        return

    print(f"Dataset {dataset_id} ({detail.get('title', '?')}) — mount root {mount_root}:\n")
    if not results:
        print("  (empty)")
    for it in results:
        tag = "DIR " if it["isDir"] else "FILE"
        mb = it["size"] / (1024 * 1024) if it["size"] else 0
        print(f"  [{tag}] {it['file']}  ({mb:.1f} MB)")
        print(f"         → 填入 pipeline: {it['mount_path']}")


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

    p_dl = sub.add_parser(
        "download", help="Download ONE file out of a dataset (writable local copy)")
    p_dl.add_argument("--id", type=int, required=True)
    p_dl.add_argument("--file", type=str, required=True, help="internal filename (from `files`)")
    p_dl.add_argument("--out", type=str, default=None, help="local output path (default: basename)")
    p_dl.add_argument("--version", type=str, default=None)

    args = parser.parse_args()

    if not AK:
        print("ERROR: set BOHR_ACCESS_KEY (or ACCESS_KEY) environment variable")
        sys.exit(1)

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
    elif args.cmd == "download":
        download_file(args.id, args.file, args.out, args.version)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
