import Syn.M916
import Syn.M1005
import Syn.M1117
import Syn.M1168
import Syn.M1343
import Syn.M2540
import Syn.M2553

namespace Syn.M2567
def val : Nat := Syn.M916.val % 7 + Syn.M1005.val % 7 + Syn.M1117.val % 7 + Syn.M1168.val % 7 + Syn.M1343.val % 7 + Syn.M2540.val % 7 + Syn.M2553.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2567
