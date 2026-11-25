import Syn.M919
import Syn.M2151
import Syn.M2187
import Syn.M2218
import Syn.M2233

namespace Syn.M2262
def val : Nat := Syn.M919.val % 7 + Syn.M2151.val % 7 + Syn.M2187.val % 7 + Syn.M2218.val % 7 + Syn.M2233.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2262
