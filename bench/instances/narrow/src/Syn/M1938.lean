import Syn.M744
import Syn.M879
import Syn.M1005
import Syn.M1831
import Syn.M1836
import Syn.M1906

namespace Syn.M1938
def val : Nat := Syn.M744.val % 7 + Syn.M879.val % 7 + Syn.M1005.val % 7 + Syn.M1831.val % 7 + Syn.M1836.val % 7 + Syn.M1906.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
end Syn.M1938
