import Syn.M1232
import Syn.M1491

namespace Syn.M1532
def val : Nat := Syn.M1232.val % 7 + Syn.M1491.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1532
