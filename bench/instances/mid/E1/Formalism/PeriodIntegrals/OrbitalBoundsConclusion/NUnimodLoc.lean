import E1.Formalism.PeriodIntegrals.NUnimodLoc
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LocalUnimodularLattice.Development
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LocalUnimodularLattice.FrameC
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.LocalUnimodularLattice.Transf

set_option Elab.async false

namespace E1N.M1484
def val : Nat := E1N.M1450.val % 7 + E1N.M1820.val % 7 + E1N.M1821.val % 7 + E1N.M1823.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1484
