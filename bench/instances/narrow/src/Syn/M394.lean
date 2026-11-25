import Syn.M184
import Syn.M185
import Syn.M285
import Syn.M313

namespace Syn.M394
def val : Nat := Syn.M184.val % 7 + Syn.M185.val % 7 + Syn.M285.val % 7 + Syn.M313.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M394
