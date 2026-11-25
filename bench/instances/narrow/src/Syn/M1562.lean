import Syn.M1065
import Syn.M1102
import Syn.M1114
import Syn.M1243
import Syn.M1245
import Syn.M1396
import Syn.M1526

namespace Syn.M1562
def val : Nat := Syn.M1065.val % 7 + Syn.M1102.val % 7 + Syn.M1114.val % 7 + Syn.M1243.val % 7 + Syn.M1245.val % 7 + Syn.M1396.val % 7 + Syn.M1526.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end Syn.M1562
