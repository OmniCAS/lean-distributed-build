import Syn.M741
import Syn.M2127
import Syn.M2129
import Syn.M2174

namespace Syn.M2188
def val : Nat := Syn.M741.val % 7 + Syn.M2127.val % 7 + Syn.M2129.val % 7 + Syn.M2174.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2188
