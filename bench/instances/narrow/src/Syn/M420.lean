import Syn.M241
import Syn.M242
import Syn.M243
import Syn.M244
import Syn.M357

namespace Syn.M420
def val : Nat := Syn.M241.val % 7 + Syn.M242.val % 7 + Syn.M243.val % 7 + Syn.M244.val % 7 + Syn.M357.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M420
