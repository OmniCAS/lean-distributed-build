import Syn.M573
import Syn.M600
import Syn.M613
import Syn.M623
import Syn.M636
import Syn.M716
import Syn.M779
import Syn.M790
import Syn.M909
import Syn.M949
import Syn.M1052
import Syn.M1055
import Syn.M1096
import Syn.M1134
import Syn.M1135

namespace Syn.M1184
def val : Nat := Syn.M573.val % 7 + Syn.M600.val % 7 + Syn.M613.val % 7 + Syn.M623.val % 7 + Syn.M636.val % 7 + Syn.M716.val % 7 + Syn.M779.val % 7 + Syn.M790.val % 7 + Syn.M909.val % 7 + Syn.M949.val % 7 + Syn.M1052.val % 7 + Syn.M1055.val % 7 + Syn.M1096.val % 7 + Syn.M1134.val % 7 + Syn.M1135.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1184
