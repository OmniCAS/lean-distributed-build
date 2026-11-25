import Syn.M637
import Syn.M818
import Syn.M819
import Syn.M821
import Syn.M822
import Syn.M823
import Syn.M824
import Syn.M825
import Syn.M928
import Syn.M1002

namespace Syn.M1064
def val : Nat := Syn.M637.val % 7 + Syn.M818.val % 7 + Syn.M819.val % 7 + Syn.M821.val % 7 + Syn.M822.val % 7 + Syn.M823.val % 7 + Syn.M824.val % 7 + Syn.M825.val % 7 + Syn.M928.val % 7 + Syn.M1002.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1064
