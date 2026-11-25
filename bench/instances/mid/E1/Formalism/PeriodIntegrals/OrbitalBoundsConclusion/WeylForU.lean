import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.WeylFormulaUnitary.NatWCastReal
import E1.Formalism.PeriodIntegrals.WeylForU

set_option Elab.async false

namespace E1N.M1519
def val : Nat := E1N.M2075.val % 7 + E1N.M2088.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end E1N.M1519
