# Bottom-up 生产模板（71）

这里只列选择所需的摘要。完整步骤、参数、`inputs` 和 `map_over` 由 `scripts/template_catalog.json` 供编译器读取，Agent 不需要逐个展开。

| template_id | 步骤 | 原始输入 |
|---|---|---|
| `basic-search` | msconvert → database → search-closed → rescore → rescore-export → report | .raw, .mzML |
| `chemprot-abpp-diatop` | msconvert → database → search-closed → rescore → rescore-export → report → speclib-build → dia-search | .raw, .mzML |
| `chemprot-abpp-iadtb-diapasef` | dia-features → database → search-closed → rescore → rescore-export → ptm-localize → report → speclib-build → dia-search | .d |
| `chemprot-abpp-iadtb-tmt16` | msconvert → database → search-closed → rescore → rescore-export → report → quant → quant-isobaric | .raw, .mzML |
| `chemprot-abpp-ipiaa` | msconvert → database → search-closed → rescore → rescore-export → report → quant | .raw, .mzML |
| `chemprot-abpp-isodtb` | msconvert → database → search-closed → rescore → rescore-export → report → quant | .raw, .mzML |
| `chemprot-abpp-isotop` | msconvert → database → search-closed → rescore → rescore-export → report → quant | .raw, .mzML |
| `citrullination` | msconvert → database → search-closed → rescore → rescore-export → report → quant | .raw, .mzML |
| `dia-dia-umpire-speclib-quant` | msconvert → dia-pseudo → database → search-closed → rescore → rescore-export → report → speclib-build → dia-search | .raw, .mzML |
| `dia-speclib-quant` | msconvert → database → search-closed → rescore → rescore-export → report → speclib-build → dia-search | .raw, .mzML |
| `dia-speclib-quant-diapasef` | dia-features → database → search-closed → rescore → rescore-export → report → speclib-build → dia-search | .d |
| `dia-speclib-quant-phospho` | msconvert → database → search-closed → rescore → rescore-export → ptm-localize → report → speclib-build → dia-search | .raw, .mzML |
| `dia-speclib-quant-phospho-diapasef` | dia-features → database → search-closed → rescore → rescore-export → ptm-localize → report → speclib-build → dia-search | .d |
| `dia-speclib-quant-ubiq` | msconvert → database → search-closed → rescore → rescore-export → ptm-localize → report → speclib-build → dia-search | .raw, .mzML |
| `diagnostic-ion-mining` | msconvert → database → search-closed → precursor-refine → validate-psm → report → ptm-profile | .raw, .mzML |
| `glyco-n-hcd` | msconvert → database → search-closed → validate-psm → report → ptm-profile | .raw, .mzML |
| `glyco-n-hybrid` | msconvert → database → search-closed → validate-psm → report → ptm-profile | .raw, .mzML |
| `glyco-n-lfq` | msconvert → database → search-closed → validate-psm → report → ptm-profile → quant | .raw, .mzML |
| `glyco-n-open-hcd` | msconvert → database → search-closed → precursor-refine → validate-psm → report → ptm-profile | .raw, .mzML |
| `glyco-n-open-hybrid` | msconvert → database → search-closed → precursor-refine → validate-psm → report → ptm-profile | .raw, .mzML |
| `glyco-n-tmt` | msconvert → database → search-closed → validate-psm → report → ptm-profile → quant → quant-isobaric | .raw, .mzML |
| `glyco-o-hcd` | msconvert → database → search-closed → validate-psm → report → ptm-profile | .raw, .mzML |
| `glyco-o-hybrid` | msconvert → database → search-closed → validate-psm → report → glyco-localize | .raw, .mzML |
| `glyco-o-open-hcd` | msconvert → database → search-closed → precursor-refine → validate-psm → report → ptm-profile | .raw, .mzML |
| `glyco-o-open-hybrid` | msconvert → database → search-closed → precursor-refine → validate-psm → report → ptm-profile | .raw, .mzML |
| `glyco-o-pair` | msconvert → database → search-closed → validate-psm → report → glyco-localize | .raw, .mzML |
| `itraq4` | msconvert → database → search-closed → rescore → rescore-export → report → quant → quant-isobaric | .raw, .mzML |
| `itraq4-phospho` | msconvert → database → search-closed → rescore → rescore-export → ptm-localize → report → quant → quant-isobaric | .raw, .mzML |
| `labile-adp-ribosylation` | msconvert → database → search-closed → validate-psm → ptm-localize → report | .raw, .mzML |
| `labile-phospho` | msconvert → database → search-closed → validate-psm → ptm-localize → report | .raw, .mzML |
| `lfq-mbr` | msconvert → database → search-closed → rescore → rescore-export → report → quant | .raw, .mzML |
| `lfq-phospho` | msconvert → database → search-closed → rescore → rescore-export → ptm-localize → report → quant | .raw, .mzML |
| `lfq-ubiquitin` | msconvert → database → search-closed → rescore → rescore-export → ptm-localize → report → quant | .raw, .mzML |
| `mass-offset-commonptms` | msconvert → database → search-closed → rescore → rescore-export → report → ptm-profile | .raw, .mzML |
| `nonspecific-hla` | msconvert → database → search-closed → rescore → rescore-export → report | .raw, .mzML |
| `nonspecific-hla-c57` | msconvert → database → search-closed → rescore → rescore-export → report | .raw, .mzML |
| `nonspecific-hla-customdb-groupfdr` | msconvert → database → search-closed → rescore → rescore-export → report | .raw, .mzML |
| `nonspecific-hla-dia` | msconvert → dia-pseudo → database → search-closed → rescore → rescore-export → report → speclib-build → dia-search | .raw, .mzML |
| `nonspecific-hla-dia-astral` | msconvert → database → search-closed → rescore → rescore-export → report → speclib-build → dia-search | .raw, .mzML |
| `nonspecific-hla-diapasef` | dia-features → database → search-closed → rescore → rescore-export → report → speclib-build → dia-search | .d |
| `nonspecific-hla-glyco` | msconvert → database → search-closed → validate-psm → report → ptm-profile | .raw, .mzML |
| `nonspecific-hla-phospho` | msconvert → database → search-closed → rescore → rescore-export → ptm-localize → report | .raw, .mzML |
| `nonspecific-peptidome` | msconvert → database → search-closed → rescore → rescore-export → report | .raw, .mzML |
| `open` | msconvert → database → search-closed → precursor-refine → validate-psm → report → ptm-profile | .raw, .mzML |
| `open-quickscan` | msconvert → database → search-closed → precursor-refine → validate-psm → report → ptm-profile | .raw, .mzML |
| `silac3` | msconvert → database → search-closed → rescore → rescore-export → report → quant | .raw, .mzML |
| `silac3-phospho` | msconvert → database → search-closed → rescore → rescore-export → report → quant | .raw, .mzML |
| `stellar-dda` | msconvert → database → search-closed → rescore → rescore-export → report | .raw, .mzML |
| `stellar-gpfdia` | msconvert → database → search-closed → rescore → rescore-export → report | .raw, .mzML |
| `tmt10` | msconvert → database → search-closed → rescore → rescore-export → report → quant → quant-isobaric | .raw, .mzML |
| `tmt10-acetyl` | msconvert → database → search-closed → rescore → rescore-export → ptm-localize → report → quant → quant-isobaric | .raw, .mzML |
| `tmt10-acetyl-noloc` | msconvert → database → search-closed → rescore → rescore-export → report → quant → quant-isobaric | .raw, .mzML |
| `tmt10-bridge` | msconvert → database → search-closed → rescore → rescore-export → report → quant → quant-isobaric | .raw, .mzML |
| `tmt10-ms3` | msconvert → database → search-closed → rescore → rescore-export → report → quant → quant-isobaric | .raw, .mzML |
| `tmt10-ms3-phospho` | msconvert → database → search-closed → rescore → rescore-export → ptm-localize → report → quant → quant-isobaric | .raw, .mzML |
| `tmt10-open` | msconvert → database → search-closed → precursor-refine → validate-psm → report → ptm-profile → quant → quant-isobaric | .raw, .mzML |
| `tmt10-phospho` | msconvert → database → search-closed → rescore → rescore-export → ptm-localize → report → quant → quant-isobaric | .raw, .mzML |
| `tmt10-phospho-bridge` | msconvert → database → search-closed → rescore → rescore-export → ptm-localize → report → quant → quant-isobaric | .raw, .mzML |
| `tmt10-ubiquitin` | msconvert → database → search-closed → rescore → rescore-export → report → quant → quant-isobaric | .raw, .mzML |
| `tmt10-ubiquitination-k-tmt-or-ubiq` | msconvert → database → search-closed → rescore → rescore-export → ptm-localize → report → quant → quant-isobaric | .raw, .mzML |
| `tmt16` | msconvert → database → search-closed → rescore → rescore-export → report → quant → quant-isobaric | .raw, .mzML |
| `tmt16-acetyl` | msconvert → database → search-closed → rescore → rescore-export → ptm-localize → report → quant → quant-isobaric | .raw, .mzML |
| `tmt16-acetyl-noloc` | msconvert → database → search-closed → rescore → rescore-export → report → quant → quant-isobaric | .raw, .mzML |
| `tmt16-ms3` | msconvert → database → search-closed → rescore → rescore-export → report → quant → quant-isobaric | .raw, .mzML |
| `tmt16-phospho` | msconvert → database → search-closed → rescore → rescore-export → ptm-localize → report → quant → quant-isobaric | .raw, .mzML |
| `tmt16-ubiquitination-k-tmt-or-ubiq` | msconvert → database → search-closed → rescore → rescore-export → ptm-localize → report → quant → quant-isobaric | .raw, .mzML |
| `tmt18-astral` | msconvert → database → search-closed → rescore → rescore-export → report → quant → quant-isobaric | .raw, .mzML |
| `tmt18-phospho` | msconvert → database → search-closed → rescore → rescore-export → ptm-localize → report → quant → quant-isobaric | .raw, .mzML |
| `tmt35` | msconvert → database → search-closed → rescore → rescore-export → report → quant → quant-isobaric | .raw, .mzML |
| `wwa` | msconvert → database → search-closed → rescore → rescore-export → report → quant | .raw, .mzML |
| `xrnax-massoffset` | msconvert → database → search-closed → precursor-refine → validate-psm → report → ptm-profile | .raw, .mzML |

生产目录只含完整跑通的 71 个模板。仓库中的 7 个边界模板、旧边界示例和手工 `bottomup-*` 示例不发布。
