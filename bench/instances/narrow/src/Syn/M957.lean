import Syn.M734
import Syn.M735
import Syn.M737
import Syn.M863

namespace Syn.M957
def val : Nat := Syn.M734.val % 7 + Syn.M735.val % 7 + Syn.M737.val % 7 + Syn.M863.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M957
