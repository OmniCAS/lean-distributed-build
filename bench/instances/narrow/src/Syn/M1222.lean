import Syn.M456
import Syn.M535
import Syn.M747
import Syn.M749
import Syn.M1043
import Syn.M1044
import Syn.M1093
import Syn.M1131
import Syn.M1157

namespace Syn.M1222
def val : Nat := Syn.M456.val % 7 + Syn.M535.val % 7 + Syn.M747.val % 7 + Syn.M749.val % 7 + Syn.M1043.val % 7 + Syn.M1044.val % 7 + Syn.M1093.val % 7 + Syn.M1131.val % 7 + Syn.M1157.val % 7 + 1
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
end Syn.M1222
