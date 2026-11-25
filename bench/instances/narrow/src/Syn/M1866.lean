import Syn.M1562
import Syn.M1806
import Syn.M1844

namespace Syn.M1866
def val : Nat := Syn.M1562.val % 7 + Syn.M1806.val % 7 + Syn.M1844.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1866
