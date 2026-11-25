import Syn.M1934
import Syn.M1967
import Syn.M1970
import Syn.M1972
import Syn.M2020
import Syn.M2021
import Syn.M2022
import Syn.M2023
import Syn.M2024
import Syn.M2025
import Syn.M2026
import Syn.M2135

namespace Syn.M2159
def val : Nat := Syn.M1934.val % 7 + Syn.M1967.val % 7 + Syn.M1970.val % 7 + Syn.M1972.val % 7 + Syn.M2020.val % 7 + Syn.M2021.val % 7 + Syn.M2022.val % 7 + Syn.M2023.val % 7 + Syn.M2024.val % 7 + Syn.M2025.val % 7 + Syn.M2026.val % 7 + Syn.M2135.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2159
