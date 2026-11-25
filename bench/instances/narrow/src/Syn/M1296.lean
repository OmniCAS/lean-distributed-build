import Syn.M954
import Syn.M1028
import Syn.M1085
import Syn.M1238
import Syn.M1239

namespace Syn.M1296
def val : Nat := Syn.M954.val % 7 + Syn.M1028.val % 7 + Syn.M1085.val % 7 + Syn.M1238.val % 7 + Syn.M1239.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1296
