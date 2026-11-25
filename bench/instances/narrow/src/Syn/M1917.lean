import Syn.M361
import Syn.M630
import Syn.M1232
import Syn.M1248
import Syn.M1879

namespace Syn.M1917
def val : Nat := Syn.M361.val % 7 + Syn.M630.val % 7 + Syn.M1232.val % 7 + Syn.M1248.val % 7 + Syn.M1879.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1917
