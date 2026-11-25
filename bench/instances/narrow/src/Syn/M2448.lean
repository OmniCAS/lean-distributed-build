import Syn.M333
import Syn.M1859
import Syn.M2169
import Syn.M2436

namespace Syn.M2448
def val : Nat := Syn.M333.val % 7 + Syn.M1859.val % 7 + Syn.M2169.val % 7 + Syn.M2436.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end Syn.M2448
