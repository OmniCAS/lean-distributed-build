import Syn.M661
import Syn.M662
import Syn.M706
import Syn.M911
import Syn.M1261
import Syn.M1396
import Syn.M1917
import Syn.M1945

namespace Syn.M1991
def val : Nat := Syn.M661.val % 7 + Syn.M662.val % 7 + Syn.M706.val % 7 + Syn.M911.val % 7 + Syn.M1261.val % 7 + Syn.M1396.val % 7 + Syn.M1917.val % 7 + Syn.M1945.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end Syn.M1991
