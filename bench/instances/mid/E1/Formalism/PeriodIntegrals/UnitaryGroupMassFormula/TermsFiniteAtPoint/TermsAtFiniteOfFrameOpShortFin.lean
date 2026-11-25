import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.TermsFiniteAtPoint.CellMain
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.TermsFiniteAtPoint.DdSPowLeOne
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.TermsFiniteAtPoint.FixedZ
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.TermsFiniteAtPoint.HeisOpHolds
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.TermsFiniteAtPoint.ResFinAlt
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.TermsFiniteAtPoint.RightInvHolds
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.TermsFiniteAtPoint.SkewSolveAlt
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.TermsFiniteAtPoint.ZhatIntegralHolds
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.TermsFiniteAtPoint.ZhatRed

set_option Elab.async false

namespace E1N.M2016
def val : Nat := E1N.M2001.val % 7 + E1N.M2003.val % 7 + E1N.M2006.val % 7 + E1N.M2010.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end E1N.M2016
