import Syn.M360
import Syn.M361
import Syn.M569
import Syn.M632
import Syn.M636
import Syn.M665
import Syn.M712
import Syn.M743
import Syn.M744
import Syn.M833
import Syn.M835
import Syn.M836
import Syn.M837
import Syn.M838
import Syn.M868
import Syn.M929
import Syn.M932
import Syn.M933
import Syn.M939
import Syn.M965
import Syn.M971
import Syn.M1004
import Syn.M1005
import Syn.M1066
import Syn.M1069
import Syn.M1098
import Syn.M1108
import Syn.M1118
import Syn.M1184
import Syn.M1245
import Syn.M1255
import Syn.M1286
import Syn.M1336
import Syn.M1343
import Syn.M1409

namespace Syn.M1446
def val : Nat := Syn.M360.val % 7 + Syn.M361.val % 7 + Syn.M569.val % 7 + Syn.M632.val % 7 + Syn.M636.val % 7 + Syn.M665.val % 7 + Syn.M712.val % 7 + Syn.M743.val % 7 + Syn.M744.val % 7 + Syn.M833.val % 7 + Syn.M835.val % 7 + Syn.M836.val % 7 + Syn.M837.val % 7 + Syn.M838.val % 7 + Syn.M868.val % 7 + Syn.M929.val % 7 + Syn.M932.val % 7 + Syn.M933.val % 7 + Syn.M939.val % 7 + Syn.M965.val % 7 + Syn.M971.val % 7 + Syn.M1004.val % 7 + Syn.M1005.val % 7 + Syn.M1066.val % 7 + Syn.M1069.val % 7 + Syn.M1098.val % 7 + Syn.M1108.val % 7 + Syn.M1118.val % 7 + Syn.M1184.val % 7 + Syn.M1245.val % 7 + Syn.M1255.val % 7 + Syn.M1286.val % 7 + Syn.M1336.val % 7 + Syn.M1343.val % 7 + Syn.M1409.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end Syn.M1446
