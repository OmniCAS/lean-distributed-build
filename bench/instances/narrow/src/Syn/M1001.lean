import Syn.M700
import Syn.M926

namespace Syn.M1001
def val : Nat := Syn.M700.val % 7 + Syn.M926.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1001
