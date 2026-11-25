import Syn.M2278
import Syn.M2281

namespace Syn.M2303
def val : Nat := Syn.M2278.val % 7 + Syn.M2281.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2303
