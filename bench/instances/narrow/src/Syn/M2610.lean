import Syn.M2068
import Syn.M2609

namespace Syn.M2610
def val : Nat := Syn.M2068.val % 7 + Syn.M2609.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M2610
