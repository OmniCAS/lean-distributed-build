import Syn.M2393
import Syn.M2404
import Syn.M2405
import Syn.M2406
import Syn.M2407

namespace Syn.M2420
def val : Nat := Syn.M2393.val % 7 + Syn.M2404.val % 7 + Syn.M2405.val % 7 + Syn.M2406.val % 7 + Syn.M2407.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M2420
