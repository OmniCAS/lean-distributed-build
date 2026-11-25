import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.HighestWeights.ContinuousRepresentations.Decomp
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.HighestWeights.ContinuousRepresentations.DerivK
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.HighestWeights.ContinuousRepresentations.EntryEqZeroOfComm
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.HighestWeights.ContinuousRepresentations.RelOpCurve
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.HighestWeights.ContinuousRepresentations.Stable
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.HighestWeights.ContinuousRepresentations.URepCompRedOf
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.HighestWeights.ContinuousRepresentations.URepHom
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.HighestWeights.FromHC

set_option Elab.async false

namespace E1N.M2936
def val : Nat := E1N.M2930.val % 7 + E1N.M2932.val % 7 + E1N.M2933.val % 7 + E1N.M2934.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end E1N.M2936
