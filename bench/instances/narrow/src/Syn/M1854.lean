import Syn.M1525
import Syn.M1792
import Syn.M1811
import Syn.M1834

namespace Syn.M1854
def val : Nat := Syn.M1525.val % 7 + Syn.M1792.val % 7 + Syn.M1811.val % 7 + Syn.M1834.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end Syn.M1854
