import Syn.M1310
import Syn.M1313
import Syn.M1532
import Syn.M1669

namespace Syn.M1683
def val : Nat := Syn.M1310.val % 7 + Syn.M1313.val % 7 + Syn.M1532.val % 7 + Syn.M1669.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end Syn.M1683
