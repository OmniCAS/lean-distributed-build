import Syn.M1914
import Syn.M2054
import Syn.M2428
import Syn.M2476

namespace Syn.M2484
def val : Nat := Syn.M1914.val % 7 + Syn.M2054.val % 7 + Syn.M2428.val % 7 + Syn.M2476.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end Syn.M2484
