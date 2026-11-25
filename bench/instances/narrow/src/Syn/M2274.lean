import Syn.M2237
import Syn.M2239
import Syn.M2242

namespace Syn.M2274
def val : Nat := Syn.M2237.val % 7 + Syn.M2239.val % 7 + Syn.M2242.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2274
