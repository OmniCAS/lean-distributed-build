import Syn.M505
import Syn.M508
import Syn.M510
import Syn.M512
import Syn.M541
import Syn.M562
import Syn.M745

namespace Syn.M874
def val : Nat := Syn.M505.val % 7 + Syn.M508.val % 7 + Syn.M510.val % 7 + Syn.M512.val % 7 + Syn.M541.val % 7 + Syn.M562.val % 7 + Syn.M745.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M874
