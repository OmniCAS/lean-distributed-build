import Syn.M1965
import Syn.M2605

namespace Syn.M2607
def val : Nat := Syn.M1965.val % 7 + Syn.M2605.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2607
