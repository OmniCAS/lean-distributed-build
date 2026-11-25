import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.TermAttractorConstant.GenericityConstantDoubleCosets

set_option Elab.async false

namespace E1N.M1512
def val : Nat := E1N.M1986.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end E1N.M1512
