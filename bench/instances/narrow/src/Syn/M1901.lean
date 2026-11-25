import Syn.M1151
import Syn.M1153
import Syn.M1845
import Syn.M1869
import Syn.M1870

namespace Syn.M1901
def val : Nat := Syn.M1151.val % 7 + Syn.M1153.val % 7 + Syn.M1845.val % 7 + Syn.M1869.val % 7 + Syn.M1870.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1901
