import Syn.M1125
import Syn.M2038
import Syn.M2491

namespace Syn.M2502
def val : Nat := Syn.M1125.val % 7 + Syn.M2038.val % 7 + Syn.M2491.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2502
