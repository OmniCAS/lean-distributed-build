import Syn.M803
import Syn.M1402
import Syn.M1634
import Syn.M1769
import Syn.M1810
import Syn.M1836
import Syn.M1948

namespace Syn.M1998
def val : Nat := Syn.M803.val % 7 + Syn.M1402.val % 7 + Syn.M1634.val % 7 + Syn.M1769.val % 7 + Syn.M1810.val % 7 + Syn.M1836.val % 7 + Syn.M1948.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end Syn.M1998
