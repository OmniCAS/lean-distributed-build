import Syn.M668
import Syn.M982

namespace Syn.M1051
def val : Nat := Syn.M668.val % 7 + Syn.M982.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1051
