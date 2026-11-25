import E1.ReciprocityTheory.L2DbarEstimates.NormFibrations.Hormander
import E1.ReciprocityTheory.L2DbarEstimates.NormFibrations.ImportsAlt
import E1.ReciprocityTheory.L2DbarEstimates.NormFibrations.LseSmoothRIffReal
import E1.ReciprocityTheory.L2DbarEstimates.NormFibrations.MvBlowup

set_option Elab.async false

namespace E1N.M3608
def val : Nat := E1N.M3690.val % 7 + E1N.M3692.val % 7 + E1N.M3693.val % 7 + E1N.M3694.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end E1N.M3608
