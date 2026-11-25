import Syn.M939
import Syn.M1148
import Syn.M1232
import Syn.M1396

namespace Syn.M1433
def val : Nat := Syn.M939.val % 7 + Syn.M1148.val % 7 + Syn.M1232.val % 7 + Syn.M1396.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M1433
