import Syn.M833
import Syn.M836
import Syn.M837
import Syn.M960
import Syn.M1108
import Syn.M1163
import Syn.M1336

namespace Syn.M1364
def val : Nat := Syn.M833.val % 7 + Syn.M836.val % 7 + Syn.M837.val % 7 + Syn.M960.val % 7 + Syn.M1108.val % 7 + Syn.M1163.val % 7 + Syn.M1336.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1364
