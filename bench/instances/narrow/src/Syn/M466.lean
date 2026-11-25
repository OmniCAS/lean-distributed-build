import Syn.M179
import Syn.M184
import Syn.M185
import Syn.M281
import Syn.M283
import Syn.M284
import Syn.M285
import Syn.M386
import Syn.M394

namespace Syn.M466
def val : Nat := Syn.M179.val % 7 + Syn.M184.val % 7 + Syn.M185.val % 7 + Syn.M281.val % 7 + Syn.M283.val % 7 + Syn.M284.val % 7 + Syn.M285.val % 7 + Syn.M386.val % 7 + Syn.M394.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M466
