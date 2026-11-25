import E1.Formalism.FormalGroupWitt.FormalGroupWittProofs.EqSingleOfDegreeEqOne

set_option Elab.async false

namespace E1N.M4295
def val : Nat := E1N.M2557.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end E1N.M4295
