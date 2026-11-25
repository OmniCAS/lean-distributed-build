import Syn.M420
import Syn.M695
import Syn.M1005
import Syn.M1058
import Syn.M1184

namespace Syn.M1243
def val : Nat := Syn.M420.val % 7 + Syn.M695.val % 7 + Syn.M1005.val % 7 + Syn.M1058.val % 7 + Syn.M1184.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1243
