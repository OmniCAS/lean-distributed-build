import Syn.M372
import Syn.M491

namespace Syn.M551
def val : Nat := Syn.M372.val % 7 + Syn.M491.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M551
