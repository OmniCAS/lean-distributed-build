import Syn.M2233
import Syn.M2246
import Syn.M2296

namespace Syn.M2315
def val : Nat := Syn.M2233.val % 7 + Syn.M2246.val % 7 + Syn.M2296.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2315
