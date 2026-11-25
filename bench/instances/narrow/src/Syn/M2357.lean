import Syn.M2281
import Syn.M2302
import Syn.M2313
import Syn.M2345

namespace Syn.M2357
def val : Nat := Syn.M2281.val % 7 + Syn.M2302.val % 7 + Syn.M2313.val % 7 + Syn.M2345.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2357
