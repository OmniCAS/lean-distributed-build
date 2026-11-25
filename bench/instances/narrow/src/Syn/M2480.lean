import Syn.M2458
import Syn.M2476

namespace Syn.M2480
def val : Nat := Syn.M2458.val % 7 + Syn.M2476.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M2480
