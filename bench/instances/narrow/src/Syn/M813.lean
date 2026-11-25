import Syn.M630
import Syn.M700

namespace Syn.M813
def val : Nat := Syn.M630.val % 7 + Syn.M700.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M813
