import Syn.M782
import Syn.M783
import Syn.M784
import Syn.M900
import Syn.M983

namespace Syn.M1052
def val : Nat := Syn.M782.val % 7 + Syn.M783.val % 7 + Syn.M784.val % 7 + Syn.M900.val % 7 + Syn.M983.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1052
