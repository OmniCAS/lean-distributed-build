import Syn.M2152
import Syn.M2153
import Syn.M2155
import Syn.M2156
import Syn.M2157
import Syn.M2158
import Syn.M2191

namespace Syn.M2209
def val : Nat := Syn.M2152.val % 7 + Syn.M2153.val % 7 + Syn.M2155.val % 7 + Syn.M2156.val % 7 + Syn.M2157.val % 7 + Syn.M2158.val % 7 + Syn.M2191.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2209
