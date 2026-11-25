import Syn.M1007
import Syn.M2454
import Syn.M2477

namespace Syn.M2485
def val : Nat := Syn.M1007.val % 7 + Syn.M2454.val % 7 + Syn.M2477.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2485
