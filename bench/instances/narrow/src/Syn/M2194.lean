import Syn.M1288
import Syn.M1701
import Syn.M1714
import Syn.M1722
import Syn.M1724
import Syn.M1725
import Syn.M1739
import Syn.M1742
import Syn.M1743
import Syn.M1824
import Syn.M2033
import Syn.M2078
import Syn.M2089
import Syn.M2117
import Syn.M2119
import Syn.M2143
import Syn.M2166
import Syn.M2178

namespace Syn.M2194
def val : Nat := Syn.M1288.val % 7 + Syn.M1701.val % 7 + Syn.M1714.val % 7 + Syn.M1722.val % 7 + Syn.M1724.val % 7 + Syn.M1725.val % 7 + Syn.M1739.val % 7 + Syn.M1742.val % 7 + Syn.M1743.val % 7 + Syn.M1824.val % 7 + Syn.M2033.val % 7 + Syn.M2078.val % 7 + Syn.M2089.val % 7 + Syn.M2117.val % 7 + Syn.M2119.val % 7 + Syn.M2143.val % 7 + Syn.M2166.val % 7 + Syn.M2178.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2194
