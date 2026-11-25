import Syn.M1810
import Syn.M2187
import Syn.M2262

namespace Syn.M2294
def val : Nat := Syn.M1810.val % 7 + Syn.M2187.val % 7 + Syn.M2262.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2294
