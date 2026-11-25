import Syn.M515
import Syn.M567
import Syn.M615
import Syn.M1157
import Syn.M1219
import Syn.M1220
import Syn.M1273
import Syn.M1558

namespace Syn.M1601
def val : Nat := Syn.M515.val % 7 + Syn.M567.val % 7 + Syn.M615.val % 7 + Syn.M1157.val % 7 + Syn.M1219.val % 7 + Syn.M1220.val % 7 + Syn.M1273.val % 7 + Syn.M1558.val % 7 + 1
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
theorem w10 (a b : Nat) : a + b + 10 = b + a + 10 := by omega
end Syn.M1601
