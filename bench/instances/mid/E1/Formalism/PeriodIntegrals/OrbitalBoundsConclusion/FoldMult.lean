import E1.Formalism.PeriodIntegrals.FoldMult
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MultiplicityMeasurability.MeasurableMult

set_option Elab.async false

namespace E1N.M1464
def val : Nat := E1N.M1426.val % 7 + E1N.M1862.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1464
