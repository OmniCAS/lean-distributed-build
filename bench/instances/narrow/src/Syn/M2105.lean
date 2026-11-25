import Syn.M2008
import Syn.M2057

namespace Syn.M2105
def val : Nat := Syn.M2008.val % 7 + Syn.M2057.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2105
