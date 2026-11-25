import Syn.M660
import Syn.M1692
import Syn.M1750
import Syn.M1765
import Syn.M1836
import Syn.M1884
import Syn.M1997
import Syn.M2296

namespace Syn.M2314
def val : Nat := Syn.M660.val % 7 + Syn.M1692.val % 7 + Syn.M1750.val % 7 + Syn.M1765.val % 7 + Syn.M1836.val % 7 + Syn.M1884.val % 7 + Syn.M1997.val % 7 + Syn.M2296.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
end Syn.M2314
