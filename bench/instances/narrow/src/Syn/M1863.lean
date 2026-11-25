import Syn.M1657
import Syn.M1685
import Syn.M1686
import Syn.M1827
import Syn.M1839

namespace Syn.M1863
def val : Nat := Syn.M1657.val % 7 + Syn.M1685.val % 7 + Syn.M1686.val % 7 + Syn.M1827.val % 7 + Syn.M1839.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1863
