import Syn.M494
import Syn.M587

namespace Syn.M602
def val : Nat := Syn.M494.val % 7 + Syn.M587.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M602
