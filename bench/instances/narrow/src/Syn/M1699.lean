import Syn.M971
import Syn.M1114
import Syn.M1244
import Syn.M1313
import Syn.M1379
import Syn.M1453
import Syn.M1468
import Syn.M1484
import Syn.M1532
import Syn.M1669
import Syn.M1685

namespace Syn.M1699
def val : Nat := Syn.M971.val % 7 + Syn.M1114.val % 7 + Syn.M1244.val % 7 + Syn.M1313.val % 7 + Syn.M1379.val % 7 + Syn.M1453.val % 7 + Syn.M1468.val % 7 + Syn.M1484.val % 7 + Syn.M1532.val % 7 + Syn.M1669.val % 7 + Syn.M1685.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end Syn.M1699
