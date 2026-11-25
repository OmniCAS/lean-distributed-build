import Syn.M381
import Syn.M401
import Syn.M663
import Syn.M874
import Syn.M993
import Syn.M1116
import Syn.M1242
import Syn.M1366

namespace Syn.M1405
def val : Nat := Syn.M381.val % 7 + Syn.M401.val % 7 + Syn.M663.val % 7 + Syn.M874.val % 7 + Syn.M993.val % 7 + Syn.M1116.val % 7 + Syn.M1242.val % 7 + Syn.M1366.val % 7 + 1
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
end Syn.M1405
