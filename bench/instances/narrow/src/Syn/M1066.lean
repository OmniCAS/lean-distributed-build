import Syn.M661
import Syn.M1004

namespace Syn.M1066
def val : Nat := Syn.M661.val % 7 + Syn.M1004.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1066
