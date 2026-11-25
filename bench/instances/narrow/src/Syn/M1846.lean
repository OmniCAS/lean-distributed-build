import Syn.M1100
import Syn.M1104
import Syn.M1483
import Syn.M1689
import Syn.M1796
import Syn.M1819

namespace Syn.M1846
def val : Nat := Syn.M1100.val % 7 + Syn.M1104.val % 7 + Syn.M1483.val % 7 + Syn.M1689.val % 7 + Syn.M1796.val % 7 + Syn.M1819.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
end Syn.M1846
