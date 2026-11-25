import Syn.M787
import Syn.M987

namespace Syn.M1056
def val : Nat := Syn.M787.val % 7 + Syn.M987.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1056
