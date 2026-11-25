import Syn.M833
import Syn.M932
import Syn.M1067
import Syn.M1164
import Syn.M1264
import Syn.M1433
import Syn.M1798

namespace Syn.M1817
def val : Nat := Syn.M833.val % 7 + Syn.M932.val % 7 + Syn.M1067.val % 7 + Syn.M1164.val % 7 + Syn.M1264.val % 7 + Syn.M1433.val % 7 + Syn.M1798.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
theorem w7 (a b : Nat) : a + b + 7 = b + a + 7 := by omega
end Syn.M1817
