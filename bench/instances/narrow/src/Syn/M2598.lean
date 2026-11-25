import Syn.M2464
import Syn.M2592

namespace Syn.M2598
def val : Nat := Syn.M2464.val % 7 + Syn.M2592.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2598
