import Syn.M2313
import Syn.M2315

namespace Syn.M2340
def val : Nat := Syn.M2313.val % 7 + Syn.M2315.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M2340
