import Syn.M739
import Syn.M864
import Syn.M1088

namespace Syn.M1129
def val : Nat := Syn.M739.val % 7 + Syn.M864.val % 7 + Syn.M1088.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1129
