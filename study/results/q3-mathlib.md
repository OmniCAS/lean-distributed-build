{
 "work_s": 43309.281,
 "critical_path_s": 1183.5970000000004,
 "max_speedup": 36.591239247818294,
 "cp_modules": 154,
 "cp_by_package": {
  "batteries": 19.605,
  "aesop": 36.192,
  "mathlib": 1127.8000000000004
 },
 "cp_small_modules_s": 23.397,
 "depth": 180,
 "depth_floor_s": 178.25,
 "redundant_edges": 12197,
 "edges": 36212,
 "cp_after_transitive_reduction_s": 1183.5970000000004
}
| module | seconds | lines | share_of_cp |
|---|---|---|---|
| Mathlib.Analysis.Distribution.SchwartzSpace.Basic | 55.0 | 1420 | 0.046 |
| Mathlib.Analysis.Normed.Module.Multilinear.Basic | 36.0 | 1295 | 0.030 |
| Mathlib.Analysis.Analytic.Constructions | 36.0 | 1299 | 0.030 |
| Mathlib.Geometry.Manifold.MFDeriv.SpecificFunctions | 33.0 | 1139 | 0.028 |
| Mathlib.Analysis.Analytic.Basic | 29.0 | 1136 | 0.025 |
| Mathlib.Analysis.Normed.Module.Multilinear.Curry | 26.0 | 713 | 0.022 |
| Mathlib.Analysis.Normed.Operator.Bilinear | 25.0 | 475 | 0.021 |
| Mathlib.Analysis.Calculus.ContDiff.Operations | 24.0 | 1052 | 0.020 |
| Mathlib.Analysis.Analytic.Composition | 23.0 | 1288 | 0.019 |
| Mathlib.Analysis.Calculus.ContDiff.Defs | 23.0 | 1283 | 0.019 |
| parts | k | cp_s | max_speedup | last_split |
|---|---|---|---|---|
| 2 | 0 | 1183.6 | 36.6 |  |
| 2 | 1 | 1156.6 | 37.4 | Mathlib.Analysis.Distribution.SchwartzSpace.Basic |
| 2 | 2 | 1139.1 | 38.0 | Mathlib.Analysis.Normed.Module.Multilinear.Basic |
| 2 | 5 | 1099.4 | 39.4 | Mathlib.Analysis.Analytic.Basic |
| 2 | 10 | 1038.9 | 41.7 | Mathlib.Analysis.Analytic.Composition |
| 2 | 20 | 962.1 | 45.0 | Mathlib.MeasureTheory.Function.LpSpace.Basic |
| 2 | 50 | 897.8 | 48.3 | Mathlib.AlgebraicGeometry.Normalization |
| 2 | 100 | 824.5 | 52.6 | Mathlib.AlgebraicGeometry.GammaSpecAdjunction |
| 2 | 200 | 730.7 | 59.5 | Mathlib.Topology.Algebra.InfiniteSum.NatInt |
| 4 | 0 | 1183.6 | 36.6 |  |
| 4 | 1 | 1143.1 | 37.9 | Mathlib.Analysis.Distribution.SchwartzSpace.Basic |
| 4 | 2 | 1117.1 | 38.8 | Mathlib.Analysis.Normed.Module.Multilinear.Basic |
| 4 | 5 | 1061.6 | 40.8 | Mathlib.Analysis.Analytic.Basic |
| 4 | 10 | 991.1 | 43.7 | Mathlib.Analysis.Calculus.ContDiff.FTaylorSeries |
| 4 | 20 | 931.3 | 46.6 | Mathlib.Analysis.Calculus.ContDiff.Convolution |
| 4 | 50 | 853.9 | 50.9 | Mathlib.MeasureTheory.Group.Arithmetic |
| 4 | 100 | 761.5 | 57.3 | Mathlib.AlgebraicGeometry.Group.Abelian |
| 4 | 200 | 649.6 | 67.6 | Mathlib.Algebra.Group.Submonoid.Operations |
| 16 | 0 | 1183.6 | 36.6 |  |
| 16 | 1 | 1134.9 | 38.2 | Mathlib.Analysis.Distribution.SchwartzSpace.Basic |
| 16 | 2 | 1108.9 | 39.1 | Mathlib.Analysis.Normed.Module.Multilinear.Basic |
| 16 | 5 | 1066.0 | 40.7 | Mathlib.Geometry.Manifold.MFDeriv.SpecificFunctions |
| 16 | 10 | 976.2 | 44.5 | Mathlib.Analysis.Calculus.ContDiff.Operations |
| 16 | 20 | 927.4 | 47.0 | Mathlib.Topology.Algebra.Module.Equiv |
| 16 | 50 | 835.0 | 52.8 | Mathlib.LinearAlgebra.TensorProduct.Tower |
| 16 | 100 | 730.1 | 61.4 | Mathlib.Topology.Semicontinuity.Basic |
| 16 | 200 | 600.6 | 77.1 | Mathlib.MeasureTheory.Integral.Prod |
| removed | edge | cp_s | max_speedup |
|---|---|---|---|
| 1 | Mathlib.Analysis.Calculus.ContDiff.Operations -> Mathlib.Analysis.Calculus.ContDiff.Comp | 1090.5 | 39.7 |
| 2 | Mathlib.Analysis.Calculus.FormalMultilinearSeries -> Mathlib.Analysis.Normed.Module.Multilinear.Curry | 1026.8 | 42.2 |
| 3 | Mathlib.Topology.Algebra.MulAction -> Mathlib.Topology.Algebra.ConstMulAction | 982.7 | 44.1 |
| 4 | Mathlib.Analysis.Distribution.SchwartzSpace.Deriv -> Mathlib.Analysis.Distribution.SchwartzSpace.Basic | 942.2 | 46.0 |
| 5 | Mathlib.Topology.Algebra.Module.ClosedSubmodule -> Mathlib.Topology.Algebra.Module.Equiv | 924.2 | 46.9 |
| 6 | Mathlib.Order.Disjoint -> Mathlib.Order.BoundedOrder.Lattice | 908.8 | 47.7 |
| 7 | Mathlib.Data.Set.Image -> Mathlib.Data.Set.SymmDiff | 899.3 | 48.2 |
| 8 | Mathlib.Tactic.Linter.Header -> Mathlib.Tactic.Linter.DirectoryDependency | 897.0 | 48.3 |
| 9 | Batteries.Tactic.Lint.Misc -> Batteries.Tactic.Lint.Basic | 896.6 | 48.3 |
| 10 | Mathlib.Tactic.Translate.TagUnfoldBoundary -> Mathlib.Tactic.Translate.Core | 891.2 | 48.6 |
| 11 | Aesop.Rule.Basic -> Aesop.RuleTac.Descr | 883.9 | 49.0 |
| 12 | Mathlib.Tactic.ExtractGoal -> Mathlib.Tactic.MinImports | 883.4 | 49.0 |
| 13 | Aesop.Search.Expansion -> Aesop.Search.Expansion.Norm | 880.9 | 49.2 |
| 14 | Mathlib.Data.Set.Defs -> Mathlib.Tactic.SetNotationForOrder | 878.5 | 49.3 |
| 15 | Mathlib.Data.Set.BooleanAlgebra -> Mathlib.Order.CompleteBooleanAlgebra | 874.3 | 49.5 |
(73.1 s)
