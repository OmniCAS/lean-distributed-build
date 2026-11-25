import Syn.M661
import Syn.M1878
import Syn.M2084

namespace Syn.M2116
def val : Nat := Syn.M661.val % 7 + Syn.M1878.val % 7 + Syn.M2084.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2116
