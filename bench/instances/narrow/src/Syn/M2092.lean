import Syn.M2045
import Syn.M2047

namespace Syn.M2092
def val : Nat := Syn.M2045.val % 7 + Syn.M2047.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2092
