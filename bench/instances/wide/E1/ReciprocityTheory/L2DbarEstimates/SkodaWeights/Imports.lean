import E1.ReciprocityTheory.L2DbarEstimates.SkodaWeights.Matrix
import E1.ReciprocityTheory.L2DbarEstimates.SkodaWeights.VolProdFinApply

set_option Elab.async false

namespace E1N.M3752
def val : Nat := E1N.M3755.val % 7 + E1N.M3761.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M3752
