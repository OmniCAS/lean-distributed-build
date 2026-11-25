import Syn.M1903
import Syn.M1973

namespace Syn.M2028
def val : Nat := Syn.M1903.val % 7 + Syn.M1973.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2028
