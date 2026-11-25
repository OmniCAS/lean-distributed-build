import Syn.M1269
import Syn.M1978
import Syn.M2521
import Syn.M2537

namespace Syn.M2542
def val : Nat := Syn.M1269.val % 7 + Syn.M1978.val % 7 + Syn.M2521.val % 7 + Syn.M2537.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end Syn.M2542
