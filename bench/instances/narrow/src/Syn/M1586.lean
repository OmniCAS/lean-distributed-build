import Syn.M361
import Syn.M1543

namespace Syn.M1586
def val : Nat := Syn.M361.val % 7 + Syn.M1543.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1586
