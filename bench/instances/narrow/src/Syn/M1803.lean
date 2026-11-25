import Syn.M1047
import Syn.M1228
import Syn.M1524
import Syn.M1598
import Syn.M1790

namespace Syn.M1803
def val : Nat := Syn.M1047.val % 7 + Syn.M1228.val % 7 + Syn.M1524.val % 7 + Syn.M1598.val % 7 + Syn.M1790.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
end Syn.M1803
