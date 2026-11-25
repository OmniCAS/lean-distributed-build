import Syn.M2202
import Syn.M2203

namespace Syn.M2226
def val : Nat := Syn.M2202.val % 7 + Syn.M2203.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2226
