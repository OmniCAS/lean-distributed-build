import E1.Formalism.PeriodIntegrals.KFinSmooth
import E1.Formalism.PeriodIntegrals.LowCyc
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LowerSmoothStability.ExistsFinStableOfMemSSup

set_option Elab.async false

namespace E1N.M1480
def val : Nat := E1N.M1444.val % 7 + E1N.M1449.val % 7 + E1N.M1826.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end E1N.M1480
