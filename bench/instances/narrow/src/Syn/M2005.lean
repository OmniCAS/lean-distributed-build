import Syn.M1953
import Syn.M1954

namespace Syn.M2005
def val : Nat := Syn.M1953.val % 7 + Syn.M1954.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2005
