import Syn.M1857
import Syn.M2001

namespace Syn.M2054
def val : Nat := Syn.M1857.val % 7 + Syn.M2001.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2054
