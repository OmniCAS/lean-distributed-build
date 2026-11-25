import Syn.M1727
import Syn.M2347

namespace Syn.M2360
def val : Nat := Syn.M1727.val % 7 + Syn.M2347.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M2360
