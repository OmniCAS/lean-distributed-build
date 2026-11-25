import Syn.M1482
import Syn.M1526
import Syn.M1706
import Syn.M1860
import Syn.M2235

namespace Syn.M2271
def val : Nat := Syn.M1482.val % 7 + Syn.M1526.val % 7 + Syn.M1706.val % 7 + Syn.M1860.val % 7 + Syn.M2235.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2271
