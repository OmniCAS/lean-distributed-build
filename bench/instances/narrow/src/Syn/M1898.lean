import Syn.M420
import Syn.M1114
import Syn.M1163
import Syn.M1526
import Syn.M1866

namespace Syn.M1898
def val : Nat := Syn.M420.val % 7 + Syn.M1114.val % 7 + Syn.M1163.val % 7 + Syn.M1526.val % 7 + Syn.M1866.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1898
