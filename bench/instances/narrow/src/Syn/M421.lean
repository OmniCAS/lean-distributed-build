import Syn.M359
import Syn.M360
import Syn.M361

namespace Syn.M421
def val : Nat := Syn.M359.val % 7 + Syn.M360.val % 7 + Syn.M361.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M421
