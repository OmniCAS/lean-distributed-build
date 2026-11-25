import Syn.M184
import Syn.M382
import Syn.M385
import Syn.M460

namespace Syn.M528
def val : Nat := Syn.M184.val % 7 + Syn.M382.val % 7 + Syn.M385.val % 7 + Syn.M460.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M528
