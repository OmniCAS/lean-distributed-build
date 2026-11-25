import Syn.M444
import Syn.M1098

namespace Syn.M1137
def val : Nat := Syn.M444.val % 7 + Syn.M1098.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1137
