import Syn.M1833
import Syn.M2054
import Syn.M2428

namespace Syn.M2434
def val : Nat := Syn.M1833.val % 7 + Syn.M2054.val % 7 + Syn.M2428.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2434
