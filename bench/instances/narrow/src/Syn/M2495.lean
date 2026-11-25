import Syn.M2481
import Syn.M2484

namespace Syn.M2495
def val : Nat := Syn.M2481.val % 7 + Syn.M2484.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2495
