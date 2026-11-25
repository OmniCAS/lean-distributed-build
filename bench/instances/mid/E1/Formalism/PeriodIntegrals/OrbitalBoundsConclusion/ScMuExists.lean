import E1.Formalism.PeriodIntegrals.ScMuExists
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MeasureDecomposition.InstAll
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MeasureDecomposition.TargetOfInstDecomp

set_option Elab.async false

namespace E1N.M1500
def val : Nat := E1N.M1532.val % 7 + E1N.M1846.val % 7 + E1N.M1855.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1500
