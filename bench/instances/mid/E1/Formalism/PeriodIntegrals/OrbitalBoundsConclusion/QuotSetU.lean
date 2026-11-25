import E1.Formalism.PeriodIntegrals.QuotSetU
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.UnitaryQuotientCompactness.ExistsModularFunction
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.UnitaryQuotientCompactness.GPolar
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.UnitaryQuotientCompactness.IsCompactInterUnitBox
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.UnitaryQuotientCompactness.QuotSetUOf
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.UnitaryQuotientCompactness.UnitaryWeylCompact

set_option Elab.async false

namespace E1N.M1497
def val : Nat := E1N.M1529.val % 7 + E1N.M2029.val % 7 + E1N.M2030.val % 7 + E1N.M2032.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1497
