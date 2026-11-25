import Syn.M1011
import Syn.M1013
import Syn.M1331

namespace Syn.M1361
def val : Nat := Syn.M1011.val % 7 + Syn.M1013.val % 7 + Syn.M1331.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M1361
