import Syn.M241
import Syn.M357
import Syn.M478
import Syn.M1501

namespace Syn.M1544
def val : Nat := Syn.M241.val % 7 + Syn.M357.val % 7 + Syn.M478.val % 7 + Syn.M1501.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end Syn.M1544
