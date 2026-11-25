import Syn.M264
import Syn.M265

namespace Syn.M376
def val : Nat := Syn.M264.val % 7 + Syn.M265.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M376
