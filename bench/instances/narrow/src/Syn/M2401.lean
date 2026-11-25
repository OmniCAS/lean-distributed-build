import Syn.M2319
import Syn.M2390

namespace Syn.M2401
def val : Nat := Syn.M2319.val % 7 + Syn.M2390.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2401
