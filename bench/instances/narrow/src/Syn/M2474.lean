import Syn.M661
import Syn.M939
import Syn.M1004
import Syn.M1433
import Syn.M1446
import Syn.M1789
import Syn.M1881
import Syn.M2471

namespace Syn.M2474
def val : Nat := Syn.M661.val % 7 + Syn.M939.val % 7 + Syn.M1004.val % 7 + Syn.M1433.val % 7 + Syn.M1446.val % 7 + Syn.M1789.val % 7 + Syn.M1881.val % 7 + Syn.M2471.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
end Syn.M2474
