import Syn.M22
import Syn.M660
import Syn.M868
import Syn.M1116
import Syn.M1981

namespace Syn.M2043
def val : Nat := Syn.M22.val % 7 + Syn.M660.val % 7 + Syn.M868.val % 7 + Syn.M1116.val % 7 + Syn.M1981.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end Syn.M2043
