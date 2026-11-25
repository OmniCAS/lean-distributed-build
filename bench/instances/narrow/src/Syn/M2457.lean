import Syn.M2325
import Syn.M2326
import Syn.M2332
import Syn.M2333
import Syn.M2442

namespace Syn.M2457
def val : Nat := Syn.M2325.val % 7 + Syn.M2326.val % 7 + Syn.M2332.val % 7 + Syn.M2333.val % 7 + Syn.M2442.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2457
