# 官方工作流模板目录(template_id)

共 81 个官方工作流模板。**优先用 `template_id` 跑**(一行调用,执行器自动展开);
**确无对应模板才手写显式 DAG**。

> 每个模板下方「DAG」用 `steps`+`edges` 表示,**和你手写 pipeline.json 完全同格式**(`edges` 用 `src`/`dst`)——
> `edges` 列表本身就是 DAG(含多父/菱形),需要变体时可直接复制改造。
> 参数一律用模板默认(要调某参数走 `overrides`,参数名见 `parameters.md`)。


## 1. 基础(closed / basic)

### `bottomup-closed`
- **用途**:谱图转换 → 闭式搜索(search-closed) → 重打分(rescore)。搜索步需要用户自备 target+decoy 合并 FASTA。
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**预建 target+decoy 库**(.fas)
- **调用(推荐)**:`{"template_id":"bottomup-closed","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"}
]}
```

### `basic-search`
- **用途**:迁移自官方模板 'Basic-Search.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"basic-search","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```


## 2. 定量 / 标记-free / 专题

### `bottomup-lfq`
- **用途**:谱图转换 → 闭式搜索(search-closed) → 结果汇总(report) → 定量(quant)。菱形 DAG:quant 步同时消费 msconvert 产出的 mzML 与 report 产出的 psm.tsv。
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**预建 target+decoy 库**(.fas)
- **调用(推荐)**:`{"template_id":"bottomup-lfq","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `chemprot-abpp-ipiaa`
- **用途**:迁移自官方模板 'chemprot-ABPP-ipIAA.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"chemprot-abpp-ipiaa","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `chemprot-abpp-isodtb`
- **用途**:迁移自官方模板 'chemprot-ABPP-isoDTB.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"chemprot-abpp-isodtb","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `chemprot-abpp-isotop`
- **用途**:迁移自官方模板 'chemprot-ABPP-isoTOP.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"chemprot-abpp-isotop","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `chemprot-pal`
- **用途**:迁移自官方模板 'chemprot-PAL.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"chemprot-pal","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "ptm_summary", "tool": "ptm-profile"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "ptm_summary"},
  {"src": "convert", "dst": "ptm_summary"}
]}
```

### `citrullination`
- **用途**:迁移自官方模板 'citrullination.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"citrullination","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `fpop`
- **用途**:迁移自官方模板 'FPOP.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fpop","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "validate"},
  {"src": "database", "dst": "validate"},
  {"src": "validate", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `lfq-mbr`
- **用途**:迁移自官方模板 'LFQ-MBR.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"lfq-mbr","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `silac3`
- **用途**:迁移自官方模板 'SILAC3.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"silac3","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `stellar-dda`
- **用途**:迁移自官方模板 'Stellar-DDA.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"stellar-dda","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `wwa`
- **用途**:迁移自官方模板 'WWA.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"wwa","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```


## 3. 开放搜索 / 质量偏移

### `mass-offset-commonptms`
- **用途**:迁移自官方模板 'Mass-Offset-CommonPTMs.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"mass-offset-commonptms","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "ptm_summary", "tool": "ptm-profile"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "ptm_summary"},
  {"src": "convert", "dst": "ptm_summary"}
]}
```

### `open`
- **用途**:迁移自官方模板 'Open.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"open","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "cleanup", "tool": "precursor-refine"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "ptm_summary", "tool": "ptm-profile"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "cleanup"},
  {"src": "database", "dst": "cleanup"},
  {"src": "convert", "dst": "cleanup"},
  {"src": "cleanup", "dst": "validate"},
  {"src": "database", "dst": "validate"},
  {"src": "validate", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "ptm_summary"},
  {"src": "convert", "dst": "ptm_summary"}
]}
```

### `open-quickscan`
- **用途**:迁移自官方模板 'Open-quickscan.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"open-quickscan","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "cleanup", "tool": "precursor-refine"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "ptm_summary", "tool": "ptm-profile"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "cleanup"},
  {"src": "database", "dst": "cleanup"},
  {"src": "convert", "dst": "cleanup"},
  {"src": "cleanup", "dst": "validate"},
  {"src": "database", "dst": "validate"},
  {"src": "validate", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "ptm_summary"},
  {"src": "convert", "dst": "ptm_summary"}
]}
```

### `xrnax-massoffset`
- **用途**:迁移自官方模板 'XRNAX-MassOffset.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"xrnax-massoffset","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "cleanup", "tool": "precursor-refine"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "ptm_summary", "tool": "ptm-profile"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "cleanup"},
  {"src": "database", "dst": "cleanup"},
  {"src": "convert", "dst": "cleanup"},
  {"src": "cleanup", "dst": "validate"},
  {"src": "database", "dst": "validate"},
  {"src": "validate", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "ptm_summary"},
  {"src": "convert", "dst": "ptm_summary"}
]}
```


## 4. 同位素标记定量(TMT / iTRAQ)

### `chemprot-abpp-iadtb-tmt16`
- **用途**:迁移自官方模板 'chemprot-ABPP-IADTB-TMT16.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"chemprot-abpp-iadtb-tmt16","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `glyco-n-tmt`
- **用途**:迁移自官方模板 'glyco-N-TMT.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"glyco-n-tmt","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "ptm_summary", "tool": "ptm-profile"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "validate"},
  {"src": "database", "dst": "validate"},
  {"src": "validate", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "ptm_summary"},
  {"src": "convert", "dst": "ptm_summary"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `itraq4`
- **用途**:迁移自官方模板 'iTRAQ4.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"itraq4","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `itraq4-phospho`
- **用途**:迁移自官方模板 'iTRAQ4-phospho.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"itraq4-phospho","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "localize", "tool": "ptm-localize"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "localize"},
  {"src": "localize", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `nonspecific-hla-tmt10`
- **用途**:迁移自官方模板 'Nonspecific-HLA-TMT10.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"nonspecific-hla-tmt10","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt10`
- **用途**:迁移自官方模板 'TMT10.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt10","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt10-acetyl`
- **用途**:迁移自官方模板 'TMT10-acetyl.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt10-acetyl","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "localize", "tool": "ptm-localize"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "localize"},
  {"src": "localize", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt10-acetyl-noloc`
- **用途**:迁移自官方模板 'TMT10-acetyl-noloc.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt10-acetyl-noloc","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt10-bridge`
- **用途**:迁移自官方模板 'TMT10-bridge.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt10-bridge","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt10-ms3`
- **用途**:迁移自官方模板 'TMT10-MS3.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt10-ms3","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt10-ms3-phospho`
- **用途**:迁移自官方模板 'TMT10-MS3-phospho.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt10-ms3-phospho","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "localize", "tool": "ptm-localize"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "localize"},
  {"src": "localize", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt10-open`
- **用途**:迁移自官方模板 'TMT10-Open.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt10-open","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "cleanup", "tool": "precursor-refine"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "ptm_summary", "tool": "ptm-profile"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "cleanup"},
  {"src": "database", "dst": "cleanup"},
  {"src": "convert", "dst": "cleanup"},
  {"src": "cleanup", "dst": "validate"},
  {"src": "database", "dst": "validate"},
  {"src": "validate", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "ptm_summary"},
  {"src": "convert", "dst": "ptm_summary"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt10-phospho`
- **用途**:迁移自官方模板 'TMT10-phospho.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt10-phospho","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "localize", "tool": "ptm-localize"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "localize"},
  {"src": "localize", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt10-phospho-bridge`
- **用途**:迁移自官方模板 'TMT10-phospho-bridge.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt10-phospho-bridge","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "localize", "tool": "ptm-localize"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "localize"},
  {"src": "localize", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt10-ubiquitin`
- **用途**:迁移自官方模板 'TMT10-ubiquitin.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt10-ubiquitin","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt10-ubiquitination-k-tmt-or-ubiq`
- **用途**:迁移自官方模板 'TMT10-ubiquitination-K_tmt_or_ubiq.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt10-ubiquitination-k-tmt-or-ubiq","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "localize", "tool": "ptm-localize"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "localize"},
  {"src": "localize", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt10-ubiquitination-k-tmt-plus-ubiq`
- **用途**:迁移自官方模板 'TMT10-ubiquitination-K_tmt_plus_ubiq.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt10-ubiquitination-k-tmt-plus-ubiq","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "localize", "tool": "ptm-localize"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "localize"},
  {"src": "localize", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt16`
- **用途**:迁移自官方模板 'TMT16.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt16","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt16-acetyl`
- **用途**:迁移自官方模板 'TMT16-acetyl.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt16-acetyl","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "localize", "tool": "ptm-localize"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "localize"},
  {"src": "localize", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt16-acetyl-noloc`
- **用途**:迁移自官方模板 'TMT16-acetyl-noloc.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt16-acetyl-noloc","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt16-ms3`
- **用途**:迁移自官方模板 'TMT16-MS3.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt16-ms3","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt16-phospho`
- **用途**:迁移自官方模板 'TMT16-phospho.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt16-phospho","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "localize", "tool": "ptm-localize"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "localize"},
  {"src": "localize", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt16-ubiquitination-k-tmt-or-ubiq`
- **用途**:迁移自官方模板 'TMT16-ubiquitination-K_tmt_or_ubiq.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt16-ubiquitination-k-tmt-or-ubiq","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "localize", "tool": "ptm-localize"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "localize"},
  {"src": "localize", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt16-ubiquitination-k-tmt-plus-ubiq`
- **用途**:迁移自官方模板 'TMT16-ubiquitination-K_tmt_plus_ubiq.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt16-ubiquitination-k-tmt-plus-ubiq","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "localize", "tool": "ptm-localize"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "localize"},
  {"src": "localize", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt18-astral`
- **用途**:迁移自官方模板 'TMT18-Astral.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt18-astral","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt18-phospho`
- **用途**:手工改自官方模板 'TMT16-phospho.workflow'(channel_num 16→18);官方没有现成的 TMT18-phospho 模板。 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt18-phospho","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "localize", "tool": "ptm-localize"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "localize"},
  {"src": "localize", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```

### `tmt35`
- **用途**:迁移自官方模板 'TMT35.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"tmt35","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "tmtquant", "tool": "quant-isobaric"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "tmtquant"}
]}
```


## 5. 糖肽(N-/O-glyco)

### `glyco-n-hcd`
- **用途**:迁移自官方模板 'glyco-N-HCD.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"glyco-n-hcd","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "validate"},
  {"src": "database", "dst": "validate"},
  {"src": "validate", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `glyco-n-hybrid`
- **用途**:迁移自官方模板 'glyco-N-Hybrid.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"glyco-n-hybrid","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "validate"},
  {"src": "database", "dst": "validate"},
  {"src": "validate", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `glyco-n-lfq`
- **用途**:迁移自官方模板 'glyco-N-LFQ.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"glyco-n-lfq","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "validate"},
  {"src": "database", "dst": "validate"},
  {"src": "validate", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `glyco-n-open-hcd`
- **用途**:迁移自官方模板 'glyco-N-open-HCD.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"glyco-n-open-hcd","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "cleanup", "tool": "precursor-refine"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "ptm_summary", "tool": "ptm-profile"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "cleanup"},
  {"src": "database", "dst": "cleanup"},
  {"src": "convert", "dst": "cleanup"},
  {"src": "cleanup", "dst": "validate"},
  {"src": "database", "dst": "validate"},
  {"src": "validate", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "ptm_summary"},
  {"src": "convert", "dst": "ptm_summary"}
]}
```

### `glyco-n-open-hybrid`
- **用途**:迁移自官方模板 'glyco-N-open-Hybrid.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"glyco-n-open-hybrid","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "cleanup", "tool": "precursor-refine"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "ptm_summary", "tool": "ptm-profile"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "cleanup"},
  {"src": "database", "dst": "cleanup"},
  {"src": "convert", "dst": "cleanup"},
  {"src": "cleanup", "dst": "validate"},
  {"src": "database", "dst": "validate"},
  {"src": "validate", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "ptm_summary"},
  {"src": "convert", "dst": "ptm_summary"}
]}
```

### `glyco-o-hcd`
- **用途**:迁移自官方模板 'glyco-O-HCD.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"glyco-o-hcd","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "validate"},
  {"src": "database", "dst": "validate"},
  {"src": "validate", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `glyco-o-hybrid`
- **用途**:迁移自官方模板 'glyco-O-Hybrid.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"glyco-o-hybrid","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "oglyc_localize", "tool": "glyco-localize"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "validate"},
  {"src": "database", "dst": "validate"},
  {"src": "validate", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "oglyc_localize"},
  {"src": "convert", "dst": "oglyc_localize"}
]}
```

### `glyco-o-open-hcd`
- **用途**:迁移自官方模板 'glyco-O-open-HCD.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"glyco-o-open-hcd","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "cleanup", "tool": "precursor-refine"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "ptm_summary", "tool": "ptm-profile"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "cleanup"},
  {"src": "database", "dst": "cleanup"},
  {"src": "convert", "dst": "cleanup"},
  {"src": "cleanup", "dst": "validate"},
  {"src": "database", "dst": "validate"},
  {"src": "validate", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "ptm_summary"},
  {"src": "convert", "dst": "ptm_summary"}
]}
```

### `glyco-o-open-hybrid`
- **用途**:迁移自官方模板 'glyco-O-open-Hybrid.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"glyco-o-open-hybrid","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "cleanup", "tool": "precursor-refine"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "ptm_summary", "tool": "ptm-profile"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "cleanup"},
  {"src": "database", "dst": "cleanup"},
  {"src": "convert", "dst": "cleanup"},
  {"src": "cleanup", "dst": "validate"},
  {"src": "database", "dst": "validate"},
  {"src": "validate", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "ptm_summary"},
  {"src": "convert", "dst": "ptm_summary"}
]}
```

### `glyco-o-pair`
- **用途**:迁移自官方模板 'glyco-O-Pair.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"glyco-o-pair","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"},
  {"step_id": "oglyc_localize", "tool": "glyco-localize"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "validate"},
  {"src": "database", "dst": "validate"},
  {"src": "validate", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"},
  {"src": "report", "dst": "oglyc_localize"},
  {"src": "convert", "dst": "oglyc_localize"}
]}
```

### `nonspecific-hla-glyco`
- **用途**:迁移自官方模板 'Nonspecific-HLA-glyco.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"nonspecific-hla-glyco","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "ptm_summary", "tool": "ptm-profile"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "validate"},
  {"src": "database", "dst": "validate"},
  {"src": "validate", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "ptm_summary"},
  {"src": "convert", "dst": "ptm_summary"}
]}
```


## 6. DIA / diaPASEF

### `chemprot-abpp-diatop`
- **用途**:迁移自官方模板 'chemprot-ABPP-diaTOP.workflow' (DIA path). 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 **DIA 搜索步骤必须有谱图库**:给 `dia_quant` 步的 `library_path` 传现成谱图库文件(.tsv/.speclib),或在流水线里加 `speclib-build` 上游步骤产出 library.tsv。**不支持只给 FASTA 的库无关(library-free)模式** —— 执行器在输入校验阶段硬性要求 `library_path` 非空,缺库直接报错。
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库;**`library_path`(必需)**=现成谱图库(.tsv/.speclib),经 `overrides` 传给 `dia_quant` 步
- **调用(推荐)**:`{"template_id":"chemprot-abpp-diatop","raw_files":["谱图"],"fasta_path":"蛋白库","overrides":{"dia_quant":{"library_path":"谱图库.tsv"}}}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "dia_quant", "tool": "dia-search"}
],"edges":[
  {"src": "convert", "dst": "dia_quant"}
]}
```

### `chemprot-abpp-iadtb-diapasef`
- **用途**:迁移自官方模板 'chemprot-ABPP-IADTB-diaPASEF.workflow' (DIA path). 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 **DIA 搜索步骤必须有谱图库**:给 `dia_quant` 步的 `library_path` 传现成谱图库文件(.tsv/.speclib),或在流水线里加 `speclib-build` 上游步骤产出 library.tsv。**不支持只给 FASTA 的库无关(library-free)模式** —— 执行器在输入校验阶段硬性要求 `library_path` 非空,缺库直接报错。
- **输入**:谱图 `raw_files`(.d(Bruker timsTOF));`fasta_path`=蛋白库;**`library_path`(必需)**=现成谱图库(.tsv/.speclib),经 `overrides` 传给 `dia_quant` 步
- **调用(推荐)**:`{"template_id":"chemprot-abpp-iadtb-diapasef","raw_files":["谱图"],"fasta_path":"蛋白库","overrides":{"dia_quant":{"library_path":"谱图库.tsv"}}}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "dia_quant", "tool": "dia-search"}
],"edges":[
  
]}
```

### `dia-pseudo-speclib-quant`
- **用途**:迁移自官方模板 'DIA_DIA-Umpire_SpecLib_Quant.workflow' (DIA path). 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 **DIA 搜索步骤必须有谱图库**:给 `dia_quant` 步的 `library_path` 传现成谱图库文件(.tsv/.speclib),或在流水线里加 `speclib-build` 上游步骤产出 library.tsv。**不支持只给 FASTA 的库无关(library-free)模式** —— 执行器在输入校验阶段硬性要求 `library_path` 非空,缺库直接报错。
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库;**`library_path`(必需)**=现成谱图库(.tsv/.speclib),经 `overrides` 传给 `dia_quant` 步
- **调用(推荐)**:`{"template_id":"dia-pseudo-speclib-quant","raw_files":["谱图"],"fasta_path":"蛋白库","overrides":{"dia_quant":{"library_path":"谱图库.tsv"}}}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "dia_quant", "tool": "dia-search"}
],"edges":[
  {"src": "convert", "dst": "dia_quant"}
]}
```

### `dia-speclib-quant`
- **用途**:迁移自官方模板 'DIA_SpecLib_Quant.workflow' (DIA path). 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 **DIA 搜索步骤必须有谱图库**:给 `dia_quant` 步的 `library_path` 传现成谱图库文件(.tsv/.speclib),或在流水线里加 `speclib-build` 上游步骤产出 library.tsv。**不支持只给 FASTA 的库无关(library-free)模式** —— 执行器在输入校验阶段硬性要求 `library_path` 非空,缺库直接报错。
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库;**`library_path`(必需)**=现成谱图库(.tsv/.speclib),经 `overrides` 传给 `dia_quant` 步
- **调用(推荐)**:`{"template_id":"dia-speclib-quant","raw_files":["谱图"],"fasta_path":"蛋白库","overrides":{"dia_quant":{"library_path":"谱图库.tsv"}}}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "dia_quant", "tool": "dia-search"}
],"edges":[
  {"src": "convert", "dst": "dia_quant"}
]}
```

### `dia-speclib-quant-diapasef`
- **用途**:迁移自官方模板 'DIA_SpecLib_Quant_diaPASEF.workflow' (DIA path). 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 **DIA 搜索步骤必须有谱图库**:给 `dia_quant` 步的 `library_path` 传现成谱图库文件(.tsv/.speclib),或在流水线里加 `speclib-build` 上游步骤产出 library.tsv。**不支持只给 FASTA 的库无关(library-free)模式** —— 执行器在输入校验阶段硬性要求 `library_path` 非空,缺库直接报错。
- **输入**:谱图 `raw_files`(.d(Bruker timsTOF));`fasta_path`=蛋白库;**`library_path`(必需)**=现成谱图库(.tsv/.speclib),经 `overrides` 传给 `dia_quant` 步
- **调用(推荐)**:`{"template_id":"dia-speclib-quant-diapasef","raw_files":["谱图"],"fasta_path":"蛋白库","overrides":{"dia_quant":{"library_path":"谱图库.tsv"}}}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "dia_quant", "tool": "dia-search"}
],"edges":[
  
]}
```

### `dia-speclib-quant-phospho`
- **用途**:迁移自官方模板 'DIA_SpecLib_Quant_Phospho.workflow' (DIA path). 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 **DIA 搜索步骤必须有谱图库**:给 `dia_quant` 步的 `library_path` 传现成谱图库文件(.tsv/.speclib),或在流水线里加 `speclib-build` 上游步骤产出 library.tsv。**不支持只给 FASTA 的库无关(library-free)模式** —— 执行器在输入校验阶段硬性要求 `library_path` 非空,缺库直接报错。
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库;**`library_path`(必需)**=现成谱图库(.tsv/.speclib),经 `overrides` 传给 `dia_quant` 步
- **调用(推荐)**:`{"template_id":"dia-speclib-quant-phospho","raw_files":["谱图"],"fasta_path":"蛋白库","overrides":{"dia_quant":{"library_path":"谱图库.tsv"}}}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "dia_quant", "tool": "dia-search"}
],"edges":[
  {"src": "convert", "dst": "dia_quant"}
]}
```

### `dia-speclib-quant-phospho-diapasef`
- **用途**:迁移自官方模板 'DIA_SpecLib_Quant_Phospho_diaPASEF.workflow' (DIA path). 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 **DIA 搜索步骤必须有谱图库**:给 `dia_quant` 步的 `library_path` 传现成谱图库文件(.tsv/.speclib),或在流水线里加 `speclib-build` 上游步骤产出 library.tsv。**不支持只给 FASTA 的库无关(library-free)模式** —— 执行器在输入校验阶段硬性要求 `library_path` 非空,缺库直接报错。
- **输入**:谱图 `raw_files`(.d(Bruker timsTOF));`fasta_path`=蛋白库;**`library_path`(必需)**=现成谱图库(.tsv/.speclib),经 `overrides` 传给 `dia_quant` 步
- **调用(推荐)**:`{"template_id":"dia-speclib-quant-phospho-diapasef","raw_files":["谱图"],"fasta_path":"蛋白库","overrides":{"dia_quant":{"library_path":"谱图库.tsv"}}}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "dia_quant", "tool": "dia-search"}
],"edges":[
  
]}
```

### `dia-speclib-quant-ubiq`
- **用途**:迁移自官方模板 'DIA_SpecLib_Quant_Ubiq.workflow' (DIA path). 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 **DIA 搜索步骤必须有谱图库**:给 `dia_quant` 步的 `library_path` 传现成谱图库文件(.tsv/.speclib),或在流水线里加 `speclib-build` 上游步骤产出 library.tsv。**不支持只给 FASTA 的库无关(library-free)模式** —— 执行器在输入校验阶段硬性要求 `library_path` 非空,缺库直接报错。
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库;**`library_path`(必需)**=现成谱图库(.tsv/.speclib),经 `overrides` 传给 `dia_quant` 步
- **调用(推荐)**:`{"template_id":"dia-speclib-quant-ubiq","raw_files":["谱图"],"fasta_path":"蛋白库","overrides":{"dia_quant":{"library_path":"谱图库.tsv"}}}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "dia_quant", "tool": "dia-search"}
],"edges":[
  {"src": "convert", "dst": "dia_quant"}
]}
```

### `diagnostic-ion-mining`
- **用途**:迁移自官方模板 'Diagnostic-ion-mining.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"diagnostic-ion-mining","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "cleanup", "tool": "precursor-refine"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "ptm_summary", "tool": "ptm-profile"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "cleanup"},
  {"src": "database", "dst": "cleanup"},
  {"src": "convert", "dst": "cleanup"},
  {"src": "cleanup", "dst": "validate"},
  {"src": "database", "dst": "validate"},
  {"src": "validate", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "ptm_summary"},
  {"src": "convert", "dst": "ptm_summary"}
]}
```

### `glyco-n-dia`
- **用途**:迁移自官方模板 'glyco-N-DIA.workflow' (DIA path). 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 **DIA 搜索步骤必须有谱图库**:给 `dia_quant` 步的 `library_path` 传现成谱图库文件(.tsv/.speclib),或在流水线里加 `speclib-build` 上游步骤产出 library.tsv。**不支持只给 FASTA 的库无关(library-free)模式** —— 执行器在输入校验阶段硬性要求 `library_path` 非空,缺库直接报错。
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库;**`library_path`(必需)**=现成谱图库(.tsv/.speclib),经 `overrides` 传给 `dia_quant` 步
- **调用(推荐)**:`{"template_id":"glyco-n-dia","raw_files":["谱图"],"fasta_path":"蛋白库","overrides":{"dia_quant":{"library_path":"谱图库.tsv"}}}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "dia_quant", "tool": "dia-search"}
],"edges":[
  {"src": "convert", "dst": "dia_quant"}
]}
```

### `glyco-o-dia-hcd`
- **用途**:迁移自官方模板 'glyco-O-DIA-HCD.workflow' (DIA path). 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 **DIA 搜索步骤必须有谱图库**:给 `dia_quant` 步的 `library_path` 传现成谱图库文件(.tsv/.speclib),或在流水线里加 `speclib-build` 上游步骤产出 library.tsv。**不支持只给 FASTA 的库无关(library-free)模式** —— 执行器在输入校验阶段硬性要求 `library_path` 非空,缺库直接报错。
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库;**`library_path`(必需)**=现成谱图库(.tsv/.speclib),经 `overrides` 传给 `dia_quant` 步
- **调用(推荐)**:`{"template_id":"glyco-o-dia-hcd","raw_files":["谱图"],"fasta_path":"蛋白库","overrides":{"dia_quant":{"library_path":"谱图库.tsv"}}}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "dia_quant", "tool": "dia-search"}
],"edges":[
  {"src": "convert", "dst": "dia_quant"}
]}
```

### `glyco-o-dia-localize`
- **用途**:O-糖 DIA 混合流程(DDA 建库 + DIA 定量 + O-糖位点定位)。DDA 链(search-closed → validate-psm → report)经 `speclib-build` 产出谱图库,`dia-search` 再用该库以 DIA 模式定量同一批 mzML;`glyco-localize` 在 DDA psm.tsv 上做 O-糖位点定位。
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"glyco-o-dia-localize","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "build_library", "tool": "speclib-build"},
  {"step_id": "dia_quant", "tool": "dia-search"},
  {"step_id": "oglyc_localize", "tool": "glyco-localize"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "validate"},
  {"src": "database", "dst": "validate"},
  {"src": "validate", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "validate", "dst": "build_library"},
  {"src": "convert", "dst": "build_library"},
  {"src": "report", "dst": "build_library"},
  {"src": "build_library", "dst": "dia_quant"},
  {"src": "convert", "dst": "dia_quant"},
  {"src": "report", "dst": "oglyc_localize"},
  {"src": "convert", "dst": "oglyc_localize"}
]}
```

### `nonspecific-hla-dia`
- **用途**:迁移自官方模板 'Nonspecific-HLA-DIA.workflow' (DIA path). 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 **DIA 搜索步骤必须有谱图库**:给 `dia_quant` 步的 `library_path` 传现成谱图库文件(.tsv/.speclib),或在流水线里加 `speclib-build` 上游步骤产出 library.tsv。**不支持只给 FASTA 的库无关(library-free)模式** —— 执行器在输入校验阶段硬性要求 `library_path` 非空,缺库直接报错。
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库;**`library_path`(必需)**=现成谱图库(.tsv/.speclib),经 `overrides` 传给 `dia_quant` 步
- **调用(推荐)**:`{"template_id":"nonspecific-hla-dia","raw_files":["谱图"],"fasta_path":"蛋白库","overrides":{"dia_quant":{"library_path":"谱图库.tsv"}}}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "dia_quant", "tool": "dia-search"}
],"edges":[
  {"src": "convert", "dst": "dia_quant"}
]}
```

### `nonspecific-hla-dia-astral`
- **用途**:迁移自官方模板 'Nonspecific-HLA-DIA-Astral.workflow' (DIA path). 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 **DIA 搜索步骤必须有谱图库**:给 `dia_quant` 步的 `library_path` 传现成谱图库文件(.tsv/.speclib),或在流水线里加 `speclib-build` 上游步骤产出 library.tsv。**不支持只给 FASTA 的库无关(library-free)模式** —— 执行器在输入校验阶段硬性要求 `library_path` 非空,缺库直接报错。
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库;**`library_path`(必需)**=现成谱图库(.tsv/.speclib),经 `overrides` 传给 `dia_quant` 步
- **调用(推荐)**:`{"template_id":"nonspecific-hla-dia-astral","raw_files":["谱图"],"fasta_path":"蛋白库","overrides":{"dia_quant":{"library_path":"谱图库.tsv"}}}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "dia_quant", "tool": "dia-search"}
],"edges":[
  {"src": "convert", "dst": "dia_quant"}
]}
```

### `nonspecific-hla-diapasef`
- **用途**:迁移自官方模板 'Nonspecific-HLA-diaPASEF.workflow' (DIA path). 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 **DIA 搜索步骤必须有谱图库**:给 `dia_quant` 步的 `library_path` 传现成谱图库文件(.tsv/.speclib),或在流水线里加 `speclib-build` 上游步骤产出 library.tsv。**不支持只给 FASTA 的库无关(library-free)模式** —— 执行器在输入校验阶段硬性要求 `library_path` 非空,缺库直接报错。
- **输入**:谱图 `raw_files`(.d(Bruker timsTOF));`fasta_path`=蛋白库;**`library_path`(必需)**=现成谱图库(.tsv/.speclib),经 `overrides` 传给 `dia_quant` 步
- **调用(推荐)**:`{"template_id":"nonspecific-hla-diapasef","raw_files":["谱图"],"fasta_path":"蛋白库","overrides":{"dia_quant":{"library_path":"谱图库.tsv"}}}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "dia_quant", "tool": "dia-search"}
],"edges":[
  
]}
```

### `stellar-gpfdia`
- **用途**:迁移自官方模板 'Stellar-GPFDIA.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"stellar-gpfdia","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```


## 7. PTM(磷酸化/泛素化/乙酰化/labile)

### `labile-adp-ribosylation`
- **用途**:迁移自官方模板 'Labile_ADP-ribosylation.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"labile-adp-ribosylation","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "localize", "tool": "ptm-localize"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "validate"},
  {"src": "database", "dst": "validate"},
  {"src": "validate", "dst": "localize"},
  {"src": "convert", "dst": "localize"},
  {"src": "localize", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `labile-phospho`
- **用途**:迁移自官方模板 'Labile_phospho.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"labile-phospho","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "localize", "tool": "ptm-localize"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "validate"},
  {"src": "database", "dst": "validate"},
  {"src": "validate", "dst": "localize"},
  {"src": "convert", "dst": "localize"},
  {"src": "localize", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `lfq-phospho`
- **用途**:迁移自官方模板 'LFQ-phospho.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"lfq-phospho","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "localize", "tool": "ptm-localize"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "localize"},
  {"src": "localize", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `lfq-ubiquitin`
- **用途**:迁移自官方模板 'LFQ-ubiquitin.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"lfq-ubiquitin","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "localize", "tool": "ptm-localize"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "localize"},
  {"src": "localize", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `nonspecific-hla-phospho`
- **用途**:迁移自官方模板 'Nonspecific-HLA-phospho.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"nonspecific-hla-phospho","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "localize", "tool": "ptm-localize"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "localize"},
  {"src": "localize", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `silac3-phospho`
- **用途**:迁移自官方模板 'SILAC3-phospho.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"silac3-phospho","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```


## 8. 非特异酶切 / HLA 免疫肽

### `nonspecific-hla`
- **用途**:迁移自官方模板 'Nonspecific-HLA.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"nonspecific-hla","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `nonspecific-hla-c57`
- **用途**:迁移自官方模板 'Nonspecific-HLA-C57.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"nonspecific-hla-c57","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `nonspecific-hla-customdb-groupfdr`
- **用途**:迁移自官方模板 'Nonspecific-HLA-customDB-groupFDR.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"nonspecific-hla-customdb-groupfdr","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `nonspecific-peptidome`
- **用途**:迁移自官方模板 'Nonspecific-peptidome.workflow'. 原模板另启用了若干非关键附加层(已省略,不影响下游 FDR)。 Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"nonspecific-peptidome","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "rescore", "tool": "rescore"},
  {"step_id": "to_pepxml", "tool": "rescore-export"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "quant", "tool": "quant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"},
  {"src": "search", "dst": "to_pepxml"},
  {"src": "rescore", "dst": "to_pepxml"},
  {"src": "convert", "dst": "to_pepxml"},
  {"src": "to_pepxml", "dst": "report"},
  {"src": "database", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

