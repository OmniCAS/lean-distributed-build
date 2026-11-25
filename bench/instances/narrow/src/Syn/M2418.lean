import Syn.M1274
import Syn.M1275
import Syn.M1325
import Syn.M1810
import Syn.M1833
import Syn.M1852
import Syn.M1877
import Syn.M1907
import Syn.M2003
import Syn.M2048
import Syn.M2122
import Syn.M2205
import Syn.M2379
import Syn.M2401

namespace Syn.M2418
def val : Nat := Syn.M1274.val % 7 + Syn.M1275.val % 7 + Syn.M1325.val % 7 + Syn.M1810.val % 7 + Syn.M1833.val % 7 + Syn.M1852.val % 7 + Syn.M1877.val % 7 + Syn.M1907.val % 7 + Syn.M2003.val % 7 + Syn.M2048.val % 7 + Syn.M2122.val % 7 + Syn.M2205.val % 7 + Syn.M2379.val % 7 + Syn.M2401.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
end Syn.M2418
