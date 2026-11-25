import Syn.M971
import Syn.M1361
import Syn.M1769
import Syn.M1779
import Syn.M2142
import Syn.M2235

namespace Syn.M2264
def val : Nat := Syn.M971.val % 7 + Syn.M1361.val % 7 + Syn.M1769.val % 7 + Syn.M1779.val % 7 + Syn.M2142.val % 7 + Syn.M2235.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2264
