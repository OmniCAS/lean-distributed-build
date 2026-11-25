import Syn.M712
import Syn.M995

namespace Syn.M1060
def val : Nat := Syn.M712.val % 7 + Syn.M995.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M1060
