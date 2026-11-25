import E1.ReciprocityTheory.L2DbarEstimates.ChartDerivatives.ChartSymmEventuallyEq
import E1.ReciprocityTheory.L2DbarEstimates.ChartDerivatives.CommFderivApply
import E1.ReciprocityTheory.L2DbarEstimates.ChartDerivatives.ExistsChartPartition
import E1.ReciprocityTheory.L2DbarEstimates.ChartDerivatives.HoloSmooth
import E1.ReciprocityTheory.L2DbarEstimates.ChartDerivatives.InhHasFDerivAtNormSq
import E1.ReciprocityTheory.L2DbarEstimates.ChartDerivatives.IntegralFderivApplyEqZero
import E1.ReciprocityTheory.L2DbarEstimates.ChartDerivatives.IsLocalHomeomorphCompFst
import E1.ReciprocityTheory.L2DbarEstimates.ChartDerivatives.MeasurableSetImageOfIsLocalHomeomorph
import E1.ReciprocityTheory.L2DbarEstimates.ChartDerivatives.TsupportDbSubset

set_option Elab.async false

namespace E1N.M3593
def val : Nat := E1N.M3588.val % 7 + E1N.M3589.val % 7 + E1N.M3591.val % 7 + E1N.M3592.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
theorem w7 (a b : Nat) : a + b + 7 = b + a + 7 := by omega
theorem w8 (a b : Nat) : a + b + 8 = b + a + 8 := by omega
end E1N.M3593
