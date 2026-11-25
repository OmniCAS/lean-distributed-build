import Syn.M12
import Syn.M97

namespace Syn.M195
def val : Nat := Syn.M12.val % 7 + Syn.M97.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M195
