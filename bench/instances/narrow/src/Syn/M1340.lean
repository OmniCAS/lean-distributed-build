import Syn.M12
import Syn.M18
import Syn.M444
import Syn.M501
import Syn.M962
import Syn.M1186
import Syn.M1301

namespace Syn.M1340
def val : Nat := Syn.M12.val % 7 + Syn.M18.val % 7 + Syn.M444.val % 7 + Syn.M501.val % 7 + Syn.M962.val % 7 + Syn.M1186.val % 7 + Syn.M1301.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M1340
