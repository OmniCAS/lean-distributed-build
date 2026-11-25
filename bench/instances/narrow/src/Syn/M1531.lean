import Syn.M1005
import Syn.M1114
import Syn.M1343
import Syn.M1391
import Syn.M1429
import Syn.M1441
import Syn.M1451
import Syn.M1452
import Syn.M1489
import Syn.M1490

namespace Syn.M1531
def val : Nat := Syn.M1005.val % 7 + Syn.M1114.val % 7 + Syn.M1343.val % 7 + Syn.M1391.val % 7 + Syn.M1429.val % 7 + Syn.M1441.val % 7 + Syn.M1451.val % 7 + Syn.M1452.val % 7 + Syn.M1489.val % 7 + Syn.M1490.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1531
