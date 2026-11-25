import Syn.M60
import Syn.M70
import Syn.M72
import Syn.M256
import Syn.M367

namespace Syn.M433
def val : Nat := Syn.M60.val % 7 + Syn.M70.val % 7 + Syn.M72.val % 7 + Syn.M256.val % 7 + Syn.M367.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M433
