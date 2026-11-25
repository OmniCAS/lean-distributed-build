import Syn.M1985
import Syn.M2035
import Syn.M2079
import Syn.M2169
import Syn.M2472
import Syn.M2480
import Syn.M2484
import Syn.M2495
import Syn.M2514
import Syn.M2563

namespace Syn.M2578
def val : Nat := Syn.M1985.val % 7 + Syn.M2035.val % 7 + Syn.M2079.val % 7 + Syn.M2169.val % 7 + Syn.M2472.val % 7 + Syn.M2480.val % 7 + Syn.M2484.val % 7 + Syn.M2495.val % 7 + Syn.M2514.val % 7 + Syn.M2563.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2578
