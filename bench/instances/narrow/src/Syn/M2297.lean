import Syn.M1404
import Syn.M1692
import Syn.M1836
import Syn.M1943
import Syn.M1947
import Syn.M1948
import Syn.M2151
import Syn.M2165
import Syn.M2246
import Syn.M2262

namespace Syn.M2297
def val : Nat := Syn.M1404.val % 7 + Syn.M1692.val % 7 + Syn.M1836.val % 7 + Syn.M1943.val % 7 + Syn.M1947.val % 7 + Syn.M1948.val % 7 + Syn.M2151.val % 7 + Syn.M2165.val % 7 + Syn.M2246.val % 7 + Syn.M2262.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2297
