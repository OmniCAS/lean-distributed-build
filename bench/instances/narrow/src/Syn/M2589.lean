import Syn.M2484
import Syn.M2532
import Syn.M2563
import Syn.M2575
import Syn.M2576
import Syn.M2580

namespace Syn.M2589
def val : Nat := Syn.M2484.val % 7 + Syn.M2532.val % 7 + Syn.M2563.val % 7 + Syn.M2575.val % 7 + Syn.M2576.val % 7 + Syn.M2580.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2589
