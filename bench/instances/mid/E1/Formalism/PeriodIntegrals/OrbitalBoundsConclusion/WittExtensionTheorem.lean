import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.WittDecomposition.AnisotropicHolds
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.WittDecomposition.OneVector
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.WittDecomposition.WittOf
import E1.Formalism.PeriodIntegrals.WittExtension

set_option Elab.async false

namespace E1N.M1521
def val : Nat := E1N.M2078.val % 7 + E1N.M2082.val % 7 + E1N.M2083.val % 7 + E1N.M2090.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1521
