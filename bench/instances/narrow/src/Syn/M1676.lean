import Syn.M649
import Syn.M853
import Syn.M952
import Syn.M1126
import Syn.M1178
import Syn.M1544
import Syn.M1659

namespace Syn.M1676
def val : Nat := Syn.M649.val % 7 + Syn.M853.val % 7 + Syn.M952.val % 7 + Syn.M1126.val % 7 + Syn.M1178.val % 7 + Syn.M1544.val % 7 + Syn.M1659.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1676
