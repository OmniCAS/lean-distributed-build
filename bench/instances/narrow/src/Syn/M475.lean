import Syn.M154
import Syn.M155
import Syn.M223
import Syn.M225
import Syn.M227
import Syn.M228
import Syn.M229
import Syn.M414

namespace Syn.M475
def val : Nat := Syn.M154.val % 7 + Syn.M155.val % 7 + Syn.M223.val % 7 + Syn.M225.val % 7 + Syn.M227.val % 7 + Syn.M228.val % 7 + Syn.M229.val % 7 + Syn.M414.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M475
