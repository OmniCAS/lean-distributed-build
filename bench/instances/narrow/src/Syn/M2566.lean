import Syn.M2465
import Syn.M2551

namespace Syn.M2566
def val : Nat := Syn.M2465.val % 7 + Syn.M2551.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2566
