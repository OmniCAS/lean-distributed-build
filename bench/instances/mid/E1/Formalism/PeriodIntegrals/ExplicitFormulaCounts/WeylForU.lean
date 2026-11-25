import E1.Formalism.PeriodIntegrals.AdmissibleModel.WeylDim
import E1.Formalism.PeriodIntegrals.OrbitalBoundsConclusion.ModelIso
import E1.Formalism.PeriodIntegrals.OrbitalBoundsConclusion.PolyCoef
import E1.Formalism.PeriodIntegrals.OrbitalBoundsConclusion.UnitaryDense
import E1.Formalism.PeriodIntegrals.OrbitalBoundsConclusion.WeylForU

set_option Elab.async false

namespace E1N.M1424
def val : Nat := E1N.M1411.val % 7 + E1N.M1483.val % 7 + E1N.M1493.val % 7 + E1N.M1517.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1424
