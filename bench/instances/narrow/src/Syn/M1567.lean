import Syn.M833
import Syn.M873
import Syn.M1114
import Syn.M1149
import Syn.M1164
import Syn.M1244
import Syn.M1510
import Syn.M1532

namespace Syn.M1567
def val : Nat := Syn.M833.val % 7 + Syn.M873.val % 7 + Syn.M1114.val % 7 + Syn.M1149.val % 7 + Syn.M1164.val % 7 + Syn.M1244.val % 7 + Syn.M1510.val % 7 + Syn.M1532.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
theorem w7 (a b : Nat) : a + b + 7 = b + a + 7 := by omega
theorem w8 (a b : Nat) : a + b + 8 = b + a + 8 := by omega
theorem w9 (a b : Nat) : a + b + 9 = b + a + 9 := by omega
end Syn.M1567
