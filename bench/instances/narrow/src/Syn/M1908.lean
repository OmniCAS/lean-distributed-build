import Syn.M1272
import Syn.M1336
import Syn.M1790
import Syn.M1836
import Syn.M1859
import Syn.M1875

namespace Syn.M1908
def val : Nat := Syn.M1272.val % 7 + Syn.M1336.val % 7 + Syn.M1790.val % 7 + Syn.M1836.val % 7 + Syn.M1859.val % 7 + Syn.M1875.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M1908
