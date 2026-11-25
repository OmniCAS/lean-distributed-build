import Syn.M1157
import Syn.M1228
import Syn.M1284
import Syn.M1478
import Syn.M1503
import Syn.M1564
import Syn.M1857
import Syn.M1905
import Syn.M1906

namespace Syn.M1939
def val : Nat := Syn.M1157.val % 7 + Syn.M1228.val % 7 + Syn.M1284.val % 7 + Syn.M1478.val % 7 + Syn.M1503.val % 7 + Syn.M1564.val % 7 + Syn.M1857.val % 7 + Syn.M1905.val % 7 + Syn.M1906.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
end Syn.M1939
