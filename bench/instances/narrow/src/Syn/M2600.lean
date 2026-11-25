import Syn.M1531
import Syn.M2431
import Syn.M2539
import Syn.M2550
import Syn.M2562
import Syn.M2566
import Syn.M2581
import Syn.M2593

namespace Syn.M2600
def val : Nat := Syn.M1531.val % 7 + Syn.M2431.val % 7 + Syn.M2539.val % 7 + Syn.M2550.val % 7 + Syn.M2562.val % 7 + Syn.M2566.val % 7 + Syn.M2581.val % 7 + Syn.M2593.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M2600
