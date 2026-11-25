import Syn.M1799
import Syn.M1800
import Syn.M1810

namespace Syn.M1832
def val : Nat := Syn.M1799.val % 7 + Syn.M1800.val % 7 + Syn.M1810.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1832
