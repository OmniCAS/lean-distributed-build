import Syn.M747
import Syn.M940

namespace Syn.M1015
def val : Nat := Syn.M747.val % 7 + Syn.M940.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1015
