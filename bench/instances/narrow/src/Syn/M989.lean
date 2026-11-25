import Syn.M796
import Syn.M911

namespace Syn.M989
def val : Nat := Syn.M796.val % 7 + Syn.M911.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M989
