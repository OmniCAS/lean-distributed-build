import Syn.M1115
import Syn.M1263
import Syn.M1800
import Syn.M1822
import Syn.M2101

namespace Syn.M2131
def val : Nat := Syn.M1115.val % 7 + Syn.M1263.val % 7 + Syn.M1800.val % 7 + Syn.M1822.val % 7 + Syn.M2101.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2131
