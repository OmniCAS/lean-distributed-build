import E1.Formalism.FlagUnipotentLattices.CoveringRadius2
import E1.Formalism.FlagUnipotentLattices.MinkowskiFactorialBounds.KappaConstantAssembly
import E1.Formalism.FlagUnipotentLattices.MinkowskiFactorialBounds.NearFarVolumeBounds

set_option Elab.async false

namespace E1N.M115
def val : Nat := E1N.M103.val % 7 + E1N.M134.val % 7 + E1N.M140.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end E1N.M115
