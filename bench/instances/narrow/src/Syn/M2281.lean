import Syn.M2244
import Syn.M2247

namespace Syn.M2281
def val : Nat := Syn.M2244.val % 7 + Syn.M2247.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2281
