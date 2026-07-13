# 官方工作流模板目录(template_id)

共 81 个官方 FragPipe 模板。**优先用 `template_id` 跑**(一行调用,执行器自动展开);
**确无对应模板才手写显式 DAG**。

> 每个模板下方「DAG」用 `steps`+`edges` 表示,**和你手写 pipeline.json 完全同格式**(`edges` 用 `src`/`dst`)——
> `edges` 列表本身就是 DAG(含多父/菱形),需要变体时可直接复制改造。
> 参数一律用模板默认(要调某参数走 `overrides`,参数名见 `parameters.md`)。


## 1. 基础(closed / basic)

### `bottomup-closed`
- **用途**:msconvert → MSFragger (closed) → Percolator. Requires user-supplied target+decoy FASTA on the MSFragger step.
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
- **用途**:迁移自官方模板 'Basic-Search.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:msconvert → MSFragger → Philosopher → IonQuant. Diamond DAG: IonQuant merges mzML (from msconvert) with psm.tsv (from Philosopher).
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
- **用途**:迁移自官方模板 'chemprot-ABPP-ipIAA.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'chemprot-ABPP-isoDTB.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'chemprot-ABPP-isoTOP.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'chemprot-PAL.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'citrullination.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'FPOP.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'LFQ-MBR.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'SILAC3.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'Stellar-DDA.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'WWA.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'Mass-Offset-CommonPTMs.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'Open.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'Open-quickscan.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'XRNAX-MassOffset.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'chemprot-ABPP-IADTB-TMT16.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'glyco-N-TMT.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'iTRAQ4.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'iTRAQ4-phospho.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'Nonspecific-HLA-TMT10.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'TMT10.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'TMT10-acetyl.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'TMT10-acetyl-noloc.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'TMT10-bridge.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'TMT10-MS3.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'TMT10-MS3-phospho.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'TMT10-Open.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'TMT10-phospho.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'TMT10-phospho-bridge.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'TMT10-ubiquitin.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'TMT10-ubiquitination-K_tmt_or_ubiq.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'TMT10-ubiquitination-K_tmt_plus_ubiq.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'TMT16.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'TMT16-acetyl.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'TMT16-acetyl-noloc.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'TMT16-MS3.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'TMT16-phospho.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'TMT16-ubiquitination-K_tmt_or_ubiq.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'TMT16-ubiquitination-K_tmt_plus_ubiq.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'TMT18-Astral.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:Custom TMTpro-18 phospho workflow derived by hand from FragPipe 'TMT16-phospho.workflow' (channel_num bumped 16→18); FragPipe ships no official TMT18-phospho. Original TMT16 workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'TMT35.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'glyco-N-HCD.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'glyco-N-Hybrid.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'glyco-N-LFQ.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'glyco-N-open-HCD.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'glyco-N-open-Hybrid.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'glyco-O-HCD.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'glyco-O-Hybrid.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'glyco-O-open-HCD.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'glyco-O-open-Hybrid.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'glyco-O-Pair.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'Nonspecific-HLA-glyco.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'chemprot-ABPP-diaTOP.workflow' (DIA path). Original workflow also enabled: ['msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"chemprot-abpp-diatop","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "diann_quant", "tool": "dia-search"}
],"edges":[
  {"src": "convert", "dst": "diann_quant"}
]}
```

### `chemprot-abpp-iadtb-diapasef`
- **用途**:迁移自官方模板 'chemprot-ABPP-IADTB-diaPASEF.workflow' (DIA path). Original workflow also enabled: ['msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(.d(Bruker timsTOF));`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"chemprot-abpp-iadtb-diapasef","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "diann_quant", "tool": "dia-search"}
],"edges":[
  
]}
```

### `dia-dia-umpire-speclib-quant`
- **用途**:迁移自官方模板 'DIA_DIA-Umpire_SpecLib_Quant.workflow' (DIA path). Original workflow also enabled: ['diaumpire', 'msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"dia-dia-umpire-speclib-quant","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "diann_quant", "tool": "dia-search"}
],"edges":[
  {"src": "convert", "dst": "diann_quant"}
]}
```

### `dia-speclib-quant`
- **用途**:迁移自官方模板 'DIA_SpecLib_Quant.workflow' (DIA path). Original workflow also enabled: ['msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"dia-speclib-quant","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "diann_quant", "tool": "dia-search"}
],"edges":[
  {"src": "convert", "dst": "diann_quant"}
]}
```

### `dia-speclib-quant-diapasef`
- **用途**:迁移自官方模板 'DIA_SpecLib_Quant_diaPASEF.workflow' (DIA path). Original workflow also enabled: ['msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(.d(Bruker timsTOF));`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"dia-speclib-quant-diapasef","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "diann_quant", "tool": "dia-search"}
],"edges":[
  
]}
```

### `dia-speclib-quant-phospho`
- **用途**:迁移自官方模板 'DIA_SpecLib_Quant_Phospho.workflow' (DIA path). Original workflow also enabled: ['msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"dia-speclib-quant-phospho","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "diann_quant", "tool": "dia-search"}
],"edges":[
  {"src": "convert", "dst": "diann_quant"}
]}
```

### `dia-speclib-quant-phospho-diapasef`
- **用途**:迁移自官方模板 'DIA_SpecLib_Quant_Phospho_diaPASEF.workflow' (DIA path). Original workflow also enabled: ['msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(.d(Bruker timsTOF));`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"dia-speclib-quant-phospho-diapasef","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "diann_quant", "tool": "dia-search"}
],"edges":[
  
]}
```

### `dia-speclib-quant-ubiq`
- **用途**:迁移自官方模板 'DIA_SpecLib_Quant_Ubiq.workflow' (DIA path). Original workflow also enabled: ['msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"dia-speclib-quant-ubiq","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "diann_quant", "tool": "dia-search"}
],"edges":[
  {"src": "convert", "dst": "diann_quant"}
]}
```

### `diagnostic-ion-mining`
- **用途**:迁移自官方模板 'Diagnostic-ion-mining.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'glyco-N-DIA.workflow' (DIA path). Original workflow also enabled: ['skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"glyco-n-dia","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "diann_quant", "tool": "dia-search"}
],"edges":[
  {"src": "convert", "dst": "diann_quant"}
]}
```

### `glyco-o-dia-hcd`
- **用途**:迁移自官方模板 'glyco-O-DIA-HCD.workflow' (DIA path). Original workflow also enabled: ['skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"glyco-o-dia-hcd","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "diann_quant", "tool": "dia-search"}
],"edges":[
  {"src": "convert", "dst": "diann_quant"}
]}
```

### `glyco-o-dia-opair`
- **用途**:迁移自官方模板 'glyco-O-DIA-OPair.workflow' (hybrid DDA-library + DIA-quant + OPair O-glycan localization). The DDA chain (msfragger → peptideprophet → report) builds a spectral library via easypqp, which DIA-NN then uses to quantify the same mzMLs in DIA mode. OPair localizes O-glycans on the DDA psm.tsv.
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"glyco-o-dia-opair","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "database"},
  {"step_id": "search", "tool": "search-closed"},
  {"step_id": "validate", "tool": "validate-psm"},
  {"step_id": "report", "tool": "report"},
  {"step_id": "build_library", "tool": "speclib-build"},
  {"step_id": "diann_quant", "tool": "dia-search"},
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
  {"src": "build_library", "dst": "diann_quant"},
  {"src": "convert", "dst": "diann_quant"},
  {"src": "report", "dst": "oglyc_localize"},
  {"src": "convert", "dst": "oglyc_localize"}
]}
```

### `nonspecific-hla-dia`
- **用途**:迁移自官方模板 'Nonspecific-HLA-DIA.workflow' (DIA path). Original workflow also enabled: ['diaumpire', 'msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"nonspecific-hla-dia","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "diann_quant", "tool": "dia-search"}
],"edges":[
  {"src": "convert", "dst": "diann_quant"}
]}
```

### `nonspecific-hla-dia-astral`
- **用途**:迁移自官方模板 'Nonspecific-HLA-DIA-Astral.workflow' (DIA path). Original workflow also enabled: ['msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"nonspecific-hla-dia-astral","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "diann_quant", "tool": "dia-search"}
],"edges":[
  {"src": "convert", "dst": "diann_quant"}
]}
```

### `nonspecific-hla-diapasef`
- **用途**:迁移自官方模板 'Nonspecific-HLA-diaPASEF.workflow' (DIA path). Original workflow also enabled: ['msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(.d(Bruker timsTOF));`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"nonspecific-hla-diapasef","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "diann_quant", "tool": "dia-search"}
],"edges":[
  
]}
```

### `stellar-gpfdia`
- **用途**:迁移自官方模板 'Stellar-GPFDIA.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'Labile_ADP-ribosylation.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'Labile_phospho.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'LFQ-phospho.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'LFQ-ubiquitin.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'Nonspecific-HLA-phospho.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'SILAC3-phospho.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'Nonspecific-HLA.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'Nonspecific-HLA-C57.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'Nonspecific-HLA-customDB-groupFDR.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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
- **用途**:迁移自官方模板 'Nonspecific-peptidome.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
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

