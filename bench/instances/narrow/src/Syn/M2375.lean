import Syn.M2276
import Syn.M2277
import Syn.M2313
import Syn.M2322
import Syn.M2340
import Syn.M2343
import Syn.M2357
import Syn.M2358
import Syn.M2370

namespace Syn.M2375
def val : Nat := Syn.M2276.val % 7 + Syn.M2277.val % 7 + Syn.M2313.val % 7 + Syn.M2322.val % 7 + Syn.M2340.val % 7 + Syn.M2343.val % 7 + Syn.M2357.val % 7 + Syn.M2358.val % 7 + Syn.M2370.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2375
