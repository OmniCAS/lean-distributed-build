import Syn.M1992
import Syn.M1994
import Syn.M1995

namespace Syn.M2053
def val : Nat := Syn.M1992.val % 7 + Syn.M1994.val % 7 + Syn.M1995.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2053
