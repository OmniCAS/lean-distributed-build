import E1.Formalism.LogSumExpBounds.CharacterSumPhase.DecayAsm
import E1.Formalism.LogSumExpBounds.CharacterSumPhase.DescEquivLiftEquiv
import E1.Formalism.LogSumExpBounds.CharacterSumPhase.DetMulDiagonalMulEqSum
import E1.Formalism.LogSumExpBounds.CharacterSumPhase.KappaModulusHolds
import E1.Formalism.LogSumExpBounds.CharacterSumPhase.LatSum
import E1.Formalism.LogSumExpBounds.CharacterSumPhase.LogSumExpBoundHolds
import E1.Formalism.LogSumExpBounds.CharacterSumPhase.NuclearNormBoundHolds
import E1.Formalism.LogSumExpBounds.CharacterSumPhase.RankLeOfSupport
import E1.Formalism.LogSumExpBounds.CharacterSumPhase.WeightedOffDiagonalHolds
import E1.Formalism.LogSumExpBounds.CharacterSumPhase.ZLiftAsm
import E1.Formalism.LogSumExpBounds.StatementE

set_option Elab.async false

namespace E1N.M1325
def val : Nat := E1N.M1315.val % 7 + E1N.M1316.val % 7 + E1N.M1317.val % 7 + E1N.M1318.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end E1N.M1325
