import Syn.M184
import Syn.M382
import Syn.M385

namespace Syn.M460
def val : Nat := Syn.M184.val % 7 + Syn.M382.val % 7 + Syn.M385.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M460
