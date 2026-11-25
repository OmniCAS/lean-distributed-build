import Syn.M535
import Syn.M605
import Syn.M746
import Syn.M747
import Syn.M748
import Syn.M749
import Syn.M751

namespace Syn.M877
def val : Nat := Syn.M535.val % 7 + Syn.M605.val % 7 + Syn.M746.val % 7 + Syn.M747.val % 7 + Syn.M748.val % 7 + Syn.M749.val % 7 + Syn.M751.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M877
