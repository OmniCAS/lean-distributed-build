import Syn.M1042
import Syn.M1043
import Syn.M1632

namespace Syn.M1653
def val : Nat := Syn.M1042.val % 7 + Syn.M1043.val % 7 + Syn.M1632.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1653
