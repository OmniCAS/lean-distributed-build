import Syn.M892
import Syn.M1095
import Syn.M1132
import Syn.M1133

namespace Syn.M1183
def val : Nat := Syn.M892.val % 7 + Syn.M1095.val % 7 + Syn.M1132.val % 7 + Syn.M1133.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1183
