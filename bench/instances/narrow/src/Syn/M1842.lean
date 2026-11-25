import Syn.M833
import Syn.M1150
import Syn.M1164
import Syn.M1200
import Syn.M1389
import Syn.M1390
import Syn.M1396
import Syn.M1454
import Syn.M1657
import Syn.M1668
import Syn.M1816

namespace Syn.M1842
def val : Nat := Syn.M833.val % 7 + Syn.M1150.val % 7 + Syn.M1164.val % 7 + Syn.M1200.val % 7 + Syn.M1389.val % 7 + Syn.M1390.val % 7 + Syn.M1396.val % 7 + Syn.M1454.val % 7 + Syn.M1657.val % 7 + Syn.M1668.val % 7 + Syn.M1816.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
end Syn.M1842
