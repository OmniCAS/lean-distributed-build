import Syn.M748
import Syn.M2101
import Syn.M2172
import Syn.M2378
import Syn.M2380
import Syn.M2382
import Syn.M2383
import Syn.M2384
import Syn.M2385
import Syn.M2386
import Syn.M2387
import Syn.M2388
import Syn.M2389
import Syn.M2398

namespace Syn.M2411
def val : Nat := Syn.M748.val % 7 + Syn.M2101.val % 7 + Syn.M2172.val % 7 + Syn.M2378.val % 7 + Syn.M2380.val % 7 + Syn.M2382.val % 7 + Syn.M2383.val % 7 + Syn.M2384.val % 7 + Syn.M2385.val % 7 + Syn.M2386.val % 7 + Syn.M2387.val % 7 + Syn.M2388.val % 7 + Syn.M2389.val % 7 + Syn.M2398.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2411
