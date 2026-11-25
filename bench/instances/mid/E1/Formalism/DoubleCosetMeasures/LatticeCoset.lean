import E1.Formalism.DoubleCosetMeasures.LowerUnipotentOrbits.DoubleCosetEqPreimage
import E1.Formalism.DoubleCosetMeasures.LowerUnipotentOrbits.ExistsContinuousLowerUpperEntry
import E1.Formalism.DoubleCosetMeasures.LowerUnipotentOrbits.IsClosedLowUni
import E1.Formalism.DoubleCosetMeasures.LowerUnipotentOrbits.IsIntOfLatOfLe
import E1.Formalism.DoubleCosetMeasures.LowerUnipotentOrbits.IsOpenIsIntSet
import E1.Formalism.DoubleCosetMeasures.LowerUnipotentOrbits.LemmaU
import E1.Formalism.DoubleCosetMeasures.LowerUnipotentOrbits.LowUniMulVecELast
import E1.Formalism.DoubleCosetMeasures.LowerUnipotentOrbits.MeasureUniformizerMatrixSetMulCard
import E1.Formalism.DoubleCosetMeasures.LowerUnipotentOrbits.MulInvBlockDiagApplySameBlock
import E1.Formalism.DoubleCosetMeasures.LowerUnipotentOrbits.RelIndexMulMeasure
import E1.Formalism.DoubleCosetMeasures.LowerUnipotentOrbits.TwoSided
import E1.Formalism.DoubleCosetMeasures.Statement
import E1.Formalism.DoubleCosetMeasures.StatementV
import E1.Formalism.DoubleCosetMeasures.StatementZ

set_option Elab.async false

namespace E1N.M83
def val : Nat := E1N.M84.val % 7 + E1N.M85.val % 7 + E1N.M86.val % 7 + E1N.M87.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
theorem w7 (a b : Nat) : a + b + 7 = b + a + 7 := by omega
theorem w8 (a b : Nat) : a + b + 8 = b + a + 8 := by omega
end E1N.M83
