import Syn.M1134
import Syn.M1182
import Syn.M1254
import Syn.M1255

namespace Syn.M1305
def val : Nat := Syn.M1134.val % 7 + Syn.M1182.val % 7 + Syn.M1254.val % 7 + Syn.M1255.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1305
