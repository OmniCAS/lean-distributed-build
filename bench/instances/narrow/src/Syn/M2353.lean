import Syn.M2331
import Syn.M2334

namespace Syn.M2353
def val : Nat := Syn.M2331.val % 7 + Syn.M2334.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2353
