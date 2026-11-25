import Syn.M811
import Syn.M1000
import Syn.M1001
import Syn.M1062

namespace Syn.M1109
def val : Nat := Syn.M811.val % 7 + Syn.M1000.val % 7 + Syn.M1001.val % 7 + Syn.M1062.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1109
