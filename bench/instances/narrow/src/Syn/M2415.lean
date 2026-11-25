import Syn.M1115
import Syn.M1336
import Syn.M2398
import Syn.M2399

namespace Syn.M2415
def val : Nat := Syn.M1115.val % 7 + Syn.M1336.val % 7 + Syn.M2398.val % 7 + Syn.M2399.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2415
