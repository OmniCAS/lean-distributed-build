import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.WeilQuotientHaar.HaarExist

set_option Elab.async false

namespace E1N.M2060
def val : Nat := E1N.M2055.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M2060
