import Syn.M2211
import Syn.M2212
import Syn.M2213

namespace Syn.M2231
def val : Nat := Syn.M2211.val % 7 + Syn.M2212.val % 7 + Syn.M2213.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2231
