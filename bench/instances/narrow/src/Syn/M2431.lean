import Syn.M1005
import Syn.M1114
import Syn.M1164
import Syn.M1256
import Syn.M1343
import Syn.M1391
import Syn.M1441
import Syn.M1450
import Syn.M1463
import Syn.M1490
import Syn.M1531
import Syn.M2425

namespace Syn.M2431
def val : Nat := Syn.M1005.val % 7 + Syn.M1114.val % 7 + Syn.M1164.val % 7 + Syn.M1256.val % 7 + Syn.M1343.val % 7 + Syn.M1391.val % 7 + Syn.M1441.val % 7 + Syn.M1450.val % 7 + Syn.M1463.val % 7 + Syn.M1490.val % 7 + Syn.M1531.val % 7 + Syn.M2425.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
end Syn.M2431
