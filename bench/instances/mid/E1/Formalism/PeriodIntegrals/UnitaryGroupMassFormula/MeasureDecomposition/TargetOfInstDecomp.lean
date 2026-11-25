import E1.Formalism.PeriodIntegrals.ScMuExists
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MeasureDecomposition.ContinuousUMatApply
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MeasureDecomposition.GenSemiOf
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MeasureDecomposition.GenericWeilRepresentation
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MeasureDecomposition.HaarSub
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MeasureDecomposition.InstDecomp
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MeasureDecomposition.InstLeftInvMuInf
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MeasureDecomposition.ModOne
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.MeasureDecomposition.Proper

set_option Elab.async false

namespace E1N.M1855
def val : Nat := E1N.M1532.val % 7 + E1N.M1839.val % 7 + E1N.M1841.val % 7 + E1N.M1842.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end E1N.M1855
