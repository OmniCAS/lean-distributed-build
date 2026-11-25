import Syn.M2508
import Syn.M2509
import Syn.M2510

namespace Syn.M2526
def val : Nat := Syn.M2508.val % 7 + Syn.M2509.val % 7 + Syn.M2510.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2526
