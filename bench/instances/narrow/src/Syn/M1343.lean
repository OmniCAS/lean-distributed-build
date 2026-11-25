import Syn.M1168
import Syn.M1169
import Syn.M1170
import Syn.M1171
import Syn.M1251
import Syn.M1252
import Syn.M1253
import Syn.M1256
import Syn.M1258
import Syn.M1305

namespace Syn.M1343
def val : Nat := Syn.M1168.val % 7 + Syn.M1169.val % 7 + Syn.M1170.val % 7 + Syn.M1171.val % 7 + Syn.M1251.val % 7 + Syn.M1252.val % 7 + Syn.M1253.val % 7 + Syn.M1256.val % 7 + Syn.M1258.val % 7 + Syn.M1305.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1343
