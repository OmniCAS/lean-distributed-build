import Syn.M369
import Syn.M370
import Syn.M372
import Syn.M437

namespace Syn.M488
def val : Nat := Syn.M369.val % 7 + Syn.M370.val % 7 + Syn.M372.val % 7 + Syn.M437.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end Syn.M488
