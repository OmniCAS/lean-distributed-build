import Syn.M160
import Syn.M232
import Syn.M346

namespace Syn.M416
def val : Nat := Syn.M160.val % 7 + Syn.M232.val % 7 + Syn.M346.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M416
