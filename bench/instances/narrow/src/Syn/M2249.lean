import Syn.M1323
import Syn.M1482
import Syn.M1882
import Syn.M2126
import Syn.M2223

namespace Syn.M2249
def val : Nat := Syn.M1323.val % 7 + Syn.M1482.val % 7 + Syn.M1882.val % 7 + Syn.M2126.val % 7 + Syn.M2223.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2249
