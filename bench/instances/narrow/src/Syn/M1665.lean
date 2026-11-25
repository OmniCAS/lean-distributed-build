import Syn.M1005
import Syn.M1041
import Syn.M1554
import Syn.M1647

namespace Syn.M1665
def val : Nat := Syn.M1005.val % 7 + Syn.M1041.val % 7 + Syn.M1554.val % 7 + Syn.M1647.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1665
