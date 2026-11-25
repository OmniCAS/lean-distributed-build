import Syn.M2234
import Syn.M2295

namespace Syn.M2313
def val : Nat := Syn.M2234.val % 7 + Syn.M2295.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2313
