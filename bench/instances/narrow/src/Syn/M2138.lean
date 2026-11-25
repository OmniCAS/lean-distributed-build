import Syn.M535
import Syn.M747
import Syn.M875
import Syn.M1024
import Syn.M2005
import Syn.M2110

namespace Syn.M2138
def val : Nat := Syn.M535.val % 7 + Syn.M747.val % 7 + Syn.M875.val % 7 + Syn.M1024.val % 7 + Syn.M2005.val % 7 + Syn.M2110.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
end Syn.M2138
