import Syn.M696
import Syn.M932
import Syn.M1366
import Syn.M1750
import Syn.M1947

namespace Syn.M1996
def val : Nat := Syn.M696.val % 7 + Syn.M932.val % 7 + Syn.M1366.val % 7 + Syn.M1750.val % 7 + Syn.M1947.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1996
