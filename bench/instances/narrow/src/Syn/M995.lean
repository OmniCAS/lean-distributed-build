import Syn.M661
import Syn.M662
import Syn.M695
import Syn.M836
import Syn.M919

namespace Syn.M995
def val : Nat := Syn.M661.val % 7 + Syn.M662.val % 7 + Syn.M695.val % 7 + Syn.M836.val % 7 + Syn.M919.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
end Syn.M995
