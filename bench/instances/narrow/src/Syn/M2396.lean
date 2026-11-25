import Syn.M882
import Syn.M1379
import Syn.M1486
import Syn.M2381

namespace Syn.M2396
def val : Nat := Syn.M882.val % 7 + Syn.M1379.val % 7 + Syn.M1486.val % 7 + Syn.M2381.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2396
