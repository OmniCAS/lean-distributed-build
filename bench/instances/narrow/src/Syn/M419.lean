import Syn.M238
import Syn.M356

namespace Syn.M419
def val : Nat := Syn.M238.val % 7 + Syn.M356.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M419
