import Syn.M2445
import Syn.M2446
import Syn.M2448
import Syn.M2459
import Syn.M2463

namespace Syn.M2469
def val : Nat := Syn.M2445.val % 7 + Syn.M2446.val % 7 + Syn.M2448.val % 7 + Syn.M2459.val % 7 + Syn.M2463.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2469
