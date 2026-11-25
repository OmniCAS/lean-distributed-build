import Syn.M1385
import Syn.M1485

namespace Syn.M1521
def val : Nat := Syn.M1385.val % 7 + Syn.M1485.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1521
