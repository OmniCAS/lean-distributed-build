import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.DiscreteSeriesExistence.DatumEmbeddingMemHlam
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.InfinitesimalDecay.FormBSelfLe
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.InfinitesimalDecay.SquareIntegrableGeneratedVectors
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.TensorRepresentations.CcARatioZero

set_option Elab.async false

namespace E1N.M3002
def val : Nat := E1N.M2857.val % 7 + E1N.M2997.val % 7 + E1N.M3006.val % 7 + E1N.M3077.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end E1N.M3002
