import Syn.M1794
import Syn.M1859
import Syn.M2079
import Syn.M2102
import Syn.M2169

namespace Syn.M2184
def val : Nat := Syn.M1794.val % 7 + Syn.M1859.val % 7 + Syn.M2079.val % 7 + Syn.M2102.val % 7 + Syn.M2169.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
end Syn.M2184
