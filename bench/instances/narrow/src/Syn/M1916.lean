import Syn.M1184
import Syn.M1360
import Syn.M1815
import Syn.M1879

namespace Syn.M1916
def val : Nat := Syn.M1184.val % 7 + Syn.M1360.val % 7 + Syn.M1815.val % 7 + Syn.M1879.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1916
