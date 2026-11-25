import Syn.M71
import Syn.M236
import Syn.M239
import Syn.M419

namespace Syn.M478
def val : Nat := Syn.M71.val % 7 + Syn.M236.val % 7 + Syn.M239.val % 7 + Syn.M419.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M478
