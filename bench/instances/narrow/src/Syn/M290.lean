import Syn.M4
import Syn.M192

namespace Syn.M290
def val : Nat := Syn.M4.val % 7 + Syn.M192.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M290
