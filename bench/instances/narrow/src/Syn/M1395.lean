import Syn.M989
import Syn.M1363

namespace Syn.M1395
def val : Nat := Syn.M989.val % 7 + Syn.M1363.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1395
