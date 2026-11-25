import E1.Formalism.FlagUnipotentLattices.MinkowskiFactorialBounds.CoefficientLeOperatorNorm
import E1.Formalism.FlagUnipotentLattices.MinkowskiFactorialBounds.ExtensionInterSubspace
import E1.Formalism.FlagUnipotentLattices.MinkowskiFactorialBounds.NearFarVolumeBounds
import E1.Formalism.LatticeRigidity.RecursionUnrestrictedFalse

set_option Elab.async false

namespace E1N.M134
def val : Nat := E1N.M122.val % 7 + E1N.M128.val % 7 + E1N.M140.val % 7 + E1N.M768.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M134
