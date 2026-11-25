import Syn.M2030
import Syn.M2179

namespace Syn.M2195
def val : Nat := Syn.M2030.val % 7 + Syn.M2179.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2195
