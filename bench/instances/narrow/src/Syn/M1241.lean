import Syn.M667
import Syn.M1050
import Syn.M1183

namespace Syn.M1241
def val : Nat := Syn.M667.val % 7 + Syn.M1050.val % 7 + Syn.M1183.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1241
