import Syn.M1781
import Syn.M2367

namespace Syn.M2374
def val : Nat := Syn.M1781.val % 7 + Syn.M2367.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2374
