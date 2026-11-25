import Syn.M2240
import Syn.M2241
import Syn.M2301

namespace Syn.M2320
def val : Nat := Syn.M2240.val % 7 + Syn.M2241.val % 7 + Syn.M2301.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M2320
