# Bottom-up 参数参考

本文件由 `deploy/bohrium-image/export_skill_assets.py` 从 `topdown_agent/service/specs.py` 生成。不要手工维护参数清单。

需要修改参数时只读取目标工具一节；机器校验使用同目录 `param_schema.json`。

## `msconvert`

版本：`3.0.25323`

输入：`.raw`, `.wiff`, `.d`, `.mzML`, `.mzXML`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `output_format` | `enum` | `mzML` | 枚举: mzML, mzXML, mz5, mzMLb, mgf, text, ms1, ms2, cms1, cms2 | Output format |
| `precision` | `int` | `64` | 枚举: 32, 64 | Binary precision (bits) |
| `zlib` | `bool` | `True` | — | Enable zlib compression |
| `filters` | `str_list` | `["peakPicking true 1-"]` | — | Spectrum list filters，每行一条；默认含质心化 filter |
| `chromatogram_filters` | `str_list` | `[]` | — | Repeated chromatogram filters |
| `extension` | `str` | `—` | — | Output extension override |
| `mz_precision` | `int` | `—` | — | m/z precision |
| `inten_precision` | `int` | `—` | — | Intensity precision |
| `mz_truncation` | `int` | `—` | — | m/z truncation bits |
| `inten_truncation` | `int` | `—` | — | Intensity truncation bits |
| `mz_delta` | `bool` | `False` | — | Enable m/z delta prediction |
| `inten_delta` | `bool` | `False` | — | Enable intensity delta prediction |
| `mz_linear` | `bool` | `False` | — | Enable m/z linear prediction |
| `inten_linear` | `bool` | `False` | — | Enable intensity linear prediction |
| `noindex` | `bool` | `False` | — | Disable index generation |
| `numpress_linear` | `bool` | `False` | — | Enable numpress linear prediction compression for m/z and RT |
| `numpress_linear_abs_tol` | `float` | `—` | — | Numpress linear absolute tolerance |
| `numpress_pic` | `bool` | `False` | — | Enable numpress pic |
| `numpress_slof` | `bool` | `False` | — | Enable numpress slof |
| `numpress_all` | `bool` | `False` | — | Enable all numpress codecs |
| `outfile` | `str` | `—` | — | Output file name |
| `contact_info` | `str` | `—` | — | Contact info file |
| `filelist` | `str` | `—` | — | Input file list |
| `config_file` | `str` | `—` | — | msconvert config file |
| `verbose` | `bool` | `True` | — | Verbose logging |
| `single_threaded` | `bool` | `False` | — | Single-threaded conversion |
| `continue_on_error` | `bool` | `False` | — | Continue on error |
| `merge` | `bool` | `False` | — | Merge multiple inputs |
| `combine_ion_mobility_spectra` | `bool` | `False` | — | Combine ion mobility spectra |
| `dda_processing` | `bool` | `False` | — | Enable DDA processing |
| `gzip` | `bool` | `False` | — | Gzip output |
| `sim_as_spectra` | `bool` | `False` | — | Write SIM as spectra |
| `srm_as_spectra` | `bool` | `False` | — | Write SRM as spectra |
| `ignore_calibration_scans` | `bool` | `False` | — | Ignore calibration scans |
| `accept_zero_length_spectra` | `bool` | `False` | — | Accept zero-length spectra |
| `ignore_missing_zero_samples` | `bool` | `False` | — | Ignore missing zero samples |
| `ignore_unknown_instrument_error` | `bool` | `False` | — | Ignore unknown instrument errors |
| `strip_location_from_source_files` | `bool` | `False` | — | Strip source file location |
| `strip_version_from_software` | `bool` | `False` | — | Strip software version |
| `mzmlb_chunk_size` | `int` | `—` | — | mzMLb chunk size |
| `mzmlb_compression_level` | `int` | `—` | — | mzMLb compression level |
| `run_index_set` | `str` | `—` | — | Run index set |

## `search-closed`

版本：`4.4`

输入：`.mzML`, `.mzXML`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `database_path` | `str` | `—` | 必填 | Path to target+decoy FASTA (toolkit database --custom output) |
| `num_threads` | `int` | `8` | ≥ 1 | Worker threads |
| `ram_gb` | `int` | `16` | ≥ 2 | JVM heap size (-Xmx) in GB. Default 16: full-proteome DBs (human-uniprot) + variable PTM mods (acetyl/ubiq/glyco) build multi-million-peptide indexes that OOM an 8 GB heap. |
| `precursor_tolerance_ppm` | `float` | `20.0` | ≥ 0 | Precursor mass window (±ppm) for closed search |
| `precursor_mass_lower_da` | `float` | `—` | — | Open-search asymmetric lower bound (Da). When set with _upper_da, overrides ppm window. |
| `precursor_mass_upper_da` | `float` | `—` | — | Open-search asymmetric upper bound (Da). When set with _lower_da, overrides ppm window. |
| `fragment_tolerance_ppm` | `float` | `20.0` | ≥ 0 | Fragment mass tolerance (ppm) |
| `isotope_error` | `str` | `0/1/2` | — | Allowed precursor monoisotopic peak offsets, slash-separated |
| `calibrate_mass` | `int` | `2` | 枚举: 0, 1, 2 | 0=off, 1=mass calibration, 2=mass+parameter optimisation |
| `mass_diff_to_variable_mod` | `int` | `0` | 枚举: 0, 1, 2 | Delta mass → variable mod. 0=no; 1=yes+remove; 2=yes+keep. Open/mass-offset searches need 1. |
| `localize_delta_mass` | `int` | `0` | 枚举: 0, 1 | Mass-shifted fragment ion localization. 0=off, 1=on. Pair with mass_diff_to_variable_mod=1 for open search. |
| `mass_offsets` | `str` | `0` | — | Slash-separated mass offsets for offset search; '0' = none |
| `mass_offsets_detailed` | `str` | `` | — | Detailed mass offset list (workflow suite format e.g. `541.0611(aa=DK);203.0794(aa=N)`); overrides mass_offsets when set |
| `labile_search_mode` | `str` | `off` | 枚举: off, labile, nglycan | Labile-mod search (glyco/labile PTM): 'nglycan' for N-glyco, 'labile' for O-glyco/labile PTMs, 'off' for standard. Pairs with mass_offsets. |
| `labile_fragment_ion_series` | `str` | `b,y` | — | Fragment ion series retained in labile search (e.g. 'b,y') |
| `enzyme_name` | `str` | `stricttrypsin` | — | search engine enzyme name (e.g. stricttrypsin, trypsin, chymotrypsin) |
| `enzyme_cut` | `str` | `KR` | — | Residues to cleave after |
| `enzyme_nocut` | `str` | `` | — | Residues that block cleavage (e.g. 'P' for trypsin) |
| `num_enzyme_termini` | `int` | `2` | 枚举: 0, 1, 2 | 0=non-specific, 1=semi-tryptic, 2=fully tryptic |
| `allowed_missed_cleavage` | `int` | `2` | ≥ 0; ≤ 5 | Maximum missed cleavages |
| `enzyme_sense` | `enum` | `C` | 枚举: C, N | Cutting terminus of the first enzyme (C- or N-terminal) |
| `enzyme_name_2` | `str` | `` | — | Second enzyme name; empty = single-enzyme digest |
| `enzyme_cut_2` | `str` | `` | — | Second enzyme's cutting residues |
| `enzyme_nocut_2` | `str` | `` | — | Second enzyme's blocking residues |
| `enzyme_sense_2` | `enum` | `C` | 枚举: C, N | Second enzyme's cutting terminus |
| `allowed_missed_cleavage_2` | `int` | `2` | ≥ 0; ≤ 5 | Second enzyme's maximum missed cleavages |
| `digest_min_length` | `int` | `7` | ≥ 1 | Min peptide length |
| `digest_max_length` | `int` | `50` | ≥ 1 | Max peptide length |
| `digest_min_mass` | `float` | `500.0` | — | Min peptide mass (Da) |
| `digest_max_mass` | `float` | `5000.0` | — | Max peptide mass (Da) |
| `var_mod_oxidation_M` | `bool` | `True` | — | Variable mod: Met oxidation (+15.9949) |
| `var_mod_acetyl_nterm` | `bool` | `True` | — | Variable mod: protein N-term acetylation (+42.0106) |
| `variable_mods` | `str` | `` | — | Extra variable mods beyond the oxidation/acetyl toggles, in workflow suite params format `<mass> <residues> <max>`, semicolon-separated. e.g. `79.966331 STY 3` (phospho), `114.04293 K 2` (GG/ubiquitin), `42.0106 K 2` (acetyl-K). |
| `fixed_mod_C_carbamidomethyl` | `bool` | `True` | — | Fixed mod: Cys carbamidomethyl (+57.02146) |
| `fixed_mods` | `str` | `` | — | Additional fixed modifications as search engine `add_*` entries, semicolon- or newline-separated `key = mass`. e.g. `add_S_serine = 79.96633; add_Nterm_protein = 42.0106`. Covers every residue/terminus beyond the C/K/N-term toggles. |
| `allow_multiple_variable_mods_on_residue` | `bool` | `False` | — | Allow more than one variable mod on the same residue |
| `max_variable_mods_combinations` | `int` | `5000` | ≥ 1; ≤ 65534 | Maximum modified forms per peptide |
| `tmt_label_mass` | `float` | `—` | — | If set, add as fixed mod on K and peptide N-term (e.g. 229.16293 for TMT-6/10/11plex). None = LFQ. |
| `tmt_kside_variable` | `bool` | `False` | — | When True, TMT is fixed only on the peptide N-term (not K). Use for acetyl/ubiquitin workflows where K carries a variable label — supply `229.16293 K 2` + the PTM via variable_mods. |
| `max_variable_mods_per_peptide` | `int` | `3` | ≥ 0; ≤ 10 | Max variable mods per peptide |
| `data_type` | `int` | `0` | 枚举: 0, 1, 2, 3 | 0 = DDA, 1 = DIA, 2 = gas-phase-fractionation DIA, 3 = DDA+ |
| `activation_types` | `str` | `all` | — | Only search scans of these activation types, '/'-separated (all, HCD, CID, ETD, ECD). ETD/EThcD workflows set this together with fragment_ion_series=c,z |
| `analyzer_types` | `str` | `all` | — | Only search scans from these analyzers, '/'-separated (all, FTMS, ITMS). mzML/raw only |
| `fragment_ion_series` | `str` | `b,y` | — | Ion series used in search: any of a,b,c,x,y,z,Y,b-18,y-18 (comma-separated). ETD/ECD data needs `c,z`; glyco labile searches add `Y` |
| `ion_series_definitions` | `str` | `` | — | Custom ion series, e.g. `b* N -17.026548;b0 N -18.010565` |
| `use_topN_peaks` | `int` | `150` | ≥ 1 | Pre-process each spectrum down to its top N peaks |
| `minimum_peaks` | `int` | `15` | ≥ 1 | Minimum peaks in an experimental spectrum for matching |
| `minimum_ratio` | `float` | `0.01` | ≥ 0 | Drop peaks below this fraction of the base peak |
| `clear_mz_range` | `str` | `0.0 0.0` | — | Remove peaks in this m/z range before matching, `<lo> <hi>` (0.0 0.0 = off). Used to clear the TMT reporter region |
| `deisotope` | `int` | `1` | 枚举: 0, 1, 2 | 0 = off, 1 = on (singletons single-charged), 2 = on (singletons single or double) |
| `deneutralloss` | `int` | `1` | 枚举: 0, 1 | Remove neutral-loss peaks |
| `remove_precursor_peak` | `int` | `1` | 枚举: 0, 1, 2 | 0 = keep, 1 = remove precursor charge peak, 2 = remove all charge states (DDA only) |
| `remove_precursor_range` | `str` | `-1.5,1.5` | — | m/z window (Th) used when removing precursor peaks |
| `intensity_transform` | `int` | `0` | 枚举: 0, 1 | 0 = raw intensities, 1 = sqrt transform |
| `require_precursor` | `int` | `1` | 枚举: 0, 1 | Discard PSMs without a precursor peak (DIA only) |
| `reuse_dia_fragment_peaks` | `int` | `0` | 枚举: 0, 1 | Allow one peak to match several peptides (DIA only) |
| `precursor_charge` | `str` | `1 4` | — | Assumed precursor charge range `<lo> <hi>`; only used when override_charge = 1 |
| `override_charge` | `int` | `0` | 枚举: 0, 1 | Ignore the precursor charge in the file and use precursor_charge instead |
| `max_fragment_charge` | `int` | `2` | ≥ 1; ≤ 4 | Maximum theoretical fragment charge to match |
| `clip_nTerm_M` | `int` | `1` | 枚举: 0, 1 | Treat protein N-terminal Met removal as a variable modification |
| `check_spectral_files` | `int` | `1` | 枚举: 0, 1 | Validate spectral files before searching |
| `Y_type_masses` | `str` | `` | — | [nglycan/labile only] Labile-mod fragments retained on intact peptides (glycan Y ions). Requires `Y` in fragment_ion_series |
| `diagnostic_fragments` | `str` | `` | — | [nglycan/labile only] Diagnostic (oxonium) fragment masses. Requires diagnostic_intensity_filter > 0 |
| `diagnostic_intensity_filter` | `float` | `0.0` | ≥ 0 | [nglycan/labile only] Minimum summed oxonium-ion intensity (relative to base peak) for a spectrum to count as diagnostic-positive |
| `remainder_fragment_masses` | `str` | `` | — | [labile only] Partial modification masses left on b/y ions after fragmentation |
| `restrict_deltamass_to` | `str` | `all` | — | Residues that may carry a delta mass / mass offset (capitalized single letters, '-' for termini, or 'all') |
| `min_matched_fragments` | `int` | `4` | ≥ 1 | Minimum matched peaks for a PSM to be reported |
| `min_sequence_matches` | `int` | `2` | ≥ 0 | [nglycan/labile only] Minimum sequence-specific (non-Y) ions for a match |
| `min_fragments_modelling` | `int` | `2` | ≥ 1 | Minimum matched peaks for a PSM to enter statistical modelling |
| `delta_mass_exclude_ranges` | `str` | `` | — | Fragment mass ranges excluded from delta-mass localization, e.g. `(-1.5,3.5)`. Empty = derived from localize_delta_mass |
| `precursor_mass_mode` | `enum` | `corrected` | 枚举: isolated, selected, corrected | Which precursor mass search engine uses (workflow suite uses 'corrected') |
| `group_variable` | `int` | `0` | 枚举: 0, 1, 2 | Group-FDR variable: 0 = no group FDR, 1 = num_enzyme_termini, 2 = PE from the protein header |
| `use_all_mods_in_first_search` | `int` | `0` | 枚举: 0, 1 | Use all variable modifications in the first search pass |
| `track_zero_topN` | `int` | `0` | ≥ 0 | Track top N unmodified hits separately (open-search boosting) |
| `zero_bin_accept_expect` | `float` | `0.0` | ≥ 0 | Rank a zero-bin hit first when its expect value is below this |
| `zero_bin_mult_expect` | `float` | `1.0` | ≥ 0 | Multiplier applied to zero-bin expect values (<1 boosts them) |
| `decoy_prefix` | `str` | `rev_` | — | Decoy sequence prefix (must match toolkit database) |
| `output_format` | `str` | `pepXML_pin` | 枚举: pepXML, pepXML_pin, tsv, tsv_pin | Output format selector |
| `output_report_topN` | `int` | `1` | ≥ 1 | Report top N PSMs per spectrum |
| `output_max_expect` | `float` | `50.0` | ≥ 0 | Suppress a PSM whose top hit has an expect value above this |
| `report_alternative_proteins` | `int` | `1` | 枚举: 0, 1 | Report alternative proteins for shared peptides |
| `write_calibrated_mzml` | `int` | `0` | 枚举: 0, 1 | Write calibrated MS2 scans to mzML (downstream rescoring predictor/quantifier can consume them) |
| `write_uncalibrated_mzml` | `int` | `1` | 枚举: 0, 1 | Write uncalibrated MS2 scans to MGF (.raw/.d inputs only) |
| `write_mzbin_all` | `int` | `0` | 枚举: 0, 1 | Write all spectra to mzBIN |
| `extra_params` | `str` | `` | — | Escape hatch: extra `key = value` lines appended to search.params (newline or ';' separated). Overrides a key we already write. |

## `precursor-refine`

版本：`1.5.10`

输入：`.pepXML`, `.fasta`, `.mzML`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `ram_gb` | `int` | `8` | ≥ 1 | JVM heap size (-Xmx<N>G) |
| `num_threads` | `int` | `-1` | — | Worker threads (-1 = cores-1) |
| `precursor_charge_min` | `int` | `1` | ≥ 1 | Lower precursor charge bound for chimeric detection |
| `precursor_charge_max` | `int` | `6` | ≥ 1 | Upper precursor charge bound |
| `isotope_number` | `int` | `3` | ≥ 1 | Number of theoretical isotope peaks to consider |
| `precursor_mass_ppm` | `float` | `20.0` | ≥ 0 | Precursor mass tolerance in ppm |
| `precursor_isolation_window` | `float` | `0.7` | ≥ 0 | Precursor isolation window (m/z) |
| `correct_isotope_error` | `bool` | `False` | — | Update precursor neutral mass with monoisotopic mass when isotope error detected |
| `raw_file_extension` | `str` | `mzML` | — | Spectra file extension (mzML / mzXML) |
| `grppr_jar_path` | `str` | `镜像内置（无需填写）` | — | Path to grppr jar (precursor refiner's required classpath sibling) |

## `rescore`

版本：`3.08`

输入：`.pin`, `.tsv`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `test_fdr` | `float` | `0.01` | ≥ 0; ≤ 1 | FDR threshold used to evaluate end results (--testFDR) |
| `train_fdr` | `float` | `0.01` | ≥ 0; ≤ 1 | FDR threshold for training positives (--trainFDR) |
| `max_iter` | `int` | `10` | ≥ 1 | Maximum SVM iterations (--maxiter) |
| `num_threads` | `int` | `8` | ≥ 1 | Worker threads |
| `seed` | `int` | `1` | ≥ 0 | RNG seed for reproducible runs |
| `subset_max_train` | `int` | `0` | ≥ 0 | Train on a subset of N PSMs (0 = use all). Recommended >0 for >1M PSMs. |
| `only_psms` | `bool` | `False` | — | Skip peptide-level aggregation (--only-psms) |
| `post_processing_tdc` | `bool` | `False` | — | Use target-decoy competition instead of mix-max (--post-processing-tdc) |
| `decoy_prefix` | `str` | `rev_` | — | Decoy protein-id prefix; only used when picked_protein_fasta is set |
| `picked_protein_fasta` | `str` | `—` | — | If set, enable picked-protein FDR using this FASTA (--picked-protein). Leave empty for PSM/peptide-only output. |
| `post_processing_mix_max` | `bool` | `False` | — | Explicitly use the mix-max method (--post-processing-mix-max); mutually exclusive with post_processing_tdc |
| `quick_validation` | `bool` | `False` | — | Faster run with reduced internal cross-validation (--quick-validation) |
| `nested_xval_bins` | `int` | `—` | ≥ 1 | Number of nested cross-validation bins (--nested-xval-bins) |
| `train_fdr_initial` | `float` | `—` | ≥ 0; ≤ 1 | FDR threshold for the first SVM iteration (--train-fdr-initial) |
| `train_best_positive` | `bool` | `False` | — | At most one PSM per spectrum may be a training positive (--train-best-positive) |
| `default_direction` | `str` | `` | — | Feature used as the initial search direction (--default-direction), e.g. `hyperscore` |
| `init_weights` | `str` | `` | — | Path to a weights file used to seed the SVM (--init-weights) |
| `static_weights` | `bool` | `False` | — | Use init_weights as a fixed scoring vector, no training (--static). Requires init_weights |
| `unit_norm` | `bool` | `False` | — | Unit [0-1] feature normalization instead of standard deviation (--unitnorm) |
| `test_each_iteration` | `bool` | `False` | — | Report test-set performance every iteration (--test-each-iteration) |
| `pep_algorithm` | `enum` | `default` | 枚举: default, irls, pava, ip | Posterior-error-probability estimator: default, cubic-spline (--irls-pep), isotonic PAVA (--pava-pep) or score-based (--ip-pep) |
| `output_retention_time` | `bool` | `False` | — | Add a retention-time column to the outputs (--output-retention-time) |
| `pepxml_output` | `str` | `` | — | Also write a rudimentary pepXML to this path (--pepxml-output) |
| `protein_enzyme` | `str` | `` | — | Enzyme used for in-silico protein digestion in picked-protein mode (--protein-enzyme) |
| `protein_report_fragments` | `bool` | `False` | — | Report protein fragments separately (--protein-report-fragments) |
| `protein_report_duplicates` | `bool` | `False` | — | Report duplicate protein groups (--protein-report-duplicates) |
| `spectral_counting_fdr` | `float` | `—` | ≥ 0; ≤ 1 | Enable protein spectral counting at this FDR (--spectral-counting-fdr) |
| `no_terminate` | `bool` | `False` | — | Keep going on recoverable input errors (--no-terminate) |
| `verbose` | `int` | `—` | 枚举: 0, 1, 2, 3, 4, 5 | Output verbosity (--verbose); unset = rescorer default 2 |
| `extra_cmdline` | `str` | `` | — | Escape hatch: extra rescorer flags appended verbatim (e.g. `--search-input concatenated`) |

## `rescore-export`

版本：`workflow suite-24.1`

输入：`.pin`, `.pepXML`, `.tsv`, `.mzML`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `jar_path` | `str` | `镜像内置（无需填写）` | — | Path to workflow suite.jar (the shadow jar that contains rescorerOutputToPepXML) |
| `data_type` | `enum` | `DDA` | 枚举: DDA, DIA | Acquisition mode — DDA reads <basename>.pepXML, DIA reads <basename>_rank<N>.pepXML |
| `min_prob` | `float` | `0.0` | ≥ 0; ≤ 1 | Minimum rescorer probability to emit (mirrors workflow suite's --min-prob) |
| `updated_fasta_path` | `str` | `` | — | Optional FASTA path rewritten into the output pepXML's <search_database local_path=...> field. Empty leaves it as-is. |

## `database`

版本：`5.1.0`

输入：`.fasta`, `.fa`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `decoy_prefix` | `str` | `rev_` | — | Decoy sequence prefix; must match search engine's decoy_prefix |
| `add_contam` | `bool` | `True` | — | Append the common-contaminants set (cRAP-style) to the target FASTA |
| `contam_prefix` | `bool` | `False` | — | Mark contaminant sequences with a prefix tag |
| `enzyme` | `str` | `trypsin` | 枚举: trypsin, lys_c, lys_n, glu_c, chymotrypsin | Enzyme for in-silico digestion (affects sequence classification only) |
| `isoform` | `bool` | `False` | — | Include isoform sequences from UniProt |
| `reviewed` | `bool` | `False` | — | Use only reviewed Swiss-Prot entries (ignored when --custom is the source) |
| `add_sequences` | `str` | `` | — | Path to an extra UniProt-format FASTA whose sequences are appended (--add), e.g. spike-ins or a mutant panel |
| `proteome_id` | `str` | `` | — | UniProt proteome ID to download instead of using a local FASTA (--id), e.g. `UP000005640`. Requires network access from the sandbox |

## `validate-psm`

版本：`5.1.0`

输入：`.pepXML`, `.fas`, `.fasta`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `decoy_prefix` | `str` | `rev_` | — | Decoy sequence tag (--decoy); must match upstream search engine / database setting |
| `output_prefix` | `str` | `interact-PXD` | — | Prefix for the interact-*.pep.xml output filename (--output) |
| `ppm` | `bool` | `True` | — | Mass model in ppm units (--ppm) |
| `accmass` | `bool` | `True` | — | Use accurate-mass binning (--accmass) |
| `nonparam` | `bool` | `True` | — | Semiparametric mixture model (--nonparam) |
| `decoyprobs` | `bool` | `True` | — | Compute probabilities for decoy hits too (--decoyprobs) |
| `combine` | `bool` | `True` | — | Combine all input pepXMLs into one model (--combine) |
| `min_prob` | `float` | `—` | ≥ 0; ≤ 1 | Report only PSMs above this probability (--minprob); unset = PSM validator default 0.05 |
| `min_pep_len` | `int` | `—` | ≥ 1 | Minimum peptide length not rejected (--minpeplen); unset = 7 |
| `mass_width` | `float` | `—` | ≥ 0 | Mass model width (--masswidth); unset = 5 |
| `clevel` | `int` | `—` | — | Conservative level in neg_stdev from neg_mean (--clevel); higher = more conservative |
| `enzyme` | `str` | `` | — | Enzyme used in the sample (--enzyme); empty = inferred from the pepXML |
| `ignore_charges` | `str` | `` | — | Comma-separated charge states excluded from modelling (--ignorechg), e.g. `1,5` |
| `phospho` | `bool` | `False` | — | Enable the phospho motif model (--phospho) |
| `glyc` | `bool` | `False` | — | Enable the glyco motif model (--glyc) |
| `expectscore` | `bool` | `True` | — | Use the expectation value as the only f-value contributor (--expectscore) |
| `no_mass_model` | `bool` | `False` | — | Disable the mass model (--nomass) |
| `no_nmc_model` | `bool` | `False` | — | Disable the missed-cleavage model (--nonmc) |
| `no_ntt_model` | `bool` | `False` | — | Disable the enzymatic-termini model (--nontt) |

## `ptm-localize`

版本：`6.3.2`

输入：`.pepXML`, `.pep.xml`, `.mzML`, `.mzXML`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `mods` | `str` | `STY:79.966331,M:15.9949,n:42.0106` | — | Modification sites + masses (site localizer positional arg). Format: `<residues>:<mass>` items joined by commas, e.g. `STY:79.966331,M:15.9949,n:42.0106` (n = peptide N-term). |
| `minprob` | `float` | `0.5` | ≥ 0; ≤ 1 | Minimum PSM validator probability for a PSM to be evaluated (MINPROB=) |
| `em` | `int` | `1` | 枚举: 0, 1, 2, 3 | EM model: 0 none, 1 intensity, 2 intensity+matched-peaks (default), 3 matched-peaks |
| `keepold` | `bool` | `True` | — | Retain prior site localizer results in the pepXML (KEEPOLD) |
| `static` | `bool` | `True` | — | Use a single fragppmtol for all PSMs (STATIC) instead of per-PSM estimation |
| `fragppmtol` | `float` | `10.0` | ≥ 0 | MS2 fragment ppm tolerance (FRAGPPMTOL=) |
| `nions` | `str` | `b` | — | Comma-separated N-term ion types (NIONS=); defaults to b for CID |
| `nostack` | `bool` | `False` | — | Disallow stacking multiple PTMs at the same residue (NOSTACK) |
| `maxthreads` | `int` | `1` | ≥ 1 | Worker threads (MAXTHREADS=). Was pinned to 1 because the key wasn't declared — large datasets should raise this |
| `cions` | `str` | `` | — | Comma-separated C-term ion types (CIONS=); empty = y for CID, z for ETD |
| `ppmtol` | `float` | `—` | ≥ 0 | MS1 precursor ppm tolerance (PPMTOL=); unset = 1 ppm |
| `daltontol` | `float` | `—` | ≥ 0 | MS2 fragment tolerance in Da (DALTONTOL=); overrides fragppmtol when set |
| `maxfragz` | `int` | `—` | — | Maximum fragment charge (MAXFRAGZ=); negative values subtract from the precursor charge |
| `modprec` | `int` | `—` | ≥ 0 | Decimal digits used when writing PTM masses (MODPREC=) |
| `massoffset` | `float` | `—` | — | Adjust the massdiff by this offset (MASSOFFSET=) |
| `massdiffmode` | `bool` | `False` | — | Treat the measured−theoretical mass difference as the modification and localize it (MASSDIFFMODE) |
| `exclude_massdiff_min` | `float` | `—` | — | Lower bound of the mass-difference range excluded in MASSDIFFMODE (EXCLUDEMASSDIFFMIN=) |
| `exclude_massdiff_max` | `float` | `—` | — | Upper bound of the mass-difference range excluded in MASSDIFFMODE (EXCLUDEMASSDIFFMAX=) |
| `lability` | `bool` | `False` | — | Compute PTM lability (LABILITY) — glyco / labile PTMs |
| `direct` | `bool` | `False` | — | Use only direct evidence for site probabilities (DIRECT) |
| `autodirect` | `bool` | `False` | — | Use direct evidence when lability is high (AUTODIRECT; pair with lability) |
| `denoise` | `bool` | `False` | — | Remove presumed noise peaks before localization (DENOISE) |
| `ifrags` | `bool` | `False` | — | Use internal fragments for localization (IFRAGS) |
| `no_update` | `bool` | `False` | — | Don't rewrite modification_info tags in the pepXML (NOUPDATE) |
| `verbose` | `bool` | `False` | — | Emit troubleshooting warnings (VERBOSE) |
| `extra_cmdline` | `str` | `` | — | Escape hatch: extra flags appended verbatim (e.g. OSCOREMODE, QUANTMODE, MINO=2). NOTE: site localizer is order-sensitive — flags that must precede the mods string (NOSTACK-style) have first-class params above; use this for the trailing long tail. |

## `report`

版本：`5.1.0`

输入：`.pepXML`, `.fas`, `.fasta`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `decoy_prefix` | `str` | `rev_` | — | Decoy sequence tag (--tag); must match upstream search engine / database setting |
| `psm_fdr` | `float` | `0.01` | ≥ 0; ≤ 1 | PSM-level FDR threshold (--psm) |
| `peptide_fdr` | `float` | `0.01` | ≥ 0; ≤ 1 | Peptide-level FDR threshold (--pep) |
| `ion_fdr` | `float` | `0.01` | ≥ 0; ≤ 1 | Peptide-ion FDR threshold (--ion) |
| `protein_fdr` | `float` | `0.01` | ≥ 0; ≤ 1 | Protein-level FDR threshold (--prot) |
| `inference` | `bool` | `True` | — | Run protein-level inference via protein inference (produces combined.prot.xml, passed to filter as --protxml; mirrors workflow suite). Disable for PSM/peptide-only reports — that also drops filter's --prot / --sequential / --razor, the way workflow suite does when no protXML exists. |
| `inference_min_prob` | `float` | `—` | ≥ 0; ≤ 1 | Minimum peptide probability protein inference admits (--minprob); unset = toolkit's 0.05. 29 official workflows ask for 0.5. |
| `inference_max_ppm_diff` | `int` | `2000000` | — | protein inference's peptide mass window for protein grouping (--maxppmdiff). workflow suite's baseline 2000000 effectively disables it. |
| `razor` | `bool` | `True` | — | Use razor-peptide algorithm for protein scoring |
| `picked` | `bool` | `False` | — | Apply picked-FDR before protein scoring |
| `sequential` | `bool` | `False` | — | Sequential FDR (PSM-then-protein) instead of 2D |
| `report_decoys` | `bool` | `False` | — | Include decoy hits in the report (--decoys) |
| `report_msstats` | `bool` | `False` | — | Emit an MSstats-compatible CSV alongside the TSVs (--msstats) |
| `remove_contam` | `bool` | `False` | — | Strip contaminants from the final report (--removecontam) |
| `pep_prob` | `float` | `—` | ≥ 0; ≤ 1 | Top-peptide probability threshold used in FDR filtering (--pepProb); unset = 0.7 |
| `prot_prob` | `float` | `—` | ≥ 0; ≤ 1 | Protein probability threshold (--protProb, ignored with razor); unset = 0.5 |
| `min_pep_len` | `int` | `—` | ≥ 1 | Minimum peptide length for protein probability assignment (--minPepLen); unset = 7 |
| `peptide_weight` | `float` | `—` | ≥ 0 | Threshold defining peptide uniqueness (--weight); unset = 1 |
| `two_dimensional` | `bool` | `False` | — | Two-dimensional FDR filtering (--2d) |
| `group_filter` | `bool` | `False` | — | Use the group label when filtering (--group) |
| `map_mods` | `bool` | `False` | — | Map modifications onto the filtered results (--mapmods) |
| `filter_mods` | `str` | `` | — | Modifications to stratify the FDR filter by (--mods), e.g. `M:15.9949,n:42.0106`. Empty = one pooled population, toolkit's default. |
| `delta_mass_stratify` | `bool` | `False` | — | Stratify PSMs by delta-mass profile before FDR filtering (--delta); open / labile searches |
| `print_models` | `bool` | `False` | — | Print the model distributions (--models) |
| `report_mzid` | `bool` | `False` | — | Also emit an mzIdentML file (--mzid) |
| `report_ionmobility` | `bool` | `False` | — | Force the ion-mobility column into the reports (--ionmobility). timsTOF data |
| `report_prefix` | `bool` | `False` | — | Prefix report filenames with the project/folder name (--prefix) |

## `quant-lfq`

版本：`5.1.0`

输入：`.tsv`, `.mzML`, `.mzXML`, `.raw`, `.d`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `ptw` | `float` | `0.4` | ≥ 0 | Peak time window in minutes (--ptw) |
| `tol` | `float` | `10.0` | ≥ 0 | m/z tolerance in ppm (--tol) |
| `faims` | `bool` | `False` | — | Use FAIMS compensation-voltage information (--faims) |
| `read_raw` | `bool` | `False` | — | Read vendor raw files instead of converted mzML/mzXML (--raw) |
| `extra_cmdline` | `str` | `` | — | Escape hatch: extra `toolkit quant-lfq` argv appended verbatim (shell-quoted) |

## `quant-reporter`

版本：`5.1.0`

输入：`.tsv`, `.mzML`, `.mzXML`, `.raw`, `.d`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `brand` | `str` | `` | — | Isobaric labeling brand (--brand): tmt, itraq or sCLIP. Required for a real run; toolkit declares no default |
| `plex` | `str` | `` | — | Number of reporter-ion channels (--plex), e.g. 10/11/16. Required for a real run; toolkit declares no default |
| `annotation_file` | `str` | `` | — | Annotation file mapping channels to sample names (--annot) |
| `level` | `int` | `2` | ≥ 1 | MS level the reporter ions are read from (--level) |
| `minprob` | `float` | `0.7` | ≥ 0; ≤ 1 | Only use PSMs above this probability (--minprob) |
| `purity` | `float` | `0.5` | ≥ 0; ≤ 1 | Ion purity threshold (--purity) |
| `tol` | `float` | `20.0` | ≥ 0 | m/z tolerance in ppm (--tol) |
| `removelow` | `float` | `0.0` | ≥ 0; ≤ 1 | Ignore the lower fraction of PSMs by summed abundance (--removelow); 0 = keep all |
| `uniqueonly` | `bool` | `False` | — | Quantify from unique peptides only (--uniqueonly) |
| `bestpsm` | `bool` | `False` | — | Keep only the best PSM per peptide for protein quantification (--bestpsm) |
| `read_raw` | `bool` | `False` | — | Read vendor raw files instead of converted mzML/mzXML (--raw) |
| `extra_cmdline` | `str` | `` | — | Escape hatch: extra `toolkit quant-reporter` argv appended verbatim (shell-quoted) |

## `aggregate-reports`

版本：`5.1.0`

输入：`.tsv`, `.prot.xml`, `.pep.xml`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `protein` | `bool` | `True` | — | Emit the global protein report combined_protein.tsv (--protein); needs combined.prot.xml from protein-infer |
| `peptide` | `bool` | `False` | — | Emit the global peptide report combined_peptide.tsv (--peptide); needs combined.pep.xml from psm-integrate |
| `decoy_prefix` | `str` | `rev_` | — | Decoy sequence tag (--tag); must match the upstream filter/database setting |
| `pep_prob` | `float` | `0.5` | ≥ 0; ≤ 1 | Minimum peptide probability (--pepProb) |
| `prot_prob` | `float` | `0.9` | ≥ 0; ≤ 1 | Minimum protein probability (--prtProb) |
| `razor` | `bool` | `False` | — | Use razor peptides for protein FDR scoring (--razor); match the upstream report setting |
| `picked` | `bool` | `False` | — | Apply the picked-FDR algorithm before protein scoring (--picked) |
| `labels` | `bool` | `False` | — | The datasets carry isobaric labels — combine channel abundances too (--labels) |
| `plex` | `str` | `10` | — | Number of isobaric channels (--plex); only meaningful with labels=True |
| `uniqueonly` | `bool` | `False` | — | Combine isobaric quantification from unique peptides only (--uniqueonly) |
| `full` | `bool` | `False` | — | Generate combined tables with extra columns (--full) |
| `reprint` | `bool` | `False` | — | Also write Reprint-format tables reprint.spc.tsv / reprint.int.tsv (--reprint) |
| `extra_cmdline` | `str` | `` | — | Escape hatch: extra `toolkit aggregate-reports` argv appended verbatim (shell-quoted) |

## `quant`

版本：`1.11.20`

输入：`.mzML`, `.mzXML`, `.tsv`, `.txt`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `binary_path` | `str` | `镜像内置（无需填写）` | — | Path to the quantifier JAR |
| `ram_gb` | `int` | `8` | ≥ 2 | JVM heap size (-Xmx) in GB |
| `threads` | `int` | `0` | ≥ 0 | Worker threads (0 = all logical cores) |
| `mztol_ppm` | `float` | `10.0` | ≥ 0 | MS1 mass tolerance (ppm) for feature extraction |
| `rttol_min` | `float` | `0.4` | ≥ 0 | Retention time tolerance (min) |
| `minisotopes` | `int` | `2` | 枚举: 1, 2, 3 | Minimum isotopes required in feature extraction |
| `minscans` | `int` | `3` | ≥ 1 | Minimum MS1 scans required in feature extraction |
| `perform_ms1quant` | `bool` | `True` | — | Run MS1 quant (LFQ); turn off for TMT-only experiments |
| `perform_isoquant` | `bool` | `False` | — | Run isobaric (TMT) quantification |
| `isotype` | `str` | `TMT-10` | 枚举: iTRAQ-4, iTRAQ-8, TMT-0, TMT-2, TMT-6, TMT-10, TMT-11, TMT-16, TMT-18, TMT-35 | Isobaric label type (only when perform_isoquant=True) |
| `isolevel` | `int` | `2` | 枚举: 2, 3 | MS level reporter ions are read from (2=MS2, 3=MS3). Only when perform_isoquant=True. |
| `annotation_file` | `str` | `` | — | TMT channel→sample annotation file. Required for isoquant (passed as --annotation <psm.tsv>=<file>). |
| `maxlfq` | `bool` | `True` | — | Calculate MaxLFQ intensity |
| `mbr` | `bool` | `False` | — | Match-between-runs (cross-sample alignment) |
| `normalization` | `bool` | `True` | — | Normalize intensities across runs |
| `msstats` | `bool` | `False` | — | Emit MSstats-compatible input |
| `isotol_ppm` | `float` | `—` | ≥ 0 | MS2 reporter-ion tolerance in ppm (--isotol); unset = quantifier default 10 |
| `site_reports` | `bool` | `True` | — | Generate PTM site reports (needs localization columns in psm.tsv) |
| `ionmobility` | `bool` | `False` | — | Data carries ion mobility (--ionmobility). Required for timsTOF LC-MS |
| `imtol` | `float` | `—` | ≥ 0 | 1/K0 tolerance (--imtol); unset = quantifier default 0.05 |
| `mbrrttol` | `float` | `—` | ≥ 0 | MBR retention-time tolerance in minutes (--mbrrttol); unset = 1.0 |
| `mbrimtol` | `float` | `—` | ≥ 0 | MBR 1/K0 tolerance (--mbrimtol); unset = 0.05 |
| `mbrtoprun` | `int` | `—` | ≥ 1 | Maximum donor runs per acceptor run (--mbrtoprun); unset = 10 |
| `mbrmincorr` | `float` | `—` | — | Minimum donor↔acceptor correlation (--mbrmincorr); unset = 0 |
| `ionfdr` | `float` | `—` | ≥ 0; ≤ 1 | Transferred-ion FDR threshold (--ionfdr); unset = 0.01 |
| `peptidefdr` | `float` | `—` | ≥ 0; ≤ 1 | Transferred-peptide FDR threshold (--peptidefdr); unset = 1 |
| `proteinfdr` | `float` | `—` | ≥ 0; ≤ 1 | Transferred-protein FDR threshold (--proteinfdr); unset = 1 |
| `minions` | `int` | `—` | ≥ 1 | Minimum ions required to quantify a protein, MaxLFQ only (--minions); unset = 1 |
| `minexps` | `int` | `—` | ≥ 1 | Minimum experiments an ion must appear in (--minexps); unset = 1 |
| `minfreq` | `float` | `—` | ≥ 0; ≤ 1 | Minimum frequency for an ion to be used in protein quant (--minfreq); unset = 0 |
| `topn_ions` | `int` | `—` | ≥ 0 | Ions used per protein, 0 = all (--tp); unset = 0 |
| `uniqueness` | `int` | `—` | 枚举: 0, 1, 2 | Peptide→protein uniqueness (--uniqueness): 0 = unique+razor, 1 = unique only, 2 = all |
| `intensitymode` | `int` | `—` | 枚举: 0, 1, 2 | Ion intensity mode (--intensitymode): 0 = apex, 1 = area, 2 = auto |
| `ibaq` | `bool` | `False` | — | Also compute iBAQ intensities (experimental) |
| `excludemods` | `str` | `` | — | Modifications excluded from quantification, `<aa><mass>;…` (--excludemods) |
| `locprob` | `float` | `—` | ≥ 0; ≤ 1 | Localization probability threshold (--locprob); unset = 0 |
| `writeindex` | `bool` | `False` | — | Write a reusable spectral index to disk (--writeindex) |
| `light_labels` | `str` | `` | — | Light channel labels `<residues><mass>;…` (--light), e.g. `K0.0;R0.0` |
| `medium_labels` | `str` | `` | — | Medium channel labels (--medium) |
| `heavy_labels` | `str` | `` | — | Heavy channel labels (--heavy), e.g. `K8.014199;R10.008269` |
| `label_formula` | `str` | `` | — | Chemical formulas of the labelling mods (--formula), e.g. `C(2)H(2)O;2H(4)C(2)`. Required for isotope-labelling quantification |
| `requantify` | `bool` | `—` | — | Re-quantify ions the search did not identify (--requantify). Unset = quantifier's default, except with light/medium/heavy labels where it defaults to on |
| `extra_cmdline` | `str` | `` | — | Escape hatch: extra quantifier flags appended verbatim (e.g. `--filelist /path/flags.txt`) |

## `ptm-profile`

版本：`3.0.11`

输入：`.tsv`, `.mzML`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `ram_gb` | `int` | `16` | ≥ 1 | JVM heap (-Xmx<N>G) |
| `threads` | `int` | `0` | — | 0 = all available |
| `glyco_mode` | `bool` | `False` | — | Enable glycan-PTM analysis path (emitted as PTM profiler's `run_glyco_mode`) |
| `n_glyco` | `bool` | `True` | — | N-glycan branch (vs O-glycan) when glyco_mode is on |
| `histo_bindivs` | `int` | `5000` | ≥ 1 | Histogram bins per Dalton used in peakpicking |
| `histo_smoothbins` | `int` | `2` | ≥ 0 | Peakpicking smoothing factor (weight spread to N adjacent bins) |
| `histo_normalizeTo` | `enum` | `psms` | 枚举: psms, scans | Normalize dataset size to PSM count or MS2 scan count |
| `peakpicking_mass_units` | `int` | `0` | 枚举: 0, 1 | Peakpicking mass units: 0 = Da, 1 = ppm. Pairs with `peakpicking_width`; workflow suite's open-search config uses 0 (0.002 Da) and its offset-search config uses 1 (3 ppm) |
| `spectra_condPeaks` | `int` | `150` | ≥ 1 | Maximum peaks kept per spectrum |
| `spectra_condRatio` | `float` | `0.0001` | ≥ 0 | Minimum peak intensity as a fraction of the base peak |
| `spectra_maxPrecursorCharge` | `int` | `4` | ≥ 1 | Maximum precursor charge considered |
| `localization_background` | `int` | `4` | 枚举: 1, 2, 3, 4 | Localization enrichment background: 1=bin peptides, 2=bin PSMs, 3=all peptides, 4=all PSMs |
| `localization_allowed_res` | `str` | `` | — | Residues allowed to carry the shift (e.g. `STY`, `N`); empty = no restriction |
| `localize_delta_mass` | `bool` | `True` | — | search engine already localized delta-mass fragment ions (pair with the search node's localize_delta_mass) |
| `reuse_search_localization` | `bool` | `False` | — | Reuse search engine's localization columns instead of re-localizing. Requires a psm.tsv that still carries them (no rescorer / precursor refiner in between) |
| `mass_delta_to_variable_mods` | `bool` | `False` | — | Re-synthesise variable mods from Delta Mass. Only for a psm.tsv whose `Modified Peptide` column is empty |
| `annotate_assigned_mods` | `bool` | `False` | — | Annotate shifts using the PSM table's assigned modifications |
| `annotation_file` | `str` | `` | — | `glyco`, `unimod`, `common`, or path to custom annotation table; empty = unimod |
| `annotation_tol` | `float` | `0.01` | ≥ 0 | Mass tolerance (Da) for matching shifts to known modifications |
| `mass_offsets` | `str` | `` | — | Slash-separated list to restrict peakpicking to (e.g. `0/-105.0248/-89.0299`); empty = full open search |
| `isotope_error` | `str` | `0` | — | Isotope correction list (e.g. `0/1/2`) |
| `peakpicking_promRatio` | `float` | `0.3` | ≥ 0 | Prominence ratio for peakpicking |
| `peakpicking_width` | `float` | `0.002` | ≥ 0 | Peakpicking width (Da) |
| `peakpicking_topN` | `int` | `500` | ≥ 1 | Maximum peaks to report |
| `peakpicking_minPsm` | `int` | `10` | ≥ 1 | Minimum PSMs per peak |
| `precursor_tol` | `float` | `0.01` | ≥ 0 | Peak-width tolerance (Da or ppm) |
| `precursor_mass_units` | `int` | `0` | 枚举: 0, 1 | 0 = Da, 1 = ppm |
| `varmod_masses` | `str` | `` | — | Additional prioritized mass shifts (e.g. `mod1:1234.456,mod2:456.789`) |
| `spectra_ppmtol` | `float` | `20.0` | ≥ 0 | MS2 ppm tolerance for localization + spectral similarity |
| `spectra_maxfragcharge` | `int` | `2` | ≥ 1 | Maximum fragment charge for localization |
| `iontype_a` | `bool` | `False` | — | Use a-ions |
| `iontype_b` | `bool` | `True` | — | Use b-ions |
| `iontype_c` | `bool` | `False` | — | Use c-ions |
| `iontype_x` | `bool` | `False` | — | Use x-ions |
| `iontype_y` | `bool` | `True` | — | Use y-ions |
| `iontype_z` | `bool` | `False` | — | Use z-ions |
| `compare_betweenRuns` | `bool` | `False` | — | Allow spectral similarity / RT calculation across runs |
| `output_extended` | `bool` | `False` | — | Retain intermediate + spectrum-level outputs |
| `prepare_for_quant` | `bool` | `False` | — | Prepare PSM table for downstream quantifier |
| `glycodatabase` | `str` | `` | — | Glycan database: comma-separated compositions (e.g. `HexNAc(2)Hex(3)`) or a path to a .glyc file; empty = PTM profiler default |
| `glyco_fdr` | `float` | `0.01` | ≥ 0; ≤ 1 | Glycan assignment FDR |
| `glyco_ppm_tol` | `float` | `30.0` | ≥ 0 | Precursor ppm tolerance for glycan mass matching |
| `glyco_isotope_min` | `int` | `-1` | — | Minimum isotope error for glycan matching |
| `glyco_isotope_max` | `int` | `3` | — | Maximum isotope error for glycan matching |
| `glyco_lda` | `bool` | `False` | — | Use LDA-based glycan scoring |
| `cap_y_ions` | `str` | `0,203.07937,406.15874,568.21156,730.26438,892.3172,349.137279` | — | Y-ion (peptide + glycan remainder) masses searched in the spectrum |
| `diag_ions` | `str` | `204.086646,186.076086,168.065526,366.139466,144.0656,138.055,512.197375,292.1026925,274.0921325,657.2349,243.026426,405.079246,485.045576,308.09761` | — | Diagnostic (oxonium) ion masses, singly charged |
| `diag_ions_normalize` | `int` | `1` | 枚举: 0, 1 | Normalize diagnostic ion intensities: 0 = off, 1 = base peak |
| `glyco_cap_y_ions_normalize` | `int` | `1` | 枚举: 0, 1 | Normalize Y-ion intensities: 0 = off, 1 = base peak |
| `max_cap_y_charge` | `int` | `0` | ≥ 0 | Maximum Y-ion charge state (0 = tool default) |
| `remainder_masses` | `str` | `203.07937` | — | Comma-separated remainder masses localized onto the peptide |
| `remainder_mass_allowed_res` | `str` | `all` | — | Residues that may carry a remainder mass (`all` or a residue list) |
| `remove_glycan_delta_mass` | `bool` | `True` | — | Strip the glycan delta mass from the reported peptide mass |
| `put_glycans_to_assigned_mods` | `bool` | `True` | — | Write assigned glycans into the psm.tsv `Assigned Modifications` column (needed by downstream quantifier/isobaric quantifier) |
| `print_full_glyco_params` | `bool` | `False` | — | Echo the full resolved glyco parameter set into the log |
| `print_decoys` | `bool` | `False` | — | Include decoy glycan assignments in the reports |
| `run_diagextract_mode` | `bool` | `False` | — | Extract intensities for the configured diagnostic ions |
| `run_diagmine_mode` | `bool` | `False` | — | Mine unknown diagnostic ions / peptide remainders (Diagnostic-ion-mining workflow) |
| `diagmine_minPeps` | `int` | `25` | ≥ 1 | Minimum peptides per mass shift for diagnostic mining |
| `diagmine_minIonsPerSpec` | `int` | `2` | ≥ 1 | Minimum ions per spectrum for diagnostic mining |
| `diagmine_diagMinFoldChange` | `float` | `3.0` | ≥ 0 | Minimum fold change for a diagnostic ion to be reported |
| `diagmine_diagMinSpecDiff` | `float` | `25.0` | ≥ 0 | Minimum spectral percentage difference for a diagnostic ion |
| `diagmine_fragMinFoldChange` | `float` | `3.0` | ≥ 0 | Minimum fold change for a fragment remainder ion |
| `diagmine_fragMinSpecDiff` | `float` | `25.0` | ≥ 0 | Minimum spectral percentage difference for a fragment remainder ion |
| `diagmine_fragMinPropensity` | `float` | `12.5` | ≥ 0 | Minimum propensity for a fragment remainder ion |
| `diagmine_pepMinFoldChange` | `float` | `3.0` | ≥ 0 | Minimum fold change for a peptide remainder mass |
| `diagmine_pepMinSpecDiff` | `float` | `25.0` | ≥ 0 | Minimum spectral percentage difference for a peptide remainder mass |
| `extra_params` | `str` | `` | — | Escape hatch: extra `key = value` lines appended to ptm-profile_config.txt (newline or ';' separated). Overrides a key we already write. |

## `quant-isobaric`

版本：`6.2.1`

输入：`.tsv`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `annotation_file` | `str` | `` | 必填 | Path to TMT annotation file (whitespace-separated `<channel> <sample>` per line). Reference channels must use the value of `ref_tag` (default 'pool'). |
| `channel_num` | `int` | `10` | 枚举: 4, 8, 6, 10, 11, 16, 18, 35 | Isobaric plex size — iTRAQ 4/8 or TMT 6/10/11/16/18/35 (label mass auto-derived: 4/8→iTRAQ 144.10, others→TMT/TMTpro) |
| `ref_tag` | `str` | `pool` | — | Reference-channel tag (matched against sample column of annotation file) |
| `add_Ref` | `int` | `-1` | 枚举: -2, -1, 0, 1, 2 | Artificial reference: -2 raw, -1 disabled, 0 sum, 1 avg, 2 median |
| `groupby` | `int` | `-1` | 枚举: -1, 0, 1, 2, 3, 4, 5 | Aggregation level: -1 all, 0 gene, 1 protein, 2 peptide, 3 multi-site, 4 single-site, 5 multi-mass |
| `prot_norm` | `int` | `-1` | 枚举: -1, 0, 1, 2, 3 | Normalization: -1 all, 0 none, 1 MC, 2 GN, 3 SL+IRS |
| `aggregation_method` | `int` | `0` | 枚举: 0, 1 | PSM→level aggregation: 0 median, 1 weighted-ratio |
| `log2transformed` | `bool` | `True` | — | Report ratios/abundances on log2 scale |
| `allow_overlabel` | `bool` | `True` | — | Accept PSMs with extra TMT on Ser |
| `allow_unlabeled` | `bool` | `False` | — | Accept PSMs without any TMT tag |
| `best_psm` | `bool` | `True` | — | Keep highest-intensity PSM per peptide per run |
| `outlier_removal` | `bool` | `True` | — | Drop intensity outliers before aggregation |
| `psm_norm` | `bool` | `False` | — | Additional RT-based PSM-level normalization |
| `ms1_int` | `bool` | `True` | — | Use MS1 precursor intensity (else MS2 reference) for ref sample abundance |
| `min_pep_prob` | `float` | `0.9` | ≥ 0; ≤ 1 | Minimum PSM probability (in addition to toolkit FDR) |
| `min_purity` | `float` | `0.5` | ≥ 0; ≤ 1 | Precursor purity threshold |
| `min_percent` | `float` | `0.05` | ≥ 0; ≤ 1 | Drop PSMs whose summed-TMT intensity is in the lowest fraction |
| `min_site_prob` | `float` | `-1.0` | — | Site-localization confidence (-1 global, 0 search engine, >0 site localizer) |
| `min_snr` | `float` | `0.0` | — | Minimum reporter-ion SNR |
| `unique_pep` | `bool` | `False` | — | Use unique peptides only (else unique+razor) |
| `unique_gene` | `int` | `0` | 枚举: 0, 1, 2 | Gene-uniqueness filter: 0 keep all, 1 drop multi-gene-evidence, 2 drop all multi-gene-in-fasta |
| `mod_tag` | `str` | `none` | — | PTM specification for site-specific reports (e.g. 'S(79.9663),T(79.9663),Y(79.9663)' for phospho) |
| `prot_exclude` | `str` | `none` | — | Protein accession prefixes to drop (e.g. 'sp\|,tr\|'). 'none' = keep all. |
| `ram_gb` | `int` | `16` | ≥ 1 | JVM heap (-Xmx<N>G) |
| `label_masses` | `float` | `—` | — | Isobaric label mass. Empty = derived from channel_num (iTRAQ 144.10253, TMT 229.16293, TMTpro 304.20715) |
| `max_pep_prob_thres` | `float` | `0.0` | ≥ 0; ≤ 1 | Peptide probability above which a PSM is always kept (0 = off) |
| `min_ntt` | `int` | `0` | 枚举: 0, 1, 2 | Minimum number of enzymatic termini |
| `glyco_qval` | `float` | `-1.0` | — | Glycan q-value filter for glyco-TMT reports (-1 = off) |
| `use_glycan_composition` | `bool` | `False` | — | Index site reports by glycan composition instead of mass (N-glyco only) |
| `print_RefInt` | `bool` | `False` | — | Print reference-channel intensities in the reports |
| `medium_subplex` | `str` | `` | — | Hyperplex medium sub-plex definition `<channelCount>:<refTag>` (e.g. `18:pool`) |
| `heavy_subplex` | `str` | `` | — | Hyperplex heavy sub-plex definition `<channelCount>:<refTag>` |
| `combined_protein` | `str` | `` | — | Path to combined_protein.tsv used for gene/protein annotation of the reports |
| `abn_type` | `int` | `—` | 枚举: 0, 1 | Abundance type reported (0 = ratio-derived, 1 = intensity); unset = isobaric quantifier default |
| `min_resolution` | `int` | `—` | ≥ 0 | Minimum MS2 resolution required to resolve the reporter ions; unset = tool default |
| `extra_params` | `str` | `` | — | Escape hatch: extra `key = value` entries merged into tmt-i_config.yml (newline or ';' separated). Overrides a key we already write. |

## `dia-search`

版本：`1.8.2-beta8`

输入：`.mzML`, `.mzXML`, `.d`, `.raw`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `library_path` | `str` | `` | — | Path to spectral library (.tsv/.speclib). DIA engine's --lib argument. Optional if upstream speclib-build supplies library*.tsv via inputs (hybrid topology). |
| `fasta_path` | `str` | `` | — | Optional fasta for protein inference (--fasta). Empty disables protein-level reports. |
| `num_threads` | `int` | `8` | ≥ 1 | Worker threads (--threads) |
| `precursor_qvalue` | `float` | `0.01` | ≥ 0; ≤ 1 | Run-specific precursor q-value cutoff (--qvalue) |
| `protein_qvalue` | `float` | `0.01` | ≥ 0; ≤ 1 | Run-specific protein q-value cutoff (--matrix-qvalue) |
| `matrix_spec_qvalue` | `float` | `—` | ≥ 0; ≤ 1 | Run-specific protein spec-q for matrix reporting (--matrix-spec-q); unset = DIA engine's default (no filter), which is what workflow suite runs with |
| `mbr` | `bool` | `False` | — | Match-between-runs / re-analysis pass (--reanalyse) |
| `matrices` | `bool` | `True` | — | Emit pr_matrix / pg_matrix abundance tables (--matrices) |
| `relaxed_protein_inference` | `bool` | `False` | — | Use relaxed protein inference (--relaxed-prot-inf) |
| `no_protein_inference` | `bool` | `False` | — | Skip protein inference entirely (--no-prot-inf) |
| `skip_quant` | `bool` | `False` | — | DEPRECATED / no-op: DIA engine has no '--no-quant' option (it warns 'unrecognised option' and quantifies anyway). Kept so existing graphs still validate. Use `no_quant_files` or `quant_only` instead. |
| `no_quant_files` | `bool` | `False` | — | Don't write intermediate .quant files to disk (--no-quant-files) |
| `quant_only` | `bool` | `False` | — | Only run quantification using existing .quant files (--quant-only) |
| `fasta_search` | `bool` | `False` | — | Library-free mode: digest the FASTA in silico (--fasta-search). Requires fasta_path (or a .fasta input); library_path becomes optional. |
| `gen_spec_lib` | `bool` | `False` | — | Generate a spectral library from this run (--gen-spec-lib) |
| `predictor` | `bool` | `False` | — | Deep-learning prediction of spectra/RT/IM for the in-silico library (--predictor) |
| `out_lib` | `str` | `` | — | Output spectral library path (--out-lib); empty = <output_dir>/report-lib.tsv when gen_spec_lib is on |
| `cut` | `str` | `` | — | In-silico digest rule (--cut), e.g. `K*,R*` for trypsin, `--cut` empty = DIA engine default |
| `missed_cleavages` | `int` | `—` | ≥ 0 | Maximum missed cleavages for the in-silico digest (--missed-cleavages) |
| `min_pep_len` | `int` | `—` | ≥ 1 | Minimum peptide length (--min-pep-len) |
| `max_pep_len` | `int` | `—` | ≥ 1 | Maximum peptide length (--max-pep-len) |
| `min_pr_mz` | `float` | `—` | ≥ 0 | Minimum precursor m/z (--min-pr-mz) |
| `max_pr_mz` | `float` | `—` | ≥ 0 | Maximum precursor m/z (--max-pr-mz) |
| `min_pr_charge` | `int` | `—` | ≥ 1 | Minimum precursor charge (--min-pr-charge) |
| `max_pr_charge` | `int` | `—` | ≥ 1 | Maximum precursor charge (--max-pr-charge) |
| `min_fr_mz` | `float` | `—` | ≥ 0 | Minimum fragment m/z (--min-fr-mz) |
| `max_fr_mz` | `float` | `—` | ≥ 0 | Maximum fragment m/z (--max-fr-mz) |
| `met_excision` | `bool` | `False` | — | Consider protein N-terminal methionine excision (--met-excision) |
| `unimod4` | `bool` | `False` | — | Fixed Cys carbamidomethylation (--unimod4) |
| `unimod35` | `bool` | `False` | — | Variable Met oxidation (--unimod35) |
| `max_var_mods` | `int` | `—` | ≥ 0 | Maximum variable modifications per peptide (--var-mods) |
| `var_mods` | `str` | `` | — | Extra variable mods, semicolon-separated `<name>,<mass>,<sites>` (each becomes a --var-mod argument), e.g. `UniMod:21,79.966331,STY` |
| `mass_acc` | `float` | `—` | ≥ 0 | MS2 mass accuracy in ppm (--mass-acc); unset = DIA engine auto-determines |
| `mass_acc_ms1` | `float` | `—` | ≥ 0 | MS1 mass accuracy in ppm (--mass-acc-ms1); unset = auto |
| `scan_window` | `int` | `—` | ≥ 0 | Scan window radius (--window); unset = auto |
| `smart_profiling` | `bool` | `False` | — | Adaptive library profiling (--smart-profiling) |
| `peak_center` | `bool` | `False` | — | Robust (peak-centred) quantification (--peak-center) |
| `no_ifs_removal` | `bool` | `False` | — | Disable interference removal (--no-ifs-removal) |
| `report_lib_info` | `bool` | `False` | — | Add the library's own columns to report.tsv (--report-lib-info) |
| `individual_mass_acc` | `bool` | `False` | — | Determine mass accuracy per run instead of once for the batch (--individual-mass-acc); workflow suite sets it for unrelated runs |
| `individual_windows` | `bool` | `False` | — | Determine the scan window per run (--individual-windows); workflow suite sets it for unrelated runs |
| `no_maxlfq` | `bool` | `False` | — | Disable MaxLFQ protein quantification (--no-maxlfq) |
| `no_normalization` | `bool` | `False` | — | Disable cross-run normalization (--no-norm) |
| `pg_level` | `int` | `—` | 枚举: 0, 1, 2 | Protein inference level (--pg-level): 0=isoform, 1=protein, 2=gene |
| `il_eq` | `bool` | `False` | — | Treat isoleucine and leucine as equal (--il-eq) |
| `reannotate` | `bool` | `False` | — | Re-annotate the library against the FASTA (--reannotate) |
| `temp_dir` | `str` | `` | — | Directory for intermediate .quant files (--temp) |
| `extra_cmdline` | `str` | `` | — | Escape hatch: free-form extra args appended verbatim (e.g. `--no-cut-after-mod --individual-mass-acc`) |

## `dia-pseudo`

版本：`2.3.4`

输入：`.mzML`, `.mzXML`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `ram_gb` | `int` | `12` | ≥ 1 | JVM heap (-Xmx<N>G) |
| `threads` | `int` | `7` | ≥ 1 | DIA pseudo-spectra worker threads |
| `RPmax` | `int` | `25` | ≥ 1 | Max precursor-fragment ratio |
| `RFmax` | `int` | `500` | ≥ 1 | Max fragment-fragment ratio |
| `CorrThreshold` | `float` | `0.0` | ≥ 0 | Precursor-fragment correlation cutoff |
| `DeltaApex` | `float` | `0.2` | ≥ 0 | Precursor-fragment apex Δ tolerance |
| `RTOverlap` | `float` | `0.3` | ≥ 0; ≤ 1 | Minimum RT overlap fraction |
| `AdjustFragIntensity` | `bool` | `True` | — | Adjust fragment intensities post-grouping |
| `BoostComplementaryIon` | `bool` | `False` | — | Boost complementary ion pairs (helpful for library building) |
| `ExportPrecursorPeak` | `bool` | `False` | — | Export detected MS1 feature file |
| `MS1PPM` | `float` | `10.0` | ≥ 0 | Signal-extraction MS1 ppm tolerance (SE.MS1PPM) |
| `MS2PPM` | `float` | `20.0` | ≥ 0 | Signal-extraction MS2 ppm tolerance (SE.MS2PPM) |
| `MS1SN` | `float` | `1.1` | ≥ 0 | MS1 signal-to-noise threshold (SE.SN) |
| `MS2SN` | `float` | `1.1` | ≥ 0 | MS2 signal-to-noise threshold (SE.MS2SN) |
| `MassDefectFilter` | `bool` | `True` | — | Apply mass-defect-based peptide filter (SE.MassDefectFilter) |
| `Q1` | `bool` | `True` | — | Emit Q1 pseudo-DDA mzML |
| `Q2` | `bool` | `True` | — | Emit Q2 pseudo-DDA mzML |
| `Q3` | `bool` | `True` | — | Emit Q3 pseudo-DDA mzML |
| `WindowType` | `enum` | `SWATH` | 枚举: SWATH, V_SWATH, MSX, MSE, pSMART | DIA isolation scheme. SWATH = fixed windows (uses WindowSize); V_SWATH = variable windows (needs a window list via extra_params `==window setting begin`); MSX / MSE / pSMART for those acquisitions |
| `WindowSize` | `int` | `10` | ≥ 0 | Isolation window width (Th) for WindowType = SWATH |
| `Resolution` | `int` | `60000` | ≥ 1 | Instrument resolving power (SE.Resolution) |
| `EstimateBG` | `bool` | `False` | — | Estimate background noise level (SE.EstimateBG) |
| `MinMSIntensity` | `float` | `1.0` | ≥ 0 | Minimum MS1 peak intensity (SE.MinMSIntensity) |
| `MinMSMSIntensity` | `float` | `1.0` | ≥ 0 | Minimum MS2 peak intensity (SE.MinMSMSIntensity) |
| `NoMissedScan` | `int` | `1` | ≥ 0 | Allowed missed scans within a peak curve (SE.NoMissedScan) |
| `MaxCurveRTRange` | `float` | `2.0` | ≥ 0 | Maximum peak-curve RT width in minutes (SE.MaxCurveRTRange) |
| `RemoveGroupedPeaks` | `bool` | `True` | — | Remove fragment peaks already grouped to another precursor (SE.RemoveGroupedPeaks) |
| `RemoveGroupedPeaksRTOverlap` | `float` | `0.3` | ≥ 0; ≤ 1 | RT overlap threshold for grouped-peak removal (SE.RemoveGroupedPeaksRTOverlap) |
| `RemoveGroupedPeaksCorr` | `float` | `0.3` | ≥ 0; ≤ 1 | Correlation threshold for grouped-peak removal (SE.RemoveGroupedPeaksCorr) |
| `MinNoPeakCluster` | `int` | `2` | ≥ 1 | Minimum isotope peaks per cluster (SE.MinNoPeakCluster) |
| `MaxNoPeakCluster` | `int` | `4` | ≥ 1 | Maximum isotope peaks per cluster (SE.MaxNoPeakCluster) |
| `IsoPattern` | `float` | `0.3` | ≥ 0 | Isotope pattern similarity threshold (SE.IsoPattern) |
| `MassDefectOffset` | `float` | `0.1` | ≥ 0 | Mass-defect filter offset (SE.MassDefectOffset) |
| `StartCharge` | `int` | `1` | ≥ 1 | Minimum precursor charge (SE.StartCharge) |
| `EndCharge` | `int` | `5` | ≥ 1 | Maximum precursor charge (SE.EndCharge) |
| `MS2StartCharge` | `int` | `2` | ≥ 1 | Minimum fragment charge (SE.MS2StartCharge) |
| `MS2EndCharge` | `int` | `5` | ≥ 1 | Maximum fragment charge (SE.MS2EndCharge) |
| `MinFrag` | `int` | `10` | ≥ 1 | Minimum fragments per pseudo-MS/MS spectrum (SE.MinFrag) |
| `StartRT` | `float` | `0.0` | ≥ 0 | Start retention time in minutes (SE.StartRT) |
| `EndRT` | `float` | `9999.0` | ≥ 0 | End retention time in minutes (SE.EndRT) |
| `MinMZ` | `float` | `200.0` | ≥ 0 | Minimum m/z considered (SE.MinMZ) |
| `MinPrecursorMass` | `float` | `600.0` | ≥ 0 | Minimum precursor mass (SE.MinPrecursorMass) |
| `MaxPrecursorMass` | `float` | `5000.0` | ≥ 0 | Maximum precursor mass (SE.MaxPrecursorMass) |
| `extra_params` | `str` | `` | — | Escape hatch: extra `key = value` lines appended to dia-pseudo_se.params (newline or ';' separated). Also how a V_SWATH variable-window table is supplied. |

## `dia-features`

版本：`2.2.1`

输入：`.d`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `ram_gb` | `int` | `16` | ≥ 1 | JVM heap (-Xmx<N>G) |
| `threads` | `int` | `8` | ≥ 1 | Worker threads (--threadNum) |
| `deltaApexIM` | `float` | `0.01` | ≥ 0 | Ion-mobility Δ for MS1/MS2 apex match (--deltaApexIM) |
| `deltaApexRT` | `int` | `3` | ≥ 0 | Apex-scan Δ range for MS1/MS2 match (--deltaApexRT, integer scans) |
| `ms1MS2Corr` | `float` | `0.3` | ≥ 0; ≤ 1 | MS1/MS2 correlation threshold (--ms1MS2Corr) |
| `massDefectFilter` | `bool` | `True` | — | Apply mass-defect filter (--massDefectFilter) |
| `massDefectOffset` | `float` | `0.1` | ≥ 0 | Mass-defect offset (--massDefectOffset) |
| `RFMax` | `int` | `500` | ≥ 1 | Top-N peaks per spectrum (--RFMax) |
| `writeInter` | `bool` | `False` | — | Write intermediate files (--writeInter) |
| `bruker_lib_dir` | `str` | `镜像内置（无需填写）` | — | Path to ext/bruker dir containing libtimsdata-*.so (JVM -Dlibs.bruker.dir) |

## `speclib-build`

版本：`0.1.59`

输入：`.xml`, `.pepxml`, `.mzML`, `.mzXML`, `.tsv`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `max_delta_unimod` | `float` | `0.02` | ≥ 0 | Maximum Δ mass (Da) for UniMod annotation |
| `max_delta_ppm` | `float` | `15.0` | ≥ 0 | Maximum Δ mass (ppm) for UniMod annotation |
| `max_psm_pep` | `float` | `—` | ≥ 0; ≤ 1 | Maximum PSM posterior-error probability for inclusion. Unset = speclib-build's own default, which differs per subcommand (0.5 for `convert`, 1 for `convertpsm`) — workflow suite passes neither, so a single value here silently over-filtered the glyco-DIA libraries |
| `fragment_types` | `str_list` | `["b", "y"]` | — | Allowed fragment ion types (a,b,c,x,y,z) |
| `fragment_charges` | `str_list` | `["1", "2", "3", "4"]` | — | Allowed fragment ion charges |
| `enable_specific_losses` | `bool` | `False` | — | Enable specific (residue-tied) fragment ion losses |
| `enable_unspecific_losses` | `bool` | `False` | — | Enable unspecific fragment ion losses |
| `rt_lowess_fraction` | `float` | `0.05` | ≥ 0; ≤ 1 | LOWESS smoothing fraction for RT calibration (0 = cross-validate) |
| `im_lowess_fraction` | `float` | `0.05` | ≥ 0; ≤ 1 | LOWESS smoothing fraction for IM calibration |
| `psm_fdr_threshold` | `float` | `0.01` | ≥ 0; ≤ 1 | PSM FDR cutoff |
| `peptide_fdr_threshold` | `float` | `0.01` | ≥ 0; ≤ 1 | Peptide FDR cutoff |
| `protein_fdr_threshold` | `float` | `0.01` | ≥ 0; ≤ 1 | Protein FDR cutoff |
| `perform_rt_calibration` | `bool` | `True` | — | Perform RT alignment across runs |
| `perform_im_calibration` | `bool` | `True` | — | Perform IM alignment (timsTOF runs) |
| `nofdr` | `bool` | `False` | — | Skip FDR reassessment (assume custom upstream FDR filtering) |
| `diannpqp` | `bool` | `False` | — | Emit DIA engine2-compatible PQP library alongside the TSV |
| `unimod_xml` | `str` | `` | — | UniMod XML used for modification annotation (--unimod); empty = spectral library builder's bundled copy |
| `exclude_range` | `str` | `-1.5,3.5` | — | Mass-difference range NOT mapped to UniMod (--exclude-range), e.g. `-1.5,3.5` |
| `enable_unannotated` | `bool` | `True` | — | Keep delta masses that have no UniMod match (--enable_unannotated) |
| `enable_massdiff` | `bool` | `False` | — | Map mass differences reported by legacy search engines (--enable_massdiff) |
| `precision_digits` | `int` | `—` | ≥ 0 | Digits of product m/z precision in the library (--precision_digits); unset = 6 |
| `convert_from_psm` | `bool` | `False` | — | Build the library from psm.tsv via `speclib-build convertpsm` instead of pepXML via `speclib-build convert` |
| `decoy_prefix` | `str` | `rev_` | — | Database decoy prefix used to flag decoy PSMs (--decoy_prefix, convertpsm only) |
| `labile_mods` | `str` | `` | — | Adjust fragment masses of labile (glyco) modifications — one of oglyc / nglyc / nglyc+ (--labile_mods, convertpsm only); empty = regular, non-glyco |
| `max_glycan_q` | `float` | `1.0` | ≥ 0; ≤ 1 | Maximum glycan q-value for a PSM to enter the library (--max_glycan_q, convertpsm only) |
| `rt_reference` | `str` | `` | — | iRT/CiRT reference file for RT alignment (--rt_reference) |
| `rt_filter` | `str` | `` | — | Tag used to pick candidate RT reference runs (--rt_filter) |
| `rt_psm_fdr_threshold` | `float` | `—` | ≥ 0; ≤ 1 | PSM FDR used for RT alignment (--rt_psm_fdr_threshold); unset = 0.001 |
| `im_reference` | `str` | `` | — | IM reference file for ion-mobility alignment (--im_reference) |
| `im_filter` | `str` | `` | — | Tag used to pick candidate IM reference runs (--im_filter) |
| `im_psm_fdr_threshold` | `float` | `—` | ≥ 0; ≤ 1 | PSM FDR used for IM alignment (--im_psm_fdr_threshold); unset = 0.001 |
| `min_peptides` | `int` | `—` | ≥ 1 | Minimum peptides required for a successful alignment (--min_peptides); unset = 5 |
| `pi0_lambda` | `str` | `` | — | Non-parametric p-value estimation `<START> <END> <STEPS>` (--pi0_lambda), e.g. `0.1 0.5 0.05`, or `0.4 0 0` for a fixed value |
| `proteotypic` | `bool` | `True` | — | Keep only proteotypic (unique, non-shared) peptides |
| `consensus` | `bool` | `True` | — | Build consensus spectra instead of picking the best replicate |
| `extra_convert_cmdline` | `str` | `` | — | Escape hatch: extra flags for each `speclib-build convert` call |
| `extra_library_cmdline` | `str` | `` | — | Escape hatch: extra flags for the `speclib-build library` call |

## `glyco-localize`

版本：`1.0.0`

输入：`.tsv`, `.mzML`, `.mzXML`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `ms1_tol` | `float` | `20.0` | ≥ 0 | Precursor mass tolerance (ppm) — CMD -c |
| `ms2_tol` | `float` | `20.0` | ≥ 0 | Product-ion mass tolerance (ppm) — CMD -b |
| `glyco_db` | `str` | `HexNAc(1),HexNAc(1)Hex(1),HexNAc(1)NeuAc(1),HexNAc(2)Hex(1),HexNAc(1)Hex(1)NeuAc(1),HexNAc(2)Hex(2),HexNAc(2)Hex(1)NeuAc(1),HexNAc(1)Hex(1)NeuAc(2),HexNAc(2)Hex(2)NeuAc(1),HexNAc(2)Hex(2)Fuc(1)NeuAc(1),HexNAc(2)Hex(2)NeuAc(2),HexNAc(2)Hex(2)Fuc(1)NeuAc(2)` | — | O-glycan composition list (comma-separated, workflow suite Byonic syntax) — CMD -g |
| `max_glycans` | `int` | `4` | ≥ 1 | Maximum glycans per PSM — CMD -n |
| `min_isotope_error` | `int` | `0` | — | Min isotope-error offset — CMD -i |
| `max_isotope_error` | `int` | `2` | — | Max isotope-error offset — CMD -j |
| `filter_oxonium` | `bool` | `False` | — | Enable oxonium-ion based glycan filtering — CMD -f |
| `oxonium_filter_file` | `str` | `` | — | Custom oxonium rules file path (empty = use CMD's default list) |
| `oxonium_min_intensity` | `float` | `0.05` | ≥ 0; ≤ 1 | Minimum relative oxonium intensity for filtering (0-1) — CMD -m |
| `threads` | `int` | `0` | ≥ 0 | Worker threads (0 = auto) — CMD -t |
| `glycan_residues_file` | `str` | `镜像内置（无需填写）` | — | Glycan residue definitions (workflow suite Glycan_Databases) — CMD -x |
| `glycan_mods_file` | `str` | `镜像内置（无需填写）` | — | Glycan modification definitions (workflow suite Glycan_Databases) — CMD -y |
| `dotnet_bin` | `str` | `镜像内置（无需填写）` | — | .NET 6 runtime executable |
| `activation1` | `str` | `HCD` | — | Primary scan activation for PairScans (glycan/oxonium scan) |
| `activation2` | `str` | `ETD` | — | Paired scan activation for PairScans (peptide-backbone scan) |
| `verbosity` | `enum` | `normal` | 枚举: none, minimal, normal | How much CMD writes to the log — CMD -v |
| `extra_cmdline` | `str` | `` | — | Escape hatch: extra glyco localizer CMD flags appended verbatim |

## `predict-rescore`

版本：`1.4.14`

输入：`.pin`, `.mzML`, `.mzXML`, `.params`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `ram_gb` | `int` | `16` | — | Java heap (-XmxN G) |
| `num_threads` | `int` | `8` | — | Worker threads (numThreads) |
| `diann_path` | `str` | `镜像内置（无需填写）` | — | Path to local DIA engine binary |
| `use_rt` | `bool` | `True` | — | Predict RT (useRT) |
| `use_spectra` | `bool` | `True` | — | Predict spectra (useSpectra) |
| `use_im` | `bool` | `False` | — | Predict ion mobility (useIM) |
| `rt_model` | `str` | `DIA engine` | — | RT prediction model (rtModel) |
| `spectra_model` | `str` | `DIA engine` | — | Spectra prediction model (spectraModel) |
| `unimod_obo` | `str` | `镜像内置（无需填写）` | — | Path to unimod.obo for modification lookup |
| `msbooster_jar` | `str` | `镜像内置（无需填写）` | — | Path to rescoring predictor jar |
| `batmass_io_jar` | `str` | `镜像内置（无需填写）` | — | Path to spectrum IO jar (required for mzML reading) |
| `im_model` | `str` | `DIA engine` | — | Ion-mobility prediction model (imModel) |
| `use_koina` | `bool` | `False` | — | Use a remote Koina server for predictions instead of the local DIA engine (useKoina). Requires koina_url and network access from the sandbox |
| `koina_url` | `str` | `` | — | Koina server URL (KoinaURL); only used when use_koina is on |
| `find_best_rt_model` | `bool` | `False` | — | Benchmark the available RT models and keep the best (findBestRtModel) |
| `find_best_spectra_model` | `bool` | `False` | — | Benchmark the available spectra models and keep the best (findBestSpectraModel) |
| `find_best_im_model` | `bool` | `False` | — | Benchmark the available IM models and keep the best (findBestImModel) |
| `fragmentation_type` | `str` | `auto` | — | Fragmentation type passed to the predictor (FragmentationType): auto, HCD, CID, ETD, ETHCD, … |
| `instrument` | `str` | `` | — | Instrument type hint for the predictor (instrument), e.g. `QE`, `LUMOS`, `TIMSTOF` |
| `ppm_tolerance` | `float` | `—` | ≥ 0 | Fragment matching tolerance in ppm (ppmTolerance); unset = rescoring predictor default 20 |
| `use_detect` | `bool` | `False` | — | Add detectability features (useDetect) |
| `features` | `str` | `` | — | Explicit feature list written into the pin (features), comma-separated. Empty = rescoring predictor's default feature set |
| `delete_predictions` | `bool` | `False` | — | Delete prediction files after the run (deletePreds) |
| `extra_params` | `str` | `` | — | Escape hatch: extra `key = value` lines appended to predict-rescore_params.txt (newline or ';' separated). Covers the remaining ~100 rescoring predictor keys |

## `psm-integrate`

版本：`5.1.0`

输入：`.pepXML`, `.pep.xml`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `decoy_prefix` | `str` | `rev_` | — | Decoy sequence tag (--decoy) |
| `min_prob` | `float` | `0.0` | — | Minimum probability of results to report (--minProb) |
| `num_threads` | `int` | `4` | — | Worker threads (--threads) |
| `output_prefix` | `str` | `interact.iproph` | — | Output name prefix (--output); produces <prefix>.pep.xml |
| `length` | `bool` | `False` | — | Use Peptide Length model (--length) |
| `sharpnse` | `bool` | `False` | — | Use more discriminating NSE model for SWATH (--sharpnse) |
| `no_fpkm` | `bool` | `False` | — | Disable FPKM model (--nofpkm) |
| `no_nrs` | `bool` | `False` | — | Disable NRS model (--nonrs) |
| `no_nse` | `bool` | `False` | — | Disable NSE model (--nonse) |
| `no_nsi` | `bool` | `False` | — | Disable NSI model (--nonsi) |
| `no_nsm` | `bool` | `False` | — | Disable NSM model (--nonsm) |
| `no_nsp` | `bool` | `False` | — | Disable NSP model (--nonsp) |
| `no_nss` | `bool` | `False` | — | Disable NSS model (--nonss) |

## `protein-infer`

版本：`5.1.0`

输入：`.pepXML`, `.pep.xml`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `max_ppm_diff` | `int` | `2000000` | — | Max peptide mass difference (ppm) for protein grouping (--maxppmdiff). workflow suite baseline uses 2000000 (effectively disabled — group only on sequence). |
| `min_prob` | `float` | `0.05` | — | Minimum peptide probability to include (--minprob) |
| `output_prefix` | `str` | `combined` | — | Output filename prefix (--output); produces <prefix>.prot.xml. workflow suite baseline uses 'combined'. |
| `iprophet` | `bool` | `False` | — | Tell protein-infer input is from PSM integrator (--psm-integrate) |
| `no_nsp` | `bool` | `False` | — | Disable NSP model (--nonsp) |
| `subgroups` | `bool` | `False` | — | Enable subgroups (--subgroups; baseline omits → no groups) |
| `unmapped` | `bool` | `False` | — | Report UNMAPPED proteins (--unmapped) |
