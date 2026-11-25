import Syn.M183

namespace Syn.M285
def val : Nat := Syn.M183.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M285
