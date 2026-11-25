import Syn.M1490
import Syn.M1530
import Syn.M1699

namespace Syn.M1711
def val : Nat := Syn.M1490.val % 7 + Syn.M1530.val % 7 + Syn.M1699.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1711
