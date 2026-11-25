import Syn.M2498
import Syn.M2499
import Syn.M2500

namespace Syn.M2514
def val : Nat := Syn.M2498.val % 7 + Syn.M2499.val % 7 + Syn.M2500.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2514
