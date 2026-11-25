import Syn.M836
import Syn.M1108
import Syn.M1187
import Syn.M1368

namespace Syn.M1409
def val : Nat := Syn.M836.val % 7 + Syn.M1108.val % 7 + Syn.M1187.val % 7 + Syn.M1368.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1409
