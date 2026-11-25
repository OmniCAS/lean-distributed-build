import Syn.M836
import Syn.M837
import Syn.M1108
import Syn.M1166

namespace Syn.M1233
def val : Nat := Syn.M836.val % 7 + Syn.M837.val % 7 + Syn.M1108.val % 7 + Syn.M1166.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1233
