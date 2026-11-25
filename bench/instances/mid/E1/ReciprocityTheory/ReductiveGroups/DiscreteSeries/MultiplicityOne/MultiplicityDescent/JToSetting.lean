import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.MultiplicityOne.JDiagExists
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.MultiplicityOne.JHaarSF
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.MultiplicityOne.MultiplicityDescent.AdmissibleAtRealPlace
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.MultiplicityOne.WeightedL1OfL2

set_option Elab.async false

namespace E1N.M3044
def val : Nat := E1N.M3027.val % 7 + E1N.M3029.val % 7 + E1N.M3041.val % 7 + E1N.M3054.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end E1N.M3044
