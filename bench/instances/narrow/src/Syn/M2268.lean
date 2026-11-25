import Syn.M1525
import Syn.M1859
import Syn.M1939
import Syn.M2235

namespace Syn.M2268
def val : Nat := Syn.M1525.val % 7 + Syn.M1859.val % 7 + Syn.M1939.val % 7 + Syn.M2235.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2268
