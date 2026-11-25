import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LatticeReferenceFrame.IdemAd
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LatticeReferenceFrame.IdemLoc
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LatticeReferenceFrame.IdemTen

set_option Elab.async false

namespace E1N.M1750
def val : Nat := E1N.M1747.val % 7 + E1N.M1749.val % 7 + E1N.M1751.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1750
