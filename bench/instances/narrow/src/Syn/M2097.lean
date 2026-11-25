import Syn.M1664
import Syn.M1846
import Syn.M1919
import Syn.M2051

namespace Syn.M2097
def val : Nat := Syn.M1664.val % 7 + Syn.M1846.val % 7 + Syn.M1919.val % 7 + Syn.M2051.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2097
