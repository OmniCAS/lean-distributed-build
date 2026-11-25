import Syn.M1846
import Syn.M1932

namespace Syn.M1964
def val : Nat := Syn.M1846.val % 7 + Syn.M1932.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1964
