import E1.Formalism.PeriodIntegrals.PhConvProj
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ConvolutionProjection.ConvProjOf
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ConvolutionProjection.SelfAdj
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.ConvolutionProjection.UrepMulApply

set_option Elab.async false

namespace E1N.M1487
def val : Nat := E1N.M1523.val % 7 + E1N.M1620.val % 7 + E1N.M1621.val % 7 + E1N.M1622.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M1487
