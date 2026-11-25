import Syn.M2596
import Syn.M2600

namespace Syn.M2603
def val : Nat := Syn.M2596.val % 7 + Syn.M2600.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2603
