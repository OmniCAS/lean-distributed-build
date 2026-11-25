import Syn.M619
import Syn.M628
import Syn.M629
import Syn.M630
import Syn.M632
import Syn.M634
import Syn.M660
import Syn.M661
import Syn.M662

namespace Syn.M742
def val : Nat := Syn.M619.val % 7 + Syn.M628.val % 7 + Syn.M629.val % 7 + Syn.M630.val % 7 + Syn.M632.val % 7 + Syn.M634.val % 7 + Syn.M660.val % 7 + Syn.M661.val % 7 + Syn.M662.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M742
