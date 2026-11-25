import Syn.M2428
import Syn.M2476
import Syn.M2482
import Syn.M2483
import Syn.M2543

namespace Syn.M2561
def val : Nat := Syn.M2428.val % 7 + Syn.M2476.val % 7 + Syn.M2482.val % 7 + Syn.M2483.val % 7 + Syn.M2543.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2561
