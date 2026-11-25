import Syn.M715
import Syn.M867
import Syn.M1112

namespace Syn.M1162
def val : Nat := Syn.M715.val % 7 + Syn.M867.val % 7 + Syn.M1112.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1162
