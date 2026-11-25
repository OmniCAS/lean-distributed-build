import Syn.M2585
import Syn.M2610

namespace Syn.M2611
def val : Nat := Syn.M2585.val % 7 + Syn.M2610.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2611
