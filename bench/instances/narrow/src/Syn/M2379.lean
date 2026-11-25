import Syn.M2316
import Syn.M2346
import Syn.M2356
import Syn.M2371
import Syn.M2375

namespace Syn.M2379
def val : Nat := Syn.M2316.val % 7 + Syn.M2346.val % 7 + Syn.M2356.val % 7 + Syn.M2371.val % 7 + Syn.M2375.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2379
