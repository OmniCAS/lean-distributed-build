import Syn.M1163
import Syn.M1404
import Syn.M1706
import Syn.M2235

namespace Syn.M2266
def val : Nat := Syn.M1163.val % 7 + Syn.M1404.val % 7 + Syn.M1706.val % 7 + Syn.M2235.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2266
