import Syn.M1962
import Syn.M2010
import Syn.M2185

namespace Syn.M2203
def val : Nat := Syn.M1962.val % 7 + Syn.M2010.val % 7 + Syn.M2185.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2203
