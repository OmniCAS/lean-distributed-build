import Syn.M540
import Syn.M794
import Syn.M912
import Syn.M913
import Syn.M914
import Syn.M1028
import Syn.M1239
import Syn.M1332
import Syn.M1407

namespace Syn.M1444
def val : Nat := Syn.M540.val % 7 + Syn.M794.val % 7 + Syn.M912.val % 7 + Syn.M913.val % 7 + Syn.M914.val % 7 + Syn.M1028.val % 7 + Syn.M1239.val % 7 + Syn.M1332.val % 7 + Syn.M1407.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
end Syn.M1444
