import Syn.M1892
import Syn.M1894
import Syn.M1930
import Syn.M2008
import Syn.M2009
import Syn.M2057
import Syn.M2185
import Syn.M2186

namespace Syn.M2204
def val : Nat := Syn.M1892.val % 7 + Syn.M1894.val % 7 + Syn.M1930.val % 7 + Syn.M2008.val % 7 + Syn.M2009.val % 7 + Syn.M2057.val % 7 + Syn.M2185.val % 7 + Syn.M2186.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2204
