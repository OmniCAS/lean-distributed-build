import Syn.M1005
import Syn.M1114
import Syn.M1343
import Syn.M1379
import Syn.M1451
import Syn.M1452
import Syn.M1453
import Syn.M1489

namespace Syn.M1530
def val : Nat := Syn.M1005.val % 7 + Syn.M1114.val % 7 + Syn.M1343.val % 7 + Syn.M1379.val % 7 + Syn.M1451.val % 7 + Syn.M1452.val % 7 + Syn.M1453.val % 7 + Syn.M1489.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M1530
