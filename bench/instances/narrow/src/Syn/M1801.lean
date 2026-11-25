import Syn.M420
import Syn.M1058
import Syn.M1116
import Syn.M1275
import Syn.M1789

namespace Syn.M1801
def val : Nat := Syn.M420.val % 7 + Syn.M1058.val % 7 + Syn.M1116.val % 7 + Syn.M1275.val % 7 + Syn.M1789.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
end Syn.M1801
