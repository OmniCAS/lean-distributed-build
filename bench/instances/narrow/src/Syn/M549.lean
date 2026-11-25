import Syn.M369
import Syn.M436
import Syn.M487

namespace Syn.M549
def val : Nat := Syn.M369.val % 7 + Syn.M436.val % 7 + Syn.M487.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M549
