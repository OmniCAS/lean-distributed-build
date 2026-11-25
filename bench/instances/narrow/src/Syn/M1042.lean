import Syn.M660
import Syn.M878
import Syn.M971

namespace Syn.M1042
def val : Nat := Syn.M660.val % 7 + Syn.M878.val % 7 + Syn.M971.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M1042
