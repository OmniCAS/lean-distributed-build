import Syn.M1262
import Syn.M1263
import Syn.M1324
import Syn.M1806

namespace Syn.M1828
def val : Nat := Syn.M1262.val % 7 + Syn.M1263.val % 7 + Syn.M1324.val % 7 + Syn.M1806.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1828
