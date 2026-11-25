import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.ClosedLocalOrbits.GGMirabolic
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ScalarConvolutionTrace.AveragingOperatorIdempotent
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ScalarConvolutionTrace.ConvScalarOfLitOf
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ScalarConvolutionTrace.IntertwinerRankLeOne
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ScalarConvolutionTrace.Reindex
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ScalarConvolutionTrace.RepresentationDimensionPos

set_option Elab.async false

namespace E1N.M1467
def val : Nat := E1N.M983.val % 7 + E1N.M1913.val % 7 + E1N.M1915.val % 7 + E1N.M1916.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end E1N.M1467
