import Syn.M1264
import Syn.M1334
import Syn.M1788
import Syn.M2104

namespace Syn.M2134
def val : Nat := Syn.M1264.val % 7 + Syn.M1334.val % 7 + Syn.M1788.val % 7 + Syn.M2104.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2134
