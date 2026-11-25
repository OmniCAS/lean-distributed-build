import Syn.M116
import Syn.M139
import Syn.M382
import Syn.M383
import Syn.M447
import Syn.M448
import Syn.M449
import Syn.M450
import Syn.M451
import Syn.M452

namespace Syn.M505
def val : Nat := Syn.M116.val % 7 + Syn.M139.val % 7 + Syn.M382.val % 7 + Syn.M383.val % 7 + Syn.M447.val % 7 + Syn.M448.val % 7 + Syn.M449.val % 7 + Syn.M450.val % 7 + Syn.M451.val % 7 + Syn.M452.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M505
