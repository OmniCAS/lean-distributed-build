import Syn.M137
import Syn.M522
import Syn.M527
import Syn.M536
import Syn.M568
import Syn.M569
import Syn.M570
import Syn.M571
import Syn.M572
import Syn.M594
import Syn.M595
import Syn.M596
import Syn.M605
import Syn.M608
import Syn.M617

namespace Syn.M625
def val : Nat := Syn.M137.val % 7 + Syn.M522.val % 7 + Syn.M527.val % 7 + Syn.M536.val % 7 + Syn.M568.val % 7 + Syn.M569.val % 7 + Syn.M570.val % 7 + Syn.M571.val % 7 + Syn.M572.val % 7 + Syn.M594.val % 7 + Syn.M595.val % 7 + Syn.M596.val % 7 + Syn.M605.val % 7 + Syn.M608.val % 7 + Syn.M617.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M625
