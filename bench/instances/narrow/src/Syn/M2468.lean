import Syn.M2449
import Syn.M2450
import Syn.M2451
import Syn.M2460
import Syn.M2461

namespace Syn.M2468
def val : Nat := Syn.M2449.val % 7 + Syn.M2450.val % 7 + Syn.M2451.val % 7 + Syn.M2460.val % 7 + Syn.M2461.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2468
