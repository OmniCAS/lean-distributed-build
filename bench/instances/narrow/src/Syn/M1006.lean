import Syn.M242
import Syn.M244
import Syn.M731
import Syn.M853
import Syn.M929
import Syn.M930

namespace Syn.M1006
def val : Nat := Syn.M242.val % 7 + Syn.M244.val % 7 + Syn.M731.val % 7 + Syn.M853.val % 7 + Syn.M929.val % 7 + Syn.M930.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
end Syn.M1006
