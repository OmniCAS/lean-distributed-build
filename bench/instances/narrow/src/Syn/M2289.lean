import Syn.M1792
import Syn.M1829
import Syn.M1854
import Syn.M1950
import Syn.M2002
import Syn.M2250
import Syn.M2251

namespace Syn.M2289
def val : Nat := Syn.M1792.val % 7 + Syn.M1829.val % 7 + Syn.M1854.val % 7 + Syn.M1950.val % 7 + Syn.M2002.val % 7 + Syn.M2250.val % 7 + Syn.M2251.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2289
