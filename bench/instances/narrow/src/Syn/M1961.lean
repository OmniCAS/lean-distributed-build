import Syn.M1897
import Syn.M1898
import Syn.M1900
import Syn.M1931

namespace Syn.M1961
def val : Nat := Syn.M1897.val % 7 + Syn.M1898.val % 7 + Syn.M1900.val % 7 + Syn.M1931.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1961
