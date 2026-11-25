import Syn.M630
import Syn.M1004
import Syn.M1150
import Syn.M1330
import Syn.M1606
import Syn.M1789

namespace Syn.M1802
def val : Nat := Syn.M630.val % 7 + Syn.M1004.val % 7 + Syn.M1150.val % 7 + Syn.M1330.val % 7 + Syn.M1606.val % 7 + Syn.M1789.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1802
