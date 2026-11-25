import Syn.M1991
import Syn.M2052
import Syn.M2150

namespace Syn.M2172
def val : Nat := Syn.M1991.val % 7 + Syn.M2052.val % 7 + Syn.M2150.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2172
