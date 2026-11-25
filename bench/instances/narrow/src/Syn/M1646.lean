import Syn.M743
import Syn.M873
import Syn.M971
import Syn.M1114
import Syn.M1149
import Syn.M1625

namespace Syn.M1646
def val : Nat := Syn.M743.val % 7 + Syn.M873.val % 7 + Syn.M971.val % 7 + Syn.M1114.val % 7 + Syn.M1149.val % 7 + Syn.M1625.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M1646
