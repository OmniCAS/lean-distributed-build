import Syn.M257
import Syn.M258
import Syn.M259
import Syn.M424
import Syn.M426
import Syn.M502
import Syn.M503
import Syn.M544
import Syn.M545
import Syn.M546
import Syn.M547
import Syn.M548

namespace Syn.M585
def val : Nat := Syn.M257.val % 7 + Syn.M258.val % 7 + Syn.M259.val % 7 + Syn.M424.val % 7 + Syn.M426.val % 7 + Syn.M502.val % 7 + Syn.M503.val % 7 + Syn.M544.val % 7 + Syn.M545.val % 7 + Syn.M546.val % 7 + Syn.M547.val % 7 + Syn.M548.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M585
