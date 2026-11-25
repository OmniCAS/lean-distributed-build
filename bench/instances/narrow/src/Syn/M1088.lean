import Syn.M724
import Syn.M857
import Syn.M1027

namespace Syn.M1088
def val : Nat := Syn.M724.val % 7 + Syn.M857.val % 7 + Syn.M1027.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1088
