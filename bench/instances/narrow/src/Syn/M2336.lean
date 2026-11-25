import Syn.M2252
import Syn.M2311

namespace Syn.M2336
def val : Nat := Syn.M2252.val % 7 + Syn.M2311.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2336
