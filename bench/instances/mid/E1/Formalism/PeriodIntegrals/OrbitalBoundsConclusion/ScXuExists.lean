import E1.Formalism.PeriodIntegrals.ScXuExists
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LatticeAutomorphismApprox.Assemble
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LatticeAutomorphismApprox.LocalDataSatisfyLinearHypotheses
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LatticeAutomorphismApprox.SplitLoc
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LatticeAutomorphismApprox.SplitUnitaryProjectionCompatibility

set_option Elab.async false

namespace E1N.M1505
def val : Nat := E1N.M1536.val % 7 + E1N.M1704.val % 7 + E1N.M1712.val % 7 + E1N.M1719.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1505
