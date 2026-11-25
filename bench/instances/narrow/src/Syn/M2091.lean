import Syn.M694
import Syn.M1404
import Syn.M1526
import Syn.M1884
import Syn.M1938
import Syn.M1983
import Syn.M2046

namespace Syn.M2091
def val : Nat := Syn.M694.val % 7 + Syn.M1404.val % 7 + Syn.M1526.val % 7 + Syn.M1884.val % 7 + Syn.M1938.val % 7 + Syn.M1983.val % 7 + Syn.M2046.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end Syn.M2091
