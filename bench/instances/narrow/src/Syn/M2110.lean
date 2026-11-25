import Syn.M1446
import Syn.M1486
import Syn.M1730
import Syn.M2046
import Syn.M2073

namespace Syn.M2110
def val : Nat := Syn.M1446.val % 7 + Syn.M1486.val % 7 + Syn.M1730.val % 7 + Syn.M2046.val % 7 + Syn.M2073.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M2110
