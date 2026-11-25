import Syn.M2004
import Syn.M2037
import Syn.M2193
import Syn.M2214
import Syn.M2263
import Syn.M2265
import Syn.M2266
import Syn.M2268
import Syn.M2269
import Syn.M2270
import Syn.M2299
import Syn.M2321
import Syn.M2338
import Syn.M2342
import Syn.M2369
import Syn.M2379

namespace Syn.M2390
def val : Nat := Syn.M2004.val % 7 + Syn.M2037.val % 7 + Syn.M2193.val % 7 + Syn.M2214.val % 7 + Syn.M2263.val % 7 + Syn.M2265.val % 7 + Syn.M2266.val % 7 + Syn.M2268.val % 7 + Syn.M2269.val % 7 + Syn.M2270.val % 7 + Syn.M2299.val % 7 + Syn.M2321.val % 7 + Syn.M2338.val % 7 + Syn.M2342.val % 7 + Syn.M2369.val % 7 + Syn.M2379.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M2390
