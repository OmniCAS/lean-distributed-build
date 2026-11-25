import Syn.M661
import Syn.M662
import Syn.M1004
import Syn.M1058
import Syn.M1409
import Syn.M1446

namespace Syn.M1483
def val : Nat := Syn.M661.val % 7 + Syn.M662.val % 7 + Syn.M1004.val % 7 + Syn.M1058.val % 7 + Syn.M1409.val % 7 + Syn.M1446.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M1483
