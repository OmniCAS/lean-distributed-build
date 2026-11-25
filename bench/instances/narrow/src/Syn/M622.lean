import Syn.M160
import Syn.M433
import Syn.M612

namespace Syn.M622
def val : Nat := Syn.M160.val % 7 + Syn.M433.val % 7 + Syn.M612.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M622
