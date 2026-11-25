import Syn.M2462
import Syn.M2468
import Syn.M2469

namespace Syn.M2472
def val : Nat := Syn.M2462.val % 7 + Syn.M2468.val % 7 + Syn.M2469.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2472
