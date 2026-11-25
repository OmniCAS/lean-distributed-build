import Syn.M2292
import Syn.M2354

namespace Syn.M2368
def val : Nat := Syn.M2292.val % 7 + Syn.M2354.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2368
