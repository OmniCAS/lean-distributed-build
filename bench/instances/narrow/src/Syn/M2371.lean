import Syn.M2343
import Syn.M2355
import Syn.M2357
import Syn.M2358

namespace Syn.M2371
def val : Nat := Syn.M2343.val % 7 + Syn.M2355.val % 7 + Syn.M2357.val % 7 + Syn.M2358.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2371
