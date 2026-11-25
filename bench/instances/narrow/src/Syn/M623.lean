import Syn.M549
import Syn.M556
import Syn.M588
import Syn.M601
import Syn.M613

namespace Syn.M623
def val : Nat := Syn.M549.val % 7 + Syn.M556.val % 7 + Syn.M588.val % 7 + Syn.M601.val % 7 + Syn.M613.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M623
