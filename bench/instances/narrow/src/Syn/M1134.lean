import Syn.M905
import Syn.M1096

namespace Syn.M1134
def val : Nat := Syn.M905.val % 7 + Syn.M1096.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1134
