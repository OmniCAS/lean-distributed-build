import Syn.M1599
import Syn.M1600

namespace Syn.M1628
def val : Nat := Syn.M1599.val % 7 + Syn.M1600.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1628
