import Syn.M959
import Syn.M1129

namespace Syn.M1181
def val : Nat := Syn.M959.val % 7 + Syn.M1129.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1181
