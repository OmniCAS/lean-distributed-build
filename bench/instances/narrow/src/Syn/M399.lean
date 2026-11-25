import Syn.M210
import Syn.M213
import Syn.M331
import Syn.M332
import Syn.M334
import Syn.M335
import Syn.M336

namespace Syn.M399
def val : Nat := Syn.M210.val % 7 + Syn.M213.val % 7 + Syn.M331.val % 7 + Syn.M332.val % 7 + Syn.M334.val % 7 + Syn.M335.val % 7 + Syn.M336.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M399
