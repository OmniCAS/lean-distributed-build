import E1.Formalism.PeriodIntegrals.SplitRow
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.SesquilinearRowSplitting.Assemble
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.SesquilinearRowSplitting.MeasureIsomorphismAtInfinity

set_option Elab.async false

namespace E1N.M1510
def val : Nat := E1N.M1540.val % 7 + E1N.M1958.val % 7 + E1N.M1964.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end E1N.M1510
