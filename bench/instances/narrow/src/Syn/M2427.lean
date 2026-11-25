import Syn.M2399
import Syn.M2412
import Syn.M2413
import Syn.M2414
import Syn.M2415
import Syn.M2416
import Syn.M2417
import Syn.M2423

namespace Syn.M2427
def val : Nat := Syn.M2399.val % 7 + Syn.M2412.val % 7 + Syn.M2413.val % 7 + Syn.M2414.val % 7 + Syn.M2415.val % 7 + Syn.M2416.val % 7 + Syn.M2417.val % 7 + Syn.M2423.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2427
