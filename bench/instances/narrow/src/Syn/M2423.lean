import Syn.M1503
import Syn.M1810
import Syn.M2052
import Syn.M2101
import Syn.M2172
import Syn.M2186
import Syn.M2415

namespace Syn.M2423
def val : Nat := Syn.M1503.val % 7 + Syn.M1810.val % 7 + Syn.M2052.val % 7 + Syn.M2101.val % 7 + Syn.M2172.val % 7 + Syn.M2186.val % 7 + Syn.M2415.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end Syn.M2423
