import Syn.M1781
import Syn.M1798
import Syn.M1845

namespace Syn.M1870
def val : Nat := Syn.M1781.val % 7 + Syn.M1798.val % 7 + Syn.M1845.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M1870
