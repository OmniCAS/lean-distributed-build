import E1.Formalism.PeriodIntegrals.ScRefExists
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LatticeReferenceFrame.PrincipalIdealRingAtPrime
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LatticeReferenceFrame.TargetOfWframe
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LatticeReferenceFrame.WFrameOf
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LatticeReferenceFrame.WeilBasisExistence

set_option Elab.async false

namespace E1N.M1504
def val : Nat := E1N.M1535.val % 7 + E1N.M1757.val % 7 + E1N.M1760.val % 7 + E1N.M1764.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1504
