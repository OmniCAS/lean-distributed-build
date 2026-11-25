import Syn.M244
import Syn.M662
import Syn.M961
import Syn.M1968
import Syn.M2011

namespace Syn.M2060
def val : Nat := Syn.M244.val % 7 + Syn.M662.val % 7 + Syn.M961.val % 7 + Syn.M1968.val % 7 + Syn.M2011.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M2060
