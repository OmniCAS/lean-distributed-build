import Syn.M2362
import Syn.M2365

namespace Syn.M2373
def val : Nat := Syn.M2362.val % 7 + Syn.M2365.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2373
