import Syn.M444
import Syn.M499
import Syn.M1343
import Syn.M1374
import Syn.M1379

namespace Syn.M1417
def val : Nat := Syn.M444.val % 7 + Syn.M499.val % 7 + Syn.M1343.val % 7 + Syn.M1374.val % 7 + Syn.M1379.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1417
