import Syn.M992
import Syn.M1157

namespace Syn.M1214
def val : Nat := Syn.M992.val % 7 + Syn.M1157.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1214
