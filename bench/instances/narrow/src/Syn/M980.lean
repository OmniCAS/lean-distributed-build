import Syn.M667
import Syn.M893

namespace Syn.M980
def val : Nat := Syn.M667.val % 7 + Syn.M893.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M980
