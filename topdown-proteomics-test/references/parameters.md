# Top-down 参数参考

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

## `topfd`

版本：`1.8.1`

输入：`.mzML`, `.mzXML`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `activation` | `enum` | `FILE` | 枚举: FILE, CID, ETD, HCD, MPD, UVPD | MS/MS activation |
| `max_charge` | `int` | `30` | — | Maximum charge |
| `max_mass` | `float` | `70000.0` | — | Maximum mass |
| `mz_error` | `float` | `0.02` | — | m/z tolerance (Da) |
| `ms_one_sn_ratio` | `float` | `3.0` | — | MS1 S/N ratio |
| `ms_two_sn_ratio` | `float` | `1.0` | — | MS2 S/N ratio |
| `precursor_window` | `float` | `3.0` | — | Precursor window (m/z) |
| `thread_number` | `int` | `4` | ≥ 1 | Thread count |
| `use_msdeconv` | `bool` | `False` | — | Use MS-Deconv score instead of the default EnvCNN scorer |
| `env_cnn_cutoff` | `float` | `0.0` | ≥ 0.0; ≤ 1.0 | EnvCNN score cutoff for MS/MS envelopes [0,1] |
| `ecscore_cutoff` | `float` | `0.1` | ≥ 0.0; ≤ 1.0 | ECScore cutoff for proteoform features [0,1] |
| `min_scan_number` | `int` | `1` | 枚举: 1, 2, 3 | Minimum MS1 scans for a proteoform feature (1\|2\|3) |
| `split_intensity_ratio` | `float` | `2.5` | > 0.0 | Intensity ratio required to split a feature |
| `missing_level_one` | `bool` | `False` | — | Missing MS1 spectra |
| `single_scan_noise` | `bool` | `False` | — | Use per-MS1-scan noise instead of LC-MS-wide noise |
| `disable_additional_feature_search` | `bool` | `False` | — | Disable the additional proteoform feature search |
| `disable_frag_num_filtering` | `bool` | `False` | — | Skip MS/MS fragment-number-based envelope filtering |
| `skip_html_folder` | `bool` | `False` | — | Skip HTML folder |
| `extra_cmdline` | `str` | `` | — | Escape hatch: extra topfd arguments inserted before the spectrum file (shell-quoted) |

## `toppic`

版本：`1.8.1`

输入：`.fasta`, `.fa`, `.msalign`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `activation` | `enum` | `FILE` | 枚举: FILE, CID, ETD, HCD, MPD, UVPD | Activation type |
| `fixed_mod` | `str` | `—` | — | Fixed modification (C57\|C58\|<file>) |
| `n_terminal_form` | `str` | `—` | — | Allowed N-terminal forms (comma list of NONE/NME/NME_ACETYLATION/M_ACETYLATION) |
| `proteoform_type` | `str` | `—` | — | Allowed proteoform types (comma list of COMPLETE/PREFIX/SUFFIX/INTERNAL) |
| `thread_number` | `int` | `4` | ≥ 1 | Thread count |
| `mass_error_tolerance` | `float` | `—` | — | Mass error tolerance (ppm); when lookup_table=true must be 5, 10, or 15 |
| `num_shift` | `int` | `—` | 枚举: 0, 1, 2 | Maximum unexpected modifications per PrSM (0\|1\|2) |
| `min_shift` | `int` | `—` | — | Min shift (Da) |
| `max_shift` | `int` | `—` | — | Max shift (Da) |
| `variable_ptm_num` | `int` | `—` | — | Maximum variable modifications per PrSM |
| `variable_ptm_file_name` | `str` | `—` | — | Variable modification file |
| `proteoform_error_tolerance` | `float` | `—` | — | Proteoform cluster error tolerance (Da) |
| `spectrum_cutoff_type` | `enum` | `—` | 枚举: EVALUE, FDR | Spectrum cutoff type |
| `spectrum_cutoff_value` | `float` | `—` | — | Spectrum cutoff value |
| `proteoform_cutoff_type` | `enum` | `—` | 枚举: EVALUE, FDR | Proteoform cutoff type |
| `proteoform_cutoff_value` | `float` | `—` | — | Proteoform cutoff value |
| `num_combined_spectra` | `int` | `—` | — | Number of combined spectra (alternating fragmentation) |
| `mod_file_name` | `str` | `—` | — | Local PTM (common modification) file for unexpected-shift characterization |
| `miscore_threshold` | `float` | `—` | ≥ 0.0; ≤ 1.0 | Modification identification score threshold [0,1] |
| `decoy` | `bool` | `False` | — | Use decoy search |
| `approximate_spectra` | `bool` | `False` | — | Use approximate spectra for protein filtering (faster, may reduce sensitivity) |
| `lookup_table` | `bool` | `False` | — | Use lookup table for p/E-values; requires mass_error_tolerance ∈ {5, 10, 15} ppm |
| `no_topfd_feature` | `bool` | `False` | — | No TopFD feature handoff |
| `skip_html_folder` | `bool` | `False` | — | Skip HTML folder |
| `keep_temp_files` | `bool` | `False` | — | Keep temp files |
| `keep_decoy_ids` | `bool` | `False` | — | Keep decoy IDs |
| `combined_file_name` | `str` | `—` | — | Combined output name |
| `msalign_preflight_blocks` | `int` | `10` | — | Msalign preflight sample blocks |
| `extra_cmdline` | `str` | `` | — | Escape hatch: extra toppic arguments inserted before the fasta/msalign positional arguments (shell-quoted) |

## `flashdeconv`

版本：`3.5.0`

输入：`.mzML`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `write_msalign1` | `bool` | `True` | — | Emit MS1 msalign (TopFD/TopPIC compatible) |
| `write_msalign2` | `bool` | `True` | — | Emit MS2 msalign (TopFD/TopPIC compatible) |
| `write_feature1` | `bool` | `True` | — | Emit MS1 feature file (TopFD compatible) |
| `write_feature2` | `bool` | `True` | — | Emit MS2 feature file (TopFD compatible) |
| `write_spec1` | `bool` | `False` | — | Emit MS1 deconvolved spectrum TSV |
| `write_spec2` | `bool` | `False` | — | Emit MS2 deconvolved spectrum TSV |
| `write_spec3` | `bool` | `False` | — | Emit MS3 deconvolved spectrum TSV |
| `write_spec4` | `bool` | `False` | — | Emit MS4 deconvolved spectrum TSV |
| `write_deconv_mzml` | `bool` | `False` | — | Emit deconvolved mzML (all MS levels) |
| `write_annotated_mzml` | `bool` | `False` | — | Emit annotated mzML retaining original peaks |
| `write_quant_tsv` | `bool` | `False` | — | Emit isobaric quantification TSV |
| `keep_empty_out` | `bool` | `False` | — | Retain empty TSV outputs |
| `write_detail` | `bool` | `False` | — | Include detailed peak info in spectrum TSVs |
| `mzml_mass_charge` | `int` | `—` | 枚举: -1, 0, 1 | Charge state for masses in deconv mzML output |
| `min_mz` | `float` | `—` | — | Minimum peak m/z |
| `max_mz` | `float` | `—` | — | Maximum peak m/z |
| `min_rt` | `float` | `—` | — | Minimum retention time (min) |
| `max_rt` | `float` | `—` | — | Maximum retention time (min) |
| `max_ms_level` | `int` | `—` | — | Maximum MS level (inclusive) |
| `threads` | `int` | `4` | ≥ 1 | Thread count |
| `debug` | `int` | `—` | — | Debug log level |
| `log_file` | `str` | `—` | — | Optional log file path |
| `ini_file` | `str` | `—` | — | Optional TOPP INI file path |
| `no_progress` | `bool` | `False` | — | Disable progress logging |
| `force` | `bool` | `False` | — | Override tool-specific checks |
| `fd_ida_log` | `str` | `—` | — | Path to FLASHIda log for acquisition coupling |
| `fd_report_fdr` | `bool` | `False` | — | Report q-values via decoy FDR (Beta) |
| `fd_allowed_isotope_error` | `int` | `—` | — | Allowed isotope index error in FDR calculation |
| `fd_use_rna_averagine` | `bool` | `False` | — | Use RNA averagine model |
| `fd_precursor_ms1_window` | `int` | `—` | ≥ 1 | MS1 spectra window around each MS2 for precursor search |
| `fd_isolation_window` | `float` | `—` | — | Fallback precursor isolation window width |
| `fd_merging_method` | `int` | `—` | 枚举: 0, 1, 2 | Spectrum merging method (0=none, 1=Gaussian, 2=block) |
| `fd_merging_min_ms_level` | `int` | `—` | ≥ 1 | Minimum MS level participating in merge |
| `fd_merging_max_ms_level` | `int` | `—` | ≥ 1 | Maximum MS level participating in merge |
| `sd_tol` | `str_list` | `[]` | — | PPM tolerance per MS level (e.g. ['10.0','5.0']); negative = auto |
| `sd_min_mass` | `float` | `—` | — | Minimum mass (Da) |
| `sd_max_mass` | `float` | `—` | — | Maximum mass (Da) |
| `sd_min_charge` | `int` | `—` | — | Minimum MS1 charge state |
| `sd_max_charge` | `int` | `—` | — | Maximum charge state (all MS levels) |
| `sd_precursor_charge` | `int` | `—` | — | Target precursor charge state |
| `sd_precursor_mz` | `float` | `—` | — | Target precursor m/z (requires sd_precursor_charge) |
| `sd_min_cos` | `str_list` | `[]` | — | Cosine similarity threshold per MS level (e.g. ['0.85','0.85']) |
| `sd_min_snr` | `str_list` | `[]` | — | Charge SNR threshold per MS level (e.g. ['0.25','0.25']) |
| `ft_mass_error_ppm` | `float` | `—` | — | Mass error tolerance (ppm); negative reuses SD:tol[0] |
| `ft_ion_mobility_tolerance` | `float` | `—` | — | Ion mobility tolerance (1/k0) |
| `ft_quant_method` | `enum` | `—` | 枚举: area, median, max_height | Quantification method |
| `ft_min_sample_rate` | `float` | `—` | — | Min fraction of scans containing a peak |
| `ft_min_trace_length` | `float` | `—` | — | Min mass trace length (s) |
| `ft_max_trace_length` | `float` | `—` | — | Max mass trace length (s); negative disables |
| `ft_min_cos` | `float` | `—` | — | Cosine similarity threshold; negative reuses SD:min_cos[0] |
| `iq_type` | `enum` | `—` | 枚举: none, itraq4plex, itraq8plex, tmt6plex, tmt10plex, tmt11plex, tmt16plex, tmt18plex | Isobaric quantification scheme |
| `iq_isotope_correction` | `enum` | `—` | 枚举: true, false | Enable isotope correction |
| `iq_reporter_mz_tol` | `float` | `—` | — | Reporter ion m/z tolerance (Th) |
| `iq_only_fully_quantified` | `bool` | `False` | — | Only spectra with all channels quantified |
| `extra_cmdline` | `str` | `` | — | Escape hatch: extra FLASHDeconv arguments appended verbatim (shell-quoted), e.g. '-instance 2' |

## `pbfgen`

版本：`1.1.7867`

输入：`.raw`, `.mzML`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `start_scan` | `int` | `—` | — | Start scan number (negative or omitted = no limit) |
| `end_scan` | `int` | `—` | — | End scan number (negative or omitted = no limit) |
| `param_file` | `str` | `—` | — | Optional PRISM-style INI parameter file |
| `extra_cmdline` | `str` | `` | — | Escape hatch: extra PbfGen arguments appended verbatim (shell-quoted). Use the 'key=value' form for any absolute path — PRISM parses a leading '/' as a flag. |

## `promex`

版本：`1.1.7867`

输入：`.pbf`, `.mzML`, `.raw`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `min_charge` | `int` | `—` | ≥ 1; ≤ 60 | Minimum precursor charge |
| `max_charge` | `int` | `—` | ≥ 1; ≤ 60 | Maximum precursor charge |
| `min_mass` | `float` | `—` | ≥ 600; ≤ 100000 | Minimum mass (Da) |
| `max_mass` | `float` | `—` | ≥ 600; ≤ 100000 | Maximum mass (Da) |
| `max_threads` | `int` | `4` | ≥ 0 | Max threads (0 = auto) |
| `bin_res_ppm` | `int` | `—` | 枚举: 1, 2, 4, 8, 16, 32, 64, 128 | Binning resolution (ppm) |
| `score_threshold` | `float` | `—` | — | Likelihood score threshold (default -10) |
| `feature_map` | `bool` | `False` | — | Output PNG heatmap; default OFF because OxyPlot crashes under wine and the PNG is unviewable on headless Linux anyway. Set true only if running on a desktop with X11. |
| `score_extended` | `bool` | `—` | — | Output extended scoring info |
| `write_csv` | `bool` | `—` | — | Also write features to CSV |
| `param_file` | `str` | `—` | — | Optional PRISM INI parameter file |
| `extra_cmdline` | `str` | `` | — | Escape hatch: extra ProMex arguments appended verbatim (shell-quoted), e.g. '-ms1ft=.' to only render the feature heatmap. Use the 'key=value' form for any absolute path — PRISM parses a leading '/' as a flag. |

## `mspathfindert`

版本：`1.1.7867`

输入：`.pbf`, `.mzML`, `.raw`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|---|---|---|---|---|
| `ic_mode` | `enum` | `—` | 枚举: NoInternalCleavage, SingleInternalCleavage, MultipleInternalCleavages | Internal cleavage mode |
| `tda` | `int` | `1` | ≥ -1; ≤ 1 | Decoy mode: 0=target only, 1=target+shuffled decoy |
| `pm_tolerance` | `float` | `10.0` | — | Precursor tolerance (ppm) |
| `frag_tolerance` | `float` | `10.0` | — | Fragment tolerance (ppm) |
| `min_length` | `int` | `21` | ≥ 0 | Min sequence length |
| `max_length` | `int` | `500` | ≥ 0 | Max sequence length |
| `min_mass` | `float` | `3000.0` | — | Min sequence mass (Da) |
| `max_mass` | `float` | `50000.0` | — | Max sequence mass (Da) |
| `min_charge` | `int` | `2` | ≥ 1 | Min precursor charge |
| `max_charge` | `int` | `50` | ≥ 1 | Max precursor charge |
| `min_frag_charge` | `int` | `1` | ≥ 1 | Min fragment ion charge |
| `max_frag_charge` | `int` | `20` | ≥ 1 | Max fragment ion charge |
| `activation` | `enum` | `—` | 枚举: CID, ETD, HCD, ECD, PQD, UVPD, Unknown | Activation method (Unknown if absent) |
| `tag_search` | `bool` | `—` | — | Enable tag-based search (default true) |
| `include_decoys` | `bool` | `—` | — | Include decoy rows in _IcTda.tsv |
| `num_matches` | `int` | `—` | — | Matches per spectrum |
| `mem_matches` | `int` | `—` | — | Matches kept in memory for E-value calc |
| `mod_file` | `str` | `—` | — | Path to PNNL modification definition file |
| `scans_file` | `str` | `—` | — | Optional file restricting MS2 scans to process |
| `overwrite` | `bool` | `—` | — | Overwrite existing _IcTarget/_IcDecoy.tsv |
| `flip_scoring` | `bool` | `—` | — | Use FLIP scoring (UVPD support) |
| `threads` | `int` | `4` | ≥ 0 | Thread count (0 = auto) |
| `param_file` | `str` | `—` | — | Optional PRISM INI parameter file. NOTE: any value we send on the command line overrides the same key in this file, and the defaults above are always sent — so the file only takes effect for keys we do not emit. |
| `extra_cmdline` | `str` | `` | — | Escape hatch: extra MSPathFinderT arguments appended verbatim (shell-quoted). Use the 'key=value' form for any absolute path — PRISM parses a leading '/' as a flag. |
