# Bottom-up 生产模板（71）

这里只列选择所需的摘要。完整步骤、参数、`inputs` 和 `map_over` 由 `scripts/template_catalog.json` 供编译器读取，Agent 不需要逐个展开。

| template_id | 步骤 | 原始输入 |
|---|---|---|
| `fp-basic-search` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report | .raw, .mzML |
| `fp-chemprot-abpp-diatop` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → easypqp → diann | .raw, .mzML |
| `fp-chemprot-abpp-iadtb-diapasef` | diatracer → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → ptmprophet → philosopher-report → easypqp → diann | .d |
| `fp-chemprot-abpp-iadtb-tmt16` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-chemprot-abpp-ipiaa` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → ionquant | .raw, .mzML |
| `fp-chemprot-abpp-isodtb` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → ionquant | .raw, .mzML |
| `fp-chemprot-abpp-isotop` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → ionquant | .raw, .mzML |
| `fp-citrullination` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → ionquant | .raw, .mzML |
| `fp-dia-dia-umpire-speclib-quant` | msconvert → diaumpire → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → easypqp → diann | .raw, .mzML |
| `fp-dia-speclib-quant` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → easypqp → diann | .raw, .mzML |
| `fp-dia-speclib-quant-diapasef` | diatracer → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → easypqp → diann | .d |
| `fp-dia-speclib-quant-phospho` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → ptmprophet → philosopher-report → easypqp → diann | .raw, .mzML |
| `fp-dia-speclib-quant-phospho-diapasef` | diatracer → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → ptmprophet → philosopher-report → easypqp → diann | .d |
| `fp-dia-speclib-quant-ubiq` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → ptmprophet → philosopher-report → easypqp → diann | .raw, .mzML |
| `fp-diagnostic-ion-mining` | msconvert → philosopher-database → msfragger-closed → crystalc → peptideprophet → philosopher-report → ptmshepherd | .raw, .mzML |
| `fp-glyco-n-hcd` | msconvert → philosopher-database → msfragger-closed → peptideprophet → philosopher-report → ptmshepherd | .raw, .mzML |
| `fp-glyco-n-hybrid` | msconvert → philosopher-database → msfragger-closed → peptideprophet → philosopher-report → ptmshepherd | .raw, .mzML |
| `fp-glyco-n-lfq` | msconvert → philosopher-database → msfragger-closed → peptideprophet → philosopher-report → ptmshepherd → ionquant | .raw, .mzML |
| `fp-glyco-n-open-hcd` | msconvert → philosopher-database → msfragger-closed → crystalc → peptideprophet → philosopher-report → ptmshepherd | .raw, .mzML |
| `fp-glyco-n-open-hybrid` | msconvert → philosopher-database → msfragger-closed → crystalc → peptideprophet → philosopher-report → ptmshepherd | .raw, .mzML |
| `fp-glyco-n-tmt` | msconvert → philosopher-database → msfragger-closed → peptideprophet → philosopher-report → ptmshepherd → ionquant → tmtintegrator | .raw, .mzML |
| `fp-glyco-o-hcd` | msconvert → philosopher-database → msfragger-closed → peptideprophet → philosopher-report → ptmshepherd | .raw, .mzML |
| `fp-glyco-o-hybrid` | msconvert → philosopher-database → msfragger-closed → peptideprophet → philosopher-report → opair | .raw, .mzML |
| `fp-glyco-o-open-hcd` | msconvert → philosopher-database → msfragger-closed → crystalc → peptideprophet → philosopher-report → ptmshepherd | .raw, .mzML |
| `fp-glyco-o-open-hybrid` | msconvert → philosopher-database → msfragger-closed → crystalc → peptideprophet → philosopher-report → ptmshepherd | .raw, .mzML |
| `fp-glyco-o-pair` | msconvert → philosopher-database → msfragger-closed → peptideprophet → philosopher-report → opair | .raw, .mzML |
| `fp-itraq4` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-itraq4-phospho` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → ptmprophet → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-labile-adp-ribosylation` | msconvert → philosopher-database → msfragger-closed → peptideprophet → ptmprophet → philosopher-report | .raw, .mzML |
| `fp-labile-phospho` | msconvert → philosopher-database → msfragger-closed → peptideprophet → ptmprophet → philosopher-report | .raw, .mzML |
| `fp-lfq-mbr` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → ionquant | .raw, .mzML |
| `fp-lfq-phospho` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → ptmprophet → philosopher-report → ionquant | .raw, .mzML |
| `fp-lfq-ubiquitin` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → ptmprophet → philosopher-report → ionquant | .raw, .mzML |
| `fp-mass-offset-commonptms` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → ptmshepherd | .raw, .mzML |
| `fp-nonspecific-hla` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report | .raw, .mzML |
| `fp-nonspecific-hla-c57` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report | .raw, .mzML |
| `fp-nonspecific-hla-customdb-groupfdr` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report | .raw, .mzML |
| `fp-nonspecific-hla-dia` | msconvert → diaumpire → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → easypqp → diann | .raw, .mzML |
| `fp-nonspecific-hla-dia-astral` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → easypqp → diann | .raw, .mzML |
| `fp-nonspecific-hla-diapasef` | diatracer → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → easypqp → diann | .d |
| `fp-nonspecific-hla-glyco` | msconvert → philosopher-database → msfragger-closed → peptideprophet → philosopher-report → ptmshepherd | .raw, .mzML |
| `fp-nonspecific-hla-phospho` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → ptmprophet → philosopher-report | .raw, .mzML |
| `fp-nonspecific-peptidome` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report | .raw, .mzML |
| `fp-open` | msconvert → philosopher-database → msfragger-closed → crystalc → peptideprophet → philosopher-report → ptmshepherd | .raw, .mzML |
| `fp-open-quickscan` | msconvert → philosopher-database → msfragger-closed → crystalc → peptideprophet → philosopher-report → ptmshepherd | .raw, .mzML |
| `fp-silac3` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → ionquant | .raw, .mzML |
| `fp-silac3-phospho` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → ionquant | .raw, .mzML |
| `fp-stellar-dda` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report | .raw, .mzML |
| `fp-stellar-gpfdia` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report | .raw, .mzML |
| `fp-tmt10` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-tmt10-acetyl` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → ptmprophet → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-tmt10-acetyl-noloc` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-tmt10-bridge` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-tmt10-ms3` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-tmt10-ms3-phospho` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → ptmprophet → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-tmt10-open` | msconvert → philosopher-database → msfragger-closed → crystalc → peptideprophet → philosopher-report → ptmshepherd → ionquant → tmtintegrator | .raw, .mzML |
| `fp-tmt10-phospho` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → ptmprophet → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-tmt10-phospho-bridge` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → ptmprophet → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-tmt10-ubiquitin` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-tmt10-ubiquitination-k-tmt-or-ubiq` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → ptmprophet → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-tmt16` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-tmt16-acetyl` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → ptmprophet → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-tmt16-acetyl-noloc` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-tmt16-ms3` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-tmt16-phospho` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → ptmprophet → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-tmt16-ubiquitination-k-tmt-or-ubiq` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → ptmprophet → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-tmt18-astral` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-tmt18-phospho` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → ptmprophet → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-tmt35` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → ionquant → tmtintegrator | .raw, .mzML |
| `fp-wwa` | msconvert → philosopher-database → msfragger-closed → percolator → percolator-to-pepxml → philosopher-report → ionquant | .raw, .mzML |
| `fp-xrnax-massoffset` | msconvert → philosopher-database → msfragger-closed → crystalc → peptideprophet → philosopher-report → ptmshepherd | .raw, .mzML |

生产目录只含完整跑通的 71 个 FragPipe 模板。仓库中的 7 个边界模板、旧 `fp-fpop` 和手工 `bottomup-*` 示例不发布。
