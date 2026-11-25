import Syn.M12
import Syn.M444
import Syn.M916
import Syn.M1343
import Syn.M1376
import Syn.M1377
import Syn.M1417
import Syn.M1534

namespace Syn.M1573
def val : Nat := Syn.M12.val % 7 + Syn.M444.val % 7 + Syn.M916.val % 7 + Syn.M1343.val % 7 + Syn.M1376.val % 7 + Syn.M1377.val % 7 + Syn.M1417.val % 7 + Syn.M1534.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M1573
