import E1.Formalism.PeriodIntegrals.ExpTri
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ExponentialTriangular.ExpTriOfHorn
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ExponentialTriangular.NormDetConjExp
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ExponentialTriangular.ProdLeOfInjective

set_option Elab.async false

namespace E1N.M1462
def val : Nat := E1N.M1421.val % 7 + E1N.M1626.val % 7 + E1N.M1627.val % 7 + E1N.M1628.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end E1N.M1462
