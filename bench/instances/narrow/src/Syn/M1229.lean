import Syn.M938
import Syn.M1060
import Syn.M1108
import Syn.M1158

namespace Syn.M1229
def val : Nat := Syn.M938.val % 7 + Syn.M1060.val % 7 + Syn.M1108.val % 7 + Syn.M1158.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1229
