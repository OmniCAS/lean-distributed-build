import Syn.M1149
import Syn.M1446

namespace Syn.M1484
def val : Nat := Syn.M1149.val % 7 + Syn.M1446.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1484
