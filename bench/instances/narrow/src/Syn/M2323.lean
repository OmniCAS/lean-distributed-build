import Syn.M2280
import Syn.M2282
import Syn.M2303
import Syn.M2304
import Syn.M2305
import Syn.M2306

namespace Syn.M2323
def val : Nat := Syn.M2280.val % 7 + Syn.M2282.val % 7 + Syn.M2303.val % 7 + Syn.M2304.val % 7 + Syn.M2305.val % 7 + Syn.M2306.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2323
