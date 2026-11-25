import Syn.M632
import Syn.M706
import Syn.M709
import Syn.M1147
import Syn.M1166
import Syn.M1396
import Syn.M1914
import Syn.M1915
import Syn.M1917

namespace Syn.M1945
def val : Nat := Syn.M632.val % 7 + Syn.M706.val % 7 + Syn.M709.val % 7 + Syn.M1147.val % 7 + Syn.M1166.val % 7 + Syn.M1396.val % 7 + Syn.M1914.val % 7 + Syn.M1915.val % 7 + Syn.M1917.val % 7 + 1
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
end Syn.M1945
