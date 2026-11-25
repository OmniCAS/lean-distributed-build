import Syn.M2328
import Syn.M2376
import Syn.M2377
import Syn.M2411
import Syn.M2466

namespace Syn.M2470
def val : Nat := Syn.M2328.val % 7 + Syn.M2376.val % 7 + Syn.M2377.val % 7 + Syn.M2411.val % 7 + Syn.M2466.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M2470
