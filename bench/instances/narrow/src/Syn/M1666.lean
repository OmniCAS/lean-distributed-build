import Syn.M885
import Syn.M1379
import Syn.M1504
import Syn.M1554
import Syn.M1647

namespace Syn.M1666
def val : Nat := Syn.M885.val % 7 + Syn.M1379.val % 7 + Syn.M1504.val % 7 + Syn.M1554.val % 7 + Syn.M1647.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end Syn.M1666
