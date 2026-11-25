import Syn.M1964
import Syn.M2097
import Syn.M2204
import Syn.M2226

namespace Syn.M2252
def val : Nat := Syn.M1964.val % 7 + Syn.M2097.val % 7 + Syn.M2204.val % 7 + Syn.M2226.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2252
