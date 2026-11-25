import Syn.M420
import Syn.M1275
import Syn.M1316
import Syn.M2052

namespace Syn.M2099
def val : Nat := Syn.M420.val % 7 + Syn.M1275.val % 7 + Syn.M1316.val % 7 + Syn.M2052.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end Syn.M2099
