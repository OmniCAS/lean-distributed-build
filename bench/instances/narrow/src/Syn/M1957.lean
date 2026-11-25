import Syn.M939
import Syn.M1004
import Syn.M1115
import Syn.M1929

namespace Syn.M1957
def val : Nat := Syn.M939.val % 7 + Syn.M1004.val % 7 + Syn.M1115.val % 7 + Syn.M1929.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1957
