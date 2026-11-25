import Syn.M371
import Syn.M434
import Syn.M435
import Syn.M436
import Syn.M438
import Syn.M440

namespace Syn.M492
def val : Nat := Syn.M371.val % 7 + Syn.M434.val % 7 + Syn.M435.val % 7 + Syn.M436.val % 7 + Syn.M438.val % 7 + Syn.M440.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end Syn.M492
