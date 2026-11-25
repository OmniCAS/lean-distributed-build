import Syn.M696
import Syn.M971
import Syn.M1366
import Syn.M1510
import Syn.M1790
import Syn.M1810
import Syn.M1836
import Syn.M1924
import Syn.M2235

namespace Syn.M2263
def val : Nat := Syn.M696.val % 7 + Syn.M971.val % 7 + Syn.M1366.val % 7 + Syn.M1510.val % 7 + Syn.M1790.val % 7 + Syn.M1810.val % 7 + Syn.M1836.val % 7 + Syn.M1924.val % 7 + Syn.M2235.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
end Syn.M2263
