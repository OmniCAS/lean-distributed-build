import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.LCcompLemmas
import E1.Formalism.GradedWeylDivisibility.StatementC

set_option Elab.async false

namespace E1N.M319
def val : Nat := E1N.M350.val % 7 + E1N.M404.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end E1N.M319
