import Syn.M633
import Syn.M1750

namespace Syn.M1765
def val : Nat := Syn.M633.val % 7 + Syn.M1750.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1765
