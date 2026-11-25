import Syn.M662
import Syn.M1262
import Syn.M1360
import Syn.M1790
import Syn.M2185
import Syn.M2378

namespace Syn.M2382
def val : Nat := Syn.M662.val % 7 + Syn.M1262.val % 7 + Syn.M1360.val % 7 + Syn.M1790.val % 7 + Syn.M2185.val % 7 + Syn.M2378.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2382
