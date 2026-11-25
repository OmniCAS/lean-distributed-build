import Syn.M2142
import Syn.M2187

namespace Syn.M2205
def val : Nat := Syn.M2142.val % 7 + Syn.M2187.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2205
