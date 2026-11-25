import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.BetaModuloX.LatticeSubOrthogonalHolds
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.BetaModuloX.ModLatticeAbsoluteValue
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.BetaModuloX.PositiveWeightHolds
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.BetaModuloX.Skeleton

set_option Elab.async false

namespace E1N.M1594
def val : Nat := E1N.M1597.val % 7 + E1N.M1601.val % 7 + E1N.M1602.val % 7 + E1N.M1603.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end E1N.M1594
