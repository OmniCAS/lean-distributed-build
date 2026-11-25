import Syn.M428
import Syn.M483
import Syn.M484
import Syn.M485
import Syn.M557

namespace Syn.M589
def val : Nat := Syn.M428.val % 7 + Syn.M483.val % 7 + Syn.M484.val % 7 + Syn.M485.val % 7 + Syn.M557.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M589
