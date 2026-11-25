import Syn.M661
import Syn.M1004
import Syn.M1066
import Syn.M1101
import Syn.M1243
import Syn.M1789

namespace Syn.M1797
def val : Nat := Syn.M661.val % 7 + Syn.M1004.val % 7 + Syn.M1066.val % 7 + Syn.M1101.val % 7 + Syn.M1243.val % 7 + Syn.M1789.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M1797
