import E1.Formalism.PeriodIntegrals.AdBridgeSteps
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.FiniteAdelicComparison.AdelicLatticeToLocalLattices
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.FiniteAdelicComparison.LocFrom
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.FiniteAdelicComparison.LocInj
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.FiniteAdelicComparison.LocLift
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.FiniteAdelicComparison.VecVMulVec

set_option Elab.async false

namespace E1N.M1455
def val : Nat := E1N.M1407.val % 7 + E1N.M1632.val % 7 + E1N.M1633.val % 7 + E1N.M1634.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1455
