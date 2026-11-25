import Syn.M1224
import Syn.M1599
import Syn.M1624

namespace Syn.M1645
def val : Nat := Syn.M1224.val % 7 + Syn.M1599.val % 7 + Syn.M1624.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1645
