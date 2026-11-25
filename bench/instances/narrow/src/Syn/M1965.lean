import Syn.M559
import Syn.M1933

namespace Syn.M1965
def val : Nat := Syn.M559.val % 7 + Syn.M1933.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1965
