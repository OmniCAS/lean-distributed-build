import Syn.M2512
import Syn.M2513

namespace Syn.M2531
def val : Nat := Syn.M2512.val % 7 + Syn.M2513.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2531
