import Syn.M694
import Syn.M2219

namespace Syn.M2237
def val : Nat := Syn.M694.val % 7 + Syn.M2219.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2237
