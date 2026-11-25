import Syn.M637
import Syn.M929
import Syn.M935

namespace Syn.M1007
def val : Nat := Syn.M637.val % 7 + Syn.M929.val % 7 + Syn.M935.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M1007
