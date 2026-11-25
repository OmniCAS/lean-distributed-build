import Syn.M232
import Syn.M344
import Syn.M416
import Syn.M422
import Syn.M722

namespace Syn.M855
def val : Nat := Syn.M232.val % 7 + Syn.M344.val % 7 + Syn.M416.val % 7 + Syn.M422.val % 7 + Syn.M722.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end Syn.M855
