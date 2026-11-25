import Syn.M659
import Syn.M797
import Syn.M1116
import Syn.M1335
import Syn.M1421
import Syn.M1424
import Syn.M1457
import Syn.M1563
import Syn.M1803
import Syn.M1905
import Syn.M1974
import Syn.M2394

namespace Syn.M2409
def val : Nat := Syn.M659.val % 7 + Syn.M797.val % 7 + Syn.M1116.val % 7 + Syn.M1335.val % 7 + Syn.M1421.val % 7 + Syn.M1424.val % 7 + Syn.M1457.val % 7 + Syn.M1563.val % 7 + Syn.M1803.val % 7 + Syn.M1905.val % 7 + Syn.M1974.val % 7 + Syn.M2394.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
theorem w7 (a b : Nat) : a + b + 7 = b + a + 7 := by omega
theorem w8 (a b : Nat) : a + b + 8 = b + a + 8 := by omega
theorem w9 (a b : Nat) : a + b + 9 = b + a + 9 := by omega
theorem w10 (a b : Nat) : a + b + 10 = b + a + 10 := by omega
theorem w11 (a b : Nat) : a + b + 11 = b + a + 11 := by omega
end Syn.M2409
