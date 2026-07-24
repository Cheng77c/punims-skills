---
name: bottomup-proteomics
version: 1.0.0
description: >
  在 Bohrium 算力上跑 bottom-up 蛋白质组学流水线(数据库搜索 / 定量 / DIA,内置行业标准工作流模板)。
  用户提供 .raw/.mzML 谱图 + FASTA 库,确认参数后提交 Bohrium job,回收 PSM/肽段/蛋白报告及定量结果。
  Use when: 用户要对 bottom-up 质谱数据做肽段鉴定 / LFQ / TMT 定量 / DIA 分析。
  NOT for: 完整蛋白(intact protein)搜索、纯文献/数据问答。
type: sandbox
requires:
  - bohrium-job
  - bohrium-sandbox          # 盘→dataset 直转靠它的 sdbx.py;不加载 = 建集必失败
  - bohrium-dataset-manager   # 谱图查重/建集全靠它;不加载 = dataset_manager.py 不存在,
                              # agent 只能手搓 REST 去猜数据集(已翻过车:重传 849MB)
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
    primaryEnv: ACCESS_KEY
l0: Bottom-up 蛋白质组学流水线(Bohrium)
l1: >
  用户给 .raw/.mzML + FASTA;确认搜索参数/定量/FDR 后,提交 Bohrium job 跑
  数据库搜索/定量/DIA 模板流水线,产 PSM/肽段/蛋白报告及定量矩阵并回收摘要。重计算在 Bohrium,不在 sandbox。
---

# bottomup-proteomics

在 **Bohrium 计算节点**上跑 bottom-up 蛋白质组学流水线;sandbox 只做编排(装配、提交、轮询、回收)。

## 镜像与执行(必读,最高优先)

- **只有一个镜像**,地址的**单一源 = skill 根的 `image.txt`**(版本迭代只改这一个文件;脚本都从它读,env `IMAGE_ADDRESS` 可临时覆盖)。
  里面**已烤入全套计算引擎 + 流水线执行器**:覆盖本 skill 声明的全部契约工具
  (`database` / `search-closed` / `validate-psm` / `report` / `quant` / `quant-isobaric` / `dia-search` / … 见下方「支持的工具」)。
  执行器入口 `/opt/topdown/bu_run.sh`(读 pipeline.json 跑链路、接线、校验)。skill 只产 pipeline.json + 取结果,不带执行器代码。
- ❌ **绝不要去 Bohrium 镜像库搜索任何"单工具镜像"**——它们不存在,全部工具都在上面这一个镜像里。
- ❌ **绝不要自己手写 job.json、自己拼 image_address、自己调 bohr image list 找镜像。**
- ✅ **一律通过 `scripts/submit_pipeline.py` 提交**——它自动用配置的 `IMAGE_ADDRESS`、装配 pipeline.json 和上传包。
  你只需提供 raw_files / fasta_path / 参数;镜像与作业配置由脚本处理。
- 重二进制都在镜像里跑(经 Bohrium 作业),**不要在 sandbox 里直接跑搜索/定量/DIA 引擎**。

如果 `IMAGE_ADDRESS`/`PROJECT_ID`/`ACCESS_KEY` 未配置,**不要猜或找替代镜像**——用 `AskUserInput` 让用户补配置或提示去启用 `bohrium-job` skill。

### 🚫 十条铁律(违反=必错)

0. **开工第一件事:加载 `bohrium-dataset-manager` skill。** 谱图的查重与建集全靠它的
   `dataset_manager.py`;不加载,`/data/skills/bohrium-dataset-manager/` 根本不存在,
   你会退回去手搓 REST 猜数据集 —— **已经翻过车:靠 dataset 标题判断"没传过",
   把一份早已在平台上的 849MB 谱图又传了一遍,还卡死在 sandbox 上。**
   查重/建集**只用**这一条命令,别自己拼:
   ```bash
   python3 /data/skills/bohrium-dataset-manager/dataset_manager.py create-from-disk \
     --project-id <pid> --disk-path share/<盘内路径> --json
   ```
   (内含查重:已存在就零传输直接返回 `mount_path`;未命中才自动建集。)
1. **写 pipeline.json 之前,先翻模板目录。** 有 81 个内置官方工作流模板,**能套模板就绝不手写 DAG**:
   ```bash
   R=/data/skills/bottomup-proteomics/references/templates.md
   grep -n '^### `' $R                                  # 列出全部 template_id
   grep -n -A2 -i 'lfq\|tmt\|itraq\|dia\|glyco' $R   # 按需求筛
   ```
   命中就一行调用:`{"template_id":"lfq-mbr","raw_files":[...],"fasta_path":"..."}`(要调参走 `overrides`)。
   **确无对应模板才手写 steps/edges,且必须在回复里说明「查过模板目录、无对应项」。**
   **已经翻过车:用户要「无标记定量 + 高丰度榜单」,agent 没翻目录,手攒了
   `database → search-closed → validate-psm → report` —— 等于把 `lfq-mbr` 重造一遍,
   还漏掉 `quant`,结果根本没有 LFQ 强度,「丰度榜单」无从谈起。**
2. **绝不手写 job.json / 绝不自己拼 `bohr job submit`** —— 一律 `scripts/submit_pipeline.py`。
3. **绝不直接调底层二进制** —— 只经 `submit_pipeline.py` 提交。
4. **谱图默认一律走 dataset(不论大小)**:共享盘/个人盘的谱图**直接转 dataset、无需下载**,工作区本地用 `make_dataset.py`;仅当用户**主动要求**"直接上传"且谱图 ≤100MB 才 `-p`。**建集失败不是启用 `-p` 的理由**——已经翻过车:sandbox 建集报错后,agent 自行把 92MB 谱图下载到工作区再建集,而报错里白纸黑字写着"不要下载到工作区绕过"。建集失败就停下报错,别自己找替代路线。**唯一需要下载的是 FASTA**(需可写)。结果用 `collect_results.py` 取。
5. **取结果只用 `collect_results.py`**:**绝不手动 `bohr job download` / 解压 zip / 拷贝产物**——手动会搞出 `dl/`、`out/out/` 之类的错乱目录,后续 collect 全部失灵。collect 已给出 `deliverable_paths` / `result_dir` / `archive`,按它给的路径用即可。
   (`out/` 由执行器直接产成**交付树**:只有结果表 + 摘要 + DAG 图,引擎中间格式与日志根本不写进去,所以这三个字段都能直接给用户。)
6. **标准流程不可跳**:`validate_pipeline.py` →(谱图建 dataset 时)`make_dataset.py` → `submit_pipeline.py` → `poll_job.py` → `collect_results.py`。
7. **单次轮询,绝不自旋**:提交后查一次状态,若仍在跑向用户报 jobId + 状态后**结束本轮**;jobId 存 Memory,用户稍后回来再查。
8. **HITL 取消 = 中止**:用户拒绝确认/参数确认时,立即停止,不得以默认值继续提交。
9. **对用户只讲功能,不报后端厂商工具名。**
   **契约名(`search-closed` / `quant` / `dia-search` …)本身是中性的**,pipeline.json、
   summary.json、日志名里出现的都是它们,**照常写、照常展示,不必遮遮掩掩**。
   要守的是:
   - 面向用户的**散文**里用中文功能名(下表),别甩英文契约名当术语——这是产品口径,不是保密。
   - **绝不报出后端厂商工具名/品牌名**(第三方搜索引擎、定量引擎的商品名)。用户直接问用什么引擎 →
     一句"具体实现不便透露",然后**立刻转向能讲的**(算法类别、参数含义、结果如何验证)。
   - **只说结论,不解释理由。** 不要说"属于不对外披露范畴""按我的工作规范""涉及工具名/内部路径"
     这类**元信息**——**说"我不能告诉你工具名",本身就是在告诉他有工具名可藏。**
   - **被索要日志/参数/中间文件 → 直接拒绝,不解释。**「我交付的是分析结果,运行中的中间文件
     不对外提供。你要排查什么现象?我帮你核参数、查状态、看数据完整性。」
   - **绝不指引用户去别处拿**(平台控制台、作业目录、运维通道、容器日志一律不提,
     也不暗示"那边不受我限制")。被拒绝后转头教用户绕过你,等于亲手拆自己的防线。
   - **绝不描述你没亲自确认存在的文件或位置。**声称"某处有完整日志"而实际没有 = 编造。
     (**已经翻过车**:agent 拒绝给日志后,主动让用户去平台看"完整的 stdout/参数文件"
     ——实测那里 0 个日志、0 个参数文件,纯属编造。)
   - **绝不编造引擎名、绝不谎称自研**——结果表里有真实的打分列,一编造就穿帮。
     这是"不主动提",不是"撒谎"。

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
- **decoy 必须由 `database` 步构建**:把 target-only FASTA 直接喂给搜索步会产生零 decoy 序列,FDR 估计静默崩溃。pipeline.json 的 steps 里必须有 `database`,其输出(target+decoy .fas)会**自动注入** `search-closed` 的 `database_path` 参数并自动排序在其后——**不要画 db→search-closed 边**(见形式 A 的警告)。
- **官方模板缺配置时,根因在模板迁移,不是执行器问题**:TMT/glyco 模板跑不通的常见根因是模板迁移脚本丢掉了配置字段(TMT `quant` 步的 `isotype`/`annotation_file`、glyco 的 `mass_offsets`/`labile_search_mode`),应对照镜像内置的官方模板源文件恢复。

## 何时用

- 用户上传了 bottom-up 质谱原始数据(`.raw`)或转换后的 `.mzML`,要做肽段/蛋白鉴定、LFQ/TMT 定量、DIA 分析。
- 关键词:bottom-up、数据库搜索、peptide、PSM、DIA、TMT、iTRAQ、LFQ、phospho、quantification。

## 环境准备(每个 Bash 调用前必做)

sandbox 每次 Bash 是独立 shell,环境变量不跨调用持久化。**第一次**用 setup.sh 落环境文件,
**之后每条命令开头**都 `source` 它:
```bash
bash scripts/setup.sh              # 装 bohr CLI + 写 /bohr-workspace/.bohr_env(只需一次)
source /bohr-workspace/.bohr_env   # 每个新 Bash 调用开头都要,确保 ACCESS_KEY/PROJECT_ID 在
```
鉴权要点:平台注入的是环境变量 `BOHR_ACCESS_KEY`;`bohr` CLI 只认 `ACCESS_KEY` 这个名字(实测),故 setup.sh 会把值同时落成两份。**脚本已从环境读 key,你不必碰 key。**
> ⛔ **key 的明文值绝不能进入命令文本/中转变量/写文件/echo** —— 平台会脱敏成 `[REDACTED]`,破坏命令或发出假值。需要认证的操作一律走脚本(`fetch_file.py` / `make_dataset.py` / `submit_pipeline.py` / `poll_job.py`);它们内部从 `os.environ` 读 key。REST 认证头 `accessKey:` 与 `Authorization: Bearer` **两种都可用**(实测),但你不该手写它们。

> ⛔ **`bohr: command not found` = 你还没跑 setup.sh,不是"CLI 需要你自己想办法装"。**
>   唯一修法是 `bash scripts/setup.sh`(幂等,装的是官方 bohr CLI)。
>   **绝不 `pip install lbg`、绝不给它建 `bohr` 符号链接、绝不手写 CLI 的认证配置文件、绝不改用别的 CLI。**
>   (已经翻过车:agent 见 `bohr` 不在就自行 `pip install lbg` + `ln -s` + 手写 `~/.config/lbg/config.yaml`,
>   一整轮步数全耗在给一个根本不该用的 CLI 做认证上,作业一次都没提交出去。)
> ⛔ **只许 `bash scripts/setup.sh` 生成 .bohr_env,绝不手写/覆写它**(setup 已兜底读 `BOHR_ACCESS_KEY`)。
> - `ACCESS_KEY` 未注入:先完成授权 + 重载 skill,再 `setup.sh`。
> - `PROJECT_ID` 未注入:**唯一合法来源 = 本轮对话里用户亲口说的项目 ID**(`export PROJECT_ID=<id>`);没说就 `AskUserInput` 索取。
>   **绝不从记忆文件 / 历史作业记录 / 过往 thread 里翻出一个项目 ID 来用,也绝不凭空编默认值。**
>   (已经翻过车:从旧记忆 `job-xxxxx.md` 里刨出上一个项目的 ID,差点把作业投到别人的项目里。
>   记忆里的项目 ID 只能用来*提问*——「上次用的是 24980,这次还是它吗?」——不能直接当参数填。)

## 工作流(严格按序)

### 1. 确认输入文件(先辨识来源)
- 用户上传到工作区:`ListUploadedFiles` 确认。
- 数据在**项目共享盘 / 个人盘**:**谱图**一律用 `dataset_manager.py create-from-disk --project-id <pid> --disk-path share/<路径> --json` —— 它**内部先查重**(已传过就零传输直接返回),未命中才自动建集;沙箱、CLI 安装、后台上传、真实挂载路径全部封装好,**不要自己拼这套流程**。拿到 `/bohr/<名>/v1/<文件>` 填入 raw_files[]。**绝不许靠 dataset 标题判断有没有传过**(换个目录/换个人跑名字就对不上,必然重传几百 MB)。**FASTA 不转 dataset,只下载它**进任务目录走 `-p`(见第 4 步)。
- 已是 **dataset**(自建或网页端上传):
  - **用户已给出完整 `/bohr/<名>/v1/<文件>` 挂载路径 → 直接填进 raw_files[],不要再去列/查数据集**(最常见,也最省事)。
  - 需要按项目列数据集时,**一律用 `dataset_manager.py list --project-id <pid>`**(可加 `--title <关键词>` 过滤),**绝不 `bohr dataset list` 也绝不手写 curl 查 `/v2/ds`** —— 那个 CLI 有 JSON 解析 bug,你一旦改用 curl 就会把 access key 内联进命令、被平台脱敏成 `[REDACTED]`、制造假的认证失败。
  - 不知内部文件名/路径时,用 `dataset_manager.py files --id <ID>` 拿确切 `/bohr/...` 路径——别猜、也别反问用户。
  - ⛔ **绝不靠"列数据集看它属于哪个项目"来反查 project_id** —— project_id 只能来自用户亲口说的 / 平台注入的;从数据集列表倒推可能把作业投进别人的项目。
- 一条流水线至少需要 `.raw`/`.mzML` 谱图;`search-closed`/`database` 步还需 `.fasta`。
- 缺文件就 `AskUserInput`,**不要假设路径**。

### 2. 确认参数(HITL,必做)
提交前**必须**用 `AskUserInput` 让用户确认(完整字段见 `references/parameters.md`):
分析模式(DDA 闭合搜索 / 开放搜索 / DIA)、FDR、定量方式(LFQ/TMT/iTRAQ)、机型(默认 `c16_m32_cpu`)。
**用功能名向用户提问,不要报后端工具名/品牌名**(见铁律 9)。
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
    {"step_id": "mf",  "tool": "search-closed"},
    {"step_id": "pp",  "tool": "validate-psm"},
    {"step_id": "rp",  "tool": "report"}
  ],
  "edges": [
    {"src": "mf", "dst": "pp"}, {"src": "pp", "dst": "rp"}
  ],
  "raw_files": ["EXAMPLE.mzML"],
  "fasta_path": "EXAMPLE.fasta"
}
```
> **⚠️ 千万别画 `database → search-closed` 边。** 谱图(raw_files)只送达
> **无入边的根节点**;`search-closed` 必须是谱图根节点才能拿到 mzML。decoy 库由 `database`
> 步经 `database_path` 参数**自动注入**、并自动排在其后,**无需也不能**用边连过去——画了这条边会让
> search-closed 变成非根,转而把 db 产出的 `.fas` 当谱图输入,运行时报 `input must be mzML/mzXML`。
> (`db` 步照写在 steps 里即可,不用连边;validate 会拦下 db→search-closed 这个错。)

**形式 B:模板入口(⭐ 优先用这个)**(`template_id`——执行器展开 81 个内置官方模板,不需要 steps/edges):
```json
{"template_id": "open", "raw_files": ["EXAMPLE.mzML"], "fasta_path": "EXAMPLE.fasta"}
```
> **有 81 个官方模板,完整目录见 `references/templates.md`(template_id + 链 + 说明 + 可复制的 steps/edges)。**
> 常见:`basic-search`(全功能基线)、`open`(开放搜索+ptm-profile)、`lfq-mbr`(LFQ定量)、
> `tmt10`/`tmt16`(TMT)、`itraq4`(iTRAQ)、`glyco-n-hcd`(N-糖)、`dia-speclib-quant`(DIA)等。

> **⚠️ 铁律:能用模板就别手写 DAG。** 官方模板的接线已验证正确;手写显式 DAG 极易漏掉
> 隐性接线 —— 例如 **ptm-profile 需要 mzML(要 msconvert→ptm-profile 边)**、open 搜索需 precursor-refine、
> quant 需谱图+psm.tsv 双父边。漏了 validate 也不一定拦(它查参数不查接线完整性),只在运行时崩。
> 想要某条链先在 `references/templates.md` 找对应 template_id;**确无对应才手写**,并对照官方同类模板的 edges 补全接线。

**单工具**:一步 + 零边即可(`"steps":[{"step_id":"x","tool":"dia-search","params":{...}}], "edges":[]`)。

**支持的工具:**
`database` · `search-closed` · `precursor-refine` · `rescore` · `rescore-export` ·
`validate-psm` · `ptm-localize` · `report` · `quant` · `ptm-profile` ·
`quant-isobaric` · `dia-search` · `dia-pseudo` · `dia-features` · `speclib-build` · `glyco-localize` · `predict-rescore` · `psm-integrate` · `protein-infer`

**典型链组合:**

| 场景 | steps | 说明 |
|---|---|---|
| 标准 DDA LFQ | `database → search-closed → validate-psm → report` | quant 可加在 report 后做 LFQ 矩阵 |
| DDA + 机器学习重打分 | `database → search-closed → precursor-refine → rescore → rescore-export → report` | 用 `rescore` 替代 `validate-psm` 做 PSM 验证 |
| TMT 定量 | 上述 DDA 链 + `quant`(perform_isoquant=true)→ `quant-isobaric` | annotation_file 和 channel_num 必填 |
| iTRAQ 定量 | **优先用模板 `itraq4` / `itraq4-phospho`** | `channel_num`=4(iTRAQ-4)或 8(iTRAQ-8)、`quant.isotype`=`iTRAQ-4`/`iTRAQ-8`;**务必让搜索步按 iTRAQ 加标(模板自动配),否则 PSM 不带 `n[144]`、通道定量全 0** |
| DIA | `dia-search`(**必须有谱图库**:填 `library_path`,或链上游接 `speclib-build` 产库) | 见下方「DIA 硬约束」 |
| PTM 定量 | DDA 链 + `ptm-profile` | 修饰位点富集分析 |

> 表中的 `→` 是**逻辑顺序,不是字面 edge**。手写 DAG 时:`search-closed` 作谱图根节点(**不连 db 边**),
> `database` 只放进 steps(库自动注入);edges 从 `search-closed → validate-psm` 开始画。
>
> **⚠️ DIA 硬约束:不支持"只给 FASTA 的库无关(library-free)搜索"。**
> 执行器的输入校验**硬性要求 `dia-search` 拿到非空的谱图库**——二者必居其一:
> ① 用户提供**现成谱图库文件**(`.tsv`/`.speclib`),填进 `dia-search` 的 `library_path`;
> ② 流水线里有 **`speclib-build` 上游步**产出 `library.tsv`,再连边 `speclib-build → dia-search`(即
> `dia-speclib-quant` 一类模板做的事)。
> **只给 FASTA、指望自动预测谱图库 = 提交必失败**。用户只有 FASTA 和 DIA 谱图时:要么用带
> `speclib-build` 的 DIA 模板,要么 `AskUserInput` 索取谱图库。**别向用户承诺"无库直搜"。**
>
> **⚠️ 多个吃谱图的步(`precursor-refine`/`quant`/`ptm-profile`/`predict-rescore`/`glyco-localize`/`speclib-build`)时**:它们既要上游产物、又硬要 mzML,
> 但 raw_files 只喂根节点——所以**必须加一个 `msconvert` 作共享谱图根**,连边 `msconvert → 每个吃谱图的步`(含 search-closed)。
> 少了这条谱图边,运行时会报 `requires mzML`(validate 已能提前拦下)。**这正是"能用模板就别手写"的原因——强烈建议直接用 `template_id`。**

### 3.5 提交前本地校验(必做,零成本)
```bash
source /bohr-workspace/.bohr_env
python3 scripts/validate_pipeline.py pipeline.json
# ok:true 才继续;否则按 errors[].{step,tool} 修 pipeline.json 后重验
```

### 4. 准备输入(按来源选通道)

> **默认路由:谱图一律走 dataset(只读挂载),不论大小、不论来自工作区还是共享盘/个人盘。** 共享盘/个人盘的谱图**直接转 dataset,不要先下载到工作区**;**唯一需要下载的是 FASTA**(因需可写,见下)。**只有当用户主动要求"直接上传/不建数据集"、且谱图 ≤100MB 时,才走 `-p`。**
>
> **铁律(数据集来源二选一,不可混):**
> - **共享盘 / 个人盘(share/… 或 personal/…)的谱图 → 必须用 sandbox 直转**(bohrium-dataset-manager 的「从共享盘/个人盘建数据集」,盘→dataset 服务端直连)。**严禁先下载到工作区再 `make_dataset.py`——那是多余的二次传输,明确禁止。**
> - **`make_dataset.py` 仅用于「用户上传到当前工作区」的本地谱图**(工作区里实打实的文件)。盘上数据不归它管。
> - 两条路径**建前都必须查重**:sandbox 直转见 bohrium-dataset-manager 的查重步骤;`make_dataset.py` 已内置查重(建前扫项目,命中同名+同大小文件直接复用、返回 `reused:true`,不重复创建)。
> - **sandbox 直转受阻时(如 `running sandbox limit reached (20/20)`、`exec` 报错进不去、盘挂载失败):向用户如实报告阻塞并停下,请其清理沙箱或改用工作区上传。绝不退化成"下载谱图到工作区再走 `-p`"——那违反本硬约束。** 浏览盘/查重优先用 HTTP API(不必开 sandbox);只有真正上传才开 sandbox。

| 数据在哪 | 怎么进作业 | 作业内可写 |
|---|---|---|
| **谱图(`.raw`/`.mzML`,任意大小)——默认建 dataset** | **工作区上传的本地文件**:`make_dataset.py`(已内置查重)。**共享盘/个人盘**:bohrium-dataset-manager 的「从共享盘/个人盘建数据集」sandbox 直转(**服务端直连、严禁先下载**,含查重)。拿 `/bohr/<名>/v1/<文件>` 填 raw_files[] | ❌ 只读 |
| **FASTA / 参数 / 需可写的小文件** | `-p` 上传目录(submit 自动打包)。共享盘/个人盘上的 fasta **只下载它**进任务目录再 -p | ✅ 可写 |
| **已有 / 网页端上传的 dataset** | 用户给了 `/bohr/…` 完整路径就直接用;需列举用 `dataset_manager.py list --project-id <pid>`(不知文件名用 `files --id <ID>`) | ❌ 只读 |
| 谱图,但用户**主动要求"直接上传"** | `-p`(校验器硬拦 >100MB;仅此情形才用 -p 传谱图) | ✅ 可写 |

`submit_pipeline.py` 自动把 `fasta_path`/本地路径放入 `-p` 目录;`/bohr/…` 路径作为 dataset 挂载引用,原样保留。

> **FASTA 必须走 `-p`,不可放 dataset。** 搜索步会于 **FASTA 同目录**写入索引(.idx);dataset 为只读挂载,建索引将失败。FASTA 体积小,放入 `-p` 即可;`make_dataset.py` 也会拒绝 FASTA 文件。
>
> **共享盘/个人盘上的 fasta:只下载这一个文件**进任务目录再走 `-p`(**别做成 dataset**)。
> **一律用 `fetch_file.py`,不要手写 curl**:
> ```bash
> source /bohr-workspace/.bohr_env
> # 个人盘:remote 以 personal/ 开头;共享盘:以 share/ 开头。路径原样传,不用拼 URL/取 userId。
> python3 scripts/fetch_file.py \
>   --remote personal/<完整路径>/xxx.fasta \
>   --out /bohr-workspace/bu-runs/<任务>/xxx.fasta
> ```
> ⛔ **绝不手写带 access key 的 curl 来下载**(取 userId、拼 download URL 都别自己做)。
> 平台会把 key 明文脱敏成 `[REDACTED]`:一旦 key 进了命令文本/中转变量/写文件/回显,
> 轻则破坏命令引号(`unexpected EOF`),重则发出假值报 `Invalid AccessKey` —— 看起来像密钥失效,
> 其实是你把它内联了。`fetch_file.py` 把 key 全程关在环境变量里,是唯一稳的下载方式。

仅**工作区上传的谱图**用 `make_dataset.py` 建 dataset(共享盘/个人盘谱图走 bohrium-dataset-manager sandbox 直转,不用这个):
```bash
source /bohr-workspace/.bohr_env
python3 scripts/make_dataset.py --file <谱图路径.raw> --name <数据集名>   # 仅谱图;FASTA 勿用
# 建前自动查重:命中同名+同大小文件则返回 {"reused": true, ...} 复用已有集,不重复创建
# 返回真实挂载路径(含随机后缀与 upload 层);填入 pipeline.json 的 raw_files[]
# submit 时附带 --dataset-path /bohr/<名>-<后缀>/v1(reused 时用返回的 mount)
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
- **`out/` 就是交付树**:执行器只往里写结果表(鉴定报告 + 定量矩阵)、`summary.json` 和 DAG 图;
  引擎中间格式(pepXML/pin)、参数文件、各步日志**根本不会写进来**。所以
  `deliverable_paths` / `result_dir` / `archive` 都可以直接给用户。
- 作业失败时,`out/failed_logs/` 里是失败步的日志(**内容已脱敏**),用来定位真因;
  向用户说明时用功能名(铁律 9),不必把日志原文贴给他。
- 返回的 `version_warning` 非空时,应转告用户(镜像需更新)。

然后:`RecordArtifact` 标记 `summary.json` 与关键报告;Chat 只回摘要(PSM/蛋白数、FDR),
不贴大表;`MemorySave` 记 `memories/projects/bottomup/runs/<run>.md`(jobId/参数/结果位置)。

## 提示与排错

### 🚫 失败排查铁律(防臆断/幻觉)
1. **先定位真实原因,不得臆测**:运行 `collect_results.py`,读取返回的 `error` / `failed_log_tail` / `missing_inputs`——工具的真实报错即在其中。未读到真实报错前,不得编造原因。
2. **失败几乎都源于数据/配置,而非"管线不支持"**:常见真因为 `database` 步漏掉(零 decoy FDR 崩)、dataset 路径漏 `upload/` 层、FASTA 置于只读 dataset、TMT 模板缺 `annotation_file`/`isotype`。
3. **绝不下"X 不支持 / 架构限制"结论**:执行器支持单工具、任意起点、显式 DAG、模板入口。怀疑不支持时,先查看真实报错并核对 `references/`,不得凭印象断言。
4. **绝不绕过执行器**手写 wrapper 直调工具二进制——违反铁律,且丢失自动接线、输入校验,降低健壮性。
5. **官方模板缺配置**:先对照镜像内置的官方模板源文件恢复缺失字段,不是执行器的问题。
6. **TMT/iTRAQ 通道定量全为 0**:**绝不归因为"引擎低 PSM 局限/归一化数据不足"**——真因几乎必是配置:① **搜索没加标**——查 PSM 修饰,应带标签质量(iTRAQ-4/8 = `n[144]`/`K[144]`,TMT = `n[229]`);若显示 `n[43]` 等其它修饰,说明搜索步未按标记搜索(用官方 `tmt*`/`itraq*` 模板可自动加标,别手写漏掉);② **少了汇总步**——isobaric 通道定量由 `quant-isobaric` 产;仅 `quant perform_isoquant` 不一定落通道列。优先整条用模板,别手改。

**判断要点:**
- **dataset 阈值(已硬拦)**:本地输入 > 100MB 时 `validate_pipeline.py` 直接报错并要求改走 make_dataset。(注:≤100MB 的谱图**默认也走 dataset**,见 §4 默认路由;-p 传谱图仅限用户主动要求。)
- **database 必须是首步**:没有 target+decoy .fas,`search-closed` 无法估 FDR。
- **运行时长**:c16_m32 上 DDA LFQ 链典型 20–60 分钟(数据量决定);`dia-search` 单样本 5–20 分钟。

**submit_pipeline.py 成功返回示例:**
```json
{"ok": true, "jobId": "22907069", "status": "scheduling", "pollAfterMs": 20000, "nextTool": "poll_job.py"}
```

**常见错误:**
| 现象 | 原因 / 处理 |
|---|---|
| `AccessKey Invalid` / `AccessKey is required` | **先判是不是你自己内联了 key**:命令/日志里出现 `[REDACTED]` = 你把 key 明文写进了命令或文件,被平台脱敏后发了出去 —— 这不是 key 失效,换 key 也没用。修法:一切认证操作走脚本(下载 `fetch_file.py`、列数据集 `dataset_manager.py list`、提交 `submit_pipeline.py`、查作业 `poll_job.py`),它们从环境读 key、绝不内联。**只有排除了内联(日志无 `[REDACTED]`、脚本也报鉴权失败)之后**,才考虑其它:①脚本报缺 key → 先 `bash scripts/setup.sh`;②高频并发限流 → 稍等重试;③确系 key 被撤销/过期/权限变更 → 这时才 `AskUserInput` 请用户重取。REST 头 `accessKey:` 与 `Authorization: Bearer` 两种都行(不是失败原因)。 |
| job `status=-1`(失败) | `collect_results.py` 直接返回 `failed_step` + `error` + `failed_log_tail`;依据真实报错修正 |
| `no files found matching X` | 输入路径问题;确认文件真存在,或 dataset 路径带 `upload/` 层 |
| 零 PSM / FDR 崩溃 | `database` 步漏掉,`search-closed` 直接拿 target-only FASTA 导致零 decoy |
| `Dataset ... has been deleted` | Bohrium 给数据集名加随机后缀;**make_dataset.py 已自动从 API 返回真实路径**,用它给的 `spectrum_mount` 即可 |
| TMT 模板无定量结果 | 检查 quant 的 `isotype`/`annotation_file`、quant-isobaric 的 `channel_num`;对照官方模板源文件补齐缺失字段 |
| `Cannot read file .meta/db.bin` | report 步的 workspace 未 annotate;确认流水线包含 database 步 |

## HARD STOP(成本确认)
机型为大核数(如 `c32_*`)或预计长时运行,提交前**必须** `AskUserInput` 用 checkbox 让用户确认费用。不静默提交高成本 job。

## 边界
- 不在 sandbox 里跑搜索/定量/DIA 引擎(它们在 Bohrium 镜像里,经作业跑)。
- GB 级谱图不经 `-p` 上传(经 dataset 挂载),也不读入对话上下文。
- 不臆造文件路径或参数;不确定就 `AskUserInput`。
- **禁止 `cat` 执行器日志 / 大 TSV**:指标取 `collect_results.py` 的 `metrics`;需细节时 `head -40` 读 TSV 顶部。
- 不在 Bohrium 镜像库查找单工具镜像;一律使用配置的 `IMAGE_ADDRESS`(默认取自 `image.txt`)。
- ACCESS_KEY 由平台注入,不写进 prompt/日志/文件。

## 配置(openclaw.json)
```json
"bottomup-proteomics": {
  "enabled": true,
  "env": { "ACCESS_KEY": "<注入>", "PROJECT_ID": "<你的项目ID>" }
}
```
`ACCESS_KEY`、`PROJECT_ID` **必填**(无默认)。`IMAGE_ADDRESS` 可选:默认用 skill 的 `image.txt`。
