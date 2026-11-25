import Syn.M1271
import Syn.M1438
import Syn.M1482

namespace Syn.M1517
def val : Nat := Syn.M1271.val % 7 + Syn.M1438.val % 7 + Syn.M1482.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1517
