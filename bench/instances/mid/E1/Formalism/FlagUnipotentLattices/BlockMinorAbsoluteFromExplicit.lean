import E1.Formalism.FlagUnipotentLattices.MinkowskiFactorialBounds.BlockMinorAbsoluteOfExplicit
import E1.Formalism.FlagUnipotentLattices.StabiliserComplementDecomposition

set_option Elab.async false

namespace E1N.M100
def val : Nat := E1N.M119.val % 7 + E1N.M149.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M100
