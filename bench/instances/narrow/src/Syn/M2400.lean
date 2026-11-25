import Syn.M873
import Syn.M1961
import Syn.M2381
import Syn.M2383

namespace Syn.M2400
def val : Nat := Syn.M873.val % 7 + Syn.M1961.val % 7 + Syn.M2381.val % 7 + Syn.M2383.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M2400
