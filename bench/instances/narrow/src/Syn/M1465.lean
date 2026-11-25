import Syn.M655
import Syn.M661
import Syn.M732
import Syn.M853
import Syn.M1431

namespace Syn.M1465
def val : Nat := Syn.M655.val % 7 + Syn.M661.val % 7 + Syn.M732.val % 7 + Syn.M853.val % 7 + Syn.M1431.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1465
