import Syn.M662
import Syn.M712
import Syn.M868

namespace Syn.M960
def val : Nat := Syn.M662.val % 7 + Syn.M712.val % 7 + Syn.M868.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M960
