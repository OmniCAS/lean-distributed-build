import Syn.M32
import Syn.M33
import Syn.M638

namespace Syn.M703
def val : Nat := Syn.M32.val % 7 + Syn.M33.val % 7 + Syn.M638.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M703
