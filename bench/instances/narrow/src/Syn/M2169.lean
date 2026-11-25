import Syn.M1221
import Syn.M1877
import Syn.M2003
import Syn.M2124
import Syn.M2147

namespace Syn.M2169
def val : Nat := Syn.M1221.val % 7 + Syn.M1877.val % 7 + Syn.M2003.val % 7 + Syn.M2124.val % 7 + Syn.M2147.val % 7 + 1
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
end Syn.M2169
