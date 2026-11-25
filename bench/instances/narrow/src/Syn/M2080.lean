import Syn.M137
import Syn.M522
import Syn.M1441
import Syn.M2036

namespace Syn.M2080
def val : Nat := Syn.M137.val % 7 + Syn.M522.val % 7 + Syn.M1441.val % 7 + Syn.M2036.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M2080
