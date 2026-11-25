import Syn.M1761
import Syn.M1762

namespace Syn.M1774
def val : Nat := Syn.M1761.val % 7 + Syn.M1762.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1774
