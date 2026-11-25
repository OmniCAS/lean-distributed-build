import Syn.M930
import Syn.M1004
import Syn.M1065
import Syn.M1101

namespace Syn.M1148
def val : Nat := Syn.M930.val % 7 + Syn.M1004.val % 7 + Syn.M1065.val % 7 + Syn.M1101.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1148
