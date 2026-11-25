import Syn.M569
import Syn.M840
import Syn.M1041
import Syn.M1091
import Syn.M1446

namespace Syn.M1486
def val : Nat := Syn.M569.val % 7 + Syn.M840.val % 7 + Syn.M1041.val % 7 + Syn.M1091.val % 7 + Syn.M1446.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1486
