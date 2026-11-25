import Syn.M1221
import Syn.M1906
import Syn.M1907

namespace Syn.M1941
def val : Nat := Syn.M1221.val % 7 + Syn.M1906.val % 7 + Syn.M1907.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1941
