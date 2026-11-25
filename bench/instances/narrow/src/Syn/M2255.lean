import Syn.M1098
import Syn.M1582
import Syn.M2227

namespace Syn.M2255
def val : Nat := Syn.M1098.val % 7 + Syn.M1582.val % 7 + Syn.M2227.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2255
