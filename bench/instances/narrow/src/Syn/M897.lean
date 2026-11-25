import Syn.M668
import Syn.M766

namespace Syn.M897
def val : Nat := Syn.M668.val % 7 + Syn.M766.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M897
