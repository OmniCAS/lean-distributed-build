import Syn.M1223
import Syn.M1692
import Syn.M1859

namespace Syn.M1884
def val : Nat := Syn.M1223.val % 7 + Syn.M1692.val % 7 + Syn.M1859.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1884
