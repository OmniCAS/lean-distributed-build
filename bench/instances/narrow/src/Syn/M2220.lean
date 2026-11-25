import Syn.M1655
import Syn.M2200

namespace Syn.M2220
def val : Nat := Syn.M1655.val % 7 + Syn.M2200.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M2220
