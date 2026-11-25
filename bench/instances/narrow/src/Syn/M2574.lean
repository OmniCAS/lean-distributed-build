import Syn.M1336
import Syn.M1606
import Syn.M1790
import Syn.M2251
import Syn.M2493
import Syn.M2561

namespace Syn.M2574
def val : Nat := Syn.M1336.val % 7 + Syn.M1606.val % 7 + Syn.M1790.val % 7 + Syn.M2251.val % 7 + Syn.M2493.val % 7 + Syn.M2561.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2574
