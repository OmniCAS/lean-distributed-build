import E1.Formalism.ThetaLogCoordinates.ResidueClassEstimates.VandermondeRankEstimates.AtypicalWeightBoundOf
import E1.Formalism.ThetaLogCoordinates.ResidueClassEstimates.VandermondeRankEstimates.Branch
import E1.Formalism.ThetaLogCoordinates.ResidueClassEstimates.VandermondeRankEstimates.LogBinomialProperties
import E1.Formalism.ThetaLogCoordinates.ResidueClassEstimates.VandermondeRankEstimates.LogWeylDimensionEstimate
import E1.Formalism.ThetaLogCoordinates.ResidueClassEstimates.VandermondeRankEstimates.N0LeNs
import E1.Formalism.ThetaLogCoordinates.ResidueClassEstimates.VandermondeRankEstimates.TTotal
import E1.Formalism.ThetaLogCoordinates.ResidueClassEstimates.VandermondeRankEstimates.WeylGT

set_option Elab.async false

namespace E1N.M2642
def val : Nat := E1N.M2646.val % 7 + E1N.M2647.val % 7 + E1N.M2648.val % 7 + E1N.M2649.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end E1N.M2642
