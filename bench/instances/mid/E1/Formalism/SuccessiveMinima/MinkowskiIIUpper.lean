import E1.Formalism.SuccessiveMinima.SuccessiveMinimaProofs.AdaptedBasis
import E1.Formalism.SuccessiveMinima.SuccessiveMinimaProofs.GjLevel
import E1.Formalism.SuccessiveMinima.SuccessiveMinimaProofs.GjScale
import E1.Formalism.SuccessiveMinima.SuccessiveMinimaProofs.MeasureEqCovolumeMulVolumeImage
import E1.Formalism.SuccessiveMinima.SuccessiveMinimaProofs.MinkCore
import E1.Formalism.SuccessiveMinima.SuccessiveMinimaProofs.MinkowskiIILowerOf
import E1.Formalism.SuccessiveMinima.SuccessiveMinimaProofs.NPUnit
import E1.Formalism.SuccessiveMinima.SuccessiveMinimaProofs.NPWDivision
import E1.Formalism.SuccessiveMinima.SuccessiveMinimaProofs.NewtonSlope
import E1.Formalism.SuccessiveMinima.SuccessiveMinimaProofs.SuccMin

set_option Elab.async false

namespace E1N.M2594
def val : Nat := E1N.M2597.val % 7 + E1N.M2598.val % 7 + E1N.M2599.val % 7 + E1N.M2600.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end E1N.M2594
