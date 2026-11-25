import Syn.M744
import Syn.M971
import Syn.M1243
import Syn.M1975

namespace Syn.M2030
def val : Nat := Syn.M744.val % 7 + Syn.M971.val % 7 + Syn.M1243.val % 7 + Syn.M1975.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M2030
