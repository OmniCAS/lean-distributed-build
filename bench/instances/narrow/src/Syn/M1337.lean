import Syn.M946
import Syn.M1291

namespace Syn.M1337
def val : Nat := Syn.M946.val % 7 + Syn.M1291.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1337
