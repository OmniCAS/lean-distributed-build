import Syn.M911
import Syn.M1216
import Syn.M1634
import Syn.M1999
import Syn.M2083
import Syn.M2151
import Syn.M2246

namespace Syn.M2275
def val : Nat := Syn.M911.val % 7 + Syn.M1216.val % 7 + Syn.M1634.val % 7 + Syn.M1999.val % 7 + Syn.M2083.val % 7 + Syn.M2151.val % 7 + Syn.M2246.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end Syn.M2275
