import Syn.M705
import Syn.M709
import Syn.M827
import Syn.M1603

namespace Syn.M1629
def val : Nat := Syn.M705.val % 7 + Syn.M709.val % 7 + Syn.M827.val % 7 + Syn.M1603.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end Syn.M1629
