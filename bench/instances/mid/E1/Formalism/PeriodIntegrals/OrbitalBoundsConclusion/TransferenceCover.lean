import E1.Formalism.PeriodIntegrals.Transference
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LatticeTransference.KeySmall
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LatticeTransference.NumericMain
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LatticeTransference.Poisson
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LatticeTransference.Skeleton

set_option Elab.async false

namespace E1N.M1515
def val : Nat := E1N.M1543.val % 7 + E1N.M1774.val % 7 + E1N.M1776.val % 7 + E1N.M1777.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1515
