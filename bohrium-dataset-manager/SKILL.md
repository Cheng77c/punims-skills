---
name: bohrium-dataset-manager
description: "Manage and inspect Bohrium datasets via bohr CLI or open.bohrium.com API. Use when: creating/listing/deleting datasets, uploading data, managing versions, checking whether a file was ALREADY uploaded before re-uploading it (dedup, `find`), OR listing the files INSIDE a dataset to resolve the exact in-job mount path (/bohr/<name>/v1/<file>) instead of guessing filenames. NOT for: share/personal disk file management (use bohrium-file), job submission, or node management."
requires:
  - bohrium-sandbox   # create-from-disk 靠它的 sdbx.py 把盘上文件直转 dataset;
                       # 不加载 = sdbx.py 不存在 = 建集必失败(且会伪装成「网关故障」)
---

# SKILL: Bohrium 数据集 (Dataset) 管理与查看

## 概述

**Bohrium 数据操作的一站式 skill。** 加载本 skill 即掌握全部数据操作,无需再依赖其他 skill:

- **数据集(dataset)**:**查重(`find`,建集前必跑)** / 创建(本地 / **从共享盘·个人盘直接建,免下载** / API)/ 列出 / 看内部文件拿确切挂载路径 / 版本 / 删除 / 在任务中挂载。
- **文件盘(个人盘 personal / 项目共享盘 share)**:列目录 / 下载 / 上传 / stat / mkdir / 移动 / 复制 / 删除 / 解压。
- **把数据喂进计算任务**:见下方「数据进任务:路由决策」——不同来源(工作区 / 文件盘 / 数据集)+ 不同用途(只读挂载 / 需可写)对应不同操作,别猜、别反问用户。

**优先使用 `bohr` CLI**;CLI 不覆盖的(版本管理、配额、看数据集内部文件、文件盘操作)走 OpenAPI(`https://open.bohrium.com/openapi`)。`bohr dataset create` 相比 Web 上传:**无大小限制**、**支持断点续传**。

数据集解决的场景:每次提交都要等打包上传 → 挂载数据集免重复上传;大文件上传慢 → 无大小限制 + 断点续传;与他人共享 → 项目内共享。

## 数据进任务:路由决策(先看这个)

把数据喂进计算任务前,先按「**数据在哪 × 要干嘛**」定位操作。核心原则:**谱图等只读大输入 → 数据集挂载(不下载);需可写的小文件(尤其 FASTA)→ 下载到本地随包上传。**

| 数据在哪 | 用途 | 怎么做 |
|---|---|---|
| 文件盘(share/personal)的**谱图** | 任务只读输入 | 一条命令:`dataset_manager.py create-from-disk --project-id <pid> --disk-path share/<路径>`(内含查重,已存在则零传输)→ 用它返回的 `mount_path`。**绝不下载到本地** |
| 文件盘(share/personal)的 **FASTA / 需可写小文件** | 搜索引擎要在同目录建索引(可写) | **下载**到任务目录(见「下载数据」)→ 随包上传 `-p`,**不要做成只读数据集** |
| **已有数据集**,但不知里面文件名 | 要引用具体文件 | `dataset_manager.py files --id <ID>` 拿确切 `/bohr/<名>/v1/<文件>`——**别猜、别问用户** |
| 已有数据集,要在任务里用 | 只读输入 | 直接挂载 `dataset_path`,**不要下载**;真要本地副本才用 `downloadUri`(整包 zip) |
| 工作区本地小文件 | 随包 | 直接 `-p` 上传 |

> 判定为某专业流程(如蛋白质组学)时,以该流程 skill 的路由表为准;本表是通用底座。

## 认证配置

BOHR_ACCESS_KEY 从 OpenClaw 配置文件 `~/.openclaw/openclaw.json` 中读取：

```json
"bohrium-dataset-manager": {
  "enabled": true,
  "apiKey": "YOUR_BOHR_ACCESS_KEY",
  "env": {
    "BOHR_ACCESS_KEY": "YOUR_BOHR_ACCESS_KEY"
  }
}
```

OpenClaw 会自动把 `env.BOHR_ACCESS_KEY` 注入运行环境。

> ⚠️ **两套工具、两个变量名,必须都设好(最常见的翻车点)**:
> - **HTTP API / `dataset_manager.py`** 读 `BOHR_ACCESS_KEY`(平台已注入)。
> - **`bohr` CLI 本体读 `ACCESS_KEY`**(不是 `BOHR_ACCESS_KEY`!)。只设 `BOHR_ACCESS_KEY` 就跑 `bohr dataset ...` 会报 `AccessKey Invalid!` 或**空 `Error:`(且 exit code 仍为 0,毫无线索)**。
> - 用 `bohr` CLI 前**先补一行**:`export ACCESS_KEY="$BOHR_ACCESS_KEY"`。

## 前置条件：安装 bohr CLI

```bash
# macOS
/bin/bash -c "$(curl -fsSL https://dp-public.oss-cn-beijing.aliyuncs.com/bohrctl/1.0.0/install_bohr_mac_curl.sh)"

# Linux
/bin/bash -c "$(curl -fsSL https://dp-public.oss-cn-beijing.aliyuncs.com/bohrctl/1.0.0/install_bohr_linux_curl.sh)"

source ~/.bashrc  # 或 source ~/.zshrc
export PATH="$HOME/.bohrium:$PATH"
export OPENAPI_HOST=https://open.bohrium.com
export ACCESS_KEY="$BOHR_ACCESS_KEY"   # ★ bohr CLI 认这个变量;不设会 AccessKey Invalid / 空 Error
```

---

## 列出数据集

```bash
export ACCESS_KEY="$BOHR_ACCESS_KEY"    # ★ bohr CLI 认 ACCESS_KEY(见「认证配置」)
bohr dataset list -p YOUR_PROJECT_ID --json      # 按项目过滤(JSON)
bohr dataset list -p YOUR_PROJECT_ID -t "my-dataset" --json   # 按标题搜索(title 跨项目重名,-p+-t 合用)
```
> ⚠️ **务必带 `--json`**:不带 `--json` 时 bohr CLI 走交互式分页,在无终端环境会报 `Error: open /dev/tty: no such device or address`。

**JSON 输出字段：**

| 字段 | 说明 |
|------|------|
| `id` | 数据集 ID |
| `title` | 数据集名称 |
| `path` | 挂载路径（如 `/bohr/my-dataset/v1`） |
| `projectName` | 所属项目 |
| `creatorName` | 创建者 |
| `updateTime` | 更新时间 |
| `desc` | 描述 |

---

## 列出数据集内文件（拿确切挂载路径）

`bohr dataset list` 只给数据集**本身**（id/title/挂载根 `/bohr/<名>/v1`），**不给内部文件名**。要在任务里引用某个具体文件（如 `raw_files`/`inputs`），必须知道数据集**内部的确切文件名**——**用这个能力查,绝不猜文件名、也绝不反问用户**：

**先按名字拿到数字 ID**(用户通常只给数据集**名**,而 `files`/`download`/`detail` 都要数字 `--id`):
```bash
export ACCESS_KEY="$BOHR_ACCESS_KEY"     # bohr CLI 认这个,见「认证配置」
bohr dataset list -p <项目ID> -t "<数据集名>" --json    # → 取 items[].id
# ⚠️ title 会跨项目重名,必须 -p + -t 一起用,否则可能拿到别的项目的同名集
```
再用拿到的 ID 查内部文件:
```bash
python dataset_manager.py files --id <ID>            # 人类可读(已递归下钻 upload/ 等子目录)
python dataset_manager.py files --id <ID> --json     # 机器可读
python dataset_manager.py files --id <ID> --version 1   # 指定版本(默认最新)
```

输出每个文件的 `file`（内部文件名，**含可能的 `upload/` 目录层**）、`size`，以及**可直接填进 pipeline 的完整挂载路径** `mount_path`（如 `/bohr/<名>/v1/upload/st_1.raw`）。例如名字很怪的数据集里其实有 `st_1.raw` 和 `st_2.raw`，就能确切拿到路径去用，不必把整个数据集名当文件名。
> `bohr dataset create -l <目录>` 建的集内部会多一层 `upload/`;`files` 已递归,直接用它给的 `mount_path`(**别自己拼、别漏 `upload/`**)。

**实现（已验证的三段式，供参考/移植）：**

```python
# 1) 版本详情 → tiefbluePath
GET  {BASE}/{id}/version                         # data[0].tiefbluePath, 形如 dataset/tiefblue/bohr/<uid>/<名>/v<verid>/
# 2) 取 tiefblue 访问 token（path 用 tiefbluePath 去掉末尾 /）
GET  {BASE}/input/token?projectId=<pid>&path=<tiefbluePath 去末尾/>   # → data.token, data.host
# 3) tiefblue 遍历（prefix 用 tiefbluePath 带末尾 /；Bearer 用上一步 token，不是 ACCESS_KEY）
POST {host}/api/iterate   {"maxObjects":200,"prefix":"<tiefbluePath 带末尾/>","nextToken":""}
#     → data.objects[].{path,size,isDir}；hasNext/nextToken 分页
```
> 坑：token 请求的 `path` **不带**末尾 `/`,而 `iterate` 的 `prefix` **要带**末尾 `/`;`/api/iterate` 用返回的 **token** 鉴权,直接拿 ACCESS_KEY 会 `ErrGatewayTokenInvalid`。

---

## 创建数据集（上传数据）

```bash
bohr dataset create \
  -n "my-dataset" \
  -p "my-dataset" \
  -i YOUR_PROJECT_ID \
  -l "/path/to/local/data"
```

**参数说明：**

| 参数 | 缩写 | 必填 | 说明 |
|------|------|------|------|
| `--name` | `-n` | 是 | 数据集名称 |
| `--path` | `-p` | 是 | 数据集路径标识（英文+数字） |
| `--pid` | `-i` | 是 | 项目 ID |
| `--lp` | `-l` | 是 | 本地数据目录路径 |
| `--comment` | `-m` | 否 | 数据集描述 |

> **断点续传**：如果上传中断（网络问题等），重新运行相同命令并输入 `y` 即可从断点继续上传。

---

## 从共享盘 / 个人盘建数据集（免下载）

盘上的谱图（GB 级）要做成 dataset，**一条命令，不要自己拼流程**：

```bash
python /data/skills/bohrium-dataset-manager/dataset_manager.py create-from-disk \
  --project-id <projectId> --disk-path share/<盘内路径> --json
```

它内部按顺序做完：**先查重**（命中就直接返回 `mount_path`，零传输、根本不开 sandbox）→ 起 sandbox（带 `--mount-user-storage`，502 网关超时自动重试且先查有没有已建成的，不留孤儿）→ 沙箱内装 bohr CLI（`--user root`）→ **后台**上传 → 轮询日志 → **读回真实 `/bohr/...` 挂载路径**（Bohrium 会加随机后缀如 `-6f7j`，只能查、不能拼）。

| exit | 含义 | 你该做什么 |
|---|---|---|
| `0` | 成功（或本来就已存在） | 用它输出的 `mount_path` |
| `2` | 源文件在盘上不存在 | 如实告诉用户路径有问题并停下 |
| `5` | 平台 sandbox 网关故障（重试 3 次仍失败） | **如实报告平台故障并停下。绝不降级去把谱图下载到工作区。** |
| `6` / `7` | 沙箱内上传失败 / 超时 | 把它打印的日志给用户，别自己另起炉灶 |

> 🚫 **不要手工重做这套流程**。以下每一步都真实翻过车：
> - 编造 CLI 安装地址（`open.bohrium.com/openapi/cli/install` → 404，下回来一个内容是 "404" 的脚本）；正确地址只有 `dp-public.oss-cn-beijing.aliyuncs.com/bohrctl/1.0.0/install_bohr_linux_curl.sh`。
> - 漏掉 `--user root`：沙箱默认用户是 `user`，读不了 `/personal`、写不了 `/root`。
> - `pip install -U lbg` 装到稳定版（1.2.x）——**它没有 `dataset` 子命令**；沙箱内该装的是 `bohr` CLI，不是 lbg。
> - 前台 `exec` 60 秒就断，几百 MB 的谱图会被截断上传却报成功 → 必须 `--background` + 轮询日志。
> - 拿 `/bohr/<标识>/v1` 硬拼挂载路径 → 少了随机后缀，任务里必然找不到文件。
>
> 这些坑 `create-from-disk` 全部封装好了。**沙箱默认复用、不 kill**（12h 自动销毁兜底）；确实要新起一个才加 `--fresh-sandbox`。

## 使用数据集

### 在计算任务中挂载

在 `job.json` 中添加 `dataset_path` 字段：

```json
{
  "job_name": "DeePMD-kit test",
  "command": "cd se_e2_a && dp train input.json > tmp_log 2>&1",
  "project_id": YOUR_PROJECT_ID,
  "machine_type": "c4_m15_1 * NVIDIA T4",
  "job_type": "container",
  "image_address": "registry.dp.tech/dptech/deepmd-kit:2.1.5-cuda11.6",
  "dataset_path": ["/bohr/my-dataset/v1", "/bohr/another-dataset/v2"]
}
```

> `dataset_path` 和 `-p`（输入文件目录）可同时使用。

### 在开发机节点中挂载

创建容器开发机时选择需要挂载的数据集版本，启动后通过路径（如 `/bohr/my-dataset/v1`）直接访问。

- 挂载数据集增加 2-4 秒启动延迟（无论数量）
- 用 `df -a | grep bohr` 查看挂载点

### 在 Notebook 中使用

1. 在 Notebook 编辑页面展开侧面板 → 选择已有数据集
2. 鼠标悬停数据集名称 → 点击复制按钮获取路径
3. 在代码中使用路径：`cd /bohr/testdataset-6xwt/v1/`

> 数据集必须在连接节点**之前**添加，之后添加需重启节点才生效。

---

## 版本管理

数据集支持多版本管理，每个版本创建后文件不可更改。

### 创建新版本

通过 Web 界面：
1. 进入数据集详情页 → 点击"新建版本"
2. 系统自动导入最新版本的文件，可增删文件
3. 创建后需等待准备时间（取决于文件大小和数量）

通过 API：
```python
requests.post(f"{BASE}/{dataset_id}/version", headers=HEADERS_JSON,
    json={"versionDesc": "v2 update"})
```

### 版本状态

| status | 含义 |
|--------|------|
| 准备中 | 文件正在复制，其他用户暂不可见 |
| 已发布 | 可用状态 |

> 大文件或大量文件的版本准备可能需要较长时间。

---

## 删除数据集

```bash
bohr dataset delete YOUR_DATASET_ID              # 删除单个
bohr dataset delete YOUR_DATASET_ID YOUR_DATASET_ID_2       # 批量删除
```

> 删除的版本无法恢复。

---

## 数据集权限模型

| 权限类型 | 说明 | 默认拥有者 |
|---------|------|-----------|
| 可管理 | 编辑、删除、创建新版本 | 数据集创建者、项目创建者和管理员 |
| 可使用 | 查看和使用数据集 | 数据集所属项目的全部成员 |

> 可通过编辑数据集将"可使用"权限授予其他项目或用户。

---

## 文件盘操作（个人盘 personal / 项目共享盘 share）

管理用户的**原始文件目录**（不是数据集）。两类盘：

| 文件盘 | 路径前缀 | 必要 ID |
|---|---|---|
| 个人盘 | `personal/` | `userId`；当前用户个人盘可用 `projectId=0` |
| 共享盘 | `share/` | 真实 `projectId` + `userId`（需项目权限） |

先取身份拿 `userId`：
```bash
AK="${BOHR_ACCESS_KEY:?missing}"; BASE=https://open.bohrium.com/openapi
USERID=$(curl -sS "$BASE/v1/ak/get" -H "Authorization: Bearer $AK" | python3 -c "import json,sys;print(json.load(sys.stdin)['data']['user_id'])")
```

**路由表**（personal/share 用 **v1** file API；`/v2/file/*` 只服务 appJob 工作区，勿用于 personal/share）：

| 动作 | 路由 | 说明 |
|---|---|---|
| 列目录 | `POST /v1/file/iterate` | body 字段是 `prefix`（不是 path）；`hasNext` 时用 `nextToken` 翻页 |
| 存在/信息 | `GET /v1/file/stat/{path}?projectId=&userId=` | 增删改前先 stat 确认 |
| 元数据 | `GET /v1/file/meta/{path}?projectId=&userId=` | |
| 下载 | `GET /v1/file/download/{path}?projectId=&userId=` | 路径作 **URL 段**；curl 用 `-L` |
| 建目录 | `POST /v1/file/mkdir` | body: `path,projectId,userId` |
| 移动/改名 | `POST /v1/file/move`（递归 `/mover`） | body: `sourcePath,destinationPath,projectId,userId` |
| 复制 | `POST /v1/file/copy`（递归 `/copyr`） | 同上 |
| 删除 | `DELETE /v1/file/delete/{path}`（递归 `/deleter`） | query: `projectId,userId` |
| 解压 | `POST /v1/file/decompress` | body: `filePath,dirName` |
| 上传 | 见下 | v2 两步凭证（推荐）/ v1 直传 |

列目录：
```bash
# 个人盘根
curl -sS -X POST "$BASE/v1/file/iterate" -H "Authorization: Bearer $AK" -H "Content-Type: application/json" \
  -d "{\"prefix\":\"personal/\",\"projectId\":0,\"userId\":$USERID,\"dirSpace\":\"personal\",\"maxObjects\":100,\"nextToken\":\"\"}"
# 共享盘（须真实 projectId）
curl -sS -X POST "$BASE/v1/file/iterate" -H "Authorization: Bearer $AK" -H "Content-Type: application/json" \
  -d "{\"prefix\":\"share/\",\"projectId\":YOUR_PROJECT_ID,\"userId\":$USERID,\"dirSpace\":\"share\",\"maxObjects\":100,\"nextToken\":\"\"}"
```

写操作（move/copy 字段是 `sourcePath`/`destinationPath`，不是 src/dst；增删改前先 `stat`）：
```bash
curl -sS -X POST "$BASE/v1/file/mkdir" -H "Authorization: Bearer $AK" -H "Content-Type: application/json" -d "{\"path\":\"personal/new\",\"projectId\":0,\"userId\":$USERID}"
curl -sS -X POST "$BASE/v1/file/move"  -H "Authorization: Bearer $AK" -H "Content-Type: application/json" -d "{\"sourcePath\":\"personal/a.txt\",\"destinationPath\":\"personal/b.txt\",\"projectId\":0,\"userId\":$USERID}"
curl -sS -X DELETE "$BASE/v1/file/delete/personal/b.txt?projectId=0&userId=$USERID" -H "Authorization: Bearer $AK"
```

**上传到文件盘（v2 两步，推荐）**：
```bash
# 1) 申请存储网关凭证（path 决定落 personal 还是 share）
curl -sS "$BASE/v2/file/upload/binary?projectId=0&userId=$USERID&path=/personal/new.txt" -H "Authorization: Bearer $AK"
#    → {data:{host, Authorization, X-Storage-Param}}
# 2) 用返回的 host 上传（Authorization / X-Storage-Param 当密钥，勿回显）
curl -sS -X POST "$HOST/api/upload/binary" -H "Authorization: $UP_AUTH" -H "X-Storage-Param: $XSP" --data-binary @local-file
```
v1 直传：`POST /v1/file/upload/binary?...&path=personal/new.txt`（返回 307，curl 必须 `-L`）。

---

## 下载数据：三种来源（重点）

搜索引擎会在 **FASTA 同目录**建索引 → FASTA 必须是**可写本地文件**（随包 `-p`），不能只读挂载。所以"把 FASTA 弄进任务"几乎总要**下载**。三种来源都已实测可用：

**① 从共享盘 / 个人盘下载**（路径作 **URL 段**，`projectId`+`userId` 作 query——**别用 `filePath=` query，后端会 `path invalid!`**）：
```bash
AK="${BOHR_ACCESS_KEY:?}"; BASE=https://open.bohrium.com/openapi
USERID=$(curl -sS "$BASE/v1/ak/get" -H "Authorization: Bearer $AK" | python3 -c "import json,sys;print(json.load(sys.stdin)['data']['user_id'])")
# 共享盘（个人盘：share→personal、projectId→0）
curl -L -sS "$BASE/v1/file/download/share/<完整路径>/xxx.fasta?projectId=YOUR_PROJECT_ID&userId=$USERID" \
  -H "Authorization: Bearer $AK" -o ./xxx.fasta
```

**② 从数据集下载单个文件**（数据集本是只读挂载；仅当需要**可写副本**时才下载，如 FASTA 卡在数据集里）：
```bash
python dataset_manager.py files    --id <ID>                       # 先看内部文件名
python dataset_manager.py download --id <ID> --file xxx.fasta --out ./xxx.fasta
```
（内部走 version→token→`tiefblue.dp.tech/api/download/<obj>`，自动跟随到预签名 OSS URL。）

**③ 整个数据集**（少用；要全量本地副本时）：版本详情的 `downloadUri`，或对每个文件用上面的 `download`。

> 记住路由：**谱图别下载——建/挂载数据集即可;只有需可写的小文件(FASTA/参数)才下载走 `-p`。**

---

## API 补充（CLI 不支持的操作）

以下操作 bohr CLI 不覆盖，需通过 API 完成：

```python
import os, requests

AK = os.environ.get("BOHR_ACCESS_KEY", "")
BASE = "https://open.bohrium.com/openapi/v2/ds"
HEADERS = {"Authorization": f"Bearer {AK}"}
HEADERS_JSON = {**HEADERS, "Content-Type": "application/json"}

# ── 获取数据集详情 ──
r = requests.get(f"{BASE}/{dataset_id}", headers=HEADERS)
# 返回: {id, title, path, versionId, projectName, ...}

# ── 获取数据集版本列表 ──
r = requests.get(f"{BASE}/{dataset_id}/version", headers=HEADERS)
# 返回: [{version, totalCount, totalSize, downloadUri, datasetPath, ...}]

# ── 获取指定版本详情 ──
r = requests.get(f"{BASE}/{dataset_id}/version/{version_id}", headers=HEADERS)

# ── 通过 API 创建数据集（程序化） ──
r = requests.post(f"{BASE}/", headers=HEADERS_JSON, json={
    "title": "my-dataset",
    "projectId": YOUR_PROJECT_ID,
    "identifier": "my-dataset",  # 必填，唯一标识（英文+数字）
})
# 返回: {datasetId, tiefbluePath, requestId}
# 然后用 tiefblue 上传文件，再调用 commit

# ── 提交数据集（上传文件后调用） ──
requests.put(f"{BASE}/commit", headers=HEADERS_JSON,
    json={"datasetId": dataset_id})

# ── 创建新版本 ──
requests.post(f"{BASE}/{dataset_id}/version", headers=HEADERS_JSON,
    json={"versionDesc": "v2 update"})

# ── 修改数据集信息 ──
requests.put(f"{BASE}/{dataset_id}", headers=HEADERS_JSON,
    json={"title": "new-title"})

# ── 删除数据集版本 ──
requests.delete(f"{BASE}/{dataset_id}/version/{version_id}", headers=HEADERS)

# ── 检查配额 ──
r = requests.get(f"{BASE}/quota/check", headers=HEADERS,
    params={"projectId": YOUR_PROJECT_ID})
# 返回: {result: true, limit: 30, used: 5}

# ── 获取上传 Token（用于 tiefblue 上传） ──
r = requests.get(f"{BASE}/input/token", headers=HEADERS,
    params={"projectId": YOUR_PROJECT_ID, "path": "/bohr/my-dataset"})
# 返回: {token, path, host}

# ── 查看数据集权限 ──
r = requests.get(f"{BASE}/{dataset_id}/permission", headers=HEADERS)

# ── 获取关联项目列表 ──
r = requests.get(f"{BASE}/project", headers=HEADERS)
```

**重要**：数据集列表 API 路径是 `GET /v2/ds/`（**带尾部斜杠**），不是 `/v2/ds/list`（`/list` 会被 `/:id` 路由捕获报错）。

---

## 数据集内容说明

| 字段 | 说明 | 示例 |
|------|------|------|
| 数据集名称 | 可随时修改 | `testdataset` |
| 数据集路径 | 唯一标识，系统自动生成版本路径 | `/bohr/testdataset-b2dh/v1` |
| 文件 | 支持上传本地文件或文件夹 | - |
| 项目 | 数据集所属项目，项目成员默认可用 | `testproject` |
| 描述 | 数据集描述信息 | `用于训练的数据` |

## 数据集状态码

| status | 含义 |
|--------|------|
| 1 | 创建中/未提交 |
| 2 | 已提交/可用 |

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 上传中断 | 网络不稳定 | 重新运行同一命令，输入 `y` 续传 |
| 数据集路径找不到 | 挂载路径错误 | 用 `bohr dataset list --json` 查看 `path` 字段 |
| Job 中无法访问数据集 | 未在 job.json 中配置 | 添加 `"dataset_path": ["/bohr/xxx/v1"]` |
| `/ds/list` 返回错误 | 路由被 `/:id` 捕获 | 使用 `GET /ds/`（根路径）获取列表 |
| 创建缺少 identifier 报错 | `identifier` 是必填字段 | 添加 `identifier` 字段（英文+数字） |
| 版本准备中（约5分钟） | 文件正在复制到新版本存储 | 大文件耐心等待，失败联系客服 |
| Notebook 中数据集不可用 | 连接节点后才添加的数据集 | 需重启节点才能生效 |
| （sandbox 建集）读 `/personal` `Permission denied` | `exec` 默认 uid=1000 无权读个人盘 | 所有 `exec` 加 `--user root` |
| （sandbox 建集）`/share` 不存在 | 建 sandbox 没带 `--project-id` | 必须带才挂对应项目共享盘 |
| （sandbox 建集）exec 60s 超时 | 前台默认 60s | 大文件上传必须 `--background` |
| （sandbox 建集）`panic: unsupported protocol scheme ""` | 沙箱内 `TIEFBLUE_HOST` 未设 | `export TIEFBLUE_HOST=https://tiefblue.dp.tech` |
| （sandbox 建集）`lbg: error: invalid choice: 'sdbx'` | 装了稳定版 lbg | `pip install --pre --upgrade lbg` |
| `code:2000` / Unauthorized（**但 key 已设置**） | 网关鉴权偶发抖动，非真失效 | **原样重试 1–2 次**即可；别急着找用户要 key |
| `bohr dataset ...` 报 `AccessKey Invalid!` 或**空 `Error:`（exit 0）** | 只设了 `BOHR_ACCESS_KEY`;bohr CLI 认 `ACCESS_KEY` | `export ACCESS_KEY="$BOHR_ACCESS_KEY"` 再跑(见「认证配置」) |
| `bohr dataset list` 报 `open /dev/tty: no such device or address` | 不带 `--json` 走交互式分页,无终端环境报错 | 一律加 `--json` |
| `dataset_manager.py` 报 `set BOHR_ACCESS_KEY (or ACCESS_KEY)` | 两个变量都没设 | 任一即可;脚本已兼容 `ACCESS_KEY`(BU/TD 的 `.bohr_env` 设的就是它) |
| `files` 只返回一个 `upload/` 目录项 | 旧版脚本不递归 | 已修:`files`/`download` 会递归下钻,直接用返回的 `mount_path` |
| `dataset_manager.py` 输出被 `Extra data` JSON 解析错误 | sdbx.py 的 upgrade 提示行混入(仅 sdbx,不是本脚本) | 见上「sdbx.py 输出的两个坑」,解析前滤掉提示行 |
| 重复上传了已有的大文件 | 靠 dataset `title` 判断有没有传过 → 换个目录/换个人跑名字就对不上,必然漏判 | 建集前一律先跑 `dataset_manager.py find --project-id <pid> --disk-path share/<路径>`;exit 0 = 命中直接用 `mount_path`,exit 4 才新建 |
