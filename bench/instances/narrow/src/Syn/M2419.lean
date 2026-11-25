import Syn.M2381
import Syn.M2382
import Syn.M2383
import Syn.M2391
import Syn.M2392
import Syn.M2397
import Syn.M2400
import Syn.M2402

namespace Syn.M2419
def val : Nat := Syn.M2381.val % 7 + Syn.M2382.val % 7 + Syn.M2383.val % 7 + Syn.M2391.val % 7 + Syn.M2392.val % 7 + Syn.M2397.val % 7 + Syn.M2400.val % 7 + Syn.M2402.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2419
