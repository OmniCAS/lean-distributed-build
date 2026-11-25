import Syn.M1116
import Syn.M1360
import Syn.M2151
import Syn.M2233

namespace Syn.M2261
def val : Nat := Syn.M1116.val % 7 + Syn.M1360.val % 7 + Syn.M2151.val % 7 + Syn.M2233.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2261
