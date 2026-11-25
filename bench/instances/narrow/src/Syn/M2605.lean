import Syn.M59
import Syn.M266
import Syn.M1968
import Syn.M1969
import Syn.M1971
import Syn.M2159
import Syn.M2603

namespace Syn.M2605
def val : Nat := Syn.M59.val % 7 + Syn.M266.val % 7 + Syn.M1968.val % 7 + Syn.M1969.val % 7 + Syn.M1971.val % 7 + Syn.M2159.val % 7 + Syn.M2603.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2605
