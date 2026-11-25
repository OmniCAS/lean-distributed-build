import Syn.M1729
import Syn.M1747
import Syn.M1749
import Syn.M1781
import Syn.M1790
import Syn.M1927
import Syn.M1936
import Syn.M2120
import Syn.M2136
import Syn.M2137
import Syn.M2183
import Syn.M2197
import Syn.M2310
import Syn.M2337
import Syn.M2339
import Syn.M2360
import Syn.M2372

namespace Syn.M2376
def val : Nat := Syn.M1729.val % 7 + Syn.M1747.val % 7 + Syn.M1749.val % 7 + Syn.M1781.val % 7 + Syn.M1790.val % 7 + Syn.M1927.val % 7 + Syn.M1936.val % 7 + Syn.M2120.val % 7 + Syn.M2136.val % 7 + Syn.M2137.val % 7 + Syn.M2183.val % 7 + Syn.M2197.val % 7 + Syn.M2310.val % 7 + Syn.M2337.val % 7 + Syn.M2339.val % 7 + Syn.M2360.val % 7 + Syn.M2372.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
end Syn.M2376
