import Syn.M2395
import Syn.M2396
import Syn.M2403
import Syn.M2419
import Syn.M2420
import Syn.M2427
import Syn.M2470

namespace Syn.M2473
def val : Nat := Syn.M2395.val % 7 + Syn.M2396.val % 7 + Syn.M2403.val % 7 + Syn.M2419.val % 7 + Syn.M2420.val % 7 + Syn.M2427.val % 7 + Syn.M2470.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2473
