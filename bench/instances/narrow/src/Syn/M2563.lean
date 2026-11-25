import Syn.M2483
import Syn.M2507
import Syn.M2526
import Syn.M2545

namespace Syn.M2563
def val : Nat := Syn.M2483.val % 7 + Syn.M2507.val % 7 + Syn.M2526.val % 7 + Syn.M2545.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2563
