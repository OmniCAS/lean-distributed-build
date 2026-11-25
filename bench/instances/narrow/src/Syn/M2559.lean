import Syn.M1446
import Syn.M1486
import Syn.M2073
import Syn.M2540

namespace Syn.M2559
def val : Nat := Syn.M1446.val % 7 + Syn.M1486.val % 7 + Syn.M2073.val % 7 + Syn.M2540.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2559
