import Syn.M278
import Syn.M643

namespace Syn.M719
def val : Nat := Syn.M278.val % 7 + Syn.M643.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M719
