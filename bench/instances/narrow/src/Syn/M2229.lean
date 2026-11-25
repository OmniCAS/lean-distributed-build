import Syn.M1391
import Syn.M1460
import Syn.M1461
import Syn.M1495
import Syn.M1680
import Syn.M1711
import Syn.M1841
import Syn.M1842
import Syn.M2190
import Syn.M2208

namespace Syn.M2229
def val : Nat := Syn.M1391.val % 7 + Syn.M1460.val % 7 + Syn.M1461.val % 7 + Syn.M1495.val % 7 + Syn.M1680.val % 7 + Syn.M1711.val % 7 + Syn.M1841.val % 7 + Syn.M1842.val % 7 + Syn.M2190.val % 7 + Syn.M2208.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2229
