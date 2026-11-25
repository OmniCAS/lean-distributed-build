import Syn.M638
import Syn.M706
import Syn.M708
import Syn.M709
import Syn.M710
import Syn.M711
import Syn.M828
import Syn.M829
import Syn.M866
import Syn.M929
import Syn.M930
import Syn.M931
import Syn.M1065

namespace Syn.M1112
def val : Nat := Syn.M638.val % 7 + Syn.M706.val % 7 + Syn.M708.val % 7 + Syn.M709.val % 7 + Syn.M710.val % 7 + Syn.M711.val % 7 + Syn.M828.val % 7 + Syn.M829.val % 7 + Syn.M866.val % 7 + Syn.M929.val % 7 + Syn.M930.val % 7 + Syn.M931.val % 7 + Syn.M1065.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1112
