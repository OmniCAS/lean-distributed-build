import Syn.M728
import Syn.M729
import Syn.M732
import Syn.M733
import Syn.M853
import Syn.M859
import Syn.M861
import Syn.M862
import Syn.M953
import Syn.M1006
import Syn.M1088

namespace Syn.M1128
def val : Nat := Syn.M728.val % 7 + Syn.M729.val % 7 + Syn.M732.val % 7 + Syn.M733.val % 7 + Syn.M853.val % 7 + Syn.M859.val % 7 + Syn.M861.val % 7 + Syn.M862.val % 7 + Syn.M953.val % 7 + Syn.M1006.val % 7 + Syn.M1088.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1128
