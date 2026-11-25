import Syn.M811
import Syn.M813
import Syn.M814
import Syn.M816
import Syn.M817
import Syn.M922
import Syn.M925
import Syn.M999
import Syn.M1000
import Syn.M1001
import Syn.M1109

namespace Syn.M1159
def val : Nat := Syn.M811.val % 7 + Syn.M813.val % 7 + Syn.M814.val % 7 + Syn.M816.val % 7 + Syn.M817.val % 7 + Syn.M922.val % 7 + Syn.M925.val % 7 + Syn.M999.val % 7 + Syn.M1000.val % 7 + Syn.M1001.val % 7 + Syn.M1109.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1159
