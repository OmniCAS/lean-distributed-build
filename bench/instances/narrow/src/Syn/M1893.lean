import Syn.M360
import Syn.M939
import Syn.M1115
import Syn.M1148
import Syn.M1364
import Syn.M1806
import Syn.M1865

namespace Syn.M1893
def val : Nat := Syn.M360.val % 7 + Syn.M939.val % 7 + Syn.M1115.val % 7 + Syn.M1148.val % 7 + Syn.M1364.val % 7 + Syn.M1806.val % 7 + Syn.M1865.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
end Syn.M1893
