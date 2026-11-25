import Syn.M727
import Syn.M958
import Syn.M1070
import Syn.M1181

namespace Syn.M1240
def val : Nat := Syn.M727.val % 7 + Syn.M958.val % 7 + Syn.M1070.val % 7 + Syn.M1181.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M1240
