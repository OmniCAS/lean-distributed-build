import Syn.M1336
import Syn.M1727

namespace Syn.M1749
def val : Nat := Syn.M1336.val % 7 + Syn.M1727.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1749
