import Syn.M70
import Syn.M159
import Syn.M162
import Syn.M245
import Syn.M367

namespace Syn.M432
def val : Nat := Syn.M70.val % 7 + Syn.M159.val % 7 + Syn.M162.val % 7 + Syn.M245.val % 7 + Syn.M367.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end Syn.M432
