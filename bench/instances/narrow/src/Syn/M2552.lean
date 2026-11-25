import Syn.M1099
import Syn.M2123
import Syn.M2540

namespace Syn.M2552
def val : Nat := Syn.M1099.val % 7 + Syn.M2123.val % 7 + Syn.M2540.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end Syn.M2552
