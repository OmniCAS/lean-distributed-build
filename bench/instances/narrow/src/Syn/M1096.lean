import Syn.M778
import Syn.M895
import Syn.M896
import Syn.M897
import Syn.M900
import Syn.M983
import Syn.M988
import Syn.M1051

namespace Syn.M1096
def val : Nat := Syn.M778.val % 7 + Syn.M895.val % 7 + Syn.M896.val % 7 + Syn.M897.val % 7 + Syn.M900.val % 7 + Syn.M983.val % 7 + Syn.M988.val % 7 + Syn.M1051.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1096
