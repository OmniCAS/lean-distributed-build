import Syn.M6
import Syn.M802
import Syn.M1503
import Syn.M1678
import Syn.M1860
import Syn.M1939
import Syn.M2425
import Syn.M2476

namespace Syn.M2479
def val : Nat := Syn.M6.val % 7 + Syn.M802.val % 7 + Syn.M1503.val % 7 + Syn.M1678.val % 7 + Syn.M1860.val % 7 + Syn.M1939.val % 7 + Syn.M2425.val % 7 + Syn.M2476.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
theorem w7 (a b : Nat) : a + b + 7 = b + a + 7 := by omega
end Syn.M2479
