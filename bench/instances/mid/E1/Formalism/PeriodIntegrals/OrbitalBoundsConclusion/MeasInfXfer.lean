import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.InfiniteMeasureTransfer.Closed
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.InfiniteMeasureTransfer.MeasInfXferOf
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.InfiniteMeasureTransfer.MeasureIsomorphismAtInfinity
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.InfiniteMeasureTransfer.NilpotentMeasureRecursion

set_option Elab.async false

namespace E1N.M1481
def val : Nat := E1N.M1686.val % 7 + E1N.M1689.val % 7 + E1N.M1690.val % 7 + E1N.M1691.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1481
