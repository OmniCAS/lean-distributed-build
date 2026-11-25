import Syn.M2483
import Syn.M2489

namespace Syn.M2499
def val : Nat := Syn.M2483.val % 7 + Syn.M2489.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2499
