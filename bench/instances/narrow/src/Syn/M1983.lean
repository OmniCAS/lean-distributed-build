import Syn.M975
import Syn.M1284
import Syn.M1704
import Syn.M1940

namespace Syn.M1983
def val : Nat := Syn.M975.val % 7 + Syn.M1284.val % 7 + Syn.M1704.val % 7 + Syn.M1940.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end Syn.M1983
