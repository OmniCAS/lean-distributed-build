import Syn.M1275
import Syn.M2425
import Syn.M2503

namespace Syn.M2522
def val : Nat := Syn.M1275.val % 7 + Syn.M2425.val % 7 + Syn.M2503.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2522
