import Syn.M1526
import Syn.M1692
import Syn.M1727
import Syn.M1906
import Syn.M2180

namespace Syn.M2197
def val : Nat := Syn.M1526.val % 7 + Syn.M1692.val % 7 + Syn.M1727.val % 7 + Syn.M1906.val % 7 + Syn.M2180.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2197
