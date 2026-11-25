import Syn.M1785
import Syn.M2587

namespace Syn.M2593
def val : Nat := Syn.M1785.val % 7 + Syn.M2587.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2593
