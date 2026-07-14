# Bottom-up 参数完整参考(以本文件为准)

> 来源:执行环境内各步骤实测参数定义。
> 以本文件为准。

`pipeline.json` 的 `steps[].params` 用下表 **snake_case 键**。留空=工具默认。

工具二进制、依赖库、模型文件的路径均由执行环境预置,无需在 `params` 里配置。

---

## ⚠️ 会导致错误的高频陷阱(先看)

- **`database` 必须是搜索链的首步**:target-only FASTA 直接喂搜索引擎 = 零 decoy → FDR 崩溃。
- **`search-closed` 的 `database_path` 必须填**:required 字段无默认值。
- **FASTA 不能放 dataset**:搜索步骤要在 fasta 同目录写 `.idx`,只读 dataset 挂载会失败。
- **DIA 搜索必须有谱图库**:`dia-search` 的 `library_path` 在输入校验阶段就是硬性要求,**不支持只给 FASTA 的库无关(library-free)模式**。要么直接提供现成谱图库文件,要么在流水线里加一个 `speclib-build` 上游步骤产出 `library.tsv` 再接入。
- **TMT 工作流**:`quant` 的 `perform_isoquant=true` + `isotype` + `annotation_file` 三件套缺一不可;`quant-isobaric` 的 `annotation_file` 也是 required。
- **decoy_prefix 一致性**:`search-closed`、`database`、`validate-psm`、`report` 的 `decoy_prefix` 必须统一(默认全为 `rev_`)。

---

## database

为搜索准备 target+decoy FASTA(`database --custom`)。

| 键 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `decoy_prefix` | str | `rev_` | Decoy 序列前缀;必须与搜索步骤保持一致 |
| `add_contam` | bool | true | 追加 cRAP 污染蛋白序列 |
| `contam_prefix` | bool | false | 为污染蛋白加前缀标记 |
| `enzyme` | enum | `trypsin` | `trypsin\|lys_c\|lys_n\|glu_c\|chymotrypsin` (仅影响序列分类) |
| `isoform` | bool | false | 含 UniProt isoform 序列 |
| `reviewed` | bool | false | 只用 Swiss-Prot reviewed 条目 |

**产出**:一个 `*-decoys[-contam]-<stem>.fas`(target+decoy 合并),作为 `search-closed.database_path`。

---

## search-closed

DDA 闭合/质量偏移搜索。`database_path` **required**。

### 数据库与线程
| 键 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `database_path` | str | — **(required)** | database 步产出的 target+decoy .fas 路径 |
| `num_threads` | int | 8 | Worker 线程数 |
| `ram_gb` | int | 16 | JVM 堆内存(GB);大库/多变修饰需 16+ |

### 前体/碎片容差
| 键 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `precursor_tolerance_ppm` | float | 20.0 | 前体质量窗口(±ppm) |
| `fragment_tolerance_ppm` | float | 20.0 | 碎片质量容差(ppm) |
| `isotope_error` | str | `0/1/2` | 允许的同位素峰偏移,斜杠分隔 |
| `calibrate_mass` | int | 2 | 0=关,1=质量校正,2=质量+参数优化 |
| `mass_offsets` | str | `0` | 斜杠分隔质量偏移(offset 搜索);`0`=无 |
| `labile_search_mode` | enum | `off` | `off\|labile\|nglycan`;糖肽/labile PTM 搜索 |

### 酶切
| 键 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `enzyme_name` | str | `stricttrypsin` | 酶名(stricttrypsin/trypsin/chymotrypsin…) |
| `num_enzyme_termini` | int | 2 | 0=非特异,1=半酶切,2=全酶切 |
| `allowed_missed_cleavage` | int | 2 | 最大漏切数(0–5) |
| `digest_min_length` / `digest_max_length` | int | 7 / 50 | 肽段长度范围 |
| `digest_min_mass` / `digest_max_mass` | float | 500.0 / 5000.0 | 肽段质量范围(Da) |

### 修饰
| 键 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `var_mod_oxidation_M` | bool | true | 可变修饰:Met 氧化(+15.9949) |
| `var_mod_acetyl_nterm` | bool | true | 可变修饰:蛋白 N 端乙酰化(+42.0106) |
| `fixed_mod_C_carbamidomethyl` | bool | true | 固定修饰:Cys 碘乙酰胺化(+57.02146) |
| `variable_mods` | str | `` | 额外可变修饰,格式 `<mass> <残基> <max>`,分号分隔 |
| `tmt_label_mass` | float | null | TMT 固定修饰质量(229.16293=TMT-6/10/11,304.20715=TMTpro) |
| `max_variable_mods_per_peptide` | int | 3 | 每肽最大可变修饰数 |

---

## validate-psm

PSM 概率校正(半参数混合模型)。

| 键 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `decoy_prefix` | str | `rev_` | 与上游保持一致 |
| `ppm` | bool | true | 质量模型用 ppm |
| `accmass` | bool | true | 精确质量分箱 |
| `nonparam` | bool | true | 半参数混合模型 |
| `decoyprobs` | bool | true | 也对 decoy hits 算概率 |
| `combine` | bool | true | 合并所有 pepXML 建模 |

---

## rescore

机器学习 PSM 重打分(SVM 后处理,可替代 `validate-psm` 的概率校正)。

| 键 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `test_fdr` | float | 0.01 | 最终结果 FDR 阈值 |
| `train_fdr` | float | 0.01 | 训练正样本 FDR |
| `max_iter` | int | 10 | 最大 SVM 迭代数 |
| `num_threads` | int | 8 | Worker 线程数 |
| `seed` | int | 1 | 随机种子(可复现) |
| `subset_max_train` | int | 0 | 训练子集大小(>1M PSM 时建议设正值) |
| `only_psms` | bool | false | 跳过肽段级聚合 |
| `picked_protein_fasta` | str | null | 设此路径启用 picked-protein FDR |

---

## report

FDR 过滤 + 最终报告(PSM/肽段/蛋白 TSV)。

| 键 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `decoy_prefix` | str | `rev_` | 与上游保持一致 |
| `psm_fdr` | float | 0.01 | PSM 级 FDR 阈值(1%) |
| `peptide_fdr` | float | 0.01 | 肽段级 FDR |
| `ion_fdr` | float | 0.01 | 肽段离子 FDR |
| `protein_fdr` | float | 0.01 | 蛋白级 FDR |
| `inference` | bool | true | 运行蛋白推断 |
| `razor` | bool | true | Razor-peptide 算法 |
| `report_msstats` | bool | false | 额外产 MSstats 兼容 CSV |
| `remove_contam` | bool | false | 从报告中去除污染蛋白 |

---

## quant

LFQ 或 TMT 定量。

| 键 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `mztol_ppm` | float | 10.0 | MS1 质量容差(ppm) |
| `rttol_min` | float | 0.4 | 保留时间容差(min) |
| `perform_ms1quant` | bool | true | 运行 LFQ;TMT-only 实验设 false |
| `perform_isoquant` | bool | false | 运行 TMT 定量(需配 isotype+annotation_file) |
| `isotype` | enum | `TMT-10` | `iTRAQ-4\|iTRAQ-8\|TMT-0\|TMT-2\|TMT-6\|TMT-10\|TMT-11\|TMT-16\|TMT-18\|TMT-35` |
| `isolevel` | int | 2 | Reporter 离子读取 MS 层(2=MS2,3=MS3) |
| `annotation_file` | str | `` | TMT 通道→样品注释文件路径(isoquant 时**必填**) |
| `mbr` | bool | false | Match-between-runs(跨样品对齐) |
| `maxlfq` | bool | true | 计算 MaxLFQ 强度 |
| `normalization` | bool | true | 跨 run 强度归一化 |
| `threads` | int | 0 | Worker 线程(0=全核) |

---

## quant-isobaric

TMT 多实验通道定量整合。

| 键 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `annotation_file` | str | — **(required)** | TMT 通道→样品注释文件(空格分隔 `<channel> <sample>`) |
| `channel_num` | int | 10 | Plex 大小:6/10/11/16/18/35 |
| `ref_tag` | str | `pool` | 参考通道标记 |
| `add_Ref` | int | -1 | 人工参考:-2 原始,-1 关,0 sum,1 avg,2 median |
| `groupby` | int | -1 | 聚合级别:-1 全,0 gene,1 protein,2 peptide,3–5 PTM 位点 |
| `prot_norm` | int | -1 | 归一化:-1 all,0 none,1 MC,2 GN,3 SL+IRS |
| `min_pep_prob` | float | 0.9 | 最低 PSM 概率 |
| `min_purity` | float | 0.5 | 前体纯度阈值 |
| `ram_gb` | int | 16 | JVM 堆内存(GB) |

---

## dia-search

DIA 搜索与定量。

> **必须有谱图库**:`library_path` 在输入校验阶段硬性要求非空,**没有库无关(library-free)模式**。
> 要么直接给一个现成的谱图库文件(`.tsv`/`.speclib`),要么在流水线里放一个 `speclib-build` 上游步骤,
> 用它产出的 `library.tsv` 作为本步的 `library_path`。只给 `fasta_path` **不能**启动 DIA 搜索。

| 键 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `library_path` | str | — **(必须有值)** | 谱图库路径(.tsv/.speclib);由上游 `speclib-build` 产出或直接提供现成库 |
| `fasta_path` | str | `` | 蛋白推断用 FASTA(空=跳过蛋白级报告);**不能替代 library_path** |
| `num_threads` | int | 8 | Worker 线程数 |
| `precursor_qvalue` | float | 0.01 | Run 级前体 q-value 阈值 |
| `protein_qvalue` | float | 0.01 | Run 级蛋白 q-value 阈值 |
| `mbr` | bool | false | Match-between-runs(重分析对齐) |
| `matrices` | bool | true | 产 pr_matrix/pg_matrix 定量矩阵 |
| `relaxed_protein_inference` | bool | false | 宽松蛋白推断 |
| `no_protein_inference` | bool | false | 跳过蛋白推断 |
| `extra_cmdline` | str | `` | 额外命令行参数(如 `--smart-profiling`) |

---

## msconvert(ProteoWizard 3.0.25323)

原始谱图格式转换；DDA/DIA 工作流的第一步，将厂商格式(raw/wiff/d 等)转为 mzML/mzXML。

### 常用参数
| 键 | 默认 | 说明 |
|---|---|---|
| `output_format` | `mzML` | 输出格式：`mzML\|mzXML\|mz5\|mzMLb\|mgf\|text\|ms1\|ms2\|cms1\|cms2` |
| `precision` | `64` | 二进制精度(位)：32 或 64 |
| `zlib` | `true` | 启用 zlib 压缩 |
| `filters` | `['peakPicking true 1-']` | 谱图处理 filter 列表(每行一条)；默认含质心化 |

### 高级/输出控制参数
| 键 | 默认 | 说明 |
|---|---|---|
| `chromatogram_filters` | `[]` | 色谱图 filter 列表 |
| `extension` | `null` | 输出文件扩展名覆盖 |
| `mz_precision` | `null` | m/z 精度位数 |
| `inten_precision` | `null` | 强度精度位数 |
| `mz_truncation` | `null` | m/z 截断位数 |
| `inten_truncation` | `null` | 强度截断位数 |
| `mz_delta` | `false` | 启用 m/z delta 预测编码 |
| `inten_delta` | `false` | 启用强度 delta 预测编码 |
| `mz_linear` | `false` | 启用 m/z 线性预测编码 |
| `inten_linear` | `false` | 启用强度线性预测编码 |
| `noindex` | `false` | 禁止生成索引 |
| `numpress_linear` | `false` | m/z 和 RT 的 numpress 线性压缩 |
| `numpress_linear_abs_tol` | `null` | numpress 线性绝对容差 |
| `numpress_pic` | `false` | 启用 numpress pic 压缩 |
| `numpress_slof` | `false` | 启用 numpress slof 压缩 |
| `numpress_all` | `false` | 启用所有 numpress 编解码器 |
| `outfile` | `null` | 指定输出文件名 |
| `contact_info` | `null` | 联系信息文件路径 |
| `filelist` | `null` | 输入文件列表路径 |
| `config_file` | `null` | msconvert 配置文件 |
| `verbose` | `true` | 详细日志 |
| `single_threaded` | `false` | 单线程转换 |
| `continue_on_error` | `false` | 出错后继续处理剩余文件 |
| `merge` | `false` | 合并多个输入文件 |
| `combine_ion_mobility_spectra` | `false` | 合并离子迁移谱 |
| `dda_processing` | `false` | 启用 DDA 处理模式 |
| `gzip` | `false` | gzip 压缩输出文件 |
| `sim_as_spectra` | `false` | 将 SIM 扫描写为谱图 |
| `srm_as_spectra` | `false` | 将 SRM 扫描写为谱图 |
| `ignore_calibration_scans` | `false` | 忽略校准扫描 |
| `accept_zero_length_spectra` | `false` | 接受零长度谱图 |
| `ignore_missing_zero_samples` | `false` | 忽略缺失零样本 |
| `ignore_unknown_instrument_error` | `false` | 忽略未知仪器错误 |
| `strip_location_from_source_files` | `false` | 去除源文件路径信息 |
| `strip_version_from_software` | `false` | 去除软件版本信息 |
| `mzmlb_chunk_size` | `null` | mzMLb chunk 大小 |
| `mzmlb_compression_level` | `null` | mzMLb 压缩级别 |
| `run_index_set` | `null` | 指定处理的 run 索引集合 |

---

## precursor-refine

非特异/开放搜索后清理嵌合前体；在开放搜索之后、`validate-psm` 之前运行，修正前体单同位素质量。

| 键 | 默认 | 说明 |
|---|---|---|
| `precursor_mass_ppm` | `20.0` | 前体质量容差(ppm) |
| `precursor_isolation_window` | `0.7` | 前体隔离窗口(m/z) |
| `precursor_charge_min` | `1` | 嵌合检测最低前体电荷 |
| `precursor_charge_max` | `6` | 嵌合检测最高前体电荷 |
| `isotope_number` | `3` | 参与考量的理论同位素峰数 |
| `correct_isotope_error` | `false` | 检测到同位素误差时用单同位素质量更新前体 |
| `raw_file_extension` | `mzML` | 谱图文件扩展名(mzML/mzXML) |
| `ram_gb` | `8` | JVM 堆内存(GB) |
| `num_threads` | `-1` | 线程数(-1 = CPU核数−1) |

---

## rescore-export

将 `rescore` 的 TSV 结果转回 pepXML 格式，供 `psm-integrate` / `protein-infer` 进一步处理。

| 键 | 默认 | 说明 |
|---|---|---|
| `data_type` | `DDA` | 采集模式：`DDA`(读 `<basename>.pepXML`)或 `DIA`(读 `<basename>_rank<N>.pepXML`) |
| `min_prob` | `0.0` | 最低重打分概率阈值，低于此值的 PSM 不输出 |
| `updated_fasta_path` | `''` | 可选：改写输出 pepXML 中的 `<search_database local_path>` 字段(空=保持原值) |

---

## ptm-localize

PTM 位点定位概率打分；糖肽/磷酸化等位点不确定时用此工具，在 `validate-psm` 后运行。

| 键 | 默认 | 说明 |
|---|---|---|
| `mods` | `STY:79.966331,M:15.9949,n:42.0106` | 修饰位点+质量列表，格式 `<残基>:<mass>` 逗号分隔 |
| `minprob` | `0.5` | 参与评估的 PSM 最低概率(MINPROB=) |
| `em` | `1` | EM 模型：0=不用,1=强度,2=强度+匹配峰,3=匹配峰 |
| `fragppmtol` | `10.0` | MS2 碎片 ppm 容差(FRAGPPMTOL=) |
| `keepold` | `true` | 保留 pepXML 中已有的定位结果(KEEPOLD) |
| `static` | `true` | 对所有 PSM 用统一 fragppmtol(STATIC) |
| `nions` | `b` | N 端离子类型(NIONS=)，CID 默认用 b |
| `nostack` | `false` | 禁止同一残基叠加多个 PTM(NOSTACK) |
| `extra_cmdline` | `''` | 额外命令行参数(如 `NOUPDATE MASSDIFFMODE LABILITY`) |

---

## ptm-profile

开放搜索后 PTM 质量偏移注释与统计；O-糖肽分析时配合 `glyco_mode=true`。

### 常用参数
| 键 | 默认 | 说明 |
|---|---|---|
| `glyco_mode` | `false` | 启用糖肽 PTM 分析路径 |
| `n_glyco` | `true` | glyco_mode 下选 N-糖(true)还是 O-糖(false) |
| `annotation_file` | `''` | `glyco`/`unimod`/`common` 或自定义注释表路径；空=unimod |
| `annotation_tol` | `0.01` | 已知修饰匹配容差(Da) |
| `mass_offsets` | `''` | 限定峰选取范围，斜杠分隔(如 `0/-105.0248`)；空=全开放搜索 |
| `precursor_tol` | `0.01` | 峰宽容差(Da 或 ppm，由 `precursor_mass_units` 决定单位) |
| `precursor_mass_units` | `0` | 0=Da，1=ppm |
| `spectra_ppmtol` | `20.0` | 定位+谱图相似度 MS2 ppm 容差 |

### 高级参数
| 键 | 默认 | 说明 |
|---|---|---|
| `isotope_error` | `0` | 同位素校正列表(如 `0/1/2`) |
| `peakpicking_promRatio` | `0.3` | 峰选取显著度比值 |
| `peakpicking_width` | `0.002` | 峰选取宽度(Da) |
| `peakpicking_topN` | `500` | 最大报告峰数 |
| `peakpicking_minPsm` | `10` | 每峰最小 PSM 数 |
| `varmod_masses` | `''` | 优先可变修饰质量列表(如 `mod1:1234.456,mod2:456.789`) |
| `spectra_maxfragcharge` | `2` | 定位最大碎片电荷 |
| `iontype_a` | `false` | 使用 a 离子 |
| `iontype_b` | `true` | 使用 b 离子 |
| `iontype_c` | `false` | 使用 c 离子 |
| `iontype_x` | `false` | 使用 x 离子 |
| `iontype_y` | `true` | 使用 y 离子 |
| `iontype_z` | `false` | 使用 z 离子 |
| `compare_betweenRuns` | `false` | 跨 run 计算谱图相似度/RT |
| `output_extended` | `false` | 保留中间产物和谱图级输出 |
| `prep_for_quant` | `false` | 为下游 `quant` 步准备 PSM 表(接 `quant` 时需设 true) |
| `threads` | `0` | 线程数(0=全核) |
| `ram_gb` | `16` | JVM 堆内存(GB) |

---

## dia-pseudo

DIA 前处理：从 DIA 原始谱图提取伪 DDA spectra(Q1/Q2/Q3)，供 DDA 搜索引擎搜索。

### 常用参数
| 键 | 默认 | 说明 |
|---|---|---|
| `MS1PPM` | `10.0` | 信号提取 MS1 ppm 容差 |
| `MS2PPM` | `20.0` | 信号提取 MS2 ppm 容差 |
| `Q1` | `true` | 输出 Q1 伪 DDA mzML |
| `Q2` | `true` | 输出 Q2 伪 DDA mzML |
| `Q3` | `true` | 输出 Q3 伪 DDA mzML |

### 高级参数
| 键 | 默认 | 说明 |
|---|---|---|
| `RPmax` | `25` | 最大前体–碎片比值 |
| `RFmax` | `500` | 最大碎片–碎片比值 |
| `CorrThreshold` | `0.0` | 前体–碎片相关性截止值 |
| `DeltaApex` | `0.2` | 前体–碎片顶点时间差容差 |
| `RTOverlap` | `0.3` | 最小 RT 重叠比例 |
| `AdjustFragIntensity` | `true` | 分组后调整碎片强度 |
| `BoostComplementaryIon` | `false` | 增强互补离子对(适合建库) |
| `ExportPrecursorPeak` | `false` | 导出检测到的 MS1 特征文件 |
| `MS1SN` | `1.1` | MS1 信噪比阈值 |
| `MS2SN` | `1.1` | MS2 信噪比阈值 |
| `MassDefectFilter` | `true` | 应用基于质量缺陷的肽段过滤器 |
| `ram_gb` | `12` | JVM 堆内存(GB) |
| `threads` | `7` | 线程数 |

---

## dia-features

timsTOF PASEF DIA 前处理：提取伪 DDA pepXML，供 DDA 搜索引擎搜索。

| 键 | 默认 | 说明 |
|---|---|---|
| `ms1MS2Corr` | `0.3` | MS1/MS2 相关性阈值(`--ms1MS2Corr`) |
| `deltaApexIM` | `0.01` | 离子迁移率 Δ(用于 MS1/MS2 顶点匹配) |
| `deltaApexRT` | `3` | RT 顶点扫描 Δ 范围(整数扫描数) |
| `massDefectFilter` | `true` | 应用质量缺陷过滤器 |
| `massDefectOffset` | `0.1` | 质量缺陷偏移 |
| `RFMax` | `500` | 每谱图保留 top-N 峰 |
| `writeInter` | `false` | 写出中间文件 |
| `ram_gb` | `16` | JVM 堆内存(GB) |
| `threads` | `8` | 线程数 |

---

## speclib-build

DIA 谱图库构建；从 DDA 搜索结果(pepXML+mzML)生成谱图库，供 `dia-search` 使用。
**这是 DIA 流水线里唯一能在线产出 `library_path` 的步骤**——没有现成谱图库时必须加这一步。

| 键 | 默认 | 说明 |
|---|---|---|
| `max_delta_ppm` | `15.0` | UniMod 注释质量差 ppm 阈值 |
| `max_delta_unimod` | `0.02` | UniMod 注释质量差 Da 阈值 |
| `max_psm_pep` | `0.5` | 纳入 PSM 的最大后验错误概率 |
| `fragment_types` | `['b', 'y']` | 允许的碎片离子类型(a/b/c/x/y/z) |
| `fragment_charges` | `['1','2','3','4']` | 允许的碎片离子电荷 |
| `enable_specific_losses` | `false` | 启用特异性碎片离子 loss |
| `enable_unspecific_losses` | `false` | 启用非特异性碎片离子 loss |
| `rt_lowess_fraction` | `0.05` | RT 校正 LOWESS 平滑分数(0=交叉验证) |
| `im_lowess_fraction` | `0.05` | IM 校正 LOWESS 平滑分数 |
| `psm_fdr_threshold` | `0.01` | PSM FDR 截止值 |
| `peptide_fdr_threshold` | `0.01` | 肽段 FDR 截止值 |
| `protein_fdr_threshold` | `0.01` | 蛋白 FDR 截止值 |
| `perform_rt_calibration` | `true` | 跨 run RT 对齐 |
| `perform_im_calibration` | `true` | timsTOF IM 对齐 |
| `nofdr` | `false` | 跳过 FDR 重评估(上游已过滤时用) |

---

## glyco-localize

O-糖肽定位：配对 HCD+ETD 双激活扫描，定位 O-连接糖基化位点。

| 键 | 默认 | 说明 |
|---|---|---|
| `ms1_tol` | `20.0` | 前体质量容差(ppm) |
| `ms2_tol` | `20.0` | 产物离子质量容差(ppm) |
| `glyco_db` | `HexNAc(1),HexNAc(1)Hex(1),…(12 组分)` | O-糖组成列表(逗号分隔，糖组成语法) |
| `max_glycans` | `4` | 每 PSM 最大糖基数 |
| `min_isotope_error` | `0` | 最小同位素误差偏移 |
| `max_isotope_error` | `2` | 最大同位素误差偏移 |
| `filter_oxonium` | `false` | 启用 oxonium 离子糖基过滤 |
| `oxonium_filter_file` | `''` | 自定义 oxonium 规则文件(空=用内置列表) |
| `oxonium_min_intensity` | `0.05` | oxonium 过滤最小相对强度(0–1) |
| `activation1` | `HCD` | 主扫描激活方式(糖/oxonium 扫描) |
| `activation2` | `ETD` | 配对扫描激活方式(肽链骨架扫描) |
| `threads` | `0` | 线程数(0=自动) |

---

## predict-rescore

深度学习 PSM 重打分：预测 RT、谱图、离子迁移率特征，增强 `rescore` 的输入特征。

| 键 | 默认 | 说明 |
|---|---|---|
| `use_rt` | `true` | 预测 RT(useRT) |
| `use_spectra` | `true` | 预测谱图(useSpectra) |
| `use_im` | `false` | 预测离子迁移率(useIM，timsTOF 时开启) |
| `rt_model` | 内置默认模型 | RT 预测模型(rtModel)；保持默认即可 |
| `spectra_model` | 内置默认模型 | 谱图预测模型(spectraModel)；保持默认即可 |
| `num_threads` | `8` | 线程数 |
| `ram_gb` | `16` | JVM 堆内存(GB) |

> 预测模型与依赖库由执行环境预置，本步不需要配置任何路径。

---

## psm-integrate

多重搜索引擎概率整合；汇总多个 pepXML 后计算联合概率，供 `protein-infer` 使用。

| 键 | 默认 | 说明 |
|---|---|---|
| `decoy_prefix` | `rev_` | decoy 序列标签(`--decoy`)，须与上游一致 |
| `num_threads` | `4` | 线程数(`--threads`) |
| `min_prob` | `0.0` | 输出最低概率阈值(`--minProb`) |
| `output_prefix` | `interact.iproph` | 输出文件名前缀；产出 `<prefix>.pep.xml` |
| `length` | `false` | 使用肽段长度模型(`--length`) |
| `sharpnse` | `false` | SWATH 更强判别 NSE 模型(`--sharpnse`) |
| `no_fpkm` | `false` | 禁用 FPKM 模型(`--nofpkm`) |
| `no_nrs` | `false` | 禁用 NRS 模型(`--nonrs`) |
| `no_nse` | `false` | 禁用 NSE 模型(`--nonse`) |
| `no_nsi` | `false` | 禁用 NSI 模型(`--nonsi`) |
| `no_nsm` | `false` | 禁用 NSM 模型(`--nonsm`) |
| `no_nsp` | `false` | 禁用 NSP 模型(`--nonsp`) |
| `no_nss` | `false` | 禁用 NSS 模型(`--nonss`) |

---

## protein-infer

蛋白推断：从肽段概率计算蛋白概率并分组；BU 流程最终蛋白鉴定步骤。

| 键 | 默认 | 说明 |
|---|---|---|
| `output_prefix` | `combined` | 输出文件名前缀；产出 `<prefix>.prot.xml` |
| `max_ppm_diff` | `2000000` | 蛋白分组最大肽段质量差(ppm)；默认值实际相当于禁用此过滤 |
| `min_prob` | `0.05` | 纳入蛋白推断的最低肽段概率 |
| `from_psm_integrate` | `false` | 声明输入来自 `psm-integrate` 步 |
| `no_nsp` | `false` | 禁用 NSP 模型(`--nonsp`) |
| `subgroups` | `false` | 启用蛋白子分组(`--subgroups`) |
| `unmapped` | `false` | 报告 UNMAPPED 蛋白(`--unmapped`) |

---

## 产物

| 工具 | 关键产物 |
|---|---|
| database | `*-decoys-*.fas`(target+decoy 合并 FASTA) |
| msconvert | `*.mzML`(或指定格式谱图文件) |
| search-closed | `*.pepXML`(每 run)、`calibration*.pepXML` |
| precursor-refine | `*_corrected.pepXML`(修正前体质量后的 pepXML) |
| dia-pseudo | `*_Q1.mzML`、`*_Q2.mzML`、`*_Q3.mzML`(伪 DDA 谱图) |
| dia-features | `*.pepXML`(timsTOF DIA 伪 DDA 结果) |
| speclib-build | `*.pqp`(谱图库)、`library.tsv`(供 `dia-search` 的 `library_path`) |
| predict-rescore | 更新后 `*.pepXML`(附加 RT/谱图预测特征) |
| validate-psm | `interact-*.pep.xml`(概率打分后 pepXML) |
| ptm-localize | 更新后 `interact-*.pep.xml`(含 PTM 位点概率) |
| rescore | `target_psms.tsv`、`target_peptides.tsv` |
| rescore-export | `*.pep.xml`(重打分结果转回 pepXML 格式) |
| psm-integrate | `interact.iproph.pep.xml`(多引擎联合概率 pepXML) |
| protein-infer | `combined.prot.xml`(蛋白概率分组结果) |
| ptm-profile | `*_global_peaklist.tsv`、`*_localization_results.tsv` 等 |
| glyco-localize | O-糖肽位点定位结果表(`*.tsv`) |
| report | `psm.tsv`、`peptide.tsv`、`protein.tsv`、`ion.tsv` |
| quant | 更新后 `psm.tsv/peptide.tsv/protein.tsv`(含强度列) |
| quant-isobaric | `abundance_gene_MD.tsv`、`abundance_protein_MD.tsv` 等 |
| dia-search | `report.tsv`、`report.pr_matrix.tsv`、`report.pg_matrix.tsv` |
