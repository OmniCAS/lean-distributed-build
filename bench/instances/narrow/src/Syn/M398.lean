import Syn.M210
import Syn.M212
import Syn.M326
import Syn.M327
import Syn.M328
import Syn.M329
import Syn.M330

namespace Syn.M398
def val : Nat := Syn.M210.val % 7 + Syn.M212.val % 7 + Syn.M326.val % 7 + Syn.M327.val % 7 + Syn.M328.val % 7 + Syn.M329.val % 7 + Syn.M330.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M398
