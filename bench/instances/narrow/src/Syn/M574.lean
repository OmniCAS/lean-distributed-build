import Syn.M91
import Syn.M189
import Syn.M190
import Syn.M191
import Syn.M531

namespace Syn.M574
def val : Nat := Syn.M91.val % 7 + Syn.M189.val % 7 + Syn.M190.val % 7 + Syn.M191.val % 7 + Syn.M531.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M574
