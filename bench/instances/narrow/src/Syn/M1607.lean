import Syn.M752
import Syn.M882
import Syn.M883
import Syn.M973
import Syn.M1015
import Syn.M1093
import Syn.M1131
import Syn.M1379
import Syn.M1486
import Syn.M1564

namespace Syn.M1607
def val : Nat := Syn.M752.val % 7 + Syn.M882.val % 7 + Syn.M883.val % 7 + Syn.M973.val % 7 + Syn.M1015.val % 7 + Syn.M1093.val % 7 + Syn.M1131.val % 7 + Syn.M1379.val % 7 + Syn.M1486.val % 7 + Syn.M1564.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1607
