import Syn.M1150
import Syn.M1415
import Syn.M1416
import Syn.M1449
import Syn.M2207
import Syn.M2544

namespace Syn.M2562
def val : Nat := Syn.M1150.val % 7 + Syn.M1415.val % 7 + Syn.M1416.val % 7 + Syn.M1449.val % 7 + Syn.M2207.val % 7 + Syn.M2544.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2562
