import E1.Formalism.PeriodIntegrals.LevelKSplit
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LevelSplitting.HeisenbergParabolicAll
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LevelSplitting.LevelSAllOfHL
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LevelSplitting.LeviPartAll

set_option Elab.async false

namespace E1N.M1479
def val : Nat := E1N.M1447.val % 7 + E1N.M1788.val % 7 + E1N.M1794.val % 7 + E1N.M1797.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1479
