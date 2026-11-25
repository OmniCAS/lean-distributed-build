import Syn.M2261
import Syn.M2294
import Syn.M2318

namespace Syn.M2343
def val : Nat := Syn.M2261.val % 7 + Syn.M2294.val % 7 + Syn.M2318.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2343
