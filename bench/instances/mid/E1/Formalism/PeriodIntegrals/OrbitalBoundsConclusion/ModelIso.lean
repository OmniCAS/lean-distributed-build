import E1.Formalism.PeriodIntegrals.OrbitalBoundsConclusion.HwIrred
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.PolynomialModelIsometry.Assembly
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.PolynomialModelIsometry.DetSplit
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.PolynomialModelIsometry.ModelMap
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.PolynomialModelIsometry.PolyExt
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.PolynomialModelIsometry.TorusEigenvalueFormula

set_option Elab.async false

namespace E1N.M1483
def val : Nat := E1N.M1473.val % 7 + E1N.M1879.val % 7 + E1N.M1880.val % 7 + E1N.M1883.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end E1N.M1483
