import Syn.M542
import Syn.M1465

namespace Syn.M1500
def val : Nat := Syn.M542.val % 7 + Syn.M1465.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M1500
