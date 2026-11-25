import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MeasureDecomposition.AdaptedBasisInstance
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MeasureDecomposition.FrameGramInstance
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MeasureDecomposition.InstExp
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MeasureDecomposition.InstPlace
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MeasureDecomposition.InstTop

set_option Elab.async false

namespace E1N.M1846
def val : Nat := E1N.M1837.val % 7 + E1N.M1840.val % 7 + E1N.M1849.val % 7 + E1N.M1851.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end E1N.M1846
