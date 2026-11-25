import Syn.M860
import Syn.M1128

namespace Syn.M1180
def val : Nat := Syn.M860.val % 7 + Syn.M1128.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M1180
