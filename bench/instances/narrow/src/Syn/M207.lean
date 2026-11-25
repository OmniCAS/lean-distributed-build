import Syn.M80
import Syn.M111
import Syn.M112
import Syn.M113

namespace Syn.M207
def val : Nat := Syn.M80.val % 7 + Syn.M111.val % 7 + Syn.M112.val % 7 + Syn.M113.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M207
