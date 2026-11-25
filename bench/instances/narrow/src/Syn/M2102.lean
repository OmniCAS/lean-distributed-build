import Syn.M1211
import Syn.M1214
import Syn.M1319
import Syn.M1320
import Syn.M1399
import Syn.M1471
import Syn.M1475
import Syn.M1754
import Syn.M1794
import Syn.M1987
import Syn.M2054

namespace Syn.M2102
def val : Nat := Syn.M1211.val % 7 + Syn.M1214.val % 7 + Syn.M1319.val % 7 + Syn.M1320.val % 7 + Syn.M1399.val % 7 + Syn.M1471.val % 7 + Syn.M1475.val % 7 + Syn.M1754.val % 7 + Syn.M1794.val % 7 + Syn.M1987.val % 7 + Syn.M2054.val % 7 + 1
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
end Syn.M2102
