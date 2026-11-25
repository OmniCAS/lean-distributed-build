import Syn.M600
import Syn.M602
import Syn.M895
import Syn.M896
import Syn.M897
import Syn.M898
import Syn.M900
import Syn.M983
import Syn.M1051
import Syn.M1054
import Syn.M1056
import Syn.M1097

namespace Syn.M1135
def val : Nat := Syn.M600.val % 7 + Syn.M602.val % 7 + Syn.M895.val % 7 + Syn.M896.val % 7 + Syn.M897.val % 7 + Syn.M898.val % 7 + Syn.M900.val % 7 + Syn.M983.val % 7 + Syn.M1051.val % 7 + Syn.M1054.val % 7 + Syn.M1056.val % 7 + Syn.M1097.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1135
