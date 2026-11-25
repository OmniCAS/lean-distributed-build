import Syn.M2046
import Syn.M2092

namespace Syn.M2122
def val : Nat := Syn.M2046.val % 7 + Syn.M2092.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2122
