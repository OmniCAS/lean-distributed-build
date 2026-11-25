import Syn.M1760
import Syn.M1774
import Syn.M2163

namespace Syn.M2178
def val : Nat := Syn.M1760.val % 7 + Syn.M1774.val % 7 + Syn.M2163.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2178
