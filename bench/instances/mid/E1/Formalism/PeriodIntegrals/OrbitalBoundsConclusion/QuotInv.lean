import E1.Formalism.PeriodIntegrals.QuotInv
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.QuotientInvariantMeasurability.MeasurableAvgS

set_option Elab.async false

namespace E1N.M1495
def val : Nat := E1N.M1527.val % 7 + E1N.M1888.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end E1N.M1495
