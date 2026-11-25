import Syn.M1031
import Syn.M1032
import Syn.M1033
import Syn.M1036
import Syn.M1144
import Syn.M1193
import Syn.M1194
import Syn.M1195
import Syn.M1196

namespace Syn.M1258
def val : Nat := Syn.M1031.val % 7 + Syn.M1032.val % 7 + Syn.M1033.val % 7 + Syn.M1036.val % 7 + Syn.M1144.val % 7 + Syn.M1193.val % 7 + Syn.M1194.val % 7 + Syn.M1195.val % 7 + Syn.M1196.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1258
