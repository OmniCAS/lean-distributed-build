import Syn.M1150
import Syn.M1595
import Syn.M1665
import Syn.M1666

namespace Syn.M1680
def val : Nat := Syn.M1150.val % 7 + Syn.M1595.val % 7 + Syn.M1665.val % 7 + Syn.M1666.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M1680
