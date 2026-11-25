import Syn.M875
import Syn.M1147
import Syn.M1184
import Syn.M1360
import Syn.M1797

namespace Syn.M1815
def val : Nat := Syn.M875.val % 7 + Syn.M1147.val % 7 + Syn.M1184.val % 7 + Syn.M1360.val % 7 + Syn.M1797.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M1815
