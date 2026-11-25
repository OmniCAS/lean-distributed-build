import Syn.M181
import Syn.M183
import Syn.M207

namespace Syn.M313
def val : Nat := Syn.M181.val % 7 + Syn.M183.val % 7 + Syn.M207.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M313
