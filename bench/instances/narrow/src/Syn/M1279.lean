import Syn.M911
import Syn.M1228

namespace Syn.M1279
def val : Nat := Syn.M911.val % 7 + Syn.M1228.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1279
