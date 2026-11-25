import Syn.M348
import Syn.M349
import Syn.M350
import Syn.M351
import Syn.M352
import Syn.M354
import Syn.M355
import Syn.M418

namespace Syn.M477
def val : Nat := Syn.M348.val % 7 + Syn.M349.val % 7 + Syn.M350.val % 7 + Syn.M351.val % 7 + Syn.M352.val % 7 + Syn.M354.val % 7 + Syn.M355.val % 7 + Syn.M418.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M477
