import Syn.M2359
import Syn.M2361
import Syn.M2363
import Syn.M2364
import Syn.M2366
import Syn.M2373

namespace Syn.M2377
def val : Nat := Syn.M2359.val % 7 + Syn.M2361.val % 7 + Syn.M2363.val % 7 + Syn.M2364.val % 7 + Syn.M2366.val % 7 + Syn.M2373.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2377
