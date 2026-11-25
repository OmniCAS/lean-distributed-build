import E1.Formalism.FlagUnipotentLattices.BlockDistFromLows
import E1.Formalism.FlagUnipotentLattices.HeightConditionFromCubic
import E1.Formalism.FlagUnipotentLattices.InterlaceBlocksW
import E1.Formalism.FlagUnipotentLattices.MemLpTwoOfOneTop
import E1.Formalism.FlagUnipotentLattices.MinkowskiFactorialBounds.AntisymmetrizedProductEqFactorialSmulQdet
import E1.Formalism.FlagUnipotentLattices.MinkowskiFactorialBounds.IntegrableOnAndSetIntegralEqZeroOfIsCompact
import E1.Formalism.FlagUnipotentLattices.MinkowskiFactorialBounds.InterlacingOfBlocksSecondCase
import E1.Formalism.FlagUnipotentLattices.MinkowskiFactorialBounds.LanglandsParameterEquivariant
import E1.Formalism.FlagUnipotentLattices.QDetNegTranspose

set_option Elab.async false

namespace E1N.M151
def val : Nat := E1N.M99.val % 7 + E1N.M113.val % 7 + E1N.M114.val % 7 + E1N.M116.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end E1N.M151
