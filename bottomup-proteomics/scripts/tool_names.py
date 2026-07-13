"""公开名 ⇄ 内部名。

对用户可见的一切 —— pipeline.json 契约、summary.json、DAG 图标签、日志文件名、
报错文本 —— 只出现**公开名**;内部实现、连线规则、参数键一律保持原样。

**为什么不全局改名**:decoy 注入认 `philosopher-database`、TMT 接线认 `tmtintegrator`、
msbooster 按 `.params` 认输入 —— 代码里有 490+ 处按工具名判定的逻辑,全局改名会静默改坏
这些判定(改坏了还不报错,只是结果悄悄不对)。所以:

    入口 to_internal() 归一  →  内部逻辑原样  →  出口 to_public() 映射

top-down 工具链(topfd / toppic / flashdeconv / mspathfindert / promex / pbfgen)与
msconvert 均为自由许可,不做遮蔽,故不在表内 —— 未登记的名字原样返回。
"""

PUBLIC_BY_INTERNAL = {
    "msfragger-closed":     "search-closed",
    "philosopher-database": "database",
    "philosopher-report":   "report",
    "peptideprophet":       "validate-psm",
    "proteinprophet":       "protein-infer",
    "iprophet":             "psm-integrate",
    "ptmprophet":           "ptm-localize",
    "percolator":           "rescore",
    "percolator-to-pepxml": "rescore-export",
    "crystalc":             "precursor-refine",
    "msbooster":            "predict-rescore",
    "ionquant":             "quant",
    "tmtintegrator":        "quant-isobaric",
    "ptmshepherd":          "ptm-profile",
    "diann":                "dia-search",
    "diatracer":            "dia-features",
    "diaumpire":            "dia-pseudo",
    "easypqp":              "speclib-build",
    "opair":                "glyco-localize",
}
INTERNAL_BY_PUBLIC = {v: k for k, v in PUBLIC_BY_INTERNAL.items()}

# 报错与日志尾里出现的**裸品牌名 / 产物名**(不是 tool id,故单列一张表)。
# 长的排前面,避免 "MSFragger-4.4" 被 "MSFragger" 截半。
_BRANDS = [
    ("fragger.params", "search.params"),
    ("TMT-Integrator", "isobaric quantifier"),
    ("MSFragger",      "search engine"),
    ("msfragger",      "search engine"),
    ("FragPipe",       "workflow suite"),
    ("fragpipe",       "workflow suite"),
    ("Philosopher",    "toolkit"),
    ("philosopher",    "toolkit"),
    ("IonQuant",       "quantifier"),
    ("DIA-NN",         "DIA engine"),
    ("Percolator",     "rescorer"),
    ("PeptideProphet", "PSM validator"),
    ("ProteinProphet", "protein inference"),
    ("CrystalC",       "precursor refiner"),
    ("MSBooster",      "rescoring predictor"),
    ("PTM-Shepherd",   "PTM profiler"),
    ("DIA-Umpire",     "DIA pseudo-spectra"),
    ("diaTracer",      "DIA feature detector"),
    ("EasyPQP",        "spectral library builder"),
]


def to_internal(tool: str) -> str:
    """公开名 → 内部名。内部名原样返回(幂等),故可无脑用在入口。"""
    return INTERNAL_BY_PUBLIC.get(tool, tool)


def to_public(tool: str) -> str:
    """内部名 → 公开名。未登记的(如 top-down 工具)原样返回。"""
    return PUBLIC_BY_INTERNAL.get(tool, tool)


def public_template_id(tid):
    """模板 id 去掉 `fp-` 前缀 —— fp = FragPipe,前缀本身就是品牌。"""
    if isinstance(tid, str) and tid.startswith("fp-"):
        return tid[3:]
    return tid


def scrub(text):
    """把任意文本(报错、日志尾)里的内部工具名与品牌名换成公开说法。"""
    if not text:
        return text
    out = str(text)
    # 先长后短:percolator-to-pepxml 必须先于 percolator 替换
    for internal, public in sorted(PUBLIC_BY_INTERNAL.items(), key=lambda kv: -len(kv[0])):
        out = out.replace(internal, public)
    for brand, public in _BRANDS:
        out = out.replace(brand, public)
    return out
