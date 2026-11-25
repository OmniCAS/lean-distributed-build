import Syn.M1631
import Syn.M2335
import Syn.M2521

namespace Syn.M2534
def val : Nat := Syn.M1631.val % 7 + Syn.M2335.val % 7 + Syn.M2521.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2534
