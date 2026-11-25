import Syn.M696
import Syn.M1482
import Syn.M1525
import Syn.M1561
import Syn.M1634
import Syn.M1706
import Syn.M1810
import Syn.M1860
import Syn.M2142
import Syn.M2245
import Syn.M2246
import Syn.M2281

namespace Syn.M2302
def val : Nat := Syn.M696.val % 7 + Syn.M1482.val % 7 + Syn.M1525.val % 7 + Syn.M1561.val % 7 + Syn.M1634.val % 7 + Syn.M1706.val % 7 + Syn.M1810.val % 7 + Syn.M1860.val % 7 + Syn.M2142.val % 7 + Syn.M2245.val % 7 + Syn.M2246.val % 7 + Syn.M2281.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
theorem w7 (a b : Nat) : a + b + 7 = b + a + 7 := by omega
theorem w8 (a b : Nat) : a + b + 8 = b + a + 8 := by omega
end Syn.M2302
