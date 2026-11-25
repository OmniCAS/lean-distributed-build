import Syn.M1746
import Syn.M1747
import Syn.M1749
import Syn.M1751
import Syn.M1936
import Syn.M2120
import Syn.M2160
import Syn.M2183
import Syn.M2197
import Syn.M2337
import Syn.M2339

namespace Syn.M2354
def val : Nat := Syn.M1746.val % 7 + Syn.M1747.val % 7 + Syn.M1749.val % 7 + Syn.M1751.val % 7 + Syn.M1936.val % 7 + Syn.M2120.val % 7 + Syn.M2160.val % 7 + Syn.M2183.val % 7 + Syn.M2197.val % 7 + Syn.M2337.val % 7 + Syn.M2339.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2354
