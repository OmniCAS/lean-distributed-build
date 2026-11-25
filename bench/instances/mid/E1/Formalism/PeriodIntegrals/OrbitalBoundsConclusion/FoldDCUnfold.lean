import E1.Formalism.PeriodIntegrals.FoldDCUnfold
import E1.Formalism.PeriodIntegrals.OrbitalBoundsConclusion.FoldUnfold
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.FoldingUnfolding.DoubleCosetTranslation
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.FoldingUnfolding.FoldDCUnfoldOf
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.FoldingUnfolding.TranslationIndependent

set_option Elab.async false

namespace E1N.M1463
def val : Nat := E1N.M1425.val % 7 + E1N.M1465.val % 7 + E1N.M1639.val % 7 + E1N.M1640.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1463
