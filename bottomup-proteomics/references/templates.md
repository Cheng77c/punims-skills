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
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "rescore"}
]}
```

### `fp-basic-search`
- **用途**:Migrated from FragPipe 'Basic-Search.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-basic-search","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
],"edges":[
  {"src": "convert", "dst": "search"},
  {"src": "search", "dst": "report"},
  {"src": "report", "dst": "quant"},
  {"src": "convert", "dst": "quant"}
]}
```

### `fp-chemprot-abpp-ipiaa`
- **用途**:Migrated from FragPipe 'chemprot-ABPP-ipIAA.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-chemprot-abpp-ipiaa","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-chemprot-abpp-isodtb`
- **用途**:Migrated from FragPipe 'chemprot-ABPP-isoDTB.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-chemprot-abpp-isodtb","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-chemprot-abpp-isotop`
- **用途**:Migrated from FragPipe 'chemprot-ABPP-isoTOP.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-chemprot-abpp-isotop","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-chemprot-pal`
- **用途**:Migrated from FragPipe 'chemprot-PAL.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-chemprot-pal","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "ptm_summary", "tool": "ptmshepherd"}
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

### `fp-citrullination`
- **用途**:Migrated from FragPipe 'citrullination.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-citrullination","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-fpop`
- **用途**:Migrated from FragPipe 'FPOP.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-fpop","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "validate", "tool": "peptideprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-lfq-mbr`
- **用途**:Migrated from FragPipe 'LFQ-MBR.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-lfq-mbr","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-silac3`
- **用途**:Migrated from FragPipe 'SILAC3.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-silac3","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-stellar-dda`
- **用途**:Migrated from FragPipe 'Stellar-DDA.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-stellar-dda","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-wwa`
- **用途**:Migrated from FragPipe 'WWA.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-wwa","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-mass-offset-commonptms`
- **用途**:Migrated from FragPipe 'Mass-Offset-CommonPTMs.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-mass-offset-commonptms","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "ptm_summary", "tool": "ptmshepherd"}
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

### `fp-open`
- **用途**:Migrated from FragPipe 'Open.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-open","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "cleanup", "tool": "crystalc"},
  {"step_id": "validate", "tool": "peptideprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "ptm_summary", "tool": "ptmshepherd"}
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

### `fp-open-quickscan`
- **用途**:Migrated from FragPipe 'Open-quickscan.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-open-quickscan","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "cleanup", "tool": "crystalc"},
  {"step_id": "validate", "tool": "peptideprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "ptm_summary", "tool": "ptmshepherd"}
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

### `fp-xrnax-massoffset`
- **用途**:Migrated from FragPipe 'XRNAX-MassOffset.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-xrnax-massoffset","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "cleanup", "tool": "crystalc"},
  {"step_id": "validate", "tool": "peptideprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "ptm_summary", "tool": "ptmshepherd"}
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

### `fp-chemprot-abpp-iadtb-tmt16`
- **用途**:Migrated from FragPipe 'chemprot-ABPP-IADTB-TMT16.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-chemprot-abpp-iadtb-tmt16","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-glyco-n-tmt`
- **用途**:Migrated from FragPipe 'glyco-N-TMT.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-glyco-n-tmt","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "validate", "tool": "peptideprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "ptm_summary", "tool": "ptmshepherd"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-itraq4`
- **用途**:Migrated from FragPipe 'iTRAQ4.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-itraq4","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-itraq4-phospho`
- **用途**:Migrated from FragPipe 'iTRAQ4-phospho.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-itraq4-phospho","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "localize", "tool": "ptmprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-nonspecific-hla-tmt10`
- **用途**:Migrated from FragPipe 'Nonspecific-HLA-TMT10.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-nonspecific-hla-tmt10","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt10`
- **用途**:Migrated from FragPipe 'TMT10.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt10","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt10-acetyl`
- **用途**:Migrated from FragPipe 'TMT10-acetyl.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt10-acetyl","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "localize", "tool": "ptmprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt10-acetyl-noloc`
- **用途**:Migrated from FragPipe 'TMT10-acetyl-noloc.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt10-acetyl-noloc","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt10-bridge`
- **用途**:Migrated from FragPipe 'TMT10-bridge.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt10-bridge","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt10-ms3`
- **用途**:Migrated from FragPipe 'TMT10-MS3.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt10-ms3","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt10-ms3-phospho`
- **用途**:Migrated from FragPipe 'TMT10-MS3-phospho.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt10-ms3-phospho","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "localize", "tool": "ptmprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt10-open`
- **用途**:Migrated from FragPipe 'TMT10-Open.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt10-open","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "cleanup", "tool": "crystalc"},
  {"step_id": "validate", "tool": "peptideprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "ptm_summary", "tool": "ptmshepherd"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt10-phospho`
- **用途**:Migrated from FragPipe 'TMT10-phospho.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt10-phospho","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "localize", "tool": "ptmprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt10-phospho-bridge`
- **用途**:Migrated from FragPipe 'TMT10-phospho-bridge.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt10-phospho-bridge","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "localize", "tool": "ptmprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt10-ubiquitin`
- **用途**:Migrated from FragPipe 'TMT10-ubiquitin.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt10-ubiquitin","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt10-ubiquitination-k-tmt-or-ubiq`
- **用途**:Migrated from FragPipe 'TMT10-ubiquitination-K_tmt_or_ubiq.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt10-ubiquitination-k-tmt-or-ubiq","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "localize", "tool": "ptmprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt10-ubiquitination-k-tmt-plus-ubiq`
- **用途**:Migrated from FragPipe 'TMT10-ubiquitination-K_tmt_plus_ubiq.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt10-ubiquitination-k-tmt-plus-ubiq","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "localize", "tool": "ptmprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt16`
- **用途**:Migrated from FragPipe 'TMT16.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt16","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt16-acetyl`
- **用途**:Migrated from FragPipe 'TMT16-acetyl.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt16-acetyl","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "localize", "tool": "ptmprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt16-acetyl-noloc`
- **用途**:Migrated from FragPipe 'TMT16-acetyl-noloc.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt16-acetyl-noloc","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt16-ms3`
- **用途**:Migrated from FragPipe 'TMT16-MS3.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt16-ms3","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt16-phospho`
- **用途**:Migrated from FragPipe 'TMT16-phospho.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt16-phospho","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "localize", "tool": "ptmprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt16-ubiquitination-k-tmt-or-ubiq`
- **用途**:Migrated from FragPipe 'TMT16-ubiquitination-K_tmt_or_ubiq.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt16-ubiquitination-k-tmt-or-ubiq","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "localize", "tool": "ptmprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt16-ubiquitination-k-tmt-plus-ubiq`
- **用途**:Migrated from FragPipe 'TMT16-ubiquitination-K_tmt_plus_ubiq.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt16-ubiquitination-k-tmt-plus-ubiq","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "localize", "tool": "ptmprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt18-astral`
- **用途**:Migrated from FragPipe 'TMT18-Astral.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt18-astral","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt18-phospho`
- **用途**:Custom TMTpro-18 phospho workflow derived by hand from FragPipe 'TMT16-phospho.workflow' (channel_num bumped 16→18); FragPipe ships no official TMT18-phospho. Original TMT16 workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt18-phospho","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "localize", "tool": "ptmprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-tmt35`
- **用途**:Migrated from FragPipe 'TMT35.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)；**`annotation_path`**=通道→样本标注(TMT/iTRAQ 必需)
- **调用(推荐)**:`{"template_id":"fp-tmt35","raw_files":["谱图"],"fasta_path":"蛋白库","annotation_path":"annotation.txt"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "tmtquant", "tool": "tmtintegrator"}
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

### `fp-glyco-n-hcd`
- **用途**:Migrated from FragPipe 'glyco-N-HCD.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-glyco-n-hcd","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "validate", "tool": "peptideprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-glyco-n-hybrid`
- **用途**:Migrated from FragPipe 'glyco-N-Hybrid.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-glyco-n-hybrid","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "validate", "tool": "peptideprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-glyco-n-lfq`
- **用途**:Migrated from FragPipe 'glyco-N-LFQ.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-glyco-n-lfq","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "validate", "tool": "peptideprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-glyco-n-open-hcd`
- **用途**:Migrated from FragPipe 'glyco-N-open-HCD.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-glyco-n-open-hcd","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "cleanup", "tool": "crystalc"},
  {"step_id": "validate", "tool": "peptideprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "ptm_summary", "tool": "ptmshepherd"}
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

### `fp-glyco-n-open-hybrid`
- **用途**:Migrated from FragPipe 'glyco-N-open-Hybrid.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-glyco-n-open-hybrid","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "cleanup", "tool": "crystalc"},
  {"step_id": "validate", "tool": "peptideprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "ptm_summary", "tool": "ptmshepherd"}
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

### `fp-glyco-o-hcd`
- **用途**:Migrated from FragPipe 'glyco-O-HCD.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-glyco-o-hcd","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "validate", "tool": "peptideprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-glyco-o-hybrid`
- **用途**:Migrated from FragPipe 'glyco-O-Hybrid.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-glyco-o-hybrid","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "validate", "tool": "peptideprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "oglyc_localize", "tool": "opair"}
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

### `fp-glyco-o-open-hcd`
- **用途**:Migrated from FragPipe 'glyco-O-open-HCD.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-glyco-o-open-hcd","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "cleanup", "tool": "crystalc"},
  {"step_id": "validate", "tool": "peptideprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "ptm_summary", "tool": "ptmshepherd"}
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

### `fp-glyco-o-open-hybrid`
- **用途**:Migrated from FragPipe 'glyco-O-open-Hybrid.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-glyco-o-open-hybrid","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "cleanup", "tool": "crystalc"},
  {"step_id": "validate", "tool": "peptideprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "ptm_summary", "tool": "ptmshepherd"}
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

### `fp-glyco-o-pair`
- **用途**:Migrated from FragPipe 'glyco-O-Pair.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-glyco-o-pair","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "validate", "tool": "peptideprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"},
  {"step_id": "oglyc_localize", "tool": "opair"}
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

### `fp-nonspecific-hla-glyco`
- **用途**:Migrated from FragPipe 'Nonspecific-HLA-glyco.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-nonspecific-hla-glyco","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "validate", "tool": "peptideprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "ptm_summary", "tool": "ptmshepherd"}
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

### `fp-chemprot-abpp-diatop`
- **用途**:Migrated from FragPipe 'chemprot-ABPP-diaTOP.workflow' (DIA path). Original workflow also enabled: ['msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"fp-chemprot-abpp-diatop","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "diann_quant", "tool": "diann"}
],"edges":[
  {"src": "convert", "dst": "diann_quant"}
]}
```

### `fp-chemprot-abpp-iadtb-diapasef`
- **用途**:Migrated from FragPipe 'chemprot-ABPP-IADTB-diaPASEF.workflow' (DIA path). Original workflow also enabled: ['msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(.d(Bruker timsTOF));`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"fp-chemprot-abpp-iadtb-diapasef","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "diann_quant", "tool": "diann"}
],"edges":[
  
]}
```

### `fp-dia-dia-umpire-speclib-quant`
- **用途**:Migrated from FragPipe 'DIA_DIA-Umpire_SpecLib_Quant.workflow' (DIA path). Original workflow also enabled: ['diaumpire', 'msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"fp-dia-dia-umpire-speclib-quant","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "diann_quant", "tool": "diann"}
],"edges":[
  {"src": "convert", "dst": "diann_quant"}
]}
```

### `fp-dia-speclib-quant`
- **用途**:Migrated from FragPipe 'DIA_SpecLib_Quant.workflow' (DIA path). Original workflow also enabled: ['msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"fp-dia-speclib-quant","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "diann_quant", "tool": "diann"}
],"edges":[
  {"src": "convert", "dst": "diann_quant"}
]}
```

### `fp-dia-speclib-quant-diapasef`
- **用途**:Migrated from FragPipe 'DIA_SpecLib_Quant_diaPASEF.workflow' (DIA path). Original workflow also enabled: ['msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(.d(Bruker timsTOF));`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"fp-dia-speclib-quant-diapasef","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "diann_quant", "tool": "diann"}
],"edges":[
  
]}
```

### `fp-dia-speclib-quant-phospho`
- **用途**:Migrated from FragPipe 'DIA_SpecLib_Quant_Phospho.workflow' (DIA path). Original workflow also enabled: ['msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"fp-dia-speclib-quant-phospho","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "diann_quant", "tool": "diann"}
],"edges":[
  {"src": "convert", "dst": "diann_quant"}
]}
```

### `fp-dia-speclib-quant-phospho-diapasef`
- **用途**:Migrated from FragPipe 'DIA_SpecLib_Quant_Phospho_diaPASEF.workflow' (DIA path). Original workflow also enabled: ['msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(.d(Bruker timsTOF));`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"fp-dia-speclib-quant-phospho-diapasef","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "diann_quant", "tool": "diann"}
],"edges":[
  
]}
```

### `fp-dia-speclib-quant-ubiq`
- **用途**:Migrated from FragPipe 'DIA_SpecLib_Quant_Ubiq.workflow' (DIA path). Original workflow also enabled: ['msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"fp-dia-speclib-quant-ubiq","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "diann_quant", "tool": "diann"}
],"edges":[
  {"src": "convert", "dst": "diann_quant"}
]}
```

### `fp-diagnostic-ion-mining`
- **用途**:Migrated from FragPipe 'Diagnostic-ion-mining.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-diagnostic-ion-mining","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "cleanup", "tool": "crystalc"},
  {"step_id": "validate", "tool": "peptideprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "ptm_summary", "tool": "ptmshepherd"}
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

### `fp-glyco-n-dia`
- **用途**:Migrated from FragPipe 'glyco-N-DIA.workflow' (DIA path). Original workflow also enabled: ['skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"fp-glyco-n-dia","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "diann_quant", "tool": "diann"}
],"edges":[
  {"src": "convert", "dst": "diann_quant"}
]}
```

### `fp-glyco-o-dia-hcd`
- **用途**:Migrated from FragPipe 'glyco-O-DIA-HCD.workflow' (DIA path). Original workflow also enabled: ['skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"fp-glyco-o-dia-hcd","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "diann_quant", "tool": "diann"}
],"edges":[
  {"src": "convert", "dst": "diann_quant"}
]}
```

### `fp-glyco-o-dia-opair`
- **用途**:Migrated from FragPipe 'glyco-O-DIA-OPair.workflow' (hybrid DDA-library + DIA-quant + OPair O-glycan localization). The DDA chain (msfragger → peptideprophet → report) builds a spectral library via easypqp, which DIA-NN then uses to quantify the same mzMLs in DIA mode. OPair localizes O-glycans on the DDA psm.tsv.
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-glyco-o-dia-opair","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "validate", "tool": "peptideprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "build_library", "tool": "easypqp"},
  {"step_id": "diann_quant", "tool": "diann"},
  {"step_id": "oglyc_localize", "tool": "opair"}
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

### `fp-nonspecific-hla-dia`
- **用途**:Migrated from FragPipe 'Nonspecific-HLA-DIA.workflow' (DIA path). Original workflow also enabled: ['diaumpire', 'msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"fp-nonspecific-hla-dia","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "diann_quant", "tool": "diann"}
],"edges":[
  {"src": "convert", "dst": "diann_quant"}
]}
```

### `fp-nonspecific-hla-dia-astral`
- **用途**:Migrated from FragPipe 'Nonspecific-HLA-DIA-Astral.workflow' (DIA path). Original workflow also enabled: ['msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"fp-nonspecific-hla-dia-astral","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "diann_quant", "tool": "diann"}
],"edges":[
  {"src": "convert", "dst": "diann_quant"}
]}
```

### `fp-nonspecific-hla-diapasef`
- **用途**:Migrated from FragPipe 'Nonspecific-HLA-diaPASEF.workflow' (DIA path). Original workflow also enabled: ['msbooster', 'skyline'] (dropped). Requires user-supplied spectral library (.tsv/.speclib) on the `diann_quant` step's `library_path` param. Library generation (easypqp / msfragger pre-search) is NOT migrated; supply a pre-built library or generate one separately.
- **输入**:谱图 `raw_files`(.d(Bruker timsTOF));`fasta_path`=蛋白库(DIA-NN 库无关预测;或 overrides 给 diann 步 `library_path` 现成谱图库)
- **调用(推荐)**:`{"template_id":"fp-nonspecific-hla-diapasef","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "diann_quant", "tool": "diann"}
],"edges":[
  
]}
```

### `fp-stellar-gpfdia`
- **用途**:Migrated from FragPipe 'Stellar-GPFDIA.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-stellar-gpfdia","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-labile-adp-ribosylation`
- **用途**:Migrated from FragPipe 'Labile_ADP-ribosylation.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-labile-adp-ribosylation","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "validate", "tool": "peptideprophet"},
  {"step_id": "localize", "tool": "ptmprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-labile-phospho`
- **用途**:Migrated from FragPipe 'Labile_phospho.workflow'. Original workflow also enabled: ['skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-labile-phospho","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "validate", "tool": "peptideprophet"},
  {"step_id": "localize", "tool": "ptmprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-lfq-phospho`
- **用途**:Migrated from FragPipe 'LFQ-phospho.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-lfq-phospho","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "localize", "tool": "ptmprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-lfq-ubiquitin`
- **用途**:Migrated from FragPipe 'LFQ-ubiquitin.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-lfq-ubiquitin","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "localize", "tool": "ptmprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-nonspecific-hla-phospho`
- **用途**:Migrated from FragPipe 'Nonspecific-HLA-phospho.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-nonspecific-hla-phospho","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "localize", "tool": "ptmprophet"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-silac3-phospho`
- **用途**:Migrated from FragPipe 'SILAC3-phospho.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-silac3-phospho","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-nonspecific-hla`
- **用途**:Migrated from FragPipe 'Nonspecific-HLA.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-nonspecific-hla","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-nonspecific-hla-c57`
- **用途**:Migrated from FragPipe 'Nonspecific-HLA-C57.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-nonspecific-hla-c57","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-nonspecific-hla-customdb-groupfdr`
- **用途**:Migrated from FragPipe 'Nonspecific-HLA-customDB-groupFDR.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-nonspecific-hla-customdb-groupfdr","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

### `fp-nonspecific-peptidome`
- **用途**:Migrated from FragPipe 'Nonspecific-peptidome.workflow'. Original workflow also enabled: ['msbooster', 'skyline'] (dropped — non-critical layers; downstream FDR still valid). Requires user-supplied target FASTA (the `database` step builds the decoy variant).
- **输入**:谱图 `raw_files`(mzML/raw);`fasta_path`=**target 蛋白库**(database 步自动建 decoy)
- **调用(推荐)**:`{"template_id":"fp-nonspecific-peptidome","raw_files":["谱图"],"fasta_path":"蛋白库"}`
- **DAG**(同 pipeline.json 格式,可复制改造):
```json
{"steps":[
  {"step_id": "convert", "tool": "msconvert"},
  {"step_id": "database", "tool": "philosopher-database"},
  {"step_id": "search", "tool": "msfragger-closed"},
  {"step_id": "rescore", "tool": "percolator"},
  {"step_id": "to_pepxml", "tool": "percolator-to-pepxml"},
  {"step_id": "report", "tool": "philosopher-report"},
  {"step_id": "quant", "tool": "ionquant"}
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

