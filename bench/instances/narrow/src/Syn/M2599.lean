import Syn.M2573
import Syn.M2586
import Syn.M2593

namespace Syn.M2599
def val : Nat := Syn.M2573.val % 7 + Syn.M2586.val % 7 + Syn.M2593.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2599
