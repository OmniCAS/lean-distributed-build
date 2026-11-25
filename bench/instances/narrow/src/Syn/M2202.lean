import Syn.M1853
import Syn.M2053
import Syn.M2131
import Syn.M2132
import Syn.M2172
import Syn.M2185

namespace Syn.M2202
def val : Nat := Syn.M1853.val % 7 + Syn.M2053.val % 7 + Syn.M2131.val % 7 + Syn.M2132.val % 7 + Syn.M2172.val % 7 + Syn.M2185.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2202
