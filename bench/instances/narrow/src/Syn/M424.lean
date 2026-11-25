import Syn.M26
import Syn.M163
import Syn.M164
import Syn.M165
import Syn.M364

namespace Syn.M424
def val : Nat := Syn.M26.val % 7 + Syn.M163.val % 7 + Syn.M164.val % 7 + Syn.M165.val % 7 + Syn.M364.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end Syn.M424
