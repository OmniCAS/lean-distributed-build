import Syn.M12
import Syn.M444
import Syn.M916
import Syn.M1168
import Syn.M1343
import Syn.M1370
import Syn.M1412
import Syn.M1414
import Syn.M1418
import Syn.M1445
import Syn.M1456

namespace Syn.M1493
def val : Nat := Syn.M12.val % 7 + Syn.M444.val % 7 + Syn.M916.val % 7 + Syn.M1168.val % 7 + Syn.M1343.val % 7 + Syn.M1370.val % 7 + Syn.M1412.val % 7 + Syn.M1414.val % 7 + Syn.M1418.val % 7 + Syn.M1445.val % 7 + Syn.M1456.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M1493
