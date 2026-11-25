import Syn.M318
import Syn.M705
import Syn.M799
import Syn.M1366

namespace Syn.M1407
def val : Nat := Syn.M318.val % 7 + Syn.M705.val % 7 + Syn.M799.val % 7 + Syn.M1366.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1407
