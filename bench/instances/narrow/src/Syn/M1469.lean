import Syn.M463
import Syn.M574
import Syn.M848
import Syn.M1074
import Syn.M1120
import Syn.M1162
import Syn.M1292
import Syn.M1337
import Syn.M1434

namespace Syn.M1469
def val : Nat := Syn.M463.val % 7 + Syn.M574.val % 7 + Syn.M848.val % 7 + Syn.M1074.val % 7 + Syn.M1120.val % 7 + Syn.M1162.val % 7 + Syn.M1292.val % 7 + Syn.M1337.val % 7 + Syn.M1434.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1469
