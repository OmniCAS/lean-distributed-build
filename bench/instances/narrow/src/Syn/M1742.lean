import Syn.M743
import Syn.M1005
import Syn.M1723

namespace Syn.M1742
def val : Nat := Syn.M743.val % 7 + Syn.M1005.val % 7 + Syn.M1723.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M1742
