import E1.Formalism.PeriodIntegrals.ExpTri
import E1.Formalism.PeriodIntegrals.SymDist
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.SymmetricDistance.SymDistOf

set_option Elab.async false

namespace E1N.M1511
def val : Nat := E1N.M1421.val % 7 + E1N.M1542.val % 7 + E1N.M1979.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end E1N.M1511
