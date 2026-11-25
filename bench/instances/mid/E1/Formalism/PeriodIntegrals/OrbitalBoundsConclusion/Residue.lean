import E1.Formalism.PeriodIntegrals.Residue
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ResidueLatticeCount.BClass
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ResidueLatticeCount.BUnfold
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ResidueLatticeCount.BoxEqConvexBodyLT
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ResidueLatticeCount.DvdSpanOfIdealSet
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ResidueLatticeCount.HeckeLowerOf
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ResidueLatticeCount.IdealEquiv
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ResidueLatticeCount.MemSmulNormLeOne
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ResidueLatticeCount.NnrealOfEnnreal
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ResidueLatticeCount.NormAtPlacePosOfNormPos
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ResidueLatticeCount.RealHitIneq
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ResidueLatticeCount.ResidueBoundOf
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ResidueLatticeCount.SumRangeLe
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ResidueLatticeCount.ThirdLeLog
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ResidueLatticeCount.UnitMulDetNeZero

set_option Elab.async false

namespace E1N.M1498
def val : Nat := E1N.M1530.val % 7 + E1N.M1894.val % 7 + E1N.M1895.val % 7 + E1N.M1896.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end E1N.M1498
