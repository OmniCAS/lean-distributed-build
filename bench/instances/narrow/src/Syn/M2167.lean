import Syn.M2039
import Syn.M2042
import Syn.M2043
import Syn.M2085
import Syn.M2088
import Syn.M2090
import Syn.M2145

namespace Syn.M2167
def val : Nat := Syn.M2039.val % 7 + Syn.M2042.val % 7 + Syn.M2043.val % 7 + Syn.M2085.val % 7 + Syn.M2088.val % 7 + Syn.M2090.val % 7 + Syn.M2145.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2167
