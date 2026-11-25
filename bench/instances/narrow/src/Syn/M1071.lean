import Syn.M642
import Syn.M660
import Syn.M662
import Syn.M1009

namespace Syn.M1071
def val : Nat := Syn.M642.val % 7 + Syn.M660.val % 7 + Syn.M662.val % 7 + Syn.M1009.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M1071
