import Syn.M2436
import Syn.M2453

namespace Syn.M2463
def val : Nat := Syn.M2436.val % 7 + Syn.M2453.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2463
