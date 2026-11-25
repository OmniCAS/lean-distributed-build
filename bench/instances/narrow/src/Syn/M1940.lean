import Syn.M1157
import Syn.M1222
import Syn.M1336
import Syn.M1859
import Syn.M1907

namespace Syn.M1940
def val : Nat := Syn.M1157.val % 7 + Syn.M1222.val % 7 + Syn.M1336.val % 7 + Syn.M1859.val % 7 + Syn.M1907.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M1940
