import Syn.M709
import Syn.M1536

namespace Syn.M1574
def val : Nat := Syn.M709.val % 7 + Syn.M1536.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1574
