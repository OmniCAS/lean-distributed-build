import Syn.M875
import Syn.M1041
import Syn.M1091
import Syn.M1093
import Syn.M2378

namespace Syn.M2386
def val : Nat := Syn.M875.val % 7 + Syn.M1041.val % 7 + Syn.M1091.val % 7 + Syn.M1093.val % 7 + Syn.M2378.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end Syn.M2386
