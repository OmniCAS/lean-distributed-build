import Syn.M1583
import Syn.M1877
import Syn.M1907
import Syn.M2003
import Syn.M2102
import Syn.M2124
import Syn.M2148

namespace Syn.M2171
def val : Nat := Syn.M1583.val % 7 + Syn.M1877.val % 7 + Syn.M1907.val % 7 + Syn.M2003.val % 7 + Syn.M2102.val % 7 + Syn.M2124.val % 7 + Syn.M2148.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2171
