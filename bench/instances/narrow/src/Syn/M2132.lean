import Syn.M1822
import Syn.M1823
import Syn.M1993
import Syn.M2101

namespace Syn.M2132
def val : Nat := Syn.M1822.val % 7 + Syn.M1823.val % 7 + Syn.M1993.val % 7 + Syn.M2101.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2132
