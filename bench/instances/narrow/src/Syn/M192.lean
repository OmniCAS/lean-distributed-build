import Syn.M0
import Syn.M4
import Syn.M92

namespace Syn.M192
def val : Nat := Syn.M0.val % 7 + Syn.M4.val % 7 + Syn.M92.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M192
