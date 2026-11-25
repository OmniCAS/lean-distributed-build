import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MirabolicBound.CardNonzero
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MirabolicBound.CharSumOne
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MirabolicBound.Development
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MirabolicBound.LastRowMul
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MirabolicBound.RowExists

set_option Elab.async false

namespace E1N.M1860
def val : Nat := E1N.M1856.val % 7 + E1N.M1857.val % 7 + E1N.M1858.val % 7 + E1N.M1859.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end E1N.M1860
