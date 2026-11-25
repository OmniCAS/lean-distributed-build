import Syn.M1620
import Syn.M2263
import Syn.M2264
import Syn.M2272

namespace Syn.M2300
def val : Nat := Syn.M1620.val % 7 + Syn.M2263.val % 7 + Syn.M2264.val % 7 + Syn.M2272.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M2300
