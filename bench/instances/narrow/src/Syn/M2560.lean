import Syn.M1158
import Syn.M1357
import Syn.M1993
import Syn.M2504
import Syn.M2532
import Syn.M2542

namespace Syn.M2560
def val : Nat := Syn.M1158.val % 7 + Syn.M1357.val % 7 + Syn.M1993.val % 7 + Syn.M2504.val % 7 + Syn.M2532.val % 7 + Syn.M2542.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M2560
