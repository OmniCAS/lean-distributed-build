import Syn.M1067
import Syn.M1116
import Syn.M1366
import Syn.M1769
import Syn.M1810
import Syn.M1836
import Syn.M2114
import Syn.M2142
import Syn.M2235
import Syn.M2296
import Syn.M2298

namespace Syn.M2317
def val : Nat := Syn.M1067.val % 7 + Syn.M1116.val % 7 + Syn.M1366.val % 7 + Syn.M1769.val % 7 + Syn.M1810.val % 7 + Syn.M1836.val % 7 + Syn.M2114.val % 7 + Syn.M2142.val % 7 + Syn.M2235.val % 7 + Syn.M2296.val % 7 + Syn.M2298.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end Syn.M2317
