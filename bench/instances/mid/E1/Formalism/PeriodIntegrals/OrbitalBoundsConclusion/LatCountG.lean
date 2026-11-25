import E1.Formalism.PeriodIntegrals.LatCountG
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LatticeCountingBound.Assemble
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LatticeCountingBound.IndexDet
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LatticeCountingBound.IndexOf

set_option Elab.async false

namespace E1N.M1478
def val : Nat := E1N.M1445.val % 7 + E1N.M1724.val % 7 + E1N.M1730.val % 7 + E1N.M1732.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1478
