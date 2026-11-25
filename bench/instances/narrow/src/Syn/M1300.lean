import Syn.M477
import Syn.M1246

namespace Syn.M1300
def val : Nat := Syn.M477.val % 7 + Syn.M1246.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M1300
