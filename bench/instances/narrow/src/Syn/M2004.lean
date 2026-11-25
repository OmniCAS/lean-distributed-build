import Syn.M1224
import Syn.M1589
import Syn.M1952

namespace Syn.M2004
def val : Nat := Syn.M1224.val % 7 + Syn.M1589.val % 7 + Syn.M1952.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2004
