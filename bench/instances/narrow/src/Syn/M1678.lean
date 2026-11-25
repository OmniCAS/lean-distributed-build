import Syn.M1406
import Syn.M1516
import Syn.M1551
import Syn.M1593
import Syn.M1640
import Syn.M1661

namespace Syn.M1678
def val : Nat := Syn.M1406.val % 7 + Syn.M1516.val % 7 + Syn.M1551.val % 7 + Syn.M1593.val % 7 + Syn.M1640.val % 7 + Syn.M1661.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1678
