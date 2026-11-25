import Syn.M1782
import Syn.M1784

namespace Syn.M1791
def val : Nat := Syn.M1782.val % 7 + Syn.M1784.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1791
