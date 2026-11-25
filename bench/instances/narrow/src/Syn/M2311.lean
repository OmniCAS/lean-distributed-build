import Syn.M1206
import Syn.M1207
import Syn.M1209
import Syn.M1288
import Syn.M1963
import Syn.M2194
import Syn.M2260
import Syn.M2293

namespace Syn.M2311
def val : Nat := Syn.M1206.val % 7 + Syn.M1207.val % 7 + Syn.M1209.val % 7 + Syn.M1288.val % 7 + Syn.M1963.val % 7 + Syn.M2194.val % 7 + Syn.M2260.val % 7 + Syn.M2293.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2311
