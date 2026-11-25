import Syn.M2407
import Syn.M2408

namespace Syn.M2421
def val : Nat := Syn.M2407.val % 7 + Syn.M2408.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2421
