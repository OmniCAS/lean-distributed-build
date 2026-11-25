import Syn.M420
import Syn.M662
import Syn.M712

namespace Syn.M835
def val : Nat := Syn.M420.val % 7 + Syn.M662.val % 7 + Syn.M712.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M835
