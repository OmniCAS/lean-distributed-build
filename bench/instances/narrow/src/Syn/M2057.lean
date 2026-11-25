import Syn.M1956
import Syn.M1957
import Syn.M1958
import Syn.M1959
import Syn.M2007

namespace Syn.M2057
def val : Nat := Syn.M1956.val % 7 + Syn.M1957.val % 7 + Syn.M1958.val % 7 + Syn.M1959.val % 7 + Syn.M2007.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2057
