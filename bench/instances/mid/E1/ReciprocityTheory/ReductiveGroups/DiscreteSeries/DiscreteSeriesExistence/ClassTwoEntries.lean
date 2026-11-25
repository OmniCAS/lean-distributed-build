import E1.Formalism.RealPlaceAnalysis.RealPlaceTaylor.IntegrableComplexContinuousBoundedSupport
import E1.Formalism.RealPlaceAnalysis.RealPlaceTaylor.RightDerivativeZeroOutsideSupport
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.DiscreteSeriesExistence.MeasurePreservingMulRight

set_option Elab.async false

namespace E1N.M2849
def val : Nat := E1N.M2120.val % 7 + E1N.M2133.val % 7 + E1N.M2868.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end E1N.M2849
