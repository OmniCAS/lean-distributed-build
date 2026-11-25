import Syn.M2330
import Syn.M2353
import Syn.M2368
import Syn.M2456
import Syn.M2457

namespace Syn.M2466
def val : Nat := Syn.M2330.val % 7 + Syn.M2353.val % 7 + Syn.M2368.val % 7 + Syn.M2456.val % 7 + Syn.M2457.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2466
