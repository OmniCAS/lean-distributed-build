import Syn.M371
import Syn.M372
import Syn.M626
import Syn.M668
import Syn.M899

namespace Syn.M982
def val : Nat := Syn.M371.val % 7 + Syn.M372.val % 7 + Syn.M626.val % 7 + Syn.M668.val % 7 + Syn.M899.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M982
