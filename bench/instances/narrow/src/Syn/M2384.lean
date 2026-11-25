import Syn.M1041
import Syn.M1091
import Syn.M2378

namespace Syn.M2384
def val : Nat := Syn.M1041.val % 7 + Syn.M1091.val % 7 + Syn.M2378.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2384
