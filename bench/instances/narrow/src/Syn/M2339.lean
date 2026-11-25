import Syn.M1727
import Syn.M1766
import Syn.M1767
import Syn.M1856
import Syn.M1996
import Syn.M2314

namespace Syn.M2339
def val : Nat := Syn.M1727.val % 7 + Syn.M1766.val % 7 + Syn.M1767.val % 7 + Syn.M1856.val % 7 + Syn.M1996.val % 7 + Syn.M2314.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2339
