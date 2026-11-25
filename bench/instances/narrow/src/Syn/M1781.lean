import Syn.M1505
import Syn.M1772

namespace Syn.M1781
def val : Nat := Syn.M1505.val % 7 + Syn.M1772.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1781
