import Syn.M705
import Syn.M1541
import Syn.M1584
import Syn.M1585

namespace Syn.M1617
def val : Nat := Syn.M705.val % 7 + Syn.M1541.val % 7 + Syn.M1584.val % 7 + Syn.M1585.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end Syn.M1617
