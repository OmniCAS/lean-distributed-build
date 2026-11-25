import Syn.M27
import Syn.M31
import Syn.M34
import Syn.M638

namespace Syn.M702
def val : Nat := Syn.M27.val % 7 + Syn.M31.val % 7 + Syn.M34.val % 7 + Syn.M638.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M702
