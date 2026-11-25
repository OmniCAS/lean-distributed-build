import Syn.M1818
import Syn.M1832

namespace Syn.M1853
def val : Nat := Syn.M1818.val % 7 + Syn.M1832.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1853
