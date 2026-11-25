import Syn.M420
import Syn.M630
import Syn.M638
import Syn.M1112
import Syn.M1290

namespace Syn.M1336
def val : Nat := Syn.M420.val % 7 + Syn.M630.val % 7 + Syn.M638.val % 7 + Syn.M1112.val % 7 + Syn.M1290.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
end Syn.M1336
