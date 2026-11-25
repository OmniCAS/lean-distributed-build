import Syn.M1420
import Syn.M1450
import Syn.M1451
import Syn.M1452
import Syn.M1489
import Syn.M1571
import Syn.M1648

namespace Syn.M1668
def val : Nat := Syn.M1420.val % 7 + Syn.M1450.val % 7 + Syn.M1451.val % 7 + Syn.M1452.val % 7 + Syn.M1489.val % 7 + Syn.M1571.val % 7 + Syn.M1648.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1668
