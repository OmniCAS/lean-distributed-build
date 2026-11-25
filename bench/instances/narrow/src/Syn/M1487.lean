import Syn.M630
import Syn.M662
import Syn.M685
import Syn.M744
import Syn.M752
import Syn.M803
import Syn.M929
import Syn.M971
import Syn.M995
import Syn.M1004
import Syn.M1065
import Syn.M1446

namespace Syn.M1487
def val : Nat := Syn.M630.val % 7 + Syn.M662.val % 7 + Syn.M685.val % 7 + Syn.M744.val % 7 + Syn.M752.val % 7 + Syn.M803.val % 7 + Syn.M929.val % 7 + Syn.M971.val % 7 + Syn.M995.val % 7 + Syn.M1004.val % 7 + Syn.M1065.val % 7 + Syn.M1446.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end Syn.M1487
