import Syn.M385
import Syn.M461

namespace Syn.M529
def val : Nat := Syn.M385.val % 7 + Syn.M461.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M529
