import Syn.M358
import Syn.M650

namespace Syn.M726
def val : Nat := Syn.M358.val % 7 + Syn.M650.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M726
