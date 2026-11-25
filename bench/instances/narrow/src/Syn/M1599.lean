import Syn.M1510
import Syn.M1556
import Syn.M1557

namespace Syn.M1599
def val : Nat := Syn.M1510.val % 7 + Syn.M1556.val % 7 + Syn.M1557.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M1599
