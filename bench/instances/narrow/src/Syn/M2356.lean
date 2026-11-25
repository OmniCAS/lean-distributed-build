import Syn.M2199
import Syn.M2216
import Syn.M2233
import Syn.M2324
import Syn.M2344

namespace Syn.M2356
def val : Nat := Syn.M2199.val % 7 + Syn.M2216.val % 7 + Syn.M2233.val % 7 + Syn.M2324.val % 7 + Syn.M2344.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2356
