import Syn.M1279
import Syn.M1280
import Syn.M1281
import Syn.M1329
import Syn.M1421
import Syn.M1424
import Syn.M1457
import Syn.M1563
import Syn.M1604
import Syn.M1627
import Syn.M1803
import Syn.M1825
import Syn.M1905
import Syn.M1906
import Syn.M1937
import Syn.M1974

namespace Syn.M2029
def val : Nat := Syn.M1279.val % 7 + Syn.M1280.val % 7 + Syn.M1281.val % 7 + Syn.M1329.val % 7 + Syn.M1421.val % 7 + Syn.M1424.val % 7 + Syn.M1457.val % 7 + Syn.M1563.val % 7 + Syn.M1604.val % 7 + Syn.M1627.val % 7 + Syn.M1803.val % 7 + Syn.M1825.val % 7 + Syn.M1905.val % 7 + Syn.M1906.val % 7 + Syn.M1937.val % 7 + Syn.M1974.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end Syn.M2029
