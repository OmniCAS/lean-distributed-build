import Syn.M1008
import Syn.M1010
import Syn.M1071
import Syn.M1072
import Syn.M1300
import Syn.M2454

namespace Syn.M2464
def val : Nat := Syn.M1008.val % 7 + Syn.M1010.val % 7 + Syn.M1071.val % 7 + Syn.M1072.val % 7 + Syn.M1300.val % 7 + Syn.M2454.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2464
