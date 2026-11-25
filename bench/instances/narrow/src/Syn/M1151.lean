import Syn.M630
import Syn.M1103

namespace Syn.M1151
def val : Nat := Syn.M630.val % 7 + Syn.M1103.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1151
