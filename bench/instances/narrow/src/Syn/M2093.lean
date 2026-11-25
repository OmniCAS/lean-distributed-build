import Syn.M1
import Syn.M2
import Syn.M3
import Syn.M2048

namespace Syn.M2093
def val : Nat := Syn.M1.val % 7 + Syn.M2.val % 7 + Syn.M3.val % 7 + Syn.M2048.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end Syn.M2093
