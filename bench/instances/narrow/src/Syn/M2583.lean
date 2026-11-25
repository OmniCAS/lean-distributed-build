import Syn.M916
import Syn.M1117
import Syn.M2540
import Syn.M2567

namespace Syn.M2583
def val : Nat := Syn.M916.val % 7 + Syn.M1117.val % 7 + Syn.M2540.val % 7 + Syn.M2567.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2583
