import Syn.M1674
import Syn.M1836
import Syn.M1998
import Syn.M2151

namespace Syn.M2173
def val : Nat := Syn.M1674.val % 7 + Syn.M1836.val % 7 + Syn.M1998.val % 7 + Syn.M2151.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2173
