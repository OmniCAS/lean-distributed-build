import Syn.M916
import Syn.M1117
import Syn.M1637
import Syn.M2540
import Syn.M2569
import Syn.M2570
import Syn.M2571
import Syn.M2584
import Syn.M2597

namespace Syn.M2602
def val : Nat := Syn.M916.val % 7 + Syn.M1117.val % 7 + Syn.M1637.val % 7 + Syn.M2540.val % 7 + Syn.M2569.val % 7 + Syn.M2570.val % 7 + Syn.M2571.val % 7 + Syn.M2584.val % 7 + Syn.M2597.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2602
