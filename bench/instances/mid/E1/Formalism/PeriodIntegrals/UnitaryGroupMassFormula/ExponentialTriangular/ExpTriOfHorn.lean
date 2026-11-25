import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ExponentialTriangular.ExpTriOf
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ExponentialTriangular.PsumEqRange
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ExponentialTriangular.SpecExists

set_option Elab.async false

namespace E1N.M1626
def val : Nat := E1N.M1625.val % 7 + E1N.M1629.val % 7 + E1N.M1631.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1626
