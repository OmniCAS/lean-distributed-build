# 示例仓库：按规模分档

给分阶段验证（`TODO.md`）挑仓库用。这里有 141 个仓库的行数，其中 73 个有依赖图统计；全部是静态统计，没有构建。
数据：[`repos.json`](repos.json)（全部字段）、[`repos.tsv`](repos.tsv)（同一份，表格）。

第三方仓库只在隔离环境里构建（无外网、无凭据）：构建会执行仓库里的元程序。

## 五档

| 档 | 行数 | 已统计 | 文件数（中位） | 构建量的参照 |
|---|---|---:|---:|---|
| T0 入门 | 不到 1 万行 | 51 | 25 | 未测。自身只有几个到一两百个文件，量级是秒到几分钟 |
| T1 万级 | 1 万–10 万行 | 51 | 182 | PFR（连同依赖 AddCombi 共 86 个模块）原版 `lake build` 58 秒（一台 12 核 macOS 机器，Mathlib 取现成缓存） |
| T2 十万级 | 10 万–100 万行 | 25 | 1,238 | 未测，介于上下两档之间 |
| T3 百万级 | 100 万–1,000 万行 | 7 | 12,734 | Mathlib 实测 12.0 核·时：16 核单机 46 分钟，两机各 16 核 23 分钟。Tau Ceti 模型约 57 核·时 |
| T4 千万级 | 1,000 万行以上 | 7 | 80,145 | 黎曼猜想归档模型约 475 核·时。CFSG 作者报告单机 22.5 小时（32 线程），产物 208 GB |

构建量主要由两项决定：行数，以及文件数乘每个文件的固定导入开销（导入整个 Mathlib 约 6 秒）。所以同一档里文件多而小的仓库更重。

## 梯度示例

每档几个，从上到下越来越大。链接是上游原始仓库，“提交”是统计时的版本。

| 档 | 仓库 | 提交 | 行数 | 文件数 | 链深 | 可并行度（估） | 工具链 | 依赖 Mathlib | 说明 |
|---|---|---|---:|---:|---:|---:|---|---|---|
| T0 | [leanprover/lean4-cli](https://github.com/leanprover/lean4-cli) | [`c24fe60`](https://github.com/leanprover/lean4-cli/tree/c24fe6078c630e89b489bffe59b3e20ac30d12c8) | 2,353 | 5 | 4 | 1.1 | v4.35.0 | 否 | 无依赖，最小的冒烟测试 |
| T0 | [leanprover-community/quote4](https://github.com/leanprover-community/quote4) | [`dce0ad7`](https://github.com/leanprover-community/quote4/tree/dce0ad79c486cb1fb504af04f953c3466b0c6db8) | 2,557 | 28 | 8 | 1.5–2.2 | v4.35.0 | 否 | 无依赖 |
| T0 | [leanprover-community/import-graph](https://github.com/leanprover-community/import-graph) | [`a41f0e9`](https://github.com/leanprover-community/import-graph/tree/a41f0e9a4dea23188ea9cc1c41ac9f8bbafe0b93) | 7,593 | 86 | 13 | 3.6–5.4 | v4.35.0 | 否 | 只依赖 Cli |
| T0 | [jsm28/IMOLean](https://github.com/jsm28/IMOLean) | [`bd4d0e1`](https://github.com/jsm28/IMOLean/tree/bd4d0e1f8560cda44a30fa3e826df21a4acc97f0) | 1,443 | 39 | 2 | 10–16 | v4.36.0-rc2 | 是 | 依赖 Mathlib 的最小例子 |
| T0 | [PatrickMassot/GlimpseOfLean](https://github.com/PatrickMassot/GlimpseOfLean) | [`7dc8169`](https://github.com/PatrickMassot/GlimpseOfLean/tree/7dc816910638406f4232d23977bbcc59a335393c) | 7,169 | 28 | — | — | v4.27.0 | 是 | 教学仓库，练习里有 `sorry`，构建会有警告 |
| T1 | [leanprover-community/batteries](https://github.com/leanprover-community/batteries) | [`87486d5`](https://github.com/leanprover-community/batteries/tree/87486d547af639cb39c01f0d2f8025aa47d7dde1) | 33,484 | 262 | 14 | 7.5–11 | v4.37.0-rc1 | 否 | 不依赖 Mathlib，从零构建 |
| T1 | [teorth/pfr](https://github.com/teorth/pfr) | [`1ef23c3`](https://github.com/teorth/pfr/tree/1ef23c3c5a83db690fe3b3b5c2e8299fae17b81a) | 21,990 | 76 | 20 | 2.3–2.6 | v4.36.0-rc2 | 是 | **阶段 1 已通过**（单机四条标准），命令见 `bench/README.md` 第 5 节 |
| T1 | [fpvandoorn/carleson](https://github.com/fpvandoorn/carleson) | [`f7487cc`](https://github.com/fpvandoorn/carleson/tree/f7487cc9da4d1e73f009dc0280cd5b958f3e2c78) | 50,325 | 128 | 30 | 3.0–3.2 | v4.36.0-rc1 | 是 | 阶段 1 待跑 |
| T1 | [ImperialCollegeLondon/FLT](https://github.com/ImperialCollegeLondon/FLT) | [`0198058`](https://github.com/ImperialCollegeLondon/FLT/tree/019805815d7da565ed1e9f427b6fbd0cbc9d00d3) | 59,080 | 271 | 18 | 8.1–9.6 | v4.35.0 | 是 |  |
| T1 | [leanprover/cslib](https://github.com/leanprover/cslib) | [`1ed150d`](https://github.com/leanprover/cslib/tree/1ed150d1cec92cd4368d4f7257c73c77e1d00b89) | 55,907 | 358 | 19 | 12–15 | v4.37.0-rc1 | 是 |  |
| T2 | [AlexKontorovich/PrimeNumberTheoremAnd](https://github.com/AlexKontorovich/PrimeNumberTheoremAnd) | [`a4fb698`](https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/tree/a4fb6989b07e9c76b511807ae93e33e25b820e9b) | 172,577 | 235 | 20 | 5.2–5.6 | v4.35.0 | 是 | 文件少而大，平均每个 700 多行 |
| T2 | [teorth/equational_theories](https://github.com/teorth/equational_theories) | [`b4b3c42`](https://github.com/teorth/equational_theories/tree/b4b3c42da2d21b858acb5dab7e90924c1396f73e) | 168,239 | 1,347 | 19 | 9.6–16 | v4.29.1 | 是 | 很宽，最宽一层 1,218 个模块 |
| T2 | [AxiomMath/Weil](https://github.com/AxiomMath/Weil) | [`27cdb20`](https://github.com/AxiomMath/Weil/tree/27cdb2049be62ee2911429b47f54774078450e32) | 214,139 | 980 | 17 | 23–28 | v4.34.0-rc2 | 是 |  |
| T2 | [leanprover-community/physlib](https://github.com/leanprover-community/physlib) | [`8c87bdf`](https://github.com/leanprover-community/physlib/tree/8c87bdfb015de47e82da811567aaa7a2a05353f4) | 462,570 | 1,683 | 83 | 12–14 | v4.35.0 | 是 |  |
| T2 | [openai/NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler) | [`f9e8bc5`](https://github.com/openai/NavierStokesAndEuler/tree/f9e8bc5b38b6e212696e8a30e3e91517af887bbd) | 643,991 | 2,659 | 97 | 9.5–12 | v4.34.0-rc2 | 是 |  |
| T2 | [provables/sequencelib](https://github.com/provables/sequencelib) | [`dfb06c1`](https://github.com/provables/sequencelib/tree/dfb06c18bba196b5aa5bcb3725fe9d201fb9a61a) | 859,926 | 25,905 | 9 | 410–1,150 | v4.30.0 | 是 | 2.6 万个小文件（平均 33 行），预计每个文件的固定导入开销占主导，是黎曼猜想归档的小号对照 |
| T3 | [leanprover-community/mathlib4](https://github.com/leanprover-community/mathlib4) | [`5f78f9c`](https://github.com/leanprover-community/mathlib4/tree/5f78f9ce46fc85fa3cb45561d47b489c4c98cd04) | 2,476,531 | 9,345 | 181 | 23–27 | v4.37.0-rc1 | 自身 | **已实测**。基准钉在 `v4.34.0`（默认目标 8,908 个模块），这里的行数是 11 月 19 日的快照 |
| T3 | [AxiomMath/MMP](https://github.com/AxiomMath/MMP) | [`1f9ade3`](https://github.com/AxiomMath/MMP/tree/1f9ade367087ec711a2ce1382bad279a5a0284c3) | 2,056,546 | 2,269 | 136 | 8.9–9.4 | v4.35.0 | 是 | 依赖 Stacks，要先有 Stacks 的产物 |
| T3 | [TauCetiProject/TauCeti](https://github.com/TauCetiProject/TauCeti) | [`aa3cfad`](https://github.com/TauCetiProject/TauCeti/tree/aa3cfad1274c06cff25f2b58848498b3c3f68d0f) | 7,954,869 | 34,782 | 50 | 400–470 | v4.36.0 | 是 | 模型约 57 核·时，未构建 |
| T3 | [Vilin97/lean-pool](https://github.com/Vilin97/lean-pool) | [`01db1d7`](https://github.com/Vilin97/lean-pool/tree/01db1d7049cf9668bda1e9e106875ee1278b43e6) | 9,956,631 | 22,324 | 250 | 15–17 | v4.35.0-rc3 | 是 |  |
| T4 | [AxiomMath/Stacks](https://github.com/AxiomMath/Stacks) | [`f56a316`](https://github.com/AxiomMath/Stacks/tree/f56a316ddf7a930906d88b78d6f9a2668cffd0cf) | 18,527,110 | 64,216 | 197 | 120–140 | v4.35.0 | 是 | MMP 的依赖 |
| T4 | [leanprover-community/riemann-hypothesis](https://github.com/leanprover-community/riemann-hypothesis) | [`40e56ba`](https://github.com/leanprover-community/riemann-hypothesis/tree/40e56bab026552e089d7afcfeff08d2defb9c005) | 17,374,215 | 175,187 | 203 | 350–600 | v4.33.1 | 是 | 模型约 475 核·时，未构建 |
| T4 | [anthropics/fermats-last-theorem](https://github.com/anthropics/fermats-last-theorem) | [`6e837e7`](https://github.com/anthropics/fermats-last-theorem/tree/6e837e75355538c7f80bab5b956861e86c4eacc2) | 13,559,858 | 60,478 | — | — | v4.33.1 | 是 | 未做依赖图统计 |
| T4 | [AxiomMath/CFSG](https://github.com/AxiomMath/CFSG) | [`965a077`](https://github.com/AxiomMath/CFSG/tree/965a0775e82217494217503621b843e1b0e1e337) | 约 43,100,000 | — | — | — | v4.35.0 | 是 | 行数取自作者，未自行统计，未分析 |

- **链深**：最长导入链上的模块数。**可并行度（估）**：总行数 ÷ 最重那条链的行数，是多机加速的上限；低于 5 的仓库，每台 16 核时多机几乎没有收益（合成窄图实测 1.00–1.05 倍），只用来验正确性。
- 这个估计只看行数。Mathlib 上估出 23–27，实测 36.6；黎曼猜想归档估出 350–600，模型是约 510。只当量级看。
- 实际构建过的只有 PFR 和 Mathlib，其余的数都来自静态统计或模型。

### 怎么跑一个

```bash
git clone <上游链接> repo && git -C repo checkout <提交>
(cd repo && elan toolchain install "$(cat lean-toolchain)")
(cd repo && lake exe cache get)     # 只有依赖 Mathlib 的仓库需要
lakeshard run repo --work work --workers 4 --slots 3 --threads 1
```

这几行只在 PFR 上跑通过。完整流程（依赖不在 Mathlib 缓存里时怎么办，以及逐字节对比、恢复、断点续建、增量四条验收）照 `bench/README.md` 第 5 节做。统计任意一个仓库：`python3 -I bench/gen/dag_stats.py <工程目录> <输出目录>`。

## 完整清单

### T0 入门（不到 1 万行，51 个）

| 仓库 | 行数 | 文件数 | 依赖 Mathlib |
|---|---:|---:|---|
| [Shashi456/atp-checkers](https://github.com/Shashi456/atp-checkers) | 9,934 | 34 | 是 |
| [cmu-l3/llmlean](https://github.com/cmu-l3/llmlean) | 9,798 | 51 | — |
| [project-numina/LeanTriathlon](https://github.com/project-numina/LeanTriathlon) | 8,507 | 179 | 是 |
| [leanprover-community/NNG4](https://github.com/leanprover-community/NNG4) | 8,462 | 182 | 是 |
| [AxiomMath/IMO2026](https://github.com/AxiomMath/IMO2026) | 8,064 | 13 | 是 |
| [leanprover-community/import-graph](https://github.com/leanprover-community/import-graph) | 7,593 | 86 | 否 |
| [leanprover/doc-gen4](https://github.com/leanprover/doc-gen4) | 7,467 | 50 | 否 |
| [leanprover-community/lean4-metaprogramming-book](https://github.com/leanprover-community/lean4-metaprogramming-book) | 7,245 | 23 | 否 |
| [PatrickMassot/GlimpseOfLean](https://github.com/PatrickMassot/GlimpseOfLean) | 7,169 | 28 | 是 |
| [math-ai-org/IMO2026](https://github.com/math-ai-org/IMO2026) | 7,101 | 6 | 是 |
| [utopia-group/VeriSoftBench](https://github.com/utopia-group/VeriSoftBench) | 6,824 | 21 | — |
| [haoyuzhao123/LeanIneqComp](https://github.com/haoyuzhao123/LeanIneqComp) | 5,991 | 150 | — |
| [haoyuzhao123/algoveri](https://github.com/haoyuzhao123/algoveri) | 5,408 | 78 | — |
| [harmonic-ai/IMO2025](https://github.com/harmonic-ai/IMO2025) | 5,315 | 13 | 是 |
| [yangky11/miniF2F-lean4](https://github.com/yangky11/miniF2F-lean4) | 5,071 | 492 | 是 |
| [formalabstracts/formalabstracts](https://github.com/formalabstracts/formalabstracts) | 4,951 | 34 | — |
| [emilyriehl/infinity-cosmos](https://github.com/emilyriehl/infinity-cosmos) | 4,777 | 32 | 是 |
| [leanprover-community/ProofWidgets4](https://github.com/leanprover-community/ProofWidgets4) | 4,721 | 49 | — |
| [ImperialCollegeLondon/AnnalsChallenge](https://github.com/ImperialCollegeLondon/AnnalsChallenge) | 4,540 | 53 | 是 |
| [leanprover-community/plausible](https://github.com/leanprover-community/plausible) | 4,218 | 28 | 否 |
| [midspiral/LemmaScript](https://github.com/midspiral/LemmaScript) | 4,129 | 103 | 是 |
| [Paper-Proof/paperproof](https://github.com/Paper-Proof/paperproof) | 4,103 | 32 | — |
| [google-deepmind/formal-putnam-like](https://github.com/google-deepmind/formal-putnam-like) | 3,516 | 97 | 是 |
| [ShirleyLIYuxin/Lean4PHYS](https://github.com/ShirleyLIYuxin/Lean4PHYS) | 3,357 | 30 | — |
| [cmu-l3/minicodeprops-eval](https://github.com/cmu-l3/minicodeprops-eval) | 3,354 | 31 | — |
| [jongwony/epistemic-protocols](https://github.com/jongwony/epistemic-protocols) | 3,310 | 30 | — |
| [google-deepmind/miniF2F](https://github.com/google-deepmind/miniF2F) | 3,204 | 4 | 是 |
| [optsuite/M2F](https://github.com/optsuite/M2F) | 2,696 | 5 | — |
| [davidsyin/leannavigator](https://github.com/davidsyin/leannavigator) | 2,595 | 7 | 是 |
| [leanprover-community/quote4](https://github.com/leanprover-community/quote4) | 2,557 | 28 | 否 |
| [grenadeComing/beyond-compilation](https://github.com/grenadeComing/beyond-compilation) | 2,547 | 97 | 是 |
| [leanprover/lean4-cli](https://github.com/leanprover/lean4-cli) | 2,353 | 5 | 否 |
| [lean-dojo/LeanCopilot](https://github.com/lean-dojo/LeanCopilot) | 2,340 | 25 | 否 |
| [rahul3613/ProofNet-lean4](https://github.com/rahul3613/ProofNet-lean4) | 2,076 | 13 | 是 |
| [stepchowfun/proofs](https://github.com/stepchowfun/proofs) | 2,064 | 6 | 是 |
| [BartoszPiotrowski/lean-premise-selection](https://github.com/BartoszPiotrowski/lean-premise-selection) | 2,017 | 21 | 否 |
| [leanprover-community/repl](https://github.com/leanprover-community/repl) | 1,815 | 25 | — |
| [jsm28/IMOLean](https://github.com/jsm28/IMOLean) | 1,443 | 39 | 是 |
| [leanprover/comparator](https://github.com/leanprover/comparator) | 1,111 | 46 | 否 |
| [leanprover-community/LeanSearchClient](https://github.com/leanprover-community/LeanSearchClient) | 1,100 | 8 | 否 |
| [lean-dojo/QuantumLean-Bench](https://github.com/lean-dojo/QuantumLean-Bench) | 1,047 | 10 | 是 |
| [ulfjack/ryu](https://github.com/ulfjack/ryu) | 582 | 4 | 是 |
| [haaaardcvZ/LeanContext](https://github.com/haaaardcvZ/LeanContext) | 579 | 3 | — |
| [math-inc/FormalQualBench](https://github.com/math-inc/FormalQualBench) | 498 | 25 | 是 |
| [prove2me/prove2me_workspace](https://github.com/prove2me/prove2me_workspace) | 442 | 12 | — |
| [quinn-dougherty/fvapps](https://github.com/quinn-dougherty/fvapps) | 430 | 7 | — |
| [wellecks/ntptutorial](https://github.com/wellecks/ntptutorial) | 294 | 5 | 否 |
| [eth-sri/lean-lean](https://github.com/eth-sri/lean-lean) | 200 | 2 | — |
| [eth-sri/matharena](https://github.com/eth-sri/matharena) | 143 | 3 | — |
| [Deicyde/WikiLean](https://github.com/Deicyde/WikiLean) | 114 | 3 | — |
| [SorryDB/SorryDB](https://github.com/SorryDB/SorryDB) | 63 | 9 | 否 |

### T1 万级（1 万–10 万行，51 个）

| 仓库 | 行数 | 文件数 | 链深 | 可并行度（估） | 工具链 | 依赖 Mathlib | 工程形态 |
|---|---:|---:|---:|---:|---|---|---|
| [josevalim/lynx](https://github.com/josevalim/lynx) | 98,792 | 280 | — | — | v4.36.0 | — | 单工程 |
| [ataylor24/TaoAnalysisBench](https://github.com/ataylor24/TaoAnalysisBench) | 93,491 | 608 | — | — | — | — | 4 个工程 |
| [verse-lab/veil](https://github.com/verse-lab/veil) | 91,310 | 501 | — | — | v4.35.0 | 否 | 单工程 |
| [lecopivo/SciLean](https://github.com/lecopivo/SciLean) | 86,723 | 568 | — | — | v4.28.0-rc1 | 是 | 单工程 |
| [leanprover/lean-eval](https://github.com/leanprover/lean-eval) | 84,910 | 2,164 | 4 | 60–180 | v4.36.0 | 是 | 单工程 |
| [plclub/sf-in-lean](https://github.com/plclub/sf-in-lean) | 83,269 | 90 | — | — | v4.34.0 | 否 | 单工程 |
| [FormalizedFormalLogic/Foundation](https://github.com/FormalizedFormalLogic/Foundation) | 80,580 | 321 | — | — | v4.35.0 | 是 | 单工程 |
| [agenticsnz/unsorry](https://github.com/agenticsnz/unsorry) | 72,395 | 11,154 | 1 | 610–5,450 | v4.30.0 | 是 | 单工程，全仓库 83,385 行 |
| [leanprover/verso](https://github.com/leanprover/verso) | 72,355 | 451 | — | — | v4.37.0-rc1 | 否 | 单工程 |
| [google-deepmind/superhuman](https://github.com/google-deepmind/superhuman) | 60,290 | 24 | 11 | 2.4 | v4.27.0 | 是 | 单工程（`FutureMath/Erdos-Hajnal/`），全仓库 104,834 行 |
| [ImperialCollegeLondon/FLT](https://github.com/ImperialCollegeLondon/FLT) | 59,080 | 271 | 18 | 8.1–9.6 | v4.35.0 | 是 | 单工程 |
| [Sequential-Intelligence-Lab/MathlibLemma](https://github.com/Sequential-Intelligence-Lab/MathlibLemma) | 58,131 | 5,024 | 1 | 100–860 | v4.25.0-rc2 | 是 | 单工程，全仓库 646,601 行 |
| [leanprover/cslib](https://github.com/leanprover/cslib) | 55,907 | 358 | 19 | 12–15 | v4.37.0-rc1 | 是 | 单工程 |
| [Verified-zkEVM/clean](https://github.com/Verified-zkEVM/clean) | 54,415 | 221 | — | — | v4.35.0 | 是 | 单工程 |
| [leansolving/SqueezeBench](https://github.com/leansolving/SqueezeBench) | 54,358 | 581 | 20 | 12–17 | v4.31.0 | 是 | 单工程 |
| [fpvandoorn/carleson](https://github.com/fpvandoorn/carleson) | 50,325 | 128 | 30 | 3.0–3.2 | v4.36.0-rc1 | 是 | 单工程 |
| [digama0/lean4lean](https://github.com/digama0/lean4lean) | 49,524 | 112 | — | — | v4.33.0-rc2 | 否 | 单工程 |
| [leanprover-community/lean-auto](https://github.com/leanprover-community/lean-auto) | 45,849 | 123 | — | — | v4.35.0 | — | 单工程 |
| [teorth/analysis](https://github.com/teorth/analysis) | 45,803 | 109 | 30 | 1.7–1.9 | v4.36.0 | 是 | 单工程 |
| [google-deepmind/alphaproof-nexus-results](https://github.com/google-deepmind/alphaproof-nexus-results) | 44,928 | 71 | 1 | 20–23 | v4.27.0 | 是 | 单工程 |
| [optpku/CAM-Bench](https://github.com/optpku/CAM-Bench) | 41,996 | 780 | 1 | 50–140 | v4.28.0 | 是 | 单工程 |
| [leanprover-community/batteries](https://github.com/leanprover-community/batteries) | 33,484 | 262 | 14 | 7.5–11 | v4.37.0-rc1 | 否 | 单工程 |
| [ufmg-smite/lean-smt](https://github.com/ufmg-smite/lean-smt) | 29,231 | 287 | — | — | v4.35.0 | 是 | 单工程 |
| [math-inc/strongpnt](https://github.com/math-inc/strongpnt) | 28,415 | 8 | 8 | 1.0 | v4.21.0 | 是 | 单工程 |
| [Eleanor-H/MUSTARD](https://github.com/Eleanor-H/MUSTARD) | 27,002 | 182 | — | — | — | — | 无 lakefile |
| [Zhitao-He/MATPBench](https://github.com/Zhitao-He/MATPBench) | 26,392 | 1,056 | — | — | — | — | 无 lakefile |
| [leanprover-community/aesop](https://github.com/leanprover-community/aesop) | 24,479 | 250 | — | — | v4.37.0-rc1 | 否 | 单工程 |
| [NyxFoundation/nyxis](https://github.com/NyxFoundation/nyxis) | 22,822 | 103 | — | — | v4.34.1 | 否 | 单工程 |
| [teorth/pfr](https://github.com/teorth/pfr) | 21,990 | 76 | 20 | 2.3–2.6 | v4.36.0-rc2 | 是 | 单工程 |
| [avigad/mathematics_in_lean_source](https://github.com/avigad/mathematics_in_lean_source) | 18,954 | 45 | — | — | v4.35.0 | 是 | 单工程 |
| [leanprover/human-eval-lean](https://github.com/leanprover/human-eval-lean) | 18,893 | 169 | 2 | 25–41 | nightly-2026-03-27 | 否 | 单工程 |
| [cmu-l3/reuF2F](https://github.com/cmu-l3/reuF2F) | 18,875 | 248 | — | — | — | — | 2 个工程 |
| [trishullab/clever](https://github.com/trishullab/clever) | 17,234 | 169 | 2 | 12–20 | v4.27.0 | 是 | 单工程（`src/lean4/`） |
| [ImperialCollegeLondon/formalising-mathematics-2024](https://github.com/ImperialCollegeLondon/formalising-mathematics-2024) | 17,136 | 176 | — | — | v4.5.0-rc1 | 是 | 单工程 |
| [project-numina/Numina-Putnam2025](https://github.com/project-numina/Numina-Putnam2025) | 16,427 | 13 | 2 | 3.7–3.8 | v4.26.0 | 是 | 单工程 |
| [marcusm117/DNA](https://github.com/marcusm117/DNA) | 16,324 | 390 | 32 | 4.1–10 | v4.8.0-rc2 | 是 | 单工程（`LeanEuclidPlus/`），全仓库 23,416 行 |
| [thefundamentaltheor3m/Sphere-Packing-Lean](https://github.com/thefundamentaltheor3m/Sphere-Packing-Lean) | 15,769 | 75 | 19 | 3.0–3.3 | v4.35.0 | 是 | 单工程 |
| [zhangir-azerbayev/ProofNet](https://github.com/zhangir-azerbayev/ProofNet) | 15,506 | 131 | — | — | — | — | 无 lakefile |
| [leanprover-community/sphere-eversion](https://github.com/leanprover-community/sphere-eversion) | 14,988 | 65 | 13 | 3.2–3.6 | v4.35.0 | 是 | 单工程 |
| [lean-dojo/LeanMillenniumPrizeProblems](https://github.com/lean-dojo/LeanMillenniumPrizeProblems) | 14,076 | 31 | 7 | 3.7–3.9 | v4.31.0 | 是 | 单工程 |
| [sunblaze-ucb/verina](https://github.com/sunblaze-ucb/verina) | 13,864 | 192 | 1 | 60–100 | v4.18.0 | 是 | 单工程 |
| [AxiomMath/Putnam2025](https://github.com/AxiomMath/Putnam2025) | 12,367 | 26 | 1 | 6.0–6.9 | v4.21.0 | 是 | 单工程 |
| [project-numina/LeanGeo](https://github.com/project-numina/LeanGeo) | 12,243 | 232 | 48 | 2.5–3.7 | v4.15.0 | 是 | 单工程 |
| [merely-true/merely-true](https://github.com/merely-true/merely-true) | 12,237 | 42 | 17 | 2.1–2.2 | v4.29.0 | 是 | 单工程 |
| [frenzymath/Archon-FirstProof-Results](https://github.com/frenzymath/Archon-FirstProof-Results) | 11,972 | 28 | 10 | 2.1–2.2 | v4.28.0 | 是 | 单工程 |
| [konne88/functorio](https://github.com/konne88/functorio) | 11,842 | 33 | — | — | v4.20.1 | — | 单工程 |
| [trishullab/PutnamBench](https://github.com/trishullab/PutnamBench) | 11,735 | 674 | 1 | 90–360 | v4.33.1 | 是 | 单工程（`lean4/`） |
| [leanprover-community/mathematics_in_lean](https://github.com/leanprover-community/mathematics_in_lean) | 11,256 | 89 | — | — | v4.34.0 | 是 | 单工程 |
| ByteDance-s··d/s··d-Prover | 11,044 | 6 | 2 | 2.5–2.6 | v4.14.0 | 是 | 单工程（`s··dProver/imo2025/`），全仓库 138,434 行 |
| [google-deepmind/formal-imo](https://github.com/google-deepmind/formal-imo) | 10,966 | 262 | 3 | 30–56 | v4.27.0 | 是 | 单工程 |
| [loganrjmurphy/LeanEuclid](https://github.com/loganrjmurphy/LeanEuclid) | 10,024 | 235 | 37 | 3.8–6.1 | v4.19.0 | 是 | 单工程 |

### T2 十万级（10 万–100 万行，25 个）

| 仓库 | 行数 | 文件数 | 链深 | 可并行度（估） | 工具链 | 依赖 Mathlib | 工程形态 |
|---|---:|---:|---:|---:|---|---|---|
| [provables/sequencelib](https://github.com/provables/sequencelib) | 859,926 | 25,905 | 9 | 410–1,150 | v4.30.0 | 是 | 单工程 |
| [ShouqiaoW/erdos](https://github.com/ShouqiaoW/erdos) | 817,110 | 5,492 | — | — | — | — | — |
| [openai/NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler) | 643,991 | 2,659 | 97 | 9.5–12 | v4.34.0-rc2 | 是 | 单工程 |
| [strata-org/Strata](https://github.com/strata-org/Strata) | 584,452 | 1,596 | — | — | v4.34.0 | 否 | 单工程 |
| [openai/ten-proofs](https://github.com/openai/ten-proofs) | 550,003 | 23 | 3 | 3.2 | v4.32.0 | 是 | 单工程 |
| [leanprover-community/physlib](https://github.com/leanprover-community/physlib) | 462,570 | 1,683 | 83 | 12–14 | v4.35.0 | 是 | 单工程 |
| [Verified-zkEVM/ArkLib](https://github.com/Verified-zkEVM/ArkLib) | 406,685 | 1,534 | — | — | v4.36.0 | 是 | 单工程 |
| [lean-dojo/TorchLean](https://github.com/lean-dojo/TorchLean) | 399,751 | 1,238 | — | — | v4.35.0 | 是 | 单工程 |
| [anthropics/formal-math](https://github.com/anthropics/formal-math) | 359,574 | 1,812 | — | — | — | — | — |
| [lean-dojo/ITPEval](https://github.com/lean-dojo/ITPEval) | 354,477 | 4,050 | — | — | — | — | 无 lakefile |
| [Beneficial-AI-Foundation/vericoding](https://github.com/Beneficial-AI-Foundation/vericoding) | 334,801 | 8,686 | 1 | 1,620–3,930 | v4.23.0-rc2 | 是 | 单工程 |
| [zirui-HIT/FormalTCS](https://github.com/zirui-HIT/FormalTCS) | 330,995 | 487 | — | — | — | — | 286 个工程 |
| [google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures) | 219,670 | 2,153 | 8 | 70–110 | v4.33.1 | 是 | 单工程 |
| [AxiomMath/Weil](https://github.com/AxiomMath/Weil) | 214,139 | 980 | 17 | 23–28 | v4.34.0-rc2 | 是 | 单工程 |
| [openai/PrimeGaps186](https://github.com/openai/PrimeGaps186) | 211,605 | 2 | 1 | 1.0 | v4.34.0-rc2 | 是 | 单工程 |
| [Verilean/sparkle](https://github.com/Verilean/sparkle) | 201,903 | 1,014 | — | — | v4.32.1 | 否 | 单工程 |
| [formal-applied-math/formal-mathfin](https://github.com/formal-applied-math/formal-mathfin) | 189,888 | 818 | 63 | 9.9–11 | v4.35.0 | 是 | 单工程 |
| [dwrensha/compfiles](https://github.com/dwrensha/compfiles) | 180,449 | 550 | 12 | 37–44 | v4.36.0 | 是 | 单工程 |
| [AlexKontorovich/PrimeNumberTheoremAnd](https://github.com/AlexKontorovich/PrimeNumberTheoremAnd) | 172,577 | 235 | 20 | 5.2–5.6 | v4.35.0 | 是 | 单工程 |
| [teorth/equational_theories](https://github.com/teorth/equational_theories) | 168,239 | 1,347 | 19 | 9.6–16 | v4.29.1 | 是 | 单工程 |
| [Vilin97/homotopy-groups-lean](https://github.com/Vilin97/homotopy-groups-lean) | 165,846 | 1,195 | 6 | 54–78 | v4.32.2 | 是 | 单工程 |
| [facebookresearch/autoformbench](https://github.com/facebookresearch/autoformbench) | 163,677 | 2,009 | — | — | — | — | 342 个工程 |
| [openai/math](https://github.com/openai/math) | 144,530 | 680 | 2 | 7.5–11 | v4.34.1 | 是 | 单工程（`lean/`），全仓库 30,001,821 行 |
| [AxiomMath/Mordell](https://github.com/AxiomMath/Mordell) | 124,542 | 432 | 35 | 8.2–9.2 | v4.35.0 | 是 | 单工程 |
| [leanprover-community/iris-lean](https://github.com/leanprover-community/iris-lean) | 100,653 | 324 | — | — | — | — | — |

### T3 百万级（100 万–1,000 万行，7 个）

| 仓库 | 行数 | 文件数 | 链深 | 可并行度（估） | 工具链 | 依赖 Mathlib | 工程形态 |
|---|---:|---:|---:|---:|---|---|---|
| [Vilin97/lean-pool](https://github.com/Vilin97/lean-pool) | 9,956,631 | 22,324 | 250 | 15–17 | v4.35.0-rc3 | 是 | 单工程 |
| [TauCetiProject/TauCeti](https://github.com/TauCetiProject/TauCeti) | 7,954,869 | 34,782 | 50 | 400–470 | v4.36.0 | 是 | 单工程 |
| [anthropics/FlashProve](https://github.com/anthropics/FlashProve) | 6,046,801 | 29,566 | — | — | — | — | — |
| [leanprover-community/mathlib4](https://github.com/leanprover-community/mathlib4) | 2,476,531 | 9,345 | 181 | 23–27 | v4.37.0-rc1 | 自身 | 单工程 |
| [plby/Erdos90](https://github.com/plby/Erdos90) | 2,401,565 | 5,271 | — | — | — | — | 2 个工程 |
| [AxiomMath/MMP](https://github.com/AxiomMath/MMP) | 2,056,546 | 2,269 | 136 | 8.9–9.4 | v4.35.0 | 是 | 单工程 |
| [frenzymath/FormalPantheon](https://github.com/frenzymath/FormalPantheon) | 1,959,885 | 12,734 | — | — | — | — | 7 个工程 |

### T4 千万级（1,000 万行以上，7 个）

| 仓库 | 行数 | 文件数 | 链深 | 可并行度（估） | 工具链 | 依赖 Mathlib | 工程形态 |
|---|---:|---:|---:|---:|---|---|---|
| [AxiomMath/CFSG](https://github.com/AxiomMath/CFSG) | 约 43,100,000 | — | — | — | v4.35.0 | 是 | 单工程 |
| [eth-sri/leanlean-october](https://github.com/eth-sri/leanlean-october) | 29,687,538 | 171,267 | — | — | — | — | 35 个工程 |
| [AxiomMath/Stacks](https://github.com/AxiomMath/Stacks) | 18,527,110 | 64,216 | 197 | 120–140 | v4.35.0 | 是 | 单工程 |
| [leanprover-community/riemann-hypothesis](https://github.com/leanprover-community/riemann-hypothesis) | 17,374,215 | 175,187 | 203 | 350–600 | v4.33.1 | 是 | 单工程 |
| [prove2me/or-formalization-drive](https://github.com/prove2me/or-formalization-drive) | 14,213,350 | 96,074 | — | — | — | — | 无 lakefile |
| [anthropics/fermats-last-theorem](https://github.com/anthropics/fermats-last-theorem) | 13,559,858 | 60,478 | — | — | v4.33.1 | 是 | 单工程 |
| [plby/lean-proofs](https://github.com/plby/lean-proofs) | 12,699,082 | 43,587 | — | — | — | — | 10 个工程 |

## 口径与缺口

- **行数**：仓库里全部 `.lean` 文件的行数，含测试、示例、注释和空行，不含依赖。如果 Lake 工程只覆盖其中一部分（不到九成），分档和表里的行数、文件数按工程目录算，“工程形态”一栏注明全仓库的行数。
- **依赖图**：只读每个文件的 import 头，范围是工程目录下的全部 `.lean` 文件，所以模块数会比默认构建目标略多（Carleson 这里是 128，默认目标 125）。
- **工程形态**：“N 个工程”是仓库里有多个互相独立的 Lake 工程、根目录没有 lakefile，不能当一个依赖图来建；“—”是没有检查。
- **工具链为“—”**：根目录没有 `lean-toolchain`，多数是数据集或 Lean 3 仓库。
- **不是全集**：能枚举到的 Lean 仓库有 22,903 个（GitHub 按语言搜索加几个索引站，2026-11-20），这里只统计了挑选过的 141 个（知名项目、数据集和几个超大仓库）。其余的只有仓库体积，体积与行数之比相差几十倍，不能用来分档；要全集的精确分档，得对每个仓库做一次只读扫描，还没做。
- **已知没统计的大仓库**：CFSG 的行数取自作者；`leanprover/lean4` 没有统计（它的构建带自举，不是普通的 Lake 工程）。
- 名字里含 `s··d` 的仓库做了遮盖，不带链接。
