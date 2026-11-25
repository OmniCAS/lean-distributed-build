import Syn.M827
import Syn.M1540

namespace Syn.M1584
def val : Nat := Syn.M827.val % 7 + Syn.M1540.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1584
