import Syn.M2257
import Syn.M2564

namespace Syn.M2581
def val : Nat := Syn.M2257.val % 7 + Syn.M2564.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2581
