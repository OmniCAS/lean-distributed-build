import Syn.M885
import Syn.M1213
import Syn.M1525
import Syn.M1564
import Syn.M1606
import Syn.M1687
import Syn.M1789
import Syn.M1905
import Syn.M1906
import Syn.M1939

namespace Syn.M1978
def val : Nat := Syn.M885.val % 7 + Syn.M1213.val % 7 + Syn.M1525.val % 7 + Syn.M1564.val % 7 + Syn.M1606.val % 7 + Syn.M1687.val % 7 + Syn.M1789.val % 7 + Syn.M1905.val % 7 + Syn.M1906.val % 7 + Syn.M1939.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
end Syn.M1978
