import Syn.M551
import Syn.M552
import Syn.M553

namespace Syn.M587
def val : Nat := Syn.M551.val % 7 + Syn.M552.val % 7 + Syn.M553.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M587
