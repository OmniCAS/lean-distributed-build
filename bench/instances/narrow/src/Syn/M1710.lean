import Syn.M1636
import Syn.M1657
import Syn.M1697

namespace Syn.M1710
def val : Nat := Syn.M1636.val % 7 + Syn.M1657.val % 7 + Syn.M1697.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M1710
