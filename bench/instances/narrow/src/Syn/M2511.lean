import Syn.M2425
import Syn.M2494

namespace Syn.M2511
def val : Nat := Syn.M2425.val % 7 + Syn.M2494.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2511
