import Syn.M1005
import Syn.M1114
import Syn.M1200
import Syn.M1343
import Syn.M1391
import Syn.M1420
import Syn.M1441
import Syn.M1490
import Syn.M1494
import Syn.M1532
import Syn.M1571

namespace Syn.M1611
def val : Nat := Syn.M1005.val % 7 + Syn.M1114.val % 7 + Syn.M1200.val % 7 + Syn.M1343.val % 7 + Syn.M1391.val % 7 + Syn.M1420.val % 7 + Syn.M1441.val % 7 + Syn.M1490.val % 7 + Syn.M1494.val % 7 + Syn.M1532.val % 7 + Syn.M1571.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end Syn.M1611
