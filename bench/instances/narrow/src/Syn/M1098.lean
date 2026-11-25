import Syn.M529
import Syn.M530
import Syn.M549
import Syn.M556
import Syn.M587
import Syn.M601
import Syn.M602
import Syn.M636
import Syn.M668
import Syn.M767
import Syn.M778
import Syn.M791
import Syn.M792
import Syn.M793
import Syn.M895
import Syn.M896
import Syn.M897
import Syn.M898
import Syn.M900
import Syn.M906
import Syn.M907
import Syn.M983
import Syn.M1051
import Syn.M1056

namespace Syn.M1098
def val : Nat := Syn.M529.val % 7 + Syn.M530.val % 7 + Syn.M549.val % 7 + Syn.M556.val % 7 + Syn.M587.val % 7 + Syn.M601.val % 7 + Syn.M602.val % 7 + Syn.M636.val % 7 + Syn.M668.val % 7 + Syn.M767.val % 7 + Syn.M778.val % 7 + Syn.M791.val % 7 + Syn.M792.val % 7 + Syn.M793.val % 7 + Syn.M895.val % 7 + Syn.M896.val % 7 + Syn.M897.val % 7 + Syn.M898.val % 7 + Syn.M900.val % 7 + Syn.M906.val % 7 + Syn.M907.val % 7 + Syn.M983.val % 7 + Syn.M1051.val % 7 + Syn.M1056.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M1098
