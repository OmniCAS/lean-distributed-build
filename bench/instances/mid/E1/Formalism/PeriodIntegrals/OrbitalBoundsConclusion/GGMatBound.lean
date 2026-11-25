import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.ClosedLocalOrbits.GGMirabolic
import E1.Formalism.PeriodIntegrals.OrbitalBoundsConclusion.GGCardUni
import E1.Formalism.PeriodIntegrals.OrbitalBoundsConclusion.GGConvScalar
import E1.Formalism.PeriodIntegrals.OrbitalBoundsConclusion.GGGenRatio
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MatrixCoefficientBound.GamOneReal
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MatrixCoefficientBound.GammaMatrixInverse
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MatrixCoefficientBound.GgMatrixBoundOfLitOf
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MatrixCoefficientBound.IrreducibleOfMinimal
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MatrixCoefficientBound.JointEigenvectorExists
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MatrixCoefficientBound.MatrixCoefficientEquation
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MatrixCoefficientBound.ProdFormula
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MatrixCoefficientBound.SpectrumPositiveSemidefinite

set_option Elab.async false

namespace E1N.M1469
def val : Nat := E1N.M983.val % 7 + E1N.M1466.val % 7 + E1N.M1467.val % 7 + E1N.M1468.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end E1N.M1469
