import Syn.M243
import Syn.M244
import Syn.M1095
import Syn.M1360
import Syn.M1366
import Syn.M1655
import Syn.M1752

namespace Syn.M1770
def val : Nat := Syn.M243.val % 7 + Syn.M244.val % 7 + Syn.M1095.val % 7 + Syn.M1360.val % 7 + Syn.M1366.val % 7 + Syn.M1655.val % 7 + Syn.M1752.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M1770
