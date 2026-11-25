import Syn.M12
import Syn.M98
import Syn.M444
import Syn.M962
import Syn.M1258
import Syn.M1345
import Syn.M1367

namespace Syn.M1408
def val : Nat := Syn.M12.val % 7 + Syn.M98.val % 7 + Syn.M444.val % 7 + Syn.M962.val % 7 + Syn.M1258.val % 7 + Syn.M1345.val % 7 + Syn.M1367.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1408
