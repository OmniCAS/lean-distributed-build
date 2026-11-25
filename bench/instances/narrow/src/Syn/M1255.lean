import Syn.M1068
import Syn.M1118
import Syn.M1138
import Syn.M1141
import Syn.M1142
import Syn.M1143
import Syn.M1190
import Syn.M1191
import Syn.M1192

namespace Syn.M1255
def val : Nat := Syn.M1068.val % 7 + Syn.M1118.val % 7 + Syn.M1138.val % 7 + Syn.M1141.val % 7 + Syn.M1142.val % 7 + Syn.M1143.val % 7 + Syn.M1190.val % 7 + Syn.M1191.val % 7 + Syn.M1192.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1255
