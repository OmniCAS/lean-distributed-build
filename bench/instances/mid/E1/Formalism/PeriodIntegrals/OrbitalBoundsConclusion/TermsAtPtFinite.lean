import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.TermsFiniteAtPoint.DShort
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.TermsFiniteAtPoint.FrameTop
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.TermsFiniteAtPoint.TermsAtFiniteOfFrameOpShortFin

set_option Elab.async false

namespace E1N.M1514
def val : Nat := E1N.M2002.val % 7 + E1N.M2009.val % 7 + E1N.M2016.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1514
