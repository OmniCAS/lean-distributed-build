import Syn.M1047
import Syn.M1845

namespace Syn.M1869
def val : Nat := Syn.M1047.val % 7 + Syn.M1845.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1869
