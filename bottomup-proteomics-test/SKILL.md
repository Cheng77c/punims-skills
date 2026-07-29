---
name: bottomup-proteomics-test
version: 1.0.1
description: >
  在 Bohrium 算力上跑 bottom-up 蛋白质组学流水线(数据库搜索 / 定量 / DIA,内置已验证工作流模板)。
  用户提供 .raw/.mzML 谱图 + FASTA 库,确认参数后提交 Bohrium job,回收 PSM/肽段/蛋白报告及定量结果。
  Use when: 用户要对 bottom-up 质谱数据做肽段鉴定 / LFQ / TMT 定量 / DIA 分析。
  NOT for: 完整蛋白(intact protein)搜索、纯文献/数据问答。
type: sandbox
requires:
  - bohrium-job
  - bohrium-sandbox
  - bohrium-dataset-manager-test
configFields:
  - name: IMAGE_ADDRESS
    type: text
    description: bottom-up 流水线镜像地址(留空则用 skill 的 image.txt;版本迭代改 image.txt 一处即可,此项仅临时覆盖)
  - name: PROJECT_ID
    type: text
    description: Bohrium 项目 ID(提交 job 所属项目;无默认,必须配置,同 ACCESS_KEY)
  - name: MACHINE_TYPE
    type: text
    description: 计算机型
    default: "c16_m32_cpu"
metadata:
  openclaw:
    primaryEnv: BOHR_ACCESS_KEY
l0: Bottom-up 蛋白质组学流水线(Bohrium)
l1: >
  用户给 .raw/.mzML + FASTA;确认搜索参数/定量/FDR 后,提交 Bohrium job 跑
  数据库搜索/定量/DIA 模板流水线,产 PSM/肽段/蛋白报告及定量矩阵并回收摘要。重计算在 Bohrium,不在 sandbox。
---

# bottomup-proteomics-test

在 **Bohrium 计算节点**上跑 bottom-up 蛋白质组学流水线;sandbox 只做编排(装配、提交、轮询、回收)。

## 镜像与执行(必读,最高优先)

- **只有一个镜像**,地址的**单一源 = skill 根的 `image.txt`**(版本迭代只改这一个文件;脚本都从它读,env `IMAGE_ADDRESS` 可临时覆盖)。
  里面**已烤入全套计算引擎 + 流水线执行器**,覆盖本 skill 声明的全部契约工具
  (`database` / `search-closed` / `validate-psm` / `report` / `quant` / `quant-isobaric` / `dia-search` / …)。
  执行器入口 `/opt/topdown/bu_run.sh`。skill 把用户写的 `pipeline.json` 编译成
  `contract_version: 4` 的 `execution_plan.json`;镜像只按显式 bindings/edges/map_over 执行,
  **不存模板、不选择模板、不推断工作流语义**。
- ❌ **绝不要去 Bohrium 镜像库搜索任何"单工具镜像"**——它们不存在,全部工具都在上面这一个镜像里。
- ❌ **绝不要自己手写 job.json、自己拼 image_address、自己调 bohr image list 找镜像。**
- ✅ **一律通过 `scripts/submit_pipeline.py` 提交**——它自动用配置的 `IMAGE_ADDRESS`、装配 pipeline.json 和上传包。
  你只需提供 raw_files / fasta_path / 参数;镜像与作业配置由脚本处理。
- 重二进制都在镜像里跑(经 Bohrium 作业),**不要在 sandbox 里直接跑搜索/定量/DIA 引擎**。

如果 `IMAGE_ADDRESS`/`PROJECT_ID` 未配置,**不要猜或找替代值**——用 `AskUserInput` 让用户补配置或提示去启用 `bohrium-job` skill。**密钥是例外:绝不向用户索取。** 平台会把表单中的密钥脱敏成 `[REDACTED]`,Agent 拿不到真值,还可能留下覆盖有效注入的陈旧记录。密钥缺失或认证失败属于平台注入问题:如实告知用户并停止本轮。

### 🚫 十条铁律(违反=必错)
0. **开工先加载 `bohrium-dataset-manager-test` skill。** 共享盘/个人盘谱图的查重和建集只用:
   ```bash
   python3 /data/skills/bohrium-dataset-manager-test/dataset_manager.py create-from-disk \
     --project-id <pid> --disk-path share/<盘内路径> --json
   ```
   不要手写 REST、不要根据标题猜是否已有数据集。
1. **绝不手写 job.json / 绝不自己拼 `bohr job submit`** —— 一律 `scripts/submit_pipeline.py`。
2. **绝不直接调底层二进制**——只经 `submit_pipeline.py` 提交。
3. **谱图默认一律走 dataset(不论大小)**:共享盘/个人盘的谱图**直接转 dataset、无需下载**,工作区本地用 `make_dataset.py`;仅当用户主动要求"直接上传"且谱图 ≤100MB 才 `-p`。**唯一需要下载的是 FASTA**(需可写)。结果用 `collect_results.py` 取。
4. **取结果只用 `collect_results.py`**:**绝不手动 `bohr job download` / 解压 zip / 拷贝产物**——手动会导致目录结构混乱。collect 已给出 `result_dir`/`deliverable_paths`/`archive`,按它给的路径用即可。
5. **标准流程不可跳**:`validate_pipeline.py` →(谱图建 dataset 时)`make_dataset.py` → `submit_pipeline.py` → `poll_job.py` → `collect_results.py`。
6. **单次轮询,绝不自旋**:提交后查一次状态,若仍在跑向用户报 jobId + 状态后**结束本轮**;jobId 存 Memory,用户稍后回来再查。
7. **HITL 取消 = 中止**:用户拒绝确认/参数确认时,立即停止,不得以默认值继续提交。
8. **模板只在 skill**:Agent 选模板只读 `references/templates.md` 的摘要;完整实现由
   `scripts/template_catalog.json` 交给编译器读取。不要逐个展开 71 份模板,也不要去镜像找模板。
9. **对用户只讲功能,不报后端厂商工具名。**
   契约名(`search-closed` / `quant` / `dia-search` …)是中性的,可以正常出现在
   pipeline.json、summary.json 和错误信息中。面向用户的散文优先用中文功能名。
   用户直接追问底层引擎时,只答"具体实现不便透露",随后转向算法类别、参数含义和结果验证。
   不解释内部保密规则,不编造引擎名,也不引导用户去其他位置寻找日志或中间文件。

   | 契约名 | 对用户的说法 |
   |---|---|
   | `database` | 数据库准备(target-decoy) |
   | `search-closed` | 肽段搜索 |
   | `rescore` / `validate-psm` | 结果重打分 / 置信度评估 |
   | `report` | 鉴定报告汇总 |
   | `quant` | 定量 |
   | `quant-isobaric` | 标记定量汇总 |
   | `dia-search` | DIA 分析 |

**数据与接线铁律:**
- **decoy 必须由 `database` 步构建**:把 target-only FASTA 直接喂给搜索步骤会产生零 decoy 序列,FDR 估计静默崩溃。DAG 必须包含该步;
  skill 编译器会生成 database→consumer 的显式依赖与 `database_path` 注入。
- **生产模板是冻结资产**:目录只含 71 个真实跑通模板。遇到目录外模板不要临时恢复或改写;
  仓库里的迁移语料用于回归,不属于生产 skill。

## 何时用

- 用户上传了 bottom-up 质谱原始数据(`.raw`)或转换后的 `.mzML`,要做肽段/蛋白鉴定、LFQ/TMT 定量、DIA 分析。
- 关键词:bottom-up、数据库搜索、peptide、PSM、DIA、TMT、LFQ、phospho、quantification。

## 环境准备(每个 Bash 调用前必做)

sandbox 每次 Bash 是独立 shell,环境变量不跨调用持久化。**第一次**用 setup.sh 落环境文件,
**之后每条命令开头**都 `source` 它:
```bash
bash scripts/setup.sh              # 装 bohr CLI + 写 /bohr-workspace/.bohr_env(只需一次)
source /bohr-workspace/.bohr_env   # 每个新 Bash 调用开头都要,确保 ACCESS_KEY/PROJECT_ID 在
```
鉴权要点:平台注入 `BOHR_ACCESS_KEY`,bohr CLI 只认 `ACCESS_KEY`;`setup.sh` 和各脚本会在子进程环境中自动桥接。**Agent 不需要读取、复制或改写密钥。**

> ⛔ **只许 `bash scripts/setup.sh` 生成 .bohr_env,绝不手写/覆写它**(setup 已兜底读 `BOHR_ACCESS_KEY`)。
> - 密钥未注入或探针认证失败:这是平台侧问题,如实告知用户后停止。**绝不向用户索取 key,不手写 curl,不反复换 header 重试。**
> - `PROJECT_ID` 未注入:对话中用户已明确的项目 ID 可直接用(`export PROJECT_ID=<id>`);未知才 `AskUserInput` 索取,**绝不凭空编造默认值**。

## 工作流(严格按序)

### 1. 确认输入文件(先辨识来源)
- 用户上传到工作区:`ListUploadedFiles` 确认。
- 数据在**项目共享盘 / 个人盘**:**谱图**用「共享盘/个人盘转数据集」能力(bohrium-dataset-manager 的「从共享盘/个人盘建数据集」)**直接转成 dataset(无需下载)**,拿到 `/bohr/<名>/v1` 填入 raw_files[];**FASTA 不转 dataset,只下载它**进任务目录走 `-p`(见第 4 步)。
- 已是 **dataset**(自建或网页端上传):`bohr dataset list -p <项目>` 找到,把 `/bohr/<名>/v1/<文件>` 填入 raw_files[];**不知内部文件名/路径时,用 bohrium-dataset-manager 的「列出数据集内文件」(`dataset_manager.py files --id <ID>`)拿确切路径——别猜、也别反问用户**。
- 一条流水线至少需要 `.raw`/`.mzML` 谱图;`search-closed`/`database` 步还需 `.fasta`。
- 缺文件就 `AskUserInput`,**不要假设路径**。

### 2. 确认参数(HITL,必做)
提交前**必须**用 `AskUserInput` 让用户确认(完整字段见 `references/parameters.md`):
分析模式(DDA 闭合搜索 / 开放搜索 / DIA)、FDR、定量方式(LFQ/TMT)、机型(默认 `c16_m32_cpu`)。
- **用户取消 = 中止本次提交**,不得用默认值继续。
- **一条链满足请求即止**:用户要"完整鉴定",跑一条 DDA chain 即可;追加额外链须先征得同意。

### 3. 写 pipeline.json(关键:两种入口形式)

> **📁 工作目录约定(必守):每个任务用独立目录 `/bohr-workspace/bu-runs/<任务名>/`,把 `pipeline.json`
> 写进去**,不要散落在 `/bohr-workspace/` 根。`submit_pipeline.py` 会**就地打包该目录**(自包含、可并发、
> 不互相覆盖);`collect_results.py --out <该目录>/result` 回收到同处。一个任务一个文件夹:
> `/bohr-workspace/bu-runs/itraq-quant/{pipeline.json, job.json, 输入文件, result/}`。
> (`submit` 会拒绝把 `/bohr-workspace` 根当打包目录——否则会上传整个工作空间。)

**形式 A:显式 DAG**(`steps`+`edges`——精确控制每步工具和参数):
```json
{
  "steps": [
    {"step_id": "db",  "tool": "database"},
    {"step_id": "search",  "tool": "search-closed"},
    {"step_id": "validate",  "tool": "validate-psm"},
    {"step_id": "report",  "tool": "report"}
  ],
  "edges": [
    {"src": "search", "dst": "validate"}, {"src": "validate", "dst": "report"}
  ],
  "raw_files": ["EXAMPLE.mzML"],
  "fasta_path": "EXAMPLE.fasta"
}
```

**形式 B:模板入口(⭐ 优先用这个)**(`template_id`——skill 编译 71 个已跑通模板,不需要 steps/edges):
```json
{"template_id": "open", "raw_files": ["EXAMPLE.mzML"], "fasta_path": "EXAMPLE.fasta"}
```
> **有 71 个生产模板,选择摘要见 `references/templates.md`。** 完整步骤/参数/`inputs`/`map_over`
> 在机器目录 `scripts/template_catalog.json` 中,由编译器读取;Agent 无需浏览其实现。
> 常见:`basic-search`(全功能基线)、`open`(开放搜索+PTM分析)、`lfq-mbr`(LFQ定量)、
> `tmt10`/`tmt16`(TMT)、`itraq4`(iTRAQ)、`glyco-n-hcd`(N-糖)、`dia-speclib-quant`(DIA)等。

> **⚠️ 铁律:能用模板就别手写 DAG。** 官方模板的接线已验证正确;手写显式 DAG 极易漏掉
> 语义接线 —— 例如 **`ptm-profile` 需要 mzML**、open 搜索需 `precursor-refine`、`quant` 需谱图+psm.tsv。
> `submit_pipeline.py` 会把模板和必要的 database/artifact 注入编译成显式 v4 plan,镜像不再补猜。
> 想要某条链先在 `references/templates.md` 找对应 template_id;**确无对应才手写**,并对照官方同类模板的 edges 补全接线。

**单工具**:一步 + 零边即可(`"steps":[{"step_id":"x","tool":"dia-search","params":{...}}], "edges":[]`)。

**支持的工具:**
`database` · `search-closed` · `precursor-refine` · `rescore` · `rescore-export` ·
`validate-psm` · `ptm-localize` · `report` · `quant-lfq` · `quant-reporter` · `aggregate-reports` ·
`quant` · `ptm-profile` · `quant-isobaric` · `dia-search` · `dia-pseudo` · `dia-features` ·
`speclib-build` · `glyco-localize` · `predict-rescore` · `psm-integrate` · `protein-infer`

**典型链组合:**

| 场景 | steps | 说明 |
|---|---|---|
| 标准 DDA LFQ | `database → search-closed → validate-psm → report` | `quant` 可加在 report 后做 LFQ 矩阵 |
| DDA + 重打分 | `database → search-closed → precursor-refine → rescore → rescore-export → report` | 用结果重打分替代基础 PSM 验证 |
| TMT 定量 | 上述 DDA 链 + `quant`(perform_isoquant=true)→ `quant-isobaric` | annotation_file 和 channel_num 必填 |
| LFQ | `report → quant-lfq` | `quant-lfq` 更新 PSM/肽/离子定量表 |
| 标记定量 | `report → quant-reporter` | 需 brand/plex/annotation_file |
| 跨实验汇总 | 多个 report/protein-infer/psm-integrate → `aggregate-reports` | 至少需要两个实验输入 |
| DIA | `dia-search`(library_path 或上游 speclib-build) | 现成谱图库可直接填 library_path |
| PTM 定量 | DDA 链 + `ptm-profile` | 修饰位点富集分析 |

### 3.5 提交前本地校验(必做,零成本)
```bash
source /bohr-workspace/.bohr_env
python3 scripts/validate_pipeline.py pipeline.json
# ok:true 才继续;否则按 errors[].{step,tool} 修 pipeline.json 后重验
```

### 4. 准备输入(按来源选通道)

> **默认路由:谱图一律走 dataset(只读挂载),不论大小、不论来自工作区还是共享盘/个人盘。** 共享盘/个人盘的谱图**直接转 dataset,不要先下载到工作区**;**唯一需要下载的是 FASTA**(因需可写,见下)。**只有当用户主动要求"直接上传/不建数据集"、且谱图 ≤100MB 时,才走 `-p`。**

| 数据在哪 | 怎么进作业 | 作业内可写 |
|---|---|---|
| **谱图(`.raw`/`.mzML`,任意大小)——默认建 dataset** | 工作区本地:`make_dataset.py`;共享盘/个人盘:「转数据集」能力(bohrium-dataset-manager,**直接转、无需下载**)。拿 `/bohr/<名>/v1/<文件>` 填 raw_files[] | ❌ 只读 |
| **FASTA / 参数 / 需可写的小文件** | `-p` 上传目录(submit 自动打包)。共享盘/个人盘上的 fasta **只下载它**进任务目录再 -p | ✅ 可写 |
| **已有 / 网页端上传的 dataset** | `bohr dataset list` 找到,引用 `/bohr/<名>/v1`(不知文件名用「列出数据集内文件」) | ❌ 只读 |
| 谱图,但用户**主动要求"直接上传"** | `-p`(校验器硬拦 >100MB;仅此情形才用 -p 传谱图) | ✅ 可写 |

`submit_pipeline.py` 自动暂存本地路径并生成 `execution_plan.json`;`/bohr/…` 路径作为 dataset 挂载引用,原样保留。

> **FASTA 必须走 `-p`,不可放 dataset。** 搜索步骤会于 **FASTA 同目录**写入索引(.idx);dataset 为只读挂载,建索引将失败。FASTA 体积小,放入 `-p` 即可;`make_dataset.py` 也会拒绝 FASTA 文件。
>
> **共享盘/个人盘上的 fasta:只下载这一个文件**进任务目录再走 `-p`(**别做成 dataset**)。
> **一律用 `fetch_file.py`,不要手写 curl**:
> ```bash
> source /bohr-workspace/.bohr_env
> # 共享盘以 share/ 开头,个人盘以 personal/ 开头;路径原样传入。
> python3 scripts/fetch_file.py \
>   --remote share/<完整路径>/xxx.fasta \
>   --out /bohr-workspace/bu-runs/<任务>/xxx.fasta
> ```
> `fetch_file.py` 负责路径校验、用户 ID 解析和认证头,且不让密钥进入命令文本。

仅**谱图**需要建 dataset:
```bash
source /bohr-workspace/.bohr_env
python3 scripts/make_dataset.py --file <谱图路径.raw> --name <数据集名>   # 仅谱图;FASTA 勿用
# 返回真实挂载路径(含随机后缀与 upload 层);填入 pipeline.json 的 raw_files[]
# submit 时附带 --dataset-path /bohr/<名>-<后缀>/v1
```

### 5. 提交 job
```bash
source /bohr-workspace/.bohr_env
python3 scripts/submit_pipeline.py --pipeline /bohr-workspace/bu-runs/<任务名>/pipeline.json [--dataset-path /bohr/<name>/v1]
# pipeline.json 在任务目录里(见上方📁约定);submit 就地打包该目录。返回 {jobId, status, pollAfterMs}
```

### 6. 轮询作业状态(**单次查询,不得循环阻塞**)
作业在 Bohrium 独立运行,完整 DDA 链通常 20–60 分钟。**提交后查询一次即可。**
```bash
source /bohr-workspace/.bohr_env
python3 scripts/poll_job.py --job-id <JobId>   # 返回 status / done
```
- `done:true`(`completed`)→ 进入第 7 步 `collect_results.py`。
- 仍 `scheduling` / `running` → **向用户报告 jobId + 当前状态,然后结束本轮**;由用户稍后回来再查。**不要自旋等待。**

作业与 sandbox 解耦:会话中断、sandbox 重建均不影响作业运行;jobId 记入 Memory,恢复后凭它继续轮询/回收。

### 7. 回收 + 汇报
```bash
source /bohr-workspace/.bohr_env
python3 scripts/collect_results.py --job-id <JobId> --out /bohr-workspace/bu-runs/<任务名>/result
# 回收到任务目录 <任务名>/result/out/(--out 省略则默认 /bohr-workspace/bu-result/<JobId>/out/),
# 返回 status + metrics(PSM/肽段/蛋白计数)+ 交付物本地路径 + 版本告警
```
- 返回的 `result_dir` 含 `out/`(所有步骤产物,含 summary.json)+ `<JobId>.zip`(完整包供用户下载)。
- 返回的 `version_warning` 非空时,应转告用户(镜像需更新)。

然后:`RecordArtifact` 标记 `summary.json` 与关键报告;Chat 只回摘要(PSM/蛋白数、FDR),
不贴大表;`MemorySave` 记 `memories/projects/bottomup/runs/<run>.md`(jobId/参数/结果位置)。

## 提示与排错

### 🚫 失败排查铁律(防臆断/幻觉)
1. **先定位真实原因,不得臆测**:运行 `collect_results.py`,读取返回的 `error` / `failed_log_tail` / `missing_inputs`——工具的真实报错即在其中。未读到真实报错前,不得编造原因。
2. **失败几乎都源于数据/配置,而非"管线不支持"**:常见真因为 `database` 步漏掉(零 decoy FDR 崩)、dataset 路径漏 `upload/` 层、FASTA 置于只读 dataset、TMT 模板缺 `annotation_file`/`isotype`。
3. **绝不下"X 不支持 / 架构限制"结论**:skill 支持单工具、任意起点、显式 DAG、模板入口;
   镜像执行 v4 plan。怀疑不支持时,先查看真实报错并核对 `references/`,不得凭印象断言。
4. **绝不绕过执行器**手写 wrapper 直调工具二进制——违反铁律,且丢失自动接线、输入校验,降低健壮性。
5. **模板目录外即不发布**:不要在任务中从镜像恢复模板。生产集合固定为已验证的 71 个;
   新模板需回仓库完成迁移、回归和资产再生成。

**判断要点:**
- **dataset 阈值(已硬拦)**:本地输入 > 100MB 时 `validate_pipeline.py` 直接报错并要求改走 make_dataset。(注:≤100MB 的谱图**默认也走 dataset**,见 §4 默认路由;-p 传谱图仅限用户主动要求。)
- **database 必须存在**:没有 target+decoy .fas,搜索步骤无法估 FDR;其排序与注入由 v4 plan 显式表达。
- **运行时长**:c16_m32 上 DDA LFQ 链典型 20–60 分钟(数据量决定);DIA 单样本 5–20 分钟。

**submit_pipeline.py 成功返回示例:**
```json
{"ok": true, "jobId": "22907069", "status": "scheduling", "pollAfterMs": 20000, "nextTool": "poll_job.py"}
```

**常见错误:**
| 现象 | 原因 / 处理 |
|---|---|
| `AccessKey Invalid` / `AccessKey is required` / `code:2000` | **终局错误,不要重试。** 先运行 `bash scripts/setup.sh`;若探针仍失败,说明平台密钥注入缺失或已失效。如实告知用户后停止,**绝不向用户索取 key**,不手写 curl,不尝试 `bohr auth login`。 |
| job `status=-1`(失败) | `collect_results.py` 直接返回 `failed_step` + `error` + `failed_log_tail`;依据真实报错修正 |
| `no files found matching X` | 输入路径问题;确认文件真存在,或 dataset 路径带 `upload/` 层 |
| 零 PSM / FDR 崩溃 | `database` 步漏掉,搜索步骤直接拿 target-only FASTA 导致零 decoy |
| `Dataset ... has been deleted` | Bohrium 给数据集名加随机后缀;**make_dataset.py 已自动从 API 返回真实路径**,用它给的 `spectrum_mount` 即可 |
| TMT 模板无定量结果 | 检查 `quant` 的 `isotype`/`annotation_file`、`quant-isobaric` 的 `channel_num`;对照模板源文件补齐缺失字段 |
| `Cannot read file .meta/db.bin` | `report` 步的 workspace 未准备;确认流水线包含 `database` 步 |

## HARD STOP(成本确认)
机型为大核数(如 `c32_*`)或预计长时运行,提交前**必须** `AskUserInput` 用 checkbox 让用户确认费用。不静默提交高成本 job。

## 边界
- 不在 sandbox 里跑搜索/定量/DIA 引擎(它们在 Bohrium 镜像里,经作业跑)。
- GB 级谱图不经 `-p` 上传(经 dataset 挂载),也不读入对话上下文。
- 不臆造文件路径或参数;不确定就 `AskUserInput`。
- **禁止 `cat` 执行器日志 / 大 TSV**:指标取 `collect_results.py` 的 `metrics`;需细节时 `head -40` 读 TSV 顶部。
- 不在 Bohrium 镜像库查找单工具镜像;一律使用配置的 `IMAGE_ADDRESS`(默认取自 `image.txt`)。
- `BOHR_ACCESS_KEY` 由平台注入,不写进 prompt/日志/文件,也不向用户索取。

## 配置(由平台注入)
`BOHR_ACCESS_KEY`(`primaryEnv`)与 `PROJECT_ID` 为必需配置;脚本会把密钥桥接为 bohr CLI 所需的 `ACCESS_KEY`。`IMAGE_ADDRESS` 可选,默认使用 skill 的 `image.txt`。密钥配置异常只能由平台侧修复,Agent 不向用户收集密钥。
