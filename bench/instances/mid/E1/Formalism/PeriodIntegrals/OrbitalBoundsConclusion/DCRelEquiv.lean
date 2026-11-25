import E1.Formalism.PeriodIntegrals.DCRelEquiv
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.RelativeEquivalence.DCRelEquivAllHolds

set_option Elab.async false

namespace E1N.M1461
def val : Nat := E1N.M1419.val % 7 + E1N.M1892.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1461
