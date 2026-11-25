import Syn.M2425
import Syn.M2428
import Syn.M2432
import Syn.M2433
import Syn.M2434

namespace Syn.M2443
def val : Nat := Syn.M2425.val % 7 + Syn.M2428.val % 7 + Syn.M2432.val % 7 + Syn.M2433.val % 7 + Syn.M2434.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2443
