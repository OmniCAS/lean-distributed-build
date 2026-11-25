import Syn.M2275
import Syn.M2345

namespace Syn.M2358
def val : Nat := Syn.M2275.val % 7 + Syn.M2345.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2358
