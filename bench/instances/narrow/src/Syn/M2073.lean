import Syn.M709
import Syn.M710
import Syn.M1005
import Syn.M1366
import Syn.M1441
import Syn.M1716
import Syn.M2029

namespace Syn.M2073
def val : Nat := Syn.M709.val % 7 + Syn.M710.val % 7 + Syn.M1005.val % 7 + Syn.M1366.val % 7 + Syn.M1441.val % 7 + Syn.M1716.val % 7 + Syn.M2029.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end Syn.M2073
