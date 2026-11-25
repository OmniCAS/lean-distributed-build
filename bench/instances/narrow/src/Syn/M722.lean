import Syn.M60
import Syn.M363
import Syn.M648

namespace Syn.M722
def val : Nat := Syn.M60.val % 7 + Syn.M363.val % 7 + Syn.M648.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M722
