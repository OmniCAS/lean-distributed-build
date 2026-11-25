import Syn.M636
import Syn.M685

namespace Syn.M790
def val : Nat := Syn.M636.val % 7 + Syn.M685.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M790
