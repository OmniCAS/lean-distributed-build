import Syn.M693
import Syn.M1750
import Syn.M1836
import Syn.M1947

namespace Syn.M1997
def val : Nat := Syn.M693.val % 7 + Syn.M1750.val % 7 + Syn.M1836.val % 7 + Syn.M1947.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1997
