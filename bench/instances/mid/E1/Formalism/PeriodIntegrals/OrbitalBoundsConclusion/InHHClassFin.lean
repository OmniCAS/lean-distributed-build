import E1.Formalism.PeriodIntegrals.InHHClassFin
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.HermitianClassFiniteness.CTFromBlocks
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.HermitianClassFiniteness.ClassSetFinIdx
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.HermitianClassFiniteness.Development
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.HermitianClassFiniteness.FrHformSumLeft
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.HermitianClassFiniteness.HformSumRight
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.HermitianClassFiniteness.LevelStep
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.HermitianClassFiniteness.OneMemKg
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.HermitianClassFiniteness.RtUnitaryOf
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.HermitianClassFiniteness.SigConj

set_option Elab.async false

namespace E1N.M1475
def val : Nat := E1N.M1442.val % 7 + E1N.M1654.val % 7 + E1N.M1655.val % 7 + E1N.M1656.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end E1N.M1475
