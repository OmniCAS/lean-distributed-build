import Syn.M1150
import Syn.M1151
import Syn.M1153
import Syn.M1201
import Syn.M1203
import Syn.M1205
import Syn.M1606
import Syn.M1820
import Syn.M1846
import Syn.M1869
import Syn.M1870
import Syn.M1932

namespace Syn.M1962
def val : Nat := Syn.M1150.val % 7 + Syn.M1151.val % 7 + Syn.M1153.val % 7 + Syn.M1201.val % 7 + Syn.M1203.val % 7 + Syn.M1205.val % 7 + Syn.M1606.val % 7 + Syn.M1820.val % 7 + Syn.M1846.val % 7 + Syn.M1869.val % 7 + Syn.M1870.val % 7 + Syn.M1932.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1962
