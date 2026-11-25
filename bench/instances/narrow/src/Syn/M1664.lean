import Syn.M1198
import Syn.M1200
import Syn.M1244
import Syn.M1468
import Syn.M1484
import Syn.M1504
import Syn.M1522
import Syn.M1567
import Syn.M1646

namespace Syn.M1664
def val : Nat := Syn.M1198.val % 7 + Syn.M1200.val % 7 + Syn.M1244.val % 7 + Syn.M1468.val % 7 + Syn.M1484.val % 7 + Syn.M1504.val % 7 + Syn.M1522.val % 7 + Syn.M1567.val % 7 + Syn.M1646.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1664
