import Syn.M797
import Syn.M1275
import Syn.M1288
import Syn.M2491

namespace Syn.M2504
def val : Nat := Syn.M797.val % 7 + Syn.M1275.val % 7 + Syn.M1288.val % 7 + Syn.M2491.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2504
