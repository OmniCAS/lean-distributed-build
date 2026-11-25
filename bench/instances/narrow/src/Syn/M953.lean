import Syn.M244
import Syn.M731
import Syn.M853

namespace Syn.M953
def val : Nat := Syn.M244.val % 7 + Syn.M731.val % 7 + Syn.M853.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M953
