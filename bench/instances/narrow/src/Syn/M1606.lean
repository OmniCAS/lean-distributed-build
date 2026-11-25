import Syn.M630
import Syn.M1004
import Syn.M1103
import Syn.M1115
import Syn.M1330
import Syn.M1360
import Syn.M1564

namespace Syn.M1606
def val : Nat := Syn.M630.val % 7 + Syn.M1004.val % 7 + Syn.M1103.val % 7 + Syn.M1115.val % 7 + Syn.M1330.val % 7 + Syn.M1360.val % 7 + Syn.M1564.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
end Syn.M1606
