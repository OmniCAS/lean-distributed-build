import Syn.M1336
import Syn.M1727
import Syn.M1906

namespace Syn.M1936
def val : Nat := Syn.M1336.val % 7 + Syn.M1727.val % 7 + Syn.M1906.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1936
