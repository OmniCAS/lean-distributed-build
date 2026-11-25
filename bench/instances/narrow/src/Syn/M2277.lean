import Syn.M2236
import Syn.M2246

namespace Syn.M2277
def val : Nat := Syn.M2236.val % 7 + Syn.M2246.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2277
