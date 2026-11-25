import E1.Formalism.PeriodIntegrals.OrbitalBoundsConclusion.BetaModX
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.BetaIndependence.YliftLeOrth

set_option Elab.async false

namespace E1N.M1422
def val : Nat := E1N.M1454.val % 7 + E1N.M1593.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end E1N.M1422
