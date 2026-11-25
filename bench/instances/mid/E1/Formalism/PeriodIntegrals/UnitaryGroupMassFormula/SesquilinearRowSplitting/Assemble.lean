import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.SesquilinearRowSplitting.AdjointActionReduction
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.SesquilinearRowSplitting.CoreStepOf
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.SesquilinearRowSplitting.FrameReduction
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.SesquilinearRowSplitting.SecondDualReduction
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.SesquilinearRowSplitting.SplitRowOf

set_option Elab.async false

namespace E1N.M1958
def val : Nat := E1N.M1957.val % 7 + E1N.M1961.val % 7 + E1N.M1963.val % 7 + E1N.M1966.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end E1N.M1958
