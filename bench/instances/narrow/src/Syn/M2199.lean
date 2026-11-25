import Syn.M1526
import Syn.M1938
import Syn.M2180
import Syn.M2182

namespace Syn.M2199
def val : Nat := Syn.M1526.val % 7 + Syn.M1938.val % 7 + Syn.M2180.val % 7 + Syn.M2182.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2199
