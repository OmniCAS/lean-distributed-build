import Syn.M1485
import Syn.M1518
import Syn.M1520
import Syn.M1521
import Syn.M1552
import Syn.M1553

namespace Syn.M1594
def val : Nat := Syn.M1485.val % 7 + Syn.M1518.val % 7 + Syn.M1520.val % 7 + Syn.M1521.val % 7 + Syn.M1552.val % 7 + Syn.M1553.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1594
