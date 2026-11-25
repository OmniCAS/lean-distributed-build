import Syn.M1433
import Syn.M1669
import Syn.M1866

namespace Syn.M1900
def val : Nat := Syn.M1433.val % 7 + Syn.M1669.val % 7 + Syn.M1866.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M1900
