import Syn.M637
import Syn.M996
import Syn.M1064
import Syn.M1230

namespace Syn.M1287
def val : Nat := Syn.M637.val % 7 + Syn.M996.val % 7 + Syn.M1064.val % 7 + Syn.M1230.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1287
