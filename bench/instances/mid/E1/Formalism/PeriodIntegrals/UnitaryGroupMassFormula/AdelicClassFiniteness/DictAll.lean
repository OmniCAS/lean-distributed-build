import E1.Formalism.PeriodIntegrals.AdelClassFin
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.AdelicClassFiniteness.DictGen
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.AdelicClassFiniteness.DictInter
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.AdelicClassFiniteness.DictLat
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.AdelicClassFiniteness.DictPlan
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.AdelicClassFiniteness.DictRing
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.AdelicClassFiniteness.DictTop
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.AdelicClassFiniteness.StGenusOf

set_option Elab.async false

namespace E1N.M1547
def val : Nat := E1N.M1410.val % 7 + E1N.M1548.val % 7 + E1N.M1549.val % 7 + E1N.M1550.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end E1N.M1547
