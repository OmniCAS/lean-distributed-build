import Syn.M930
import Syn.M1402
import Syn.M1752
import Syn.M1970

namespace Syn.M2022
def val : Nat := Syn.M930.val % 7 + Syn.M1402.val % 7 + Syn.M1752.val % 7 + Syn.M1970.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2022
