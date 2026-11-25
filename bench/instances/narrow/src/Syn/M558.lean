import Syn.M444
import Syn.M498
import Syn.M500

namespace Syn.M558
def val : Nat := Syn.M444.val % 7 + Syn.M498.val % 7 + Syn.M500.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M558
