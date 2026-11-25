import Syn.M1153
import Syn.M1269
import Syn.M1326
import Syn.M1525
import Syn.M1627
import Syn.M2523

namespace Syn.M2535
def val : Nat := Syn.M1153.val % 7 + Syn.M1269.val % 7 + Syn.M1326.val % 7 + Syn.M1525.val % 7 + Syn.M1627.val % 7 + Syn.M2523.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2535
