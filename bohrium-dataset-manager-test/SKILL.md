---
name: bohrium-dataset-manager-test
description: "Manage and inspect Bohrium datasets via bohr CLI or open.bohrium.com API. Use when: creating/listing/deleting datasets, uploading data, managing versions, checking whether a file was ALREADY uploaded before re-uploading it (dedup, `find`), OR listing the files INSIDE a dataset to resolve the exact in-job mount path (/bohr/<name>/v1/<file>) instead of guessing filenames. NOT for: share/personal disk file management (use bohrium-file), job submission, or node management."
requires:
  - bohrium-sandbox   # create-from-disk 靠它的 sdbx.py 把盘上文件直转 dataset;
                       # 不加载 = sdbx.py 不存在 = 建集必失败(且会伪装成「网关故障」)
---

# SKILL: Bohrium 数据集 (Dataset) 管理与查看

## 概述

**Bohrium 数据集操作 skill。** 本测试版只负责数据集,文件盘通用管理不在范围内:

- **数据集(dataset)**:**查重(`find`,建集前必跑)** / 创建(本地 / **从共享盘·个人盘直接建,免下载** / API)/ 列出 / 看内部文件拿确切挂载路径 / 版本 / 删除 / 在任务中挂载。
- **把数据喂进计算任务**:见下方「数据进任务:路由决策」——不同来源(工作区 / 文件盘 / 数据集)+ 不同用途(只读挂载 / 需可写)对应不同操作,别猜、别反问用户。

> ⛔ **Agent 环境中的安全铁律:**数据集查重、列举、建集和下载只运行本 skill 的
> `dataset_manager.py`;**不要手写 curl,不要把 key 放进命令文本、中转变量、文件或回显,
> 也不要向用户索取 key。** BU/TD 任务需要从共享盘取 FASTA 时,使用对应专业 skill 的
> `scripts/fetch_file.py`,不由本 skill 拼下载 URL。

数据集解决的场景:每次提交都要等打包上传 → 挂载数据集免重复上传;大文件上传慢 → 无大小限制 + 断点续传;与他人共享 → 项目内共享。

## 数据进任务:路由决策(先看这个)

把数据喂进计算任务前,先按「**数据在哪 × 要干嘛**」定位操作。核心原则:**谱图等只读大输入 → 数据集挂载(不下载);需可写的小文件(尤其 FASTA)→ 下载到本地随包上传。**

| 数据在哪 | 用途 | 怎么做 |
|---|---|---|
| 文件盘(share/personal)的**谱图** | 任务只读输入 | 一条命令:`dataset_manager.py create-from-disk --project-id <pid> --disk-path share/<路径>`(内含查重,已存在则零传输)→ 用它返回的 `mount_path`。**绝不下载到本地** |
| 文件盘(share/personal)的 **FASTA / 需可写小文件** | 搜索引擎要在同目录建索引(可写) | 调用 BU/TD 专业 skill 的 `scripts/fetch_file.py` 下载到任务目录→随包上传 `-p`;**不要手写 curl,不要做成只读数据集** |
| **已有数据集**,但不知里面文件名 | 要引用具体文件 | `dataset_manager.py files --id <ID>` 拿确切 `/bohr/<名>/v1/<文件>`——**别猜、别问用户** |
| 已有数据集,要在任务里用 | 只读输入 | 直接挂载 `dataset_path`,**不要下载**;真要本地副本才用 `downloadUri`(整包 zip) |
| 工作区本地小文件 | 随包 | 直接 `-p` 上传 |

> 判定为某专业流程(如蛋白质组学)时,以该流程 skill 的路由表为准;本表是通用底座。

## 认证与环境

平台负责注入 `BOHR_ACCESS_KEY`;`dataset_manager.py` 只从进程环境读取并在内部构造认证请求。
Agent 不读取、不复制、不落盘密钥。认证缺失或失败属于平台侧问题:如实告知用户后停止本轮,
**绝不向用户索取 key,不改 header,不手写 curl 重试。**

BU/TD 会先运行自己的 `scripts/setup.sh`;不要在本 skill 里重复安装 CLI 或手写认证配置。

---

## 列出数据集

```bash
# ★ 列数据集用本脚本的 list 子命令,不要用 bohr CLI —— key 从环境读,不进命令文本。
python3 dataset_manager.py list --project-id YOUR_PROJECT_ID --json          # 按项目
python3 dataset_manager.py list --project-id YOUR_PROJECT_ID --title my-set   # 按标题过滤
```
> ⛔ **不要手写 `bohr dataset list` 或 `curl .../v2/ds`**:`bohr dataset list` 在**未认证时**输出 `json: cannot unmarshal object into Go struct field RespErr.error` —— 实测用「完全不给 key」做对照组输出逐字相同,**这是鉴权失败的表现,不是 CLI 的 JSON bug**。`list` 子命令走 `api()`,key 只在进程内,且能把 401 报成人话。
> ⛔ **绝不靠列数据集反查 project_id** —— project_id 只来自用户 / 平台注入,不能从"数据集属于哪个项目"倒推。

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

`dataset_manager.py list --project-id <pid>` 只给数据集**本身**（id/title/挂载根 `/bohr/<名>/v1`），**不给内部文件名**。要在任务里引用某个具体文件（如 `raw_files`/`inputs`），必须知道数据集**内部的确切文件名**——**用这个能力查,绝不猜文件名、也绝不反问用户**：

**先按名字拿到数字 ID**(用户通常只给数据集**名**,而 `files`/`download`/`detail` 都要数字 `--id`):
```bash
python3 dataset_manager.py list --project-id <项目ID> --title "<数据集名>" --json
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
python /data/skills/bohrium-dataset-manager-test/dataset_manager.py create-from-disk \
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

## 文件盘输入与安全下载

本 skill 不做 personal/share 文件盘的通用列举、上传、移动或删除。专业分析只需要两条安全路线:

- 谱图:运行 `dataset_manager.py create-from-disk`，服务端直转 dataset，绝不下载到工作区。
- 共享盘/个人盘 FASTA:运行当前 BU/TD skill 的 `scripts/fetch_file.py`。该包装器在进程内完成
  身份解析和下载，**不要手写 curl、下载 URL或认证头**。

若 FASTA 已经误放在数据集里，需要可写副本时可使用本脚本:

```bash
python dataset_manager.py files    --id <ID>                       # 先看内部文件名
python dataset_manager.py download --id <ID> --file xxx.fasta --out ./xxx.fasta
```
（内部走 version→token→`tiefblue.dp.tech/api/download/<obj>`，自动跟随到预签名 OSS URL。）

> 记住路由：**谱图不下载;FASTA 只经包装脚本下载;认证操作不手写。**

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
| 数据集路径找不到 | 挂载路径错误 | 用 `dataset_manager.py list --project-id <pid> --json` 查看 `path` 字段（不要手写 bohr dataset list / curl）|
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
| `code:2000` / Unauthorized（**但 key 已设置**） | **终局错误**（响应带 `retryable:false`）。头号真因:**平台注入的密钥已失效** —— 有值、32 位、格式正常但认证不过（2026-07-27 线上事故）。次因才是把 key 的**明文值**写进了命令被脱敏；注意脱敏是**概率性**的，日志里没有 `[REDACTED]` **不能**证明没发生 | 认证操作走脚本（`list`/`files`/`create-from-disk`/`fetch_file.py`）；⛔ **绝不找用户要 key** —— 表单值会被脱敏成 `[REDACTED]`，且会在平台凭据库留下一条日后覆盖有效密钥的陈旧记录；**这是平台侧的密钥注入问题,不在本 skill 的处理范围** —— 如实告知用户「当前平台注入的密钥已失效」后结束本轮，不要替平台猜处置步骤 |
| `bohr dataset ...` 报 `AccessKey Invalid!` 或**空 `Error:`（exit 0）** | 只设了 `BOHR_ACCESS_KEY`;bohr CLI 认 `ACCESS_KEY` | 跑 `bash scripts/setup.sh` 后 `source /bohr-workspace/.bohr_env`（会把 ACCESS_KEY 从平台 BOHR_ACCESS_KEY 派生好，无需手动桥接）|
| `bohr dataset list` 报 `open /dev/tty: no such device or address` | 不带 `--json` 走交互式分页,无终端环境报错 | 一律加 `--json` |
| `dataset_manager.py` 报 `set BOHR_ACCESS_KEY (or ACCESS_KEY)` | 两个变量都没设 | 任一即可;脚本已兼容 `ACCESS_KEY`(BU/TD 的 `.bohr_env` 设的就是它) |
| `files` 只返回一个 `upload/` 目录项 | 旧版脚本不递归 | 已修:`files`/`download` 会递归下钻,直接用返回的 `mount_path` |
| `dataset_manager.py` 输出被 `Extra data` JSON 解析错误 | sdbx.py 的 upgrade 提示行混入(仅 sdbx,不是本脚本) | 见上「sdbx.py 输出的两个坑」,解析前滤掉提示行 |
| 重复上传了已有的大文件 | 靠 dataset `title` 判断有没有传过 → 换个目录/换个人跑名字就对不上,必然漏判 | 建集前一律先跑 `dataset_manager.py find --project-id <pid> --disk-path share/<路径>`;exit 0 = 命中直接用 `mount_path`,exit 4 才新建 |
