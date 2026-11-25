import Syn.M1386
import Syn.M1387
import Syn.M1569
import Syn.M1635

namespace Syn.M1657
def val : Nat := Syn.M1386.val % 7 + Syn.M1387.val % 7 + Syn.M1569.val % 7 + Syn.M1635.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1657
