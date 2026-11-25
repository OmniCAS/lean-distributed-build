import Syn.M421
import Syn.M628
import Syn.M930
import Syn.M1004
import Syn.M1107
import Syn.M1114
import Syn.M1157
import Syn.M1242
import Syn.M1339
import Syn.M1366
import Syn.M1526
import Syn.M1551

namespace Syn.M1593
def val : Nat := Syn.M421.val % 7 + Syn.M628.val % 7 + Syn.M930.val % 7 + Syn.M1004.val % 7 + Syn.M1107.val % 7 + Syn.M1114.val % 7 + Syn.M1157.val % 7 + Syn.M1242.val % 7 + Syn.M1339.val % 7 + Syn.M1366.val % 7 + Syn.M1526.val % 7 + Syn.M1551.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
theorem w7 (a b : Nat) : a + b + 7 = b + a + 7 := by omega
theorem w8 (a b : Nat) : a + b + 8 = b + a + 8 := by omega
end Syn.M1593
